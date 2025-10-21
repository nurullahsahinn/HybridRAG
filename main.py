"""
Smart RAG system - Decides when to use documents vs direct chat.
Includes chat memory and source citation.
"""
import sys
from config import get_config
from utils.logger import setup_logger, get_logger
from utils.validation import validate_question
from llm_provider import get_llm
from ingestion import get_retriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from typing import List

# Initialize
config = get_config()
setup_logger(
    name="advanced_rag",
    log_level=config.log_level,
    log_format=config.log_format,
    log_file="logs/advanced_rag.log"
)
logger = get_logger(__name__)

# Global chat memory
CHAT_MEMORY = []  # List of {"role": "user"/"assistant", "content": "..."}
MAX_MEMORY = 10  # Son 10 mesajı sakla


def get_conversation_context() -> str:
    """Get recent conversation history as context."""
    if not CHAT_MEMORY:
        return ""
    
    # Son 6 mesajı al (3 soru-cevap)
    recent = CHAT_MEMORY[-6:]
    context = "\n".join([
        f"{'Kullanıcı' if msg['role'] == 'user' else 'Sen'}: {msg['content']}"
        for msg in recent
    ])
    return context


def add_to_memory(role: str, content: str):
    """Add message to conversation memory."""
    CHAT_MEMORY.append({"role": role, "content": content})
    
    # Keep only last MAX_MEMORY messages
    if len(CHAT_MEMORY) > MAX_MEMORY:
        CHAT_MEMORY.pop(0)


def classify_question(question: str, llm) -> str:
    """
    Classify if question needs documents or can be answered directly.
    
    Returns:
        "casual" - for greetings, small talk
        "knowledge" - for questions requiring specific knowledge
    """
    # Get conversation context
    context = get_conversation_context()
    
    classifier_template = """Aşağıdaki soruyu analiz et ve kategorize et.

{context}

YENİ SORU: {question}

KATEGORİLER:
- "casual" → Günlük sohbet, selamlaşma, hal hatır, takip soruları (örn: "nasılsın?", "merhaba", "peki ya?", "o ne demek?")
- "knowledge" → Spesifik bilgi gerektiren sorular (örn: "agent memory nedir?", "prompt engineering nasıl yapılır?")

ÖNEMLİ: Eğer önceki sohbete atıfta bulunuyorsa (örn: "peki bu nasıl çalışır?", "daha fazla anlat"), context'e bak.

Sadece kategori ismini yaz (casual veya knowledge):"""
    
    prompt = ChatPromptTemplate.from_template(classifier_template)
    chain = prompt | llm | StrOutputParser()
    
    result = chain.invoke({
        "question": question,
        "context": f"ÖNCEKİ SOHBET:\n{context}" if context else "ÖNCEKİ SOHBET YOK"
    }).strip().lower()
    
    # Parse result
    if "casual" in result:
        return "casual"
    else:
        return "knowledge"


def answer_casual(question: str, llm) -> str:
    """Answer casual questions directly with memory."""
    # Get conversation context
    context = get_conversation_context()
    
    casual_template = """Sen dostça ve yardımsever bir asistansın. 

{context}

YENİ MESAJ: {question}

GÖREV: Önceki sohbeti dikkate alarak doğal ve samimi bir şekilde cevap ver. Kısa ve öz ol.
Eğer önceki bir konuya atıfta bulunuyorsa, onu hatırladığını göster.

CEVAP:"""
    
    prompt = ChatPromptTemplate.from_template(casual_template)
    chain = prompt | llm | StrOutputParser()
    
    return chain.invoke({
        "question": question,
        "context": f"ÖNCEKİ SOHBET:\n{context}" if context else "ÖNCEKİ SOHBET YOK"
    })


