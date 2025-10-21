"""
Configuration management with validation for Advanced RAG system.
"""
import os
from typing import Optional
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv

load_dotenv()


class Config(BaseModel):
    """Main configuration class with validation."""
    
    # LLM Provider Configuration
    llm_provider: str = Field(default="ollama", description="LLM provider: 'openai' or 'ollama'")
    
    # OpenAI Configuration (if using OpenAI)
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API key")
    openai_model: str = Field(default="gpt-4o-mini", description="OpenAI model to use")
    openai_temperature: float = Field(default=0.3, ge=0.0, le=2.0, description="Temperature for generation")
    
    # Ollama Configuration (if using Ollama - local LLM)
    ollama_base_url: str = Field(default="http://localhost:11434", description="Ollama server URL")
    ollama_model: str = Field(default="llama3.1:8b", description="Ollama model to use")
    
    # Embedding Provider Configuration
    embedding_provider: str = Field(default="ollama", description="Embedding provider: 'openai' or 'ollama'")
    embedding_model: str = Field(default="nomic-embed-text", description="Embedding model (for Ollama)")
    
    # LangChain Configuration
    langchain_api_key: Optional[str] = Field(default=None, description="LangChain API key for tracing")
    langchain_tracing_v2: bool = Field(default=False, description="Enable LangChain tracing")
    langchain_project: Optional[str] = Field(default="advanced-rag", description="LangChain project name")
    
    # Tavily Configuration (optional - for web search)
    tavily_api_key: Optional[str] = Field(default=None, description="Tavily API key for web search")
    
    # Vector Store Configuration
    chroma_persist_directory: str = Field(default="./.chroma", description="Chroma persistence directory")
    chroma_collection_name: str = Field(default="rag-chroma", description="Chroma collection name")
    
    # Chunking Configuration
    chunk_size: int = Field(default=250, gt=0, le=2000, description="Text chunk size")
    chunk_overlap: int = Field(default=50, ge=0, description="Chunk overlap size")
    
    # Retrieval Configuration
    retrieval_k: int = Field(default=4, gt=0, le=20, description="Number of documents to retrieve")
    
    # Web Search Configuration
    web_search_k: int = Field(default=3, gt=0, le=10, description="Number of web search results")
    
    # Retry Configuration
    max_retries: int = Field(default=3, gt=0, le=10, description="Maximum number of retries")
    retry_delay: float = Field(default=1.0, gt=0, description="Delay between retries in seconds")
    
    # Cache Configuration
    enable_cache: bool = Field(default=True, description="Enable response caching")
    cache_ttl: int = Field(default=3600, gt=0, description="Cache TTL in seconds")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", description="Logging level")
    log_format: str = Field(default="json", description="Log format: json or console")
    
    @validator("llm_provider", "embedding_provider")
    def validate_providers(cls, v):
        """Validate provider values."""
        valid_providers = ["openai", "ollama"]
        if v not in valid_providers:
            raise ValueError(f"Provider must be one of {valid_providers}")
        return v
    
    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        v = v.upper()
        if v not in valid_levels:
            raise ValueError(f"log_level must be one of {valid_levels}")
        return v
    
    @validator("log_format")
    def validate_log_format(cls, v):
        """Validate log format."""
        valid_formats = ["json", "console"]
        v = v.lower()
        if v not in valid_formats:
            raise ValueError(f"log_format must be one of {valid_formats}")
        return v
    
    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        arbitrary_types_allowed = True


def load_config() -> Config:
    """
    Load and validate configuration from environment variables.
    
    Returns:
        Config: Validated configuration object
        
    Raises:
        ValueError: If required configuration is missing or invalid
    """
    try:
        config = Config(
            # LLM Provider
            llm_provider=os.getenv("LLM_PROVIDER", "ollama"),
            
            # OpenAI (optional)
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            openai_temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.0")),
            
            # Ollama (local LLM)
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
            
            # Embeddings
            embedding_provider=os.getenv("EMBEDDING_PROVIDER", "ollama"),
            embedding_model=os.getenv("EMBEDDING_MODEL", "nomic-embed-text"),
            
            # LangChain
            langchain_api_key=os.getenv("LANGCHAIN_API_KEY"),
            langchain_tracing_v2=os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true",
            langchain_project=os.getenv("LANGCHAIN_PROJECT", "advanced-rag"),
            
            # Tavily (optional)
            tavily_api_key=os.getenv("TAVILY_API_KEY"),
            chroma_persist_directory=os.getenv("CHROMA_PERSIST_DIRECTORY", "./.chroma"),
            chroma_collection_name=os.getenv("CHROMA_COLLECTION_NAME", "rag-chroma"),
            chunk_size=int(os.getenv("CHUNK_SIZE", "250")),
            chunk_overlap=int(os.getenv("CHUNK_OVERLAP", "50")),
            retrieval_k=int(os.getenv("RETRIEVAL_K", "4")),
            web_search_k=int(os.getenv("WEB_SEARCH_K", "3")),
            max_retries=int(os.getenv("MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("RETRY_DELAY", "1.0")),
            enable_cache=os.getenv("ENABLE_CACHE", "true").lower() == "true",
            cache_ttl=int(os.getenv("CACHE_TTL", "3600")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_format=os.getenv("LOG_FORMAT", "json"),
        )
        return config
    except Exception as e:
        raise ValueError(f"Configuration error: {str(e)}") from e


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get the global configuration instance (singleton pattern).
    
    Returns:
        Config: Global configuration object
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config

