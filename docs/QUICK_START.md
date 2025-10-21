# ⚡ Hızlı Başlangıç - Local LLM ile Advanced RAG

## 🎯 Hedef
Projenizi OpenAI API yerine **tamamen ücretsiz** local LLM (Ollama) ile çalıştırmak!

---

## 📋 Adım Adım Rehber

### 1️⃣ Ollama Kur (5 dakika)

#### Windows:
```bash
# İndir: https://ollama.com/download/windows
# Kur: OllamaSetup.exe dosyasını çalıştır

# Kontrol et:
ollama --version
```

### 2️⃣ Model İndir (10 dakika)

```bash
# Ana model (Türkçe desteği harika!)
ollama pull llama3.1:8b

# Embedding model (önemli!)
ollama pull nomic-embed-text

# Test et:
ollama run llama3.1:8b
>>> Merhaba!  # Türkçe cevap gelmeli
>>> /bye      # Çıkmak için
```

### 3️⃣ Python Paketlerini Güncelle

```bash
# Projenin ana dizininde:
pip install -r requirements.txt
```

### 4️⃣ .env Dosyası Oluştur

```bash
# .env.local dosyasını kopyala
copy .env.local .env

# VEYA manuel oluştur ve şunu ekle:
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
EMBEDDING_MODEL=nomic-embed-text
```

### 5️⃣ Test Et!

```bash
# Ollama kurulumunu test et
python test_ollama.py

# Her şey ✅ ise hazırsın!
```

### 6️⃣ Vector Store Oluştur

```bash
# İlk kez çalıştırıyorsan vector store oluştur
python -c "from ingestion import initialize_vectorstore; initialize_vectorstore()"
```

### 7️⃣ Çalıştır! 🚀

```bash
# Ana uygulamayı çalıştır
python main.py

# VEYA CLI kullan
python cli.py interactive
```

---

## ✅ Başarı Kontrolü

Eğer şunları görüyorsan her şey tamam:

```
✓ LLM connection test successful
✓ Embeddings connection test successful
✓ Vector store initialized successfully
```

---

## 🐛 Sorun mu Var?

### "Ollama is not running"
```bash
# Ollama'yı başlat
ollama serve

# VEYA Windows'ta görev çubuğundan Ollama ikonunu ara
```

### "Model not found"
```bash
# Modelleri kontrol et
ollama list

# Yoksa indir
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

### "ImportError: langchain-community"
```bash
pip install langchain-community
```

---

## 🎓 DBS Entegrasyonu İçin Sonraki Adımlar

Sistem local'de çalıştıktan sonra:

1. **Hocayla konuş**: DBS API dokümantasyonu
2. **DBS Connector ekle**: `dbs_connector.py` oluştur
3. **Auto-sync ekle**: Dokümanları otomatik çek
4. **Test et**: Gerçek ders dokümanları ile
5. **Deploy**: Üniversite sunucusuna kur

---

## 💡 İpuçları

### Daha Hızlı Çalıştırmak İçin:
```bash
# Daha küçük model kullan
ollama pull llama3.2:3b

# .env'de güncelle:
OLLAMA_MODEL=llama3.2:3b
```

### Daha İyi Kalite İçin:
```bash
# Daha büyük model (64GB RAM gerekir!)
ollama pull llama3.1:70b

# .env'de güncelle:
OLLAMA_MODEL=llama3.1:70b
```

### GPU Kullanımı:
Ollama otomatik olarak GPU kullanır (varsa). Kontrol için:
```bash
nvidia-smi  # NVIDIA GPU varsa
```

---

## 📊 Maliyet Karşılaştırması

| Seçenek | Aylık Maliyet | Kurulum | Performans |
|---------|---------------|---------|------------|
| **OpenAI API** | $30-100 | 5 dk | ⚡⚡⚡⚡⚡ |
| **Ollama Local** | **$0** 🎉 | 15 dk | ⚡⚡⚡⚡ |

**Kazancınız**: $30-100/ay tasarruf! 💰

---

## 🎉 Başarılı!

Artık tamamen ücretsiz, local bir RAG sisteminiz var!

**Sonraki adım**: `python cli.py interactive` ile soru sormaya başla! 🚀