def answer_with_rag(question: str, llm, retriever) -> dict:
    """Answer using RAG - check documents first with memory."""
    
    # Get conversation context
    conv_context = get_conversation_context()
    
    # Retrieve documents
    documents = retriever.invoke(question)
    
    # Extract sources
    sources = []
    for doc in documents:
        source = doc.metadata.get("source", "Unknown")
        if source not in sources:
            sources.append(source)
    
    # Check if documents are relevant
    if not documents:
        logger.info("No documents found, using LLM's own knowledge")
        return answer_with_llm_knowledge(question, llm)
    
    # Check document relevance
    doc_context = "\n\n".join([doc.page_content for doc in documents])
    
    # Use documents to answer
    rag_template = """Sen bir eğitim asistanısın. Aşağıdaki kaynaklara, önceki sohbete ve kendi bilgine dayanarak soruyu yanıtla.

{conv_context}

KAYNAK BİLGİLER:
{doc_context}

YENİ SORU: {question}

ÖNEMLİ KURALLAR:
1. Önceki sohbete atıfta bulunuyorsa, onu dikkate al
2. Eğer kaynaklarda doğrudan cevap varsa, onu kendi kelimerinle açıkla
3. Eğer kaynaklarda kısmi bilgi varsa, kendi bilginle tamamla
4. Eğer kaynaklarda hiç bilgi yoksa, kendi bilginle cevapla ama belirt
5. Doğal ve akıcı bir dille konuş, robotik olma
6. Gerekirse örnek ver

CEVAP:"""
    
    prompt = ChatPromptTemplate.from_template(rag_template)
    chain = prompt | llm | StrOutputParser()
    
    answer = chain.invoke({
        "doc_context": doc_context,
        "question": question,
        "conv_context": f"ÖNCEKİ SOHBET:\n{conv_context}" if conv_context else ""
    })
    
    return {
        "answer": answer,
        "used_documents": True,
        "num_documents": len(documents),
        "sources": sources
    }


def answer_with_llm_knowledge(question: str, llm) -> dict:
    """Answer using LLM's own knowledge when documents don't help."""
    
    # Get conversation context
    conv_context = get_conversation_context()
    
    knowledge_template = """Sen yardımcı bir asistansın. Kullanıcının sorusunu kendi bilginle yanıtla.

{conv_context}

YENİ SORU: {question}

KURALLAR:
1. Önceki sohbeti dikkate al
2. Doğal ve akıcı bir dille konuş
3. Biliyorsan detaylı açıkla, bilmiyorsan dürüst ol
4. Gerekirse örnekler ver
5. Emin olmadığın konularda "kesin değilim" de

CEVAP:"""
    
    prompt = ChatPromptTemplate.from_template(knowledge_template)
    chain = prompt | llm | StrOutputParser()
    
    answer = chain.invoke({
        "question": question,
        "conv_context": f"ÖNCEKİ SOHBET:\n{conv_context}" if conv_context else ""
    })
    
    return {
        "answer": answer,
        "used_documents": False,
        "num_documents": 0,
        "sources": []
    }


def ask_question_smart(question: str) -> dict:
    """
    Smart question answering with routing and memory.
    """
    try:
        # Validate
        question = validate_question(question)
        
        # Add user question to memory
        add_to_memory("user", question)
        
        # Get LLM
        llm = get_llm()
        
        # Classify question
        logger.info(f"Classifying question: {question[:50]}")
        question_type = classify_question(question, llm)
        logger.info(f"Question type: {question_type}")
        
        # Route based on type
        if question_type == "casual":
            # Direct chat
            logger.info("Answering as casual chat")
            answer = answer_casual(question, llm)
            
            # Add to memory
            add_to_memory("assistant", answer)
            
            return {
                "question": question,
                "answer": answer,
                "type": "casual",
                "used_documents": False,
                "num_documents": 0,
                "sources": [],
                "success": True
            }
        
        else:  # knowledge
            # Use RAG
            logger.info("Answering with RAG")
            retriever = get_retriever()
            result = answer_with_rag(question, llm, retriever)
            
            # Add to memory
            add_to_memory("assistant", result["answer"])
            
            return {
                "question": question,
                "answer": result["answer"],
                "type": "knowledge",
                "used_documents": result["used_documents"],
                "num_documents": result["num_documents"],
                "sources": result.get("sources", []),
                "success": True
            }
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            "question": question,
            "answer": f"Üzgünüm, bir hata oluştu: {str(e)}",
            "type": "error",
            "used_documents": False,
            "num_documents": 0,
            "success": False
        }


def main():
    """Test function."""
    logger.info("=" * 80)
    logger.info("Smart RAG System Started")
    logger.info("=" * 80)
    
    # Test questions
    test_questions = [
        "Merhaba, nasılsın?",
        "What is agent memory?",
        "Ne yapıyorsun?",
        "Prompt engineering nedir?",
    ]
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{'='*80}")
        print(f"Test {i}/{len(test_questions)}")
        print(f"{'='*80}")
        
        result = ask_question_smart(question)
        
        print(f"Soru: {result['question']}")
        print(f"Tip: {result['type']}")
        print(f"Döküman kullanıldı: {result['used_documents']}")
        print(f"{'-'*80}")
        print(f"Cevap: {result['answer']}")
        print(f"{'='*80}\n")


if __name__ == "__main__":
    main()

