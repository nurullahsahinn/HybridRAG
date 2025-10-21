"""
Load custom documents (PDFs, TXT) into vector store.
Usage: python load_custom_docs.py path/to/your/documents/
"""
import sys
from pathlib import Path
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredWordDocumentLoader
)
from ingestion import split_documents, create_vectorstore
from utils.logger import setup_logger, get_logger
from config import get_config

config = get_config()
setup_logger(
    name="advanced_rag",
    log_level=config.log_level,
    log_format=config.log_format
)
logger = get_logger(__name__)


def load_documents_from_folder(folder_path: str):
    """Load all documents from a folder."""
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"❌ Klasör bulunamadı: {folder_path}")
        return []
    
    documents = []
    supported_extensions = {'.pdf', '.txt', '.docx'}
    
    files = list(folder.glob('**/*'))
    pdf_files = [f for f in files if f.suffix.lower() in supported_extensions]
    
    print(f"\n📁 {len(pdf_files)} dosya bulundu")
    print("="*80)
    
    for file_path in pdf_files:
        try:
            print(f"📄 Yükleniyor: {file_path.name}")
            
            if file_path.suffix.lower() == '.pdf':
                loader = PyPDFLoader(str(file_path))
            elif file_path.suffix.lower() == '.txt':
                loader = TextLoader(str(file_path), encoding='utf-8')
            elif file_path.suffix.lower() == '.docx':
                loader = UnstructuredWordDocumentLoader(str(file_path))
            else:
                continue
            
            docs = loader.load()
            documents.extend(docs)
            print(f"   ✅ {len(docs)} sayfa yüklendi")
            
        except Exception as e:
            print(f"   ❌ Hata: {str(e)}")
            continue
    
    print("="*80)
    print(f"✅ Toplam {len(documents)} döküman yüklendi\n")
    
    return documents


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Kullanım: python load_custom_docs.py <klasor_yolu>")
        print("Örnek: python load_custom_docs.py C:/Dersler/CS101/")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    
    print("\n" + "="*80)
    print("📚 Özel Dökümanları Yükleme")
    print("="*80)
    
    # Load documents
    documents = load_documents_from_folder(folder_path)
    
    if not documents:
        print("❌ Hiç döküman yüklenemedi!")
        sys.exit(1)
    
    # Split documents
    print("\n📝 Dökümanlar parçalanıyor...")
    doc_splits = split_documents(documents)
    print(f"✅ {len(doc_splits)} parçaya bölündü")
    
    # Create vector store
    print("\n🔄 Vector store oluşturuluyor...")
    vectorstore = create_vectorstore(doc_splits)
    print("✅ Vector store hazır!")
    
    print("\n" + "="*80)
    print("🎉 Dökümanlar başarıyla yüklendi!")
    print("Artık bu dökümanlar hakkında soru sorabilirsiniz.")
    print("="*80 + "\n")
    
    # Test
    print("Test sorusu sorabilirsiniz (Enter'a basın veya sorunuzu yazın):")
    question = input("Soru: ").strip()
    
    if question:
        from main_simple import ask_question_simple
        result = ask_question_simple(question)
        print(f"\n📄 Cevap:\n{result['answer']}\n")


if __name__ == "__main__":
    main()


