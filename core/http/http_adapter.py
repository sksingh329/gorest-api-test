from requests.adapters import HTTPAdapter
from core.http.retry_strategy import RetryStrategy
from core.config.config_manager import ConfigManager
from typing import Optional


class HTTPRetryAdapter:
    """Create and configure HTTPAdapter with retry strategy."""
    
    @staticmethod
    def create_adapter(config: Optional[ConfigManager] = None) -> Optional[HTTPAdapter]:
        """
        Create HTTPAdapter with retry strategy from config.
        
        Args:
            config: ConfigManager instance with retry settings. 
                   If None or retry disabled, returns None.
            
        Returns:
            Configured HTTPAdapter instance or None if retry is disabled
        """
        if not config or not config.is_retry_enabled():
            return None
        
        retry_strategy = RetryStrategy.create(
            max_retries=config.get_max_retries(),
            backoff_factor=config.get_backoff_factor(),
            status_forcelist=config.get_status_forcelist(),
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        return adapter
