# 🏗️ Architecture Documentation

## System Overview

Smart RAG Chatbot is designed with a modular, production-ready architecture that separates concerns and enables easy maintenance and extension.

## Core Components

### 1. RAG Engine (`main.py`)

The heart of the system, implementing intelligent routing and conversation management.

```
┌─────────────────────────────────────────┐
│         User Question                    │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Question Classifier (LLM)            │
│    - Casual vs Knowledge                 │
│    - Context-aware classification        │
└──────────────┬──────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
┌──────────────┐  ┌──────────────┐
│ Casual Mode  │  │ Knowledge    │
│ (Direct LLM) │  │ Mode (RAG)   │
└──────────────┘  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │  Retriever   │
                  │  (VectorDB)  │
                  └──────┬───────┘
                         │
                         ▼
                  ┌──────────────┐
                  │ LLM Generate │
                  │ with Context │
                  └──────────────┘
```

### 2. LLM Provider Abstraction (`llm_provider.py`)

Enables seamless switching between Ollama (local) and OpenAI (cloud).

```python
get_llm() → Returns appropriate LLM instance
get_embeddings() → Returns appropriate embeddings instance
```

**Benefits:**
- Easy provider switching
- Consistent interface
- Environment-based configuration

### 3. Document Processing Pipeline (`ingestion.py`)

Handles document loading, chunking, and vectorization.

```
Document → Load → Chunk → Embed → Store → Retrieve
```

**Supported Formats:**
- PDF
- TXT
- DOCX
- Web URLs

### 4. Utilities Layer

#### a. Caching (`utils/cache.py`)
- Thread-safe in-memory cache
- TTL support
- Decorator-based usage

#### b. Logging (`utils/logger.py`)
- Structured logging (JSON/Console)
- Context enrichment
- Multiple handlers

#### c. Metrics (`utils/metrics.py`)
- Request tracking
- Latency measurement
- Error counting
- Cache hit rates

#### d. Retry & Circuit Breaker (`utils/retry.py`)
- Exponential backoff
- Configurable retry logic
- Circuit breaker pattern

#### e. Validation (`utils/validation.py`)
- Input sanitization
- Security checks
- Type validation

## Data Flow

### Conversation with Memory

```
┌─────────────────────────────────────────┐
│         Conversation Memory              │
│  [user: "What is X?",                   │
│   assistant: "X is...",                 │
│   user: "How does it work?"]           │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    New Question + Context                │
│    "How does it work?" + memory         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│    Context-Aware Processing              │
│    (Knows "it" refers to X)             │
└──────────────────────────────────────────┘
```

### RAG Pipeline

```
┌──────────────┐
│   Question   │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  Embed Question  │
└──────┬───────────┘
       │
       ▼
┌──────────────────────────┐
│  Vector Similarity       │
│  Search (top-k docs)     │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  Rank & Filter           │
│  (relevance check)       │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  Augment Prompt          │
│  (question + context)    │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  LLM Generate            │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│  Post-process            │
│  (add sources, etc.)     │
└──────────────────────────┘
```

## Configuration System

Environment-based configuration with validation:

```python
Config (Pydantic BaseModel)
├── LLM Provider Settings
├── Embedding Settings
├── Vector Store Settings
├── System Settings
└── Logging Settings
```

**Features:**
- Type checking
- Value validation
- Default values
- Environment variable loading

## Error Handling Strategy

```
Exception Hierarchy:
AdvancedRAGException (base)
├── ConfigurationError
├── RetrievalError
├── VectorStoreError
├── GenerationError
├── WebSearchError
├── GradingError
├── ValidationError
├── CacheError
└── RetryExhaustedError
```

Each exception includes:
- Detailed message
- Context dictionary
- Logging integration

## Performance Optimizations

### 1. Caching
- Function-level caching with decorators
- LRU eviction policy
- TTL support

### 2. Batch Processing
- Document loading in batches
- Parallel embedding (when supported)

### 3. Lazy Loading
- LLM models loaded on first use
- Vector store initialized on demand

### 4. Memory Management
- Conversation memory limited to last N messages
- Automatic cleanup of expired cache entries

## Security Considerations

### 1. Input Validation
- XSS prevention
- SQL injection prevention
- Path traversal prevention

### 2. API Key Management
- Environment variables only
- Never logged or exposed

### 3. Rate Limiting
- Circuit breaker for external APIs
- Configurable retry limits

## Extensibility Points

### Adding New LLM Providers

```python
# In llm_provider.py
if config.llm_provider == "new_provider":
    return NewProviderLLM(...)
```

### Adding New Document Loaders

```python
# In ingestion.py or load_custom_docs.py
if file_ext == ".new_format":
    loader = NewFormatLoader(file_path)
```

### Adding New Features

The modular design makes it easy to add:
- New conversation modes
- Additional grading steps
- Custom retrieval strategies
- Alternative vector stores

## Testing Strategy

### Unit Tests
- Individual component testing
- Mocked dependencies
- Edge case coverage

### Integration Tests
- End-to-end flows
- Real LLM interactions (optional)
- Vector store operations

## Deployment Considerations

### Development
```bash
LOG_LEVEL=DEBUG
LOG_FORMAT=console
LLM_PROVIDER=ollama
```

### Production
```bash
LOG_LEVEL=INFO
LOG_FORMAT=json
LLM_PROVIDER=openai  # or optimized Ollama setup
ENABLE_CACHE=true
```

## Monitoring & Observability

### Metrics Collected
- Request count (total/success/failure)
- Latency (avg/min/max per operation)
- Cache hit rate
- Error counts by type
- LLM token usage (if tracked)

### Logging Levels
- DEBUG: Detailed execution flow
- INFO: Key operations and results
- WARNING: Degraded performance or recoverable errors
- ERROR: Operation failures
- CRITICAL: System-level failures

## Future Architecture Enhancements

### Planned
1. **Async/Await Support**
   - Non-blocking I/O
   - Concurrent request handling

2. **Distributed Caching**
   - Redis integration
   - Shared cache across instances

3. **Database Integration**
   - Persistent conversation history
   - User management

4. **API Layer**
   - FastAPI REST endpoints
   - WebSocket support for streaming

5. **Multi-tenancy**
   - Isolated vector stores per user
   - Resource quotas

---

*This architecture is designed to be simple enough for understanding but robust enough for production use.*

