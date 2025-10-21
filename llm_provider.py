"""
LLM Provider abstraction for switching between OpenAI and Local LLMs (Ollama).
"""
from typing import Union, Any
from langchain_core.language_models import BaseChatModel, BaseLanguageModel
from langchain_core.embeddings import Embeddings

from config import get_config
from utils.logger import get_logger

logger = get_logger(__name__)


def get_llm() -> Union[BaseChatModel, BaseLanguageModel]:
    """
    Get LLM instance based on configuration.
    
    Supports:
    - OpenAI (default)
    - Ollama (local LLM)
    
    Returns:
        LLM instance ready to use
        
    Example:
        >>> llm = get_llm()
        >>> result = llm.invoke("Hello!")
    """
    config = get_config()
    
    if config.llm_provider == "ollama":
        logger.info(f"Initializing Ollama LLM: {config.ollama_model}")
        
        try:
            from langchain_community.llms import Ollama
            
            llm = Ollama(
                model=config.ollama_model,
                base_url=config.ollama_base_url,
                temperature=0.3,  # Biraz yaratıcılık için (0=robotik, 1=yaratıcı)
            )
            
            logger.info("Ollama LLM initialized successfully")
            return llm
            
        except ImportError:
            logger.error("langchain-community not installed. Install: pip install langchain-community")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Ollama: {str(e)}")
            logger.warning("Make sure Ollama is running: ollama serve")
            raise
    
    elif config.llm_provider == "openai":
        logger.info(f"Initializing OpenAI LLM: {config.openai_model}")
        
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(
            model=config.openai_model,
            temperature=config.openai_temperature,
        )
        
        logger.info("OpenAI LLM initialized successfully")
        return llm
    
    else:
        raise ValueError(
            f"Unknown LLM provider: {config.llm_provider}. "
            f"Supported: 'openai', 'ollama'"
        )


def get_embeddings() -> Embeddings:
    """
    Get embeddings instance based on configuration.
    
    Supports:
    - OpenAI (default)
    - Ollama (local embeddings)
    
    Returns:
        Embeddings instance ready to use
        
    Example:
        >>> embeddings = get_embeddings()
        >>> vectors = embeddings.embed_documents(["Hello", "World"])
    """
    config = get_config()
    
    if config.embedding_provider == "ollama":
        logger.info(f"Initializing Ollama embeddings: {config.embedding_model}")
        
        try:
            from langchain_community.embeddings import OllamaEmbeddings
            
            embeddings = OllamaEmbeddings(
                model=config.embedding_model,
                base_url=config.ollama_base_url,
            )
            
            logger.info("Ollama embeddings initialized successfully")
            return embeddings
            
        except ImportError:
            logger.error("langchain-community not installed. Install: pip install langchain-community")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize Ollama embeddings: {str(e)}")
            logger.warning("Make sure Ollama is running and model is pulled: ollama pull nomic-embed-text")
            raise
    
    elif config.embedding_provider == "openai":
        logger.info("Initializing OpenAI embeddings")
        
        from langchain_openai import OpenAIEmbeddings
        
        embeddings = OpenAIEmbeddings()
        
        logger.info("OpenAI embeddings initialized successfully")
        return embeddings
    
    else:
        raise ValueError(
            f"Unknown embedding provider: {config.embedding_provider}. "
            f"Supported: 'openai', 'ollama'"
        )


def test_llm_connection():
    """
    Test LLM connection and basic functionality.
    
    Returns:
        bool: True if connection successful
    """
    try:
        logger.info("Testing LLM connection...")
        
        llm = get_llm()
        response = llm.invoke("Hello! Please respond with 'OK'")
        
        logger.info(f"LLM test response: {response}")
        logger.info("✓ LLM connection test successful")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ LLM connection test failed: {str(e)}")
        return False


def test_embeddings_connection():
    """
    Test embeddings connection and basic functionality.
    
    Returns:
        bool: True if connection successful
    """
    try:
        logger.info("Testing embeddings connection...")
        
        embeddings = get_embeddings()
        vectors = embeddings.embed_documents(["Test document"])
        
        logger.info(f"Embeddings test: generated {len(vectors[0])} dimensions")
        logger.info("✓ Embeddings connection test successful")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Embeddings connection test failed: {str(e)}")
        return False


if __name__ == "__main__":
    # Test script
    print("Testing LLM Provider...")
    print("=" * 80)
    
    llm_ok = test_llm_connection()
    print()
    
    embeddings_ok = test_embeddings_connection()
    print()
    
    if llm_ok and embeddings_ok:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed. Check configuration and Ollama status.")

