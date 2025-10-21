"""
Document ingestion and vector store management for Advanced RAG system.
"""
from typing import List, Optional
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

from config import get_config
from exceptions import VectorStoreError
from utils.logger import get_logger, setup_logger
from utils.retry import retry_with_backoff
from utils.metrics import track_time, get_metrics_collector
from llm_provider import get_embeddings

# Setup logger
config = get_config()
setup_logger(
    name="advanced_rag",
    log_level=config.log_level,
    log_format=config.log_format,
    log_file="logs/advanced_rag.log"
)
logger = get_logger(__name__)

# Default URLs for ingestion
DEFAULT_URLS = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
]


@retry_with_backoff(max_retries=3, initial_delay=2.0, exceptions=(Exception,))
@track_time("load_documents")
def load_documents(urls: List[str]) -> List[Document]:
    """
    Load documents from URLs with retry logic.
    
    Args:
        urls: List of URLs to load
        
    Returns:
        List of loaded documents
        
    Raises:
        VectorStoreError: If document loading fails
    """
    try:
        logger.info(f"Loading documents from {len(urls)} URLs")
        
        docs = []
        for url in urls:
            try:
                logger.debug(f"Loading URL: {url}")
                loader = WebBaseLoader(url)
                loaded_docs = loader.load()
                docs.extend(loaded_docs)
                logger.debug(f"Loaded {len(loaded_docs)} documents from {url}")
            except Exception as e:
                logger.warning(f"Failed to load URL {url}: {str(e)}")
                # Continue with other URLs
                continue
        
        if not docs:
            raise VectorStoreError(
                "No documents could be loaded from any URL",
                details={"urls": urls}
            )
        
        logger.info(f"Successfully loaded {len(docs)} total documents")
        return docs
        
    except Exception as e:
        logger.error(f"Document loading failed: {str(e)}")
        raise VectorStoreError(f"Failed to load documents: {str(e)}") from e


@track_time("split_documents")
def split_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into chunks.
    
    Args:
        documents: List of documents to split
        
    Returns:
        List of document chunks
        
    Raises:
        VectorStoreError: If splitting fails
    """
    try:
        logger.info(f"Splitting {len(documents)} documents")
        
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap
        )
        
        doc_splits = text_splitter.split_documents(documents)
        
        logger.info(
            f"Split into {len(doc_splits)} chunks",
            extra={
                "original_docs": len(documents),
                "chunks": len(doc_splits),
                "chunk_size": config.chunk_size,
                "overlap": config.chunk_overlap
            }
        )
        
        return doc_splits
        
    except Exception as e:
        logger.error(f"Document splitting failed: {str(e)}")
        raise VectorStoreError(f"Failed to split documents: {str(e)}") from e


@track_time("create_vectorstore")
def create_vectorstore(
    documents: List[Document],
    persist_directory: Optional[str] = None,
    collection_name: Optional[str] = None
) -> Chroma:
    """
    Create vector store from documents.
    
    Args:
        documents: List of documents to index
        persist_directory: Optional custom persist directory
        collection_name: Optional custom collection name
        
    Returns:
        Chroma vector store instance
        
    Raises:
        VectorStoreError: If vector store creation fails
    """
    try:
        persist_dir = persist_directory or config.chroma_persist_directory
        collection = collection_name or config.chroma_collection_name
        
        logger.info(
            f"Creating vector store",
            extra={
                "documents": len(documents),
                "collection": collection,
                "persist_dir": persist_dir
            }
        )
        
        # Create directory if it doesn't exist
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        
        embeddings = get_embeddings()
        
        vectorstore = Chroma.from_documents(
            documents=documents,
            collection_name=collection,
            embedding=embeddings,
            persist_directory=persist_dir,
        )
        
        logger.info("Vector store created successfully")
        return vectorstore
        
    except Exception as e:
        logger.error(f"Vector store creation failed: {str(e)}")
        raise VectorStoreError(f"Failed to create vector store: {str(e)}") from e


def get_retriever(
    persist_directory: Optional[str] = None,
    collection_name: Optional[str] = None,
    k: Optional[int] = None
):
    """
    Get retriever from existing vector store.
    
    Args:
        persist_directory: Optional custom persist directory
        collection_name: Optional custom collection name
        k: Optional number of documents to retrieve
        
    Returns:
        Retriever instance
        
    Raises:
        VectorStoreError: If retriever creation fails
    """
    try:
        persist_dir = persist_directory or config.chroma_persist_directory
        collection = collection_name or config.chroma_collection_name
        retrieval_k = k or config.retrieval_k
        
        logger.info(
            f"Getting retriever",
            extra={
                "collection": collection,
                "persist_dir": persist_dir,
                "k": retrieval_k
            }
        )
        
        # Check if vector store exists
        if not Path(persist_dir).exists():
            logger.warning(f"Vector store not found at {persist_dir}, creating new one")
            docs = load_documents(DEFAULT_URLS)
            doc_splits = split_documents(docs)
            create_vectorstore(doc_splits, persist_dir, collection)
        
        embeddings = get_embeddings()
        
        retriever = Chroma(
            collection_name=collection,
            persist_directory=persist_dir,
            embedding_function=embeddings,
        ).as_retriever(search_kwargs={"k": retrieval_k})
        
        logger.info("Retriever created successfully")
        return retriever
        
    except Exception as e:
        logger.error(f"Retriever creation failed: {str(e)}")
        raise VectorStoreError(f"Failed to get retriever: {str(e)}") from e


def initialize_vectorstore(urls: Optional[List[str]] = None, force: bool = False):
    """
    Initialize vector store with documents.
    
    Args:
        urls: Optional list of URLs (defaults to DEFAULT_URLS)
        force: Force re-creation even if exists
        
    Returns:
        Tuple of (vectorstore, retriever)
    """
    try:
        persist_dir = config.chroma_persist_directory
        
        # Check if already exists
        if Path(persist_dir).exists() and not force:
            logger.info(f"Vector store already exists at {persist_dir}")
            retriever = get_retriever()
            embeddings = get_embeddings()
            vectorstore = Chroma(
                collection_name=config.chroma_collection_name,
                persist_directory=persist_dir,
                embedding_function=embeddings,
            )
            return vectorstore, retriever
        
        # Load and process documents
        urls = urls or DEFAULT_URLS
        docs = load_documents(urls)
        doc_splits = split_documents(docs)
        
        # Create vector store
        vectorstore = create_vectorstore(doc_splits)
        retriever = get_retriever()
        
        metrics = get_metrics_collector()
        logger.info(
            "Vector store initialized successfully",
            extra={
                "urls_count": len(urls),
                "documents": len(docs),
                "chunks": len(doc_splits)
            }
        )
        
        return vectorstore, retriever
        
    except Exception as e:
        logger.error(f"Vector store initialization failed: {str(e)}")
        raise VectorStoreError(f"Failed to initialize vector store: {str(e)}") from e


# Initialize retriever on module import
try:
    retriever = get_retriever()
except Exception as e:
    logger.error(f"Failed to initialize retriever on import: {str(e)}")
    retriever = None