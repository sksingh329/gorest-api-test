from urllib3.util.retry import Retry
from typing import List


class RetryStrategy:
    """Configure retry strategy using urllib3.Retry."""
    
    @staticmethod
    def create(
        max_retries: int = 3,
        backoff_factor: float = 0.5,
        status_forcelist: List[int] = None,
        allowed_methods: List[str] = None
    ) -> Retry:
        """
        Create a Retry strategy for urllib3.
        
        Args:
            max_retries: Maximum number of retry attempts
            backoff_factor: Backoff factor for exponential backoff (delay = backoff_factor * (2 ** (retries - 1)))
            status_forcelist: List of HTTP status codes to retry on
            allowed_methods: List of HTTP methods to retry (default: safe methods)
            
        Returns:
            urllib3.util.retry.Retry instance
        """
        if status_forcelist is None:
            status_forcelist = [429, 500, 502, 503, 504]
        
        if allowed_methods is None:
            allowed_methods = ["GET", "PUT", "DELETE", "HEAD", "OPTIONS", "TRACE"]
        
        return Retry(
            total=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
            allowed_methods=allowed_methods,
            raise_on_status=False,  # Don't raise, let requests handle response
        )
