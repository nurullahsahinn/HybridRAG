"""Tests for retry mechanism."""
import pytest
from utils.retry import retry_with_backoff, CircuitBreaker
from exceptions import RetryExhaustedError


def test_retry_success():
    """Test successful retry."""
    call_count = [0]
    
    @retry_with_backoff(max_retries=3, initial_delay=0.1)
    def sometimes_fails():
        call_count[0] += 1
        if call_count[0] < 3:
            raise Exception("Temporary failure")
        return "success"
    
    result = sometimes_fails()
    assert result == "success"
    assert call_count[0] == 3


def test_retry_exhausted():
    """Test retry exhaustion."""
    call_count = [0]
    
    @retry_with_backoff(max_retries=2, initial_delay=0.1)
    def always_fails():
        call_count[0] += 1
        raise ValueError("Always fails")
    
    with pytest.raises(RetryExhaustedError):
        always_fails()
    
    assert call_count[0] == 3  # Initial + 2 retries


def test_retry_specific_exceptions():
    """Test retry with specific exceptions."""
    call_count = [0]
    
    @retry_with_backoff(max_retries=3, initial_delay=0.1, exceptions=(ValueError,))
    def fails_with_type_error():
        call_count[0] += 1
        raise TypeError("Not retryable")
    
    # Should not retry TypeError
    with pytest.raises(TypeError):
        fails_with_type_error()
    
    assert call_count[0] == 1  # No retries


def test_circuit_breaker_closed():
    """Test circuit breaker in closed state."""
    breaker = CircuitBreaker(failure_threshold=3, timeout=10)
    
    def successful_operation():
        return "success"
    
    result = breaker.call(successful_operation)
    assert result == "success"
    assert breaker.state == "CLOSED"


def test_circuit_breaker_opens():
    """Test circuit breaker opening after failures."""
    breaker = CircuitBreaker(failure_threshold=3, timeout=1)
    
    def failing_operation():
        raise Exception("Failure")
    
    # Cause enough failures to open circuit
    for _ in range(3):
        with pytest.raises(Exception):
            breaker.call(failing_operation)
    
    assert breaker.state == "OPEN"
    
    # Circuit should reject requests
    with pytest.raises(Exception, match="Circuit breaker is OPEN"):
        breaker.call(failing_operation)


def test_circuit_breaker_half_open():
    """Test circuit breaker half-open state."""
    breaker = CircuitBreaker(failure_threshold=2, timeout=0.5)
    
    def failing_operation():
        raise Exception("Failure")
    
    # Open the circuit
    for _ in range(2):
        with pytest.raises(Exception):
            breaker.call(failing_operation)
    
    assert breaker.state == "OPEN"
    
    # Wait for timeout
    import time
    time.sleep(0.6)
    
    # Next call should attempt (half-open)
    def successful_operation():
        return "success"
    
    result = breaker.call(successful_operation)
    assert result == "success"
    assert breaker.state == "CLOSED"


