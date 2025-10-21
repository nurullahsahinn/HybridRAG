"""
Custom exceptions for Advanced RAG system.
"""


class AdvancedRAGException(Exception):
    """Base exception for all Advanced RAG errors."""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self):
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class ConfigurationError(AdvancedRAGException):
    """Raised when configuration is invalid or missing."""
    pass


class APIKeyError(ConfigurationError):
    """Raised when API keys are missing or invalid."""
    pass


class RetrievalError(AdvancedRAGException):
    """Raised when document retrieval fails."""
    pass


class VectorStoreError(AdvancedRAGException):
    """Raised when vector store operations fail."""
    pass


class GenerationError(AdvancedRAGException):
    """Raised when text generation fails."""
    pass


class WebSearchError(AdvancedRAGException):
    """Raised when web search fails."""
    pass


class GradingError(AdvancedRAGException):
    """Raised when document/answer grading fails."""
    pass


class ValidationError(AdvancedRAGException):
    """Raised when input validation fails."""
    pass


class CacheError(AdvancedRAGException):
    """Raised when cache operations fail."""
    pass


class RetryExhaustedError(AdvancedRAGException):
    """Raised when maximum retry attempts are exhausted."""
    pass


