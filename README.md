# 🤖 Smart RAG Chatbot with Ollama

**Tamamen ücretsiz, local olarak çalışan, akıllı bir RAG (Retrieval-Augmented Generation) chatbot sistemi.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-0.2.7-green.svg)](https://langchain.com)
[![Ollama](https://img.shields.io/badge/Ollama-Llama%203.1-orange.svg)](https://ollama.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ Özellikler

### 🎯 Temel Özellikler
- **🆓 Tamamen Ücretsiz**: Local LLM (Ollama) kullanır, API maliyeti $0
- **🧠 Akıllı Routing**: Sohbet vs bilgi sorularını otomatik ayırır
- **📚 RAG Sistemi**: Kendi dökümanlarınızdan bilgi öğrenir
- **💬 Sohbet Hafızası**: Son 10 mesajı hatırlar, context-aware cevaplar verir
- **🔍 Kaynak Gösterimi**: Hangi dökümanlardan bilgi aldığını gösterir
- **🌐 Hibrid Mode**: Dökümanlarda bilgi yoksa LLM'in kendi bilgisiyle cevaplar

### 🛡️ Profesyonel Özellikler
- **Structured Logging**: JSON formatında detaylı loglar
- **Error Handling**: Comprehensive exception handling
- **Input Validation**: Güvenlik odaklı input validasyonu
- **Retry Mechanism**: Exponential backoff ile otomatik retry
- **Circuit Breaker**: Tekrarlayan hatalardan korunma
- **Caching**: In-memory cache ile performans optimizasyonu
- **Metrics**: Real-time performans metrikleri

---

## 🎬 Demo

### Sohbet Modu
```
Sen: Merhaba, nasılsın?
🤖: Merhaba! İyiyim, teşekkürler. Size nasıl yardımcı olabilirim?

Sen: Ne yapıyorsun?
🤖: Sizinle sohbet ediyorum! Sorularınızı yanıtlamaya hazırım.
```

### Bilgi Modu (Dökümanlardan)
```
Sen: What is agent memory?
🤖: Agent memory, LLM-based autonomous ajanların geçmiş 
    etkileşimleri ve bilgileri saklama yeteneğidir...
📚 Kaynak: 4 döküman
   Dosyalar: 2023-06-23-agent.md
```

### Hibrid Mod (LLM Bilgisi)
```
Sen: Python nedir?
🤖: Python, yüksek seviye, yorumlamalı bir programlama dilidir...
🧠 (Kendi bilgimle cevapladım)
```

### Context-Aware (Hafıza)
```
Sen: What is agent memory?
🤖: [detaylı cevap]

Sen: Peki bu nasıl çalışır?  ← Önceki soruyu hatırlıyor!
🤖: Agent memory'nin çalışma prensibi...
```

---

## 📦 Kurulum

### Gereksinimler
- Python 3.10+
- 8GB+ RAM (16GB önerilir)
- Windows/Linux/Mac

### 1️⃣ Repository'yi Klonlayın
```bash
git clone https://github.com/nurullahsahinn/HybridRAG.git
cd HybridRAG
```

### 2️⃣ Python Bağımlılıklarını Yükleyin
```bash
pip install -r requirements.txt
```

### 3️⃣ Ollama'yı Kurun

**Windows:**
```bash
# İndir: https://ollama.com/download/windows
# Kur ve ardından:
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

**Linux/Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

### 4️⃣ Konfigürasyonu Ayarlayın

`.env` dosyası oluşturun:
```bash
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
EMBEDDING_MODEL=nomic-embed-text

CHROMA_PERSIST_DIRECTORY=./.chroma
CHROMA_COLLECTION_NAME=rag-chroma
CHUNK_SIZE=250
CHUNK_OVERLAP=50
RETRIEVAL_K=4

LOG_LEVEL=INFO
LOG_FORMAT=console
```

### 5️⃣ Dökümanları Yükleyin (İsteğe Bağlı)

Sistem default olarak AI/ML hakkında 3 web sayfası yükler. Kendi dökümanlarınızı eklemek için:

```bash
python load_custom_docs.py path/to/your/documents/
```

Desteklenen formatlar: PDF, TXT, DOCX

---

## 🚀 Kullanım

### İnteraktif Mod (Önerilen)
```bash
python cli.py
```

Sürekli soru sorabileceğiniz interactive bir chat başlatır.

### Programatik Kullanım
```python
from main import ask_question_smart

result = ask_question_smart("What is machine learning?")

print(result['answer'])
print(f"Döküman kullanıldı: {result['used_documents']}")
print(f"Kaynak: {result['sources']}")
```

### Kendi Dökümanlarınızı Yükleyin
```bash
# PDF klasörünüzü gösterin
python load_custom_docs.py "C:/MyDocuments/AI/"

# Ardından cli'yi başlatın
python cli.py
```

---

## 📁 Proje Yapısı

```
smart-rag-chatbot/
├── main.py                    # Ana RAG engine (smart routing, memory)
├── cli.py                     # Interactive CLI
├── config.py                  # Configuration management
├── exceptions.py              # Custom exceptions
├── llm_provider.py            # LLM abstraction (OpenAI/Ollama)
├── ingestion.py               # Document processing & vectorstore
├── load_custom_docs.py        # Custom document loader
│
├── utils/                     # Utility modules
│   ├── cache.py              # Caching mechanism
│   ├── logger.py             # Structured logging
│   ├── metrics.py            # Performance metrics
│   ├── retry.py              # Retry & circuit breaker
│   └── validation.py         # Input validation
│
├── tests/                     # Unit tests
│   ├── test_cache.py
│   ├── test_config.py
│   ├── test_metrics.py
│   ├── test_retry.py
│   └── test_validation.py
│
├── docs/                      # Documentation
│   ├── QUICK_START.md        # Quick start guide
│   └── setup_ollama.md       # Ollama setup guide
│
├── requirements.txt           # Python dependencies
├── .env.example              # Example environment config
└── README.md                 # This file
```

---

## 🔧 Konfigürasyon

### LLM Provider Seçimi

**Ollama (Local - Ücretsiz):**
```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.1:8b
```

**OpenAI (Cloud - Ücretli):**
```env
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your_key_here
OPENAI_MODEL=gpt-4o-mini
```

### Embedding Provider

**Ollama (Yavaş ama ücretsiz):**
```env
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text
```

**OpenAI (Hızlı, ~$0.01/1000 döküman):**
```env
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=sk-your_key_here
```

**💡 Tavsiye:** Embedding için OpenAI, LLM için Ollama kullanın!

---

## 🎯 Kullanım Senaryoları

### 📚 Ders Çalışma Asistanı
```bash
# Ders notlarınızı yükleyin
python load_custom_docs.py "~/University/CS101/"

# Sorular sorun
python cli.py
> "Explain recursion with examples"
```

### 📖 Dokümantasyon Asistanı
```bash
# Proje dokümantasyonunu yükleyin
python load_custom_docs.py "./project-docs/"

# API kullanımı hakkında sorun
python cli.py
> "How do I authenticate with the API?"
```

### 🧠 Kişisel Bilgi Tabanı
```bash
# Notlarınızı, makalelerinizi yükleyin
python load_custom_docs.py "~/Documents/Notes/"

# İstediğiniz zaman arayın
python cli.py
> "What did I learn about neural networks?"
```

---

## 📊 Performans

### Sistem Gereksinimleri

| Bileşen | Minimum | Önerilen | Optimal |
|---------|---------|----------|---------|
| **RAM** | 8GB | 16GB | 32GB+ |
| **CPU** | i5 | i7 | Ryzen 9 |
| **GPU** | - | GTX 1660 Ti | RTX 3070+ |
| **Disk** | 10GB | 20GB | 50GB+ |

### Hız Karşılaştırması

| İşlem | CPU Only | With GPU | OpenAI API |
|-------|----------|----------|------------|
| **Soru-Cevap** | 30-60s | 3-8s | 2-3s |
| **Embedding (100 döküman)** | 5-10 min | 2-3 min | 10-30s |
| **İlk Model Yükleme** | 20-30s | 5-10s | - |

### Maliyet Karşılaştırması

| Seçenek | Setup | Aylık | Notlar |
|---------|-------|-------|--------|
| **Full Ollama** | $0 | $0 | Yavaş embedding |
| **Ollama + OpenAI Embedding** | $0.01 | $0 | ✅ **Önerilen** |
| **Full OpenAI** | $0 | $30-100 | En hızlı |

---

## 🧪 Testler

```bash
# Tüm testleri çalıştır
pytest

# Coverage raporu ile
pytest --cov=. --cov-report=html

# Belirli testler
pytest tests/test_validation.py -v
```

---

## 🐛 Sorun Giderme

### "Ollama is not running"
```bash
# Windows: Start menüden Ollama uygulamasını başlat
# Linux/Mac:
ollama serve
```

### "Model not found"
```bash
# Modelleri kontrol et
ollama list

# İndir
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

### "GPU kullanılmıyor"
```bash
# GPU kontrolü
nvidia-smi

# CUDA kurulu mu?
# https://developer.nvidia.com/cuda-downloads
```

### "Çok yavaş cevap veriyor"
1. **GPU kullanın** (30-50x hızlanır)
2. **Embedding için OpenAI** kullanın ($0.01, 40x hızlı)
3. **Daha küçük model** kullanın: `llama3.2:3b`

---

## 🚧 Gelecek Geliştirmeler

- [ ] Web UI (Gradio/Streamlit)
- [ ] Multi-user support
- [ ] Persistent chat history (database)
- [ ] File upload via web interface
- [ ] Multi-language support
- [ ] Voice interface
- [ ] Mobile app
- [ ] Docker deployment
- [ ] API endpoints (FastAPI)
- [ ] Streaming responses

---

## 🤝 Katkıda Bulunma

Katkılar memnuniyetle karşılanır! İşte nasıl katkıda bulunabilirsiniz:

1. Fork edin
2. Feature branch oluşturun: `git checkout -b feature/amazing-feature`
3. Commit edin: `git commit -m 'Add amazing feature'`
4. Push edin: `git push origin feature/amazing-feature`
5. Pull Request açın

---

## 📄 Lisans

Bu proje MIT lisansı altındadır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 🙏 Teşekkürler

Bu proje şu harika teknolojileri kullanır:

- [LangChain](https://langchain.com) - LLM framework
- [Ollama](https://ollama.com) - Local LLM runtime
- [Chroma](https://www.trychroma.com/) - Vector database
- [Llama 3.1](https://ai.meta.com/llama/) - Meta'nın açık kaynak LLM'i

---

## 📞 İletişim

Sorularınız veya önerileriniz için:
- GitHub Issues: [Create an issue](https://github.com/nurullahsahinn/HybridRAG/issues)
- Email: nurullahsahin0088@gmail.com

---


**Not:** Bu proje tamamen ücretsiz ve açık kaynaklıdır. Kendi AI asistanınızı oluşturmak için mükemmel bir başlangıç noktasıdır!

**Made with ❤️ and 🤖 by Nurullah Sahin**
