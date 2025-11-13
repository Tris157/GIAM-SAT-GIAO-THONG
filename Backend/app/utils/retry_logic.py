"""
Retry logic and error recovery utilities
Improves system reliability and resilience
"""
import asyncio
import functools
import logging
from typing import TypeVar, Callable, Any, Optional
from sqlalchemy.exc import OperationalError, DBAPIError

logger = logging.getLogger(__name__)

T = TypeVar('T')


def retry_on_exception(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (OperationalError, DBAPIError, ConnectionError)
):
    """
    Decorator to retry function on specified exceptions

    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry on
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> T:
            current_delay = delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt < max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries + 1} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {current_delay}s..."
                        )
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(
                            f"All {max_retries + 1} attempts failed for {func.__name__}: {str(e)}"
                        )

            raise last_exception

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> T:
            import time
            current_delay = delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e

                    if attempt < max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_retries + 1} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {current_delay}s..."
                        )
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(
                            f"All {max_retries + 1} attempts failed for {func.__name__}: {str(e)}"
                        )

            raise last_exception

        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


class CircuitBreaker:
    """
    Circuit breaker pattern implementation
    Prevents cascading failures by temporarily disabling failing operations
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exceptions: tuple = (Exception,)
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exceptions = expected_exceptions

        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = "closed"  # closed, open, half_open

    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> T:
            import time

            # Check if circuit is open
            if self.state == "open":
                if time.time() - self.last_failure_time >= self.recovery_timeout:
                    self.state = "half_open"
                    logger.info(f"Circuit breaker for {func.__name__} entering half-open state")
                else:
                    raise Exception(
                        f"Circuit breaker is OPEN for {func.__name__}. "
                        f"Try again in {self.recovery_timeout - (time.time() - self.last_failure_time):.1f}s"
                    )

            try:
                result = await func(*args, **kwargs)

                # Reset on success
                if self.state == "half_open":
                    self.state = "closed"
                    self.failure_count = 0
                    logger.info(f"Circuit breaker for {func.__name__} is now CLOSED")

                return result

            except self.expected_exceptions as e:
                self.failure_count += 1
                self.last_failure_time = time.time()

                if self.failure_count >= self.failure_threshold:
                    self.state = "open"
                    logger.error(
                        f"Circuit breaker OPENED for {func.__name__} after {self.failure_count} failures"
                    )

                raise e

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> T:
            import time

            # Check if circuit is open
            if self.state == "open":
                if time.time() - self.last_failure_time >= self.recovery_timeout:
                    self.state = "half_open"
                    logger.info(f"Circuit breaker for {func.__name__} entering half-open state")
                else:
                    raise Exception(
                        f"Circuit breaker is OPEN for {func.__name__}. "
                        f"Try again in {self.recovery_timeout - (time.time() - self.last_failure_time):.1f}s"
                    )

            try:
                result = func(*args, **kwargs)

                # Reset on success
                if self.state == "half_open":
                    self.state = "closed"
                    self.failure_count = 0
                    logger.info(f"Circuit breaker for {func.__name__} is now CLOSED")

                return result

            except self.expected_exceptions as e:
                self.failure_count += 1
                self.last_failure_time = time.time()

                if self.failure_count >= self.failure_threshold:
                    self.state = "open"
                    logger.error(
                        f"Circuit breaker OPENED for {func.__name__} after {self.failure_count} failures"
                    )

                raise e

        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper


async def with_timeout(coro, timeout: float, error_message: str = "Operation timed out"):
    """
    Run coroutine with timeout

    Args:
        coro: Coroutine to run
        timeout: Timeout in seconds
        error_message: Error message if timeout occurs
    """
    try:
        return await asyncio.wait_for(coro, timeout=timeout)
    except asyncio.TimeoutError:
        logger.error(f"{error_message} after {timeout}s")
        raise TimeoutError(error_message)
