import configparser
import os
from typing import List
from pathlib import Path


class ConfigManager:
    """Manage environment-specific configuration from config.ini."""
    
    def __init__(self, env: str = "dev", config_path: str = "config.ini"):
        """
        Initialize ConfigManager and load environment-specific settings.
        
        Args:
            env: Environment name (dev, staging, prod)
            config_path: Path to config.ini file
            
        Raises:
            FileNotFoundError: If config.ini is not found
            ValueError: If environment not found in config
        """
        self.env = env.lower()
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        
        # Load config file
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        self.config.read(config_path)
        
        # Validate environment exists
        if self.env not in self.config:
            available_envs = [s for s in self.config.sections()]
            raise ValueError(
                f"Environment '{self.env}' not found in config.ini. "
                f"Available: {available_envs}"
            )
    
    def get_timeout(self) -> int:
        """Get timeout in seconds for the environment."""
        return self.config.getint(self.env, "timeout_seconds")
    
    def get_max_retries(self) -> int:
        """Get maximum number of retries for the environment."""
        return self.config.getint(self.env, "max_retries")
    
    def get_backoff_factor(self) -> float:
        """Get backoff factor for exponential backoff."""
        return self.config.getfloat(self.env, "backoff_factor")
    
    def get_status_forcelist(self) -> List[int]:
        """Get list of HTTP status codes to retry on."""
        status_str = self.config.get(self.env, "status_forcelist")
        return [int(s.strip()) for s in status_str.split(",")]
    
    def is_retry_enabled(self) -> bool:
        """Check if retry is enabled for the environment."""
        return self.config.getboolean(self.env, "enable_retry")
    
    def get_all_settings(self) -> dict:
        """Get all configuration settings for the environment."""
        return {
            "timeout_seconds": self.get_timeout(),
            "max_retries": self.get_max_retries(),
            "backoff_factor": self.get_backoff_factor(),
            "status_forcelist": self.get_status_forcelist(),
            "enable_retry": self.is_retry_enabled(),
            "environment": self.env,
        }
