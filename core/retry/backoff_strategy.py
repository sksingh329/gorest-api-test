import random
from typing import Tuple


class BackoffStrategy:
    """
    Exponential backoff with jitter to prevent retry storms.
    
    Formula: delay = min(base_delay * (2 ^ attempt), max_delay) + random_jitter
    """
    
    @staticmethod
    def calculate_delay(
        attempt: int,
        base_delay_ms: int,
        max_delay_ms: int
    ) -> float:
        """
        Calculate delay in seconds with exponential backoff and jitter.
        
        Args:
            attempt: Attempt number (0-indexed)
            base_delay_ms: Base delay in milliseconds
            max_delay_ms: Maximum delay cap in milliseconds
            
        Returns:
            Delay in seconds
        """
        # Exponential backoff: base_delay * (2 ^ attempt)
        exponential_delay_ms = base_delay_ms * (2 ** attempt)
        
        # Cap at max_delay
        capped_delay_ms = min(exponential_delay_ms, max_delay_ms)
        
        # Add jitter: random value between 0 and capped_delay
        jitter_ms = random.uniform(0, capped_delay_ms)
        
        # Return in seconds
        total_delay_ms = capped_delay_ms + jitter_ms
        return total_delay_ms / 1000.0
    
    @staticmethod
    def get_backoff_sequence(
        max_attempts: int,
        base_delay_ms: int,
        max_delay_ms: int
    ) -> list:
        """
        Generate backoff delays for all retry attempts.
        
        Args:
            max_attempts: Total attempts allowed
            base_delay_ms: Base delay in milliseconds
            max_delay_ms: Maximum delay cap
            
        Returns:
            List of delays in seconds for each retry (excluding initial request)
        """
        delays = []
        for attempt in range(max_attempts - 1):  # -1 because initial request has no delay
            delay = BackoffStrategy.calculate_delay(
                attempt,
                base_delay_ms,
                max_delay_ms
            )
            delays.append(delay)
        return delays
