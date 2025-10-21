"""
Retry mechanism with exponential backoff for Advanced RAG system.
"""
import time
from typing import Callable, Type, Tuple
from functools import wraps

from exceptions import RetryExhaustedError
from utils.logger import get_logger

logger = get_logger(__name__)


def retry_with_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    on_retry: Callable = None
):
    """
    Decorator to retry function with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry
        on_retry: Optional callback function called on each retry
        
    Returns:
        Decorated function
        
    Raises:
        RetryExhaustedError: If all retries are exhausted
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    result = func(*args, **kwargs)
                    
                    # Log success if this was a retry
                    if attempt > 0:
                        logger.info(
                            f"Function {func.__name__} succeeded after retry",
                            extra={
                                "function": func.__name__,
                                "attempt": attempt + 1,
                                "total_attempts": max_retries + 1
                            }
                        )
                    
                    return result
                
                except exceptions as e:
                    last_exception = e
                    
                    # If this was the last attempt, raise
                    if attempt == max_retries:
                        logger.error(
                            f"Function {func.__name__} failed after all retries",
                            extra={
                                "function": func.__name__,
                                "total_attempts": max_retries + 1,
                                "error": str(e)
                            }
                        )
                        raise RetryExhaustedError(
                            f"Failed after {max_retries + 1} attempts: {str(e)}",
                            details={
                                "function": func.__name__,
                                "attempts": max_retries + 1,
                                "last_error": str(e)
                            }
                        ) from e
                    
                    # Log retry
                    logger.warning(
                        f"Function {func.__name__} failed, retrying",
                        extra={
                            "function": func.__name__,
                            "attempt": attempt + 1,
                            "max_retries": max_retries,
                            "delay": delay,
                            "error": str(e)
                        }
                    )
                    
                    # Call retry callback if provided
                    if on_retry:
                        on_retry(attempt, e)
                    
                    # Wait before retry
                    time.sleep(delay)
                    delay *= backoff_factor
            
            # This should never be reached, but just in case
            raise RetryExhaustedError(
                f"Unexpected retry exhaustion: {str(last_exception)}",
                details={"function": func.__name__}
            )
        
        return wrapper
    return decorator


class CircuitBreaker:
    """
    Circuit breaker pattern implementation.
    
    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Failures exceeded threshold, requests fail fast
    - HALF_OPEN: Testing if service recovered
    """
    
    def __init__(
        self,
        failure_threshold: int = 5,
        timeout: float = 60.0,
        expected_exception: Type[Exception] = Exception
    ):
        """
        Initialize circuit breaker.
        
        Args:
            failure_threshold: Number of failures before opening circuit
            timeout: Time in seconds before attempting recovery
            expected_exception: Exception type to count as failure
        """
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.expected_exception = expected_exception
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"
        
        logger.info(
            "Circuit breaker initialized",
            extra={
                "failure_threshold": failure_threshold,
                "timeout": timeout
            }
        )
    
    def call(self, func: Callable, *args, **kwargs):
        """
        Execute function with circuit breaker protection.
        
        Args:
            func: Function to execute
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result
            
        Raises:
            Exception: If circuit is open or function fails
        """
        # Check if circuit is open
        if self.state == "OPEN":
            # Check if timeout has passed
            if time.time() - self.last_failure_time >= self.timeout:
                logger.info("Circuit breaker entering HALF_OPEN state")
                self.state = "HALF_OPEN"
            else:
                logger.warning(
                    "Circuit breaker is OPEN, rejecting request",
                    extra={"state": self.state}
                )
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            
            # Success - reset if we were in HALF_OPEN
            if self.state == "HALF_OPEN":
                logger.info("Circuit breaker recovered, entering CLOSED state")
                self.failure_count = 0
                self.state = "CLOSED"
            
            return result
        
        except self.expected_exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            logger.warning(
                "Circuit breaker registered failure",
                extra={
                    "failure_count": self.failure_count,
                    "threshold": self.failure_threshold,
                    "error": str(e)
                }
            )
            
            # Open circuit if threshold exceeded
            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                logger.error(
                    "Circuit breaker OPENED due to failures",
                    extra={
                        "failure_count": self.failure_count,
                        "threshold": self.failure_threshold
                    }
                )
            
            raise
    
    def reset(self):
        """Manually reset circuit breaker."""
        self.failure_count = 0
        self.state = "CLOSED"
        logger.info("Circuit breaker manually reset")


