"""Tests for configuration management."""
import os
import pytest
from config import Config, load_config
from exceptions import ConfigurationError


def test_config_validation():
    """Test configuration validation."""
    # Valid configuration
    config = Config(
        openai_api_key="sk-test123456789012345",
        tavily_api_key="tvly-test123456789012345"
    )
    assert config.openai_api_key == "sk-test123456789012345"
    assert config.openai_model == "gpt-4o-mini"
    assert config.chunk_size == 250


def test_config_invalid_api_key():
    """Test that invalid API keys are rejected."""
    with pytest.raises(ValueError):
        Config(
            openai_api_key="",
            tavily_api_key="test"
        )


def test_config_temperature_bounds():
    """Test temperature validation."""
    # Valid temperature
    config = Config(
        openai_api_key="sk-test123456789012345",
        tavily_api_key="tvly-test123456789012345",
        openai_temperature=1.5
    )
    assert config.openai_temperature == 1.5
    
    # Invalid temperature
    with pytest.raises(ValueError):
        Config(
            openai_api_key="sk-test123456789012345",
            tavily_api_key="tvly-test123456789012345",
            openai_temperature=3.0
        )


def test_config_chunk_size():
    """Test chunk size validation."""
    # Valid chunk size
    config = Config(
        openai_api_key="sk-test123456789012345",
        tavily_api_key="tvly-test123456789012345",
        chunk_size=500
    )
    assert config.chunk_size == 500
    
    # Invalid chunk size
    with pytest.raises(ValueError):
        Config(
            openai_api_key="sk-test123456789012345",
            tavily_api_key="tvly-test123456789012345",
            chunk_size=0
        )


