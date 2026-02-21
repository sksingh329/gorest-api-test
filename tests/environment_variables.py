import os
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
        Environment.STAGING: "https://gorest.co.in/public/v2",
        Environment.PROD: "https://gorest.co.in/public/v2",
    }

    # Maps each environment to its corresponding OS environment variable name.
    # Set the appropriate variable before running tests, e.g.:
    #   export DEV_API_TOKEN=<token>
    #   export STAGING_API_TOKEN=<token>
    #   export PROD_API_TOKEN=<token>
    TOKEN_ENV_KEYS: Dict[Environment, str] = {
        Environment.DEV: "DEV_API_TOKEN",
        Environment.STAGING: "STAGING_API_TOKEN",
        Environment.PROD: "PROD_API_TOKEN",
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
    def get_api_token(cls, env: str) -> str:
        """
        Retrieve the API token for the specified environment from OS env vars.

        Args:
            env: Environment name (dev, staging, prod)

        Returns:
            API token string

        Raises:
            ValueError: If environment is not supported
            EnvironmentError: If the token env var is not set
        """
        try:
            environment = Environment(env.lower())
        except ValueError:
            available_envs = ", ".join([e.value for e in Environment])
            raise ValueError(
                f"Invalid environment '{env}'. "
                f"Available options: {available_envs}"
            )

        env_var_name = cls.TOKEN_ENV_KEYS[environment]
        token = os.getenv(env_var_name)

        if not token:
            raise EnvironmentError(
                f"API token for environment '{env}' not found. "
                f"Please set the '{env_var_name}' environment variable."
            )

        return token

    @classmethod
    def get_all_environments(cls) -> list[str]:
        """
        Get list of all available environments.
        
        Returns:
            List of environment names
        """
        return [env.value for env in Environment]
