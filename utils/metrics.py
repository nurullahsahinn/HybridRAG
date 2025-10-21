"""
Metrics and monitoring utilities for Advanced RAG system.
"""
import time
from typing import Dict, Any, Optional
from functools import wraps
from threading import Lock
from datetime import datetime

from utils.logger import get_logger

logger = get_logger(__name__)


class MetricsCollector:
    """Thread-safe metrics collector for monitoring system performance."""
    
    def __init__(self):
        """Initialize metrics collector."""
        self._metrics: Dict[str, Any] = {
            "requests": {
                "total": 0,
                "success": 0,
                "failure": 0,
            },
            "nodes": {},
            "latency": {},
            "errors": {},
            "cache": {
                "hits": 0,
                "misses": 0,
            }
        }
        self._lock = Lock()
        self._start_time = time.time()
        logger.info("Metrics collector initialized")
    
    def increment_request(self, success: bool = True) -> None:
        """Increment request counter."""
        with self._lock:
            self._metrics["requests"]["total"] += 1
            if success:
                self._metrics["requests"]["success"] += 1
            else:
                self._metrics["requests"]["failure"] += 1
    
    def record_node_execution(self, node_name: str, duration: float, success: bool = True) -> None:
        """
        Record node execution metrics.
        
        Args:
            node_name: Name of the node
            duration: Execution duration in seconds
            success: Whether execution was successful
        """
        with self._lock:
            if node_name not in self._metrics["nodes"]:
                self._metrics["nodes"][node_name] = {
                    "count": 0,
                    "success": 0,
                    "failure": 0,
                    "total_duration": 0.0,
                    "avg_duration": 0.0,
                    "min_duration": float('inf'),
                    "max_duration": 0.0,
                }
            
            node_metrics = self._metrics["nodes"][node_name]
            node_metrics["count"] += 1
            
            if success:
                node_metrics["success"] += 1
            else:
                node_metrics["failure"] += 1
            
            node_metrics["total_duration"] += duration
            node_metrics["avg_duration"] = node_metrics["total_duration"] / node_metrics["count"]
            node_metrics["min_duration"] = min(node_metrics["min_duration"], duration)
            node_metrics["max_duration"] = max(node_metrics["max_duration"], duration)
    
    def record_latency(self, operation: str, duration: float) -> None:
        """
        Record operation latency.
        
        Args:
            operation: Operation name
            duration: Duration in seconds
        """
        with self._lock:
            if operation not in self._metrics["latency"]:
                self._metrics["latency"][operation] = {
                    "count": 0,
                    "total": 0.0,
                    "avg": 0.0,
                    "min": float('inf'),
                    "max": 0.0,
                }
            
            lat = self._metrics["latency"][operation]
            lat["count"] += 1
            lat["total"] += duration
            lat["avg"] = lat["total"] / lat["count"]
            lat["min"] = min(lat["min"], duration)
            lat["max"] = max(lat["max"], duration)
    
    def record_error(self, error_type: str) -> None:
        """
        Record error occurrence.
        
        Args:
            error_type: Type of error
        """
        with self._lock:
            if error_type not in self._metrics["errors"]:
                self._metrics["errors"][error_type] = 0
            self._metrics["errors"][error_type] += 1
    
    def record_cache_hit(self, hit: bool = True) -> None:
        """Record cache hit or miss."""
        with self._lock:
            if hit:
                self._metrics["cache"]["hits"] += 1
            else:
                self._metrics["cache"]["misses"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get all metrics.
        
        Returns:
            Dictionary of all metrics
        """
        with self._lock:
            uptime = time.time() - self._start_time
            
            # Calculate cache hit rate
            cache_total = self._metrics["cache"]["hits"] + self._metrics["cache"]["misses"]
            cache_hit_rate = (
                self._metrics["cache"]["hits"] / cache_total
                if cache_total > 0 else 0.0
            )
            
            # Calculate success rate
            total_requests = self._metrics["requests"]["total"]
            success_rate = (
                self._metrics["requests"]["success"] / total_requests
                if total_requests > 0 else 0.0
            )
            
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "uptime_seconds": uptime,
                "requests": self._metrics["requests"],
                "success_rate": success_rate,
                "nodes": self._metrics["nodes"],
                "latency": self._metrics["latency"],
                "errors": self._metrics["errors"],
                "cache": {
                    **self._metrics["cache"],
                    "hit_rate": cache_hit_rate,
                }
            }
    
    def reset(self) -> None:
        """Reset all metrics."""
        with self._lock:
            self._metrics = {
                "requests": {"total": 0, "success": 0, "failure": 0},
                "nodes": {},
                "latency": {},
                "errors": {},
                "cache": {"hits": 0, "misses": 0},
            }
            self._start_time = time.time()
            logger.info("Metrics reset")


# Global metrics collector
_metrics: Optional[MetricsCollector] = None


def get_metrics_collector() -> MetricsCollector:
    """
    Get global metrics collector instance (singleton pattern).
    
    Returns:
        MetricsCollector instance
    """
    global _metrics
    if _metrics is None:
        _metrics = MetricsCollector()
    return _metrics


def track_time(operation: str = None):
    """
    Decorator to track execution time.
    
    Args:
        operation: Optional operation name (defaults to function name)
        
    Returns:
        Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                raise
            finally:
                duration = time.time() - start_time
                op_name = operation or func.__name__
                
                metrics = get_metrics_collector()
                metrics.record_latency(op_name, duration)
                
                logger.debug(
                    f"Operation {op_name} completed",
                    extra={
                        "operation": op_name,
                        "duration": duration,
                        "success": success
                    }
                )
        
        return wrapper
    return decorator


def track_node_execution(node_name: str):
    """
    Decorator to track node execution metrics.
    
    Args:
        node_name: Name of the node
        
    Returns:
        Decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            success = True
            
            try:
                logger.info(f"Node {node_name} started")
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                success = False
                logger.error(
                    f"Node {node_name} failed",
                    extra={"node": node_name, "error": str(e)}
                )
                raise
            finally:
                duration = time.time() - start_time
                
                metrics = get_metrics_collector()
                metrics.record_node_execution(node_name, duration, success)
                
                logger.info(
                    f"Node {node_name} completed",
                    extra={
                        "node": node_name,
                        "duration": duration,
                        "success": success
                    }
                )
        
        return wrapper
    return decorator


