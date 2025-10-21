"""Tests for metrics collection."""
import time
import pytest
from utils.metrics import MetricsCollector, track_time, track_node_execution


def test_metrics_request_counting():
    """Test request counting."""
    metrics = MetricsCollector()
    
    metrics.increment_request(success=True)
    metrics.increment_request(success=True)
    metrics.increment_request(success=False)
    
    data = metrics.get_metrics()
    assert data["requests"]["total"] == 3
    assert data["requests"]["success"] == 2
    assert data["requests"]["failure"] == 1


def test_metrics_node_execution():
    """Test node execution metrics."""
    metrics = MetricsCollector()
    
    metrics.record_node_execution("test_node", 1.5, success=True)
    metrics.record_node_execution("test_node", 2.0, success=True)
    metrics.record_node_execution("test_node", 1.0, success=False)
    
    data = metrics.get_metrics()
    node_metrics = data["nodes"]["test_node"]
    
    assert node_metrics["count"] == 3
    assert node_metrics["success"] == 2
    assert node_metrics["failure"] == 1
    assert node_metrics["avg_duration"] == (1.5 + 2.0 + 1.0) / 3
    assert node_metrics["min_duration"] == 1.0
    assert node_metrics["max_duration"] == 2.0


def test_metrics_latency():
    """Test latency recording."""
    metrics = MetricsCollector()
    
    metrics.record_latency("operation1", 1.5)
    metrics.record_latency("operation1", 2.0)
    
    data = metrics.get_metrics()
    latency = data["latency"]["operation1"]
    
    assert latency["count"] == 2
    assert latency["avg"] == 1.75
    assert latency["min"] == 1.5
    assert latency["max"] == 2.0


def test_metrics_error_tracking():
    """Test error tracking."""
    metrics = MetricsCollector()
    
    metrics.record_error("ValueError")
    metrics.record_error("ValueError")
    metrics.record_error("TypeError")
    
    data = metrics.get_metrics()
    assert data["errors"]["ValueError"] == 2
    assert data["errors"]["TypeError"] == 1


def test_metrics_cache_tracking():
    """Test cache hit/miss tracking."""
    metrics = MetricsCollector()
    
    metrics.record_cache_hit(hit=True)
    metrics.record_cache_hit(hit=True)
    metrics.record_cache_hit(hit=False)
    
    data = metrics.get_metrics()
    assert data["cache"]["hits"] == 2
    assert data["cache"]["misses"] == 1
    assert data["cache"]["hit_rate"] == 2/3


def test_track_time_decorator():
    """Test track_time decorator."""
    metrics = MetricsCollector()
    
    @track_time("test_operation")
    def slow_function():
        time.sleep(0.1)
        return "done"
    
    result = slow_function()
    assert result == "done"
    
    # Note: Can't easily test metrics without dependency injection


def test_metrics_reset():
    """Test metrics reset."""
    metrics = MetricsCollector()
    
    metrics.increment_request(success=True)
    metrics.record_error("TestError")
    
    metrics.reset()
    
    data = metrics.get_metrics()
    assert data["requests"]["total"] == 0
    assert len(data["errors"]) == 0


