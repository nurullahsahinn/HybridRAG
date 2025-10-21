"""
Input validation utilities for Advanced RAG system.
"""
from typing import List, Any
import re

from exceptions import ValidationError
from utils.logger import get_logger

logger = get_logger(__name__)


def validate_question(question: str) -> str:
    """
    Validate and sanitize user question.
    
    Args:
        question: User question to validate
        
    Returns:
        Sanitized question
        
    Raises:
        ValidationError: If question is invalid
    """
    if not question:
        raise ValidationError("Question cannot be empty")
    
    if not isinstance(question, str):
        raise ValidationError(
            "Question must be a string",
            details={"type": type(question).__name__}
        )
    
    # Strip whitespace
    question = question.strip()
    
    # Check minimum length
    if len(question) < 3:
        raise ValidationError(
            "Question too short (minimum 3 characters)",
            details={"length": len(question)}
        )
    
    # Check maximum length
    if len(question) > 1000:
        raise ValidationError(
            "Question too long (maximum 1000 characters)",
            details={"length": len(question)}
        )
    
    # Check for potentially malicious patterns
    suspicious_patterns = [
        r"<script",
        r"javascript:",
        r"onerror=",
        r"onclick=",
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, question, re.IGNORECASE):
            logger.warning(
                "Suspicious pattern detected in question",
                extra={"pattern": pattern}
            )
            raise ValidationError(
                "Question contains suspicious content",
                details={"pattern": pattern}
            )
    
    logger.debug("Question validated", extra={"question_length": len(question)})
    return question


def validate_documents(documents: List[Any]) -> List[Any]:
    """
    Validate document list.
    
    Args:
        documents: List of documents to validate
        
    Returns:
        Validated documents
        
    Raises:
        ValidationError: If documents are invalid
    """
    if not documents:
        logger.warning("Empty document list provided")
        return []
    
    if not isinstance(documents, list):
        raise ValidationError(
            "Documents must be a list",
            details={"type": type(documents).__name__}
        )
    
    # Check maximum number of documents
    if len(documents) > 100:
        logger.warning(
            "Too many documents, truncating",
            extra={"count": len(documents), "limit": 100}
        )
        documents = documents[:100]
    
    logger.debug("Documents validated", extra={"count": len(documents)})
    return documents


def validate_generation(generation: str) -> str:
    """
    Validate generated text.
    
    Args:
        generation: Generated text to validate
        
    Returns:
        Validated generation
        
    Raises:
        ValidationError: If generation is invalid
    """
    if not generation:
        raise ValidationError("Generation cannot be empty")
    
    if not isinstance(generation, str):
        raise ValidationError(
            "Generation must be a string",
            details={"type": type(generation).__name__}
        )
    
    generation = generation.strip()
    
    # Check minimum length
    if len(generation) < 10:
        raise ValidationError(
            "Generation too short (minimum 10 characters)",
            details={"length": len(generation)}
        )
    
    logger.debug("Generation validated", extra={"length": len(generation)})
    return generation


def sanitize_text(text: str, max_length: int = None) -> str:
    """
    Sanitize text by removing unwanted characters.
    
    Args:
        text: Text to sanitize
        max_length: Optional maximum length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove null bytes
    text = text.replace("\x00", "")
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Strip
    text = text.strip()
    
    # Truncate if needed
    if max_length and len(text) > max_length:
        text = text[:max_length]
    
    return text


