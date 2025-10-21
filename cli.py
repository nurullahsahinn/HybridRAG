"""
Smart interactive CLI - Natural conversation + RAG when needed.
"""
import sys
from main import ask_question_smart
from config import get_config
from utils.logger import setup_logger, get_logger

# Setup
config = get_config()
setup_logger(
    name="advanced_rag",
    log_level=config.log_level,
    log_format=config.log_format,
    log_file="logs/advanced_rag.log"
)
logger = get_logger(__name__)


def main():
    """Smart interactive CLI."""
    print("\n" + "="*80)
    print("🤖 Akıllı RAG Sistemi - Doğal Sohbet + Bilgi Asistanı")
    print("="*80)
    print("💬 Benimle sohbet edebilir veya sorularınızı sorabilirsiniz!")
    print("📚 Gerektiğinde dökümanlardan bilgi getiririm")
    print("🧠 Dökümanlar yardımcı olmazsa kendi bilgimle cevaplarım")
    print("💡 'quit' veya 'exit' yazarak çıkabilirsiniz")
    print("="*80 + "\n")
    
    while True:
        try:
            question = input("🎯 Sen: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ["quit", "exit", "çık", "çıkış"]:
                print("\n👋 Görüşmek üzere! İyi çalışmalar!\n")
                break
            
            print("\n⏳ Düşünüyorum...\n")
            result = ask_question_smart(question)
            
            print(f"🤖 Asistan: {result['answer']}")
            
            # Source citation
            if result['type'] == 'knowledge' and result['used_documents']:
                print(f"\n📚 Kaynak: {result['num_documents']} döküman")
                if result.get('sources'):
                    print(f"   Dosyalar: {', '.join([s.split('/')[-1] for s in result['sources'][:3]])}")
            elif result['type'] == 'knowledge' and not result['used_documents']:
                print(f"\n🧠 (Kendi bilgimle cevapladım)")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Görüşmek üzere!\n")
            break
        except Exception as e:
            print(f"\n❌ Hata: {str(e)}\n")


if __name__ == "__main__":
    main()

