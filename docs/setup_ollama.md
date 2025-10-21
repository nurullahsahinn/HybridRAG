# 🚀 Ollama Kurulum ve Çalıştırma Rehberi

## Adım 1: Ollama Kurulumu

### Windows
1. **İndir**: https://ollama.com/download/windows
2. **Kur**: `OllamaSetup.exe` dosyasını çalıştır
3. **Kontrol**: Terminal'de şunu çalıştır:
   ```bash
   ollama --version
   ```

### Kurulum Başarılı mı?
Eğer `ollama version x.x.x` gibi bir çıktı görüyorsanız, başarılı! ✅

---

## Adım 2: Model İndirme

### Önerilen Model: Llama 3.1 8B (Türkçe Desteği Harika!)

```bash
# Model'i indir (yaklaşık 4.7 GB)
ollama pull llama3.1:8b

# Embedding model'i indir (önemli!)
ollama pull nomic-embed-text
```

### Alternatif Modeller

**Daha Küçük (Daha Hızlı)**:
```bash
ollama pull llama3.2:3b  # 2GB - Hafif sistemler için
```

**Daha İyi Kalite (Daha Yavaş)**:
```bash
ollama pull llama3.1:70b  # 40GB - Güçlü sistemler için
```

---

## Adım 3: Model Test Et

```bash
# Model'i çalıştır
ollama run llama3.1:8b

# Şunu yaz:
>>> Merhaba, nasılsın?

# Türkçe cevap gelirse başarılı! ✅
# Çıkmak için: /bye
```

---

## Adım 4: Server Başlat

Ollama otomatik olarak arka planda çalışır, ama manuel başlatmak isterseniz:

```bash
ollama serve
```

**Port**: http://localhost:11434

---

## Adım 5: Python Kurulumları

```bash
# Gerekli paketleri yükle
pip install langchain-community

# Test et
python llm_provider.py
```

---

## 🐛 Sorun Giderme

### "Ollama is not running"
```bash
# Windows'ta Ollama'yı başlat
# Görev Çubuğunda Ollama ikonunu arayın
# Veya terminalde:
ollama serve
```

### Model indirilemedi
```bash
# İnternet bağlantınızı kontrol edin
# Tekrar deneyin:
ollama pull llama3.1:8b --insecure
```

### Port 11434 kullanımda
```bash
# Başka bir port kullan
ollama serve --port 11435

# .env dosyasını güncelle:
OLLAMA_BASE_URL=http://localhost:11435
```

---

## ✅ Kurulum Kontrolü

Her şey tamam mı kontrol et:

```bash
# 1. Ollama çalışıyor mu?
ollama list

# 2. Modeller inmiş mi?
# Şunu görmelisin:
# llama3.1:8b
# nomic-embed-text

# 3. Python test
python -c "from langchain_community.llms import Ollama; print('OK')"
```

Hepsi ✅ ise, hazırsın! 🎉

---

## 📊 Sistem Gereksinimleri

| Model | RAM | Disk | GPU |
|-------|-----|------|-----|
| llama3.1:8b | 8GB | 5GB | İsteğe bağlı |
| llama3.2:3b | 4GB | 2GB | İsteğe bağlı |
| llama3.1:70b | 64GB | 40GB | Önerilir |

---

## 🚀 Sonraki Adımlar

Kurulum tamamsa:

```bash
# .env dosyasını kopyala
copy .env.local .env

# Test et
python llm_provider.py

# RAG sistemini çalıştır
python main.py
```


