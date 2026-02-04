from typing import Dict
from enum import Enum


class Environment(str, Enum):
    """Supported environment options."""
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"


class EnvironmentVariables:
    """Load and manage environment-specific configuration."""
    
    BASE_URLS: Dict[Environment, str] = {
        Environment.DEV: "https://gorest.co.in/public/v2",
        Environment.PROD: "https://gorest.co.in/public/v2",
    }
    
    @classmethod
    def get_base_url(cls, env: str) -> str:
        """
        Retrieve base URL for specified environment.
        
        Args:
            env: Environment name (dev, staging, prod)
            
        Returns:
            Base URL string for the environment
            
        Raises:
            ValueError: If environment is not supported
        """
        try:
            environment = Environment(env.lower())
            return cls.BASE_URLS[environment]
        except ValueError:
            available_envs = ", ".join([e.value for e in Environment])
            raise ValueError(
                f"Invalid environment '{env}'. "
                f"Available options: {available_envs}"
            )
    
    @classmethod
    def get_all_environments(cls) -> list[str]:
        """
        Get list of all available environments.
        
        Returns:
            List of environment names
        """
        return [env.value for env in Environment]
