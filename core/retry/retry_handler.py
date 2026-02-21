import time
import logging
from typing import Callable, TypeVar, Any
from requests.exceptions import RequestException, Timeout, ConnectionError
import requests

from core.retry.retry_config import RetryConfig, DEFAULT_RETRY_CONFIG
from core.retry.backoff_strategy import BackoffStrategy


logger = logging.getLogger(__name__)
T = TypeVar("T")


class RetryHandler:
    """
    Handles retry logic for HTTP requests.
    
    Retries only for:
    - Network errors (ConnectionError, Timeout)
    - HTTP 408 (Request Timeout)
    - HTTP 429 (Too Many Requests)
    - HTTP 500 (Internal Server Error)
    - HTTP 502 (Bad Gateway)
    - HTTP 503 (Service Unavailable)
    - HTTP 504 (Gateway Timeout)
    
    Uses exponential backoff with jitter and re-raises final failure.
    """
    
    # HTTP status codes that should trigger a retry
    RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}
    
    # Network error types that should trigger a retry
    RETRYABLE_ERRORS = (ConnectionError, Timeout, TimeoutError)
    
    def __init__(self, config: RetryConfig = DEFAULT_RETRY_CONFIG):
        """
        Initialize RetryHandler with retry configuration.
        
        Args:
            config: RetryConfig instance with retry settings
        """
        self.config = config
    
    def execute(
        self,
        request_func: Callable[..., requests.Response],
        *args: Any,
        **kwargs: Any
    ) -> requests.Response:
        """
        Execute HTTP request with automatic retry logic.
        
        Args:
            request_func: Callable that performs the HTTP request
            *args: Positional arguments for request_func
            **kwargs: Keyword arguments for request_func
            
        Returns:
            Response object if successful
            
        Raises:
            RequestException: Final failure after all retries exhausted
        """
        last_exception = None
        
        for attempt in range(self.config.max_attempts):
            try:
                response = request_func(*args, **kwargs)
                
                # Check if response status code is retryable
                if response.status_code in self.RETRYABLE_STATUS_CODES:
                    if attempt < self.config.max_attempts - 1:
                        self._log_retry(
                            attempt,
                            reason=f"HTTP {response.status_code}",
                            is_last=False
                        )
                        self._sleep(attempt)
                        continue
                    else:
                        # Last attempt and status is retryable, but we still return it
                        self._log_retry(
                            attempt,
                            reason=f"HTTP {response.status_code}",
                            is_last=True
                        )
                        return response
                
                # Success - return response
                if attempt > 0:
                    logger.info(f"Request succeeded on attempt {attempt + 1}")
                return response
                
            except self.RETRYABLE_ERRORS as e:
                last_exception = e
                
                if attempt < self.config.max_attempts - 1:
                    self._log_retry(
                        attempt,
                        reason=f"{type(e).__name__}: {str(e)}",
                        is_last=False
                    )
                    self._sleep(attempt)
                    continue
                else:
                    self._log_retry(
                        attempt,
                        reason=f"{type(e).__name__}: {str(e)}",
                        is_last=True
                    )
                    raise
            
            except RequestException as e:
                # Non-retryable request exception - re-raise immediately
                logger.error(f"Non-retryable error on attempt {attempt + 1}: {str(e)}")
                raise
        
        # Should not reach here, but re-raise if it does
        if last_exception:
            raise last_exception
    
    def _log_retry(self, attempt: int, reason: str, is_last: bool) -> None:
        """
        Log retry attempt.
        
        Args:
            attempt: Current attempt number (0-indexed)
            reason: Reason for retry (error message or status code)
            is_last: Whether this is the final attempt
        """
        attempt_num = attempt + 1
        if is_last:
            logger.error(
                f"Request failed after {self.config.max_attempts} attempts. "
                f"Last failure on attempt {attempt_num}: {reason}"
            )
        else:
            next_attempt = attempt_num + 1
            logger.warning(
                f"Request failed on attempt {attempt_num}: {reason}. "
                f"Retrying (attempt {next_attempt}/{self.config.max_attempts})..."
            )
    
    def _sleep(self, attempt: int) -> None:
        """
        Sleep before retry with exponential backoff and jitter.
        
        Args:
            attempt: Current attempt number (0-indexed)
        """
        delay = BackoffStrategy.calculate_delay(
            attempt,
            self.config.base_delay_ms,
            self.config.max_delay_ms
        )
        logger.debug(f"Sleeping {delay:.3f}s before retry")
        time.sleep(delay)
