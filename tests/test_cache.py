"""Tests for caching mechanism."""
import time
import pytest
from utils.cache import InMemoryCache, get_cache, cached


def test_cache_basic_operations():
    """Test basic cache operations."""
    cache = InMemoryCache(ttl=10)
    
    # Set and get
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    
    # Get non-existent key
    assert cache.get("nonexistent") is None


def test_cache_expiration():
    """Test cache expiration."""
    cache = InMemoryCache(ttl=1)
    
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    
    # Wait for expiration
    time.sleep(1.1)
    assert cache.get("key1") is None


def test_cache_delete():
    """Test cache deletion."""
    cache = InMemoryCache(ttl=10)
    
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"
    
    cache.delete("key1")
    assert cache.get("key1") is None


def test_cache_clear():
    """Test cache clear."""
    cache = InMemoryCache(ttl=10)
    
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    
    cache.clear()
    assert cache.get("key1") is None
    assert cache.get("key2") is None


def test_cache_cleanup():
    """Test cleanup of expired entries."""
    cache = InMemoryCache(ttl=1)
    
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    
    time.sleep(1.1)
    removed = cache.cleanup_expired()
    assert removed == 2


def test_cached_decorator():
    """Test cached decorator."""
    call_count = [0]
    
    @cached(ttl=10, enabled=True)
    def expensive_function(x):
        call_count[0] += 1
        return x * 2
    
    # First call
    result1 = expensive_function(5)
    assert result1 == 10
    assert call_count[0] == 1
    
    # Second call (should be cached)
    result2 = expensive_function(5)
    assert result2 == 10
    assert call_count[0] == 1  # Not incremented
    
    # Different argument (not cached)
    result3 = expensive_function(10)
    assert result3 == 20
    assert call_count[0] == 2


def test_cached_decorator_disabled():
    """Test cached decorator when disabled."""
    call_count = [0]
    
    @cached(ttl=10, enabled=False)
    def expensive_function(x):
        call_count[0] += 1
        return x * 2
    
    result1 = expensive_function(5)
    result2 = expensive_function(5)
    
    # Both calls should execute the function
    assert call_count[0] == 2


