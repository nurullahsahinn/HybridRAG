"""Tests for input validation."""
import pytest
from utils.validation import (
    validate_question,
    validate_documents,
    validate_generation,
    sanitize_text
)
from exceptions import ValidationError


def test_validate_question_valid():
    """Test valid question validation."""
    question = "What is machine learning?"
    result = validate_question(question)
    assert result == question


def test_validate_question_empty():
    """Test empty question rejection."""
    with pytest.raises(ValidationError):
        validate_question("")


def test_validate_question_too_short():
    """Test too short question rejection."""
    with pytest.raises(ValidationError):
        validate_question("Hi")


def test_validate_question_too_long():
    """Test too long question rejection."""
    with pytest.raises(ValidationError):
        validate_question("a" * 1001)


def test_validate_question_suspicious():
    """Test suspicious content detection."""
    with pytest.raises(ValidationError):
        validate_question("<script>alert('xss')</script>")


def test_validate_documents_valid():
    """Test valid documents validation."""
    docs = ["doc1", "doc2", "doc3"]
    result = validate_documents(docs)
    assert result == docs


def test_validate_documents_empty():
    """Test empty documents list."""
    result = validate_documents([])
    assert result == []


def test_validate_documents_too_many():
    """Test too many documents truncation."""
    docs = [f"doc{i}" for i in range(150)]
    result = validate_documents(docs)
    assert len(result) == 100


def test_validate_generation_valid():
    """Test valid generation validation."""
    generation = "This is a valid answer to the question."
    result = validate_generation(generation)
    assert result == generation


def test_validate_generation_empty():
    """Test empty generation rejection."""
    with pytest.raises(ValidationError):
        validate_generation("")


def test_validate_generation_too_short():
    """Test too short generation rejection."""
    with pytest.raises(ValidationError):
        validate_generation("Short")


def test_sanitize_text():
    """Test text sanitization."""
    text = "  Hello   World  \n\n  Test  "
    result = sanitize_text(text)
    assert result == "Hello World Test"
    
    # Test with null bytes
    text_with_null = "Hello\x00World"
    result = sanitize_text(text_with_null)
    assert "\x00" not in result
    
    # Test max length
    long_text = "a" * 100
    result = sanitize_text(long_text, max_length=50)
    assert len(result) == 50


