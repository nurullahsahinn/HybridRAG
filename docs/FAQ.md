# ❓ Frequently Asked Questions

## General

### Q: What is RAG?
**A:** RAG (Retrieval-Augmented Generation) is a technique that enhances LLM responses by retrieving relevant documents and including them as context in the prompt.

### Q: Why use local LLMs instead of OpenAI?
**A:** 
- **Cost**: $0 vs $30-100/month
- **Privacy**: Your data never leaves your machine
- **Control**: Full control over the model
- **Learning**: Great for understanding how LLMs work

### Q: Can I use both Ollama and OpenAI?
**A:** Yes! You can mix and match:
- Ollama for LLM (free)
- OpenAI for embeddings (fast, ~$0.01)

## Setup

### Q: How much RAM do I need?
**A:** 
- Minimum: 8GB
- Recommended: 16GB
- Optimal: 32GB+

### Q: Do I need a GPU?
**A:** 
- No, but it helps significantly
- CPU: 30-60s per response
- GPU: 3-8s per response

### Q: What models can I use?
**A:** Any Ollama model:
```bash
ollama pull llama3.1:8b     # Recommended
ollama pull llama3.2:3b     # Faster, smaller
ollama pull mistral:7b      # Alternative
```

### Q: Installation fails on Windows
**A:** Common issues:
1. Python not in PATH → Reinstall and check "Add to PATH"
2. Visual C++ missing → Install Visual Studio Build Tools
3. Ollama not running → Start Ollama app

## Usage

### Q: How do I add my own documents?
**A:** 
```bash
python load_custom_docs.py path/to/your/documents/
```
Supports PDF, TXT, DOCX files.

### Q: Can it search the web?
**A:** Currently focuses on local documents. Web search can be added with Tavily API (see config).

### Q: Does it remember previous conversations?
**A:** Yes! It remembers the last 10 messages and uses them for context.

### Q: How do I reset the conversation?
**A:** Restart the CLI (`python cli.py`). Memory is not persistent between sessions.

## Performance

### Q: Why is it slow?
**A:** Possible reasons:
1. Using CPU instead of GPU
2. Ollama embedding (try OpenAI embedding)
3. Model is too large (try smaller model)
4. First run (model loading takes time)

### Q: How to make it faster?
**A:**
1. **Use GPU** (biggest impact!)
2. **OpenAI embeddings** for document loading
3. **Smaller model**: `llama3.2:3b` instead of `llama3.1:8b`
4. **Enable caching** in .env

### Q: Embedding takes forever!
**A:** Switch to OpenAI for embeddings:
```env
EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=sk-...
```
Cost: ~$0.01 for 1000 documents

## Errors

### Q: "Ollama is not running"
**A:** 
```bash
# Windows: Start Ollama app from Start menu
# Linux/Mac:
ollama serve
```

### Q: "Model not found"
**A:**
```bash
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

### Q: "Configuration error"
**A:** Check `.env` file exists and has required values:
```env
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama
```

### Q: "Out of memory"
**A:** 
- Use smaller model: `llama3.2:3b`
- Close other applications
- Upgrade RAM

## Advanced

### Q: Can I use this in production?
**A:** Yes, but consider:
- Error handling is comprehensive
- Add database for persistent conversations
- Set up proper monitoring
- Use GPU for better performance

### Q: How to deploy on a server?
**A:**
1. Install Ollama on server
2. Set up systemd service (Linux)
3. Configure firewall
4. Use reverse proxy (nginx) if exposing API

### Q: Can I fine-tune the model?
**A:** Not directly with Ollama, but you can:
- Use different models
- Adjust temperature in config
- Customize prompts in `main.py`

### Q: How to add new document types?
**A:** Edit `load_custom_docs.py`:
```python
elif file_path.suffix.lower() == '.your_format':
    loader = YourFormatLoader(str(file_path))
```

### Q: Can I use multiple vector stores?
**A:** Yes, modify `ingestion.py` to create separate collections per category/course.

## Privacy & Security

### Q: Is my data safe?
**A:** When using Ollama:
- Everything runs locally
- No data sent to external servers
- Complete privacy

### Q: What about API keys in .env?
**A:** 
- Never commit .env to git
- .env is in .gitignore
- Use environment variables in production

### Q: Can others access my documents?
**A:** No, when running locally only you have access. If deploying to a server, implement proper authentication.

## Troubleshooting

### Q: Responses are nonsensical
**A:**
- Check if using correct model
- Try lowering temperature
- Ensure documents are properly loaded

### Q: It doesn't find relevant documents
**A:**
- Check if documents are in vector store
- Try different chunking size
- Use better search terms

### Q: Memory usage keeps growing
**A:** 
- Restart the application periodically
- Clear .chroma folder and re-index
- Adjust CHUNK_SIZE in config

## Contributing

### Q: How can I contribute?
**A:** See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines!

### Q: I found a bug!
**A:** Create an issue on GitHub with details.

### Q: I have an idea!
**A:** Great! Open an issue to discuss it.

---

**Didn't find your question?** Open an issue on GitHub!

