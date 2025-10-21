"""
Caching mechanism for Advanced RAG system.
"""
import hashlib
import json
import time
from typing import Any, Dict, Optional, Callable
from functools import wraps
from threading import Lock

from utils.logger import get_logger

logger = get_logger(__name__)


class InMemoryCache:
    """Thread-safe in-memory cache with TTL support."""
    
    def __init__(self, ttl: int = 3600):
        """
        Initialize cache.
        
        Args:
            ttl: Time to live in seconds
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        self.ttl = ttl
        logger.info("Cache initialized", extra={"ttl": ttl})
    
    def _generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments."""
        key_data = {
            "args": str(args),
            "kwargs": sorted(kwargs.items())
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_string.encode()).hexdigest()
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        with self._lock:
            if key not in self._cache:
                logger.debug("Cache miss", extra={"key": key})
                return None
            
            entry = self._cache[key]
            
            # Check if expired
            if time.time() > entry["expires_at"]:
                logger.debug("Cache expired", extra={"key": key})
                del self._cache[key]
                return None
            
            logger.debug("Cache hit", extra={"key": key})
            return entry["value"]
    
    def set(self, key: str, value: Any, ttl: int = None) -> None:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Optional custom TTL
        """
        ttl = ttl or self.ttl
        with self._lock:
            self._cache[key] = {
                "value": value,
                "expires_at": time.time() + ttl,
                "created_at": time.time()
            }
            logger.debug("Cache set", extra={"key": key, "ttl": ttl})
    
    def delete(self, key: str) -> None:
        """Delete key from cache."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                logger.debug("Cache deleted", extra={"key": key})
    
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            logger.info("Cache cleared", extra={"entries_removed": count})
    
    def cleanup_expired(self) -> int:
        """
        Remove expired entries from cache.
        
        Returns:
            Number of entries removed
        """
        with self._lock:
            current_time = time.time()
            expired_keys = [
                key for key, entry in self._cache.items()
                if current_time > entry["expires_at"]
            ]
            
            for key in expired_keys:
                del self._cache[key]
            
            if expired_keys:
                logger.info(
                    "Expired cache entries cleaned",
                    extra={"count": len(expired_keys)}
                )
            
            return len(expired_keys)
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            return {
                "total_entries": len(self._cache),
                "ttl": self.ttl
            }


# Global cache instance
_cache: Optional[InMemoryCache] = None


def get_cache(ttl: int = 3600) -> InMemoryCache:
    """
    Get global cache instance (singleton pattern).
    
    Args:
        ttl: Time to live in seconds
        
    Returns:
        Cache instance
    """
    global _cache
    if _cache is None:
        _cache = InMemoryCache(ttl=ttl)
    return _cache


def cached(ttl: int = None, enabled: bool = True):
    """
    Decorator to cache function results.
    
    Args:
        ttl: Optional custom TTL
        enabled: Whether caching is enabled
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not enabled:
                return func(*args, **kwargs)
            
            cache = get_cache()
            cache_key = cache._generate_key(func.__name__, *args, **kwargs)
            
            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                logger.debug(
                    f"Returning cached result for {func.__name__}",
                    extra={"function": func.__name__}
                )
                return cached_value
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cache result
            cache.set(cache_key, result, ttl=ttl)
            logger.debug(
                f"Cached result for {func.__name__}",
                extra={"function": func.__name__}
            )
            
            return result
        
        return wrapper
    return decorator


