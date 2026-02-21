from dataclasses import dataclass


@dataclass(frozen=True)
class RetryConfig:
    """
    Immutable retry configuration.
    
    Attributes:
        max_attempts: Maximum number of retry attempts (including initial request)
        base_delay_ms: Initial delay in milliseconds for exponential backoff
        max_delay_ms: Maximum delay cap in milliseconds
    """
    max_attempts: int = 3
    base_delay_ms: int = 150
    max_delay_ms: int = 2000
    
    def __post_init__(self) -> None:
        """Validate configuration values."""
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        if self.base_delay_ms < 1:
            raise ValueError("base_delay_ms must be >= 1")
        if self.max_delay_ms < self.base_delay_ms:
            raise ValueError("max_delay_ms must be >= base_delay_ms")


# Default retry config
DEFAULT_RETRY_CONFIG = RetryConfig(
    max_attempts=3,
    base_delay_ms=150,
    max_delay_ms=2000
)
