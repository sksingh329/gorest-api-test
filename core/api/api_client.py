import requests
from typing import Optional, Any, Dict
from core.utils.http_logger import log_request, log_response
from core.http.http_adapter import HTTPRetryAdapter
from core.config.config_manager import ConfigManager

class APIClient:
    def __init__(self, base_url: str, timeout: int = 30, headers: Optional[Dict[str, str]] = None, config: Optional[ConfigManager] = None):
        """
        Initialize API Client with session-based HTTP communication.
        
        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            headers: Default headers to include in all requests
            config: ConfigManager instance with retry/timeout settings
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = headers or {}
        self.config = config
        
        # Initialize session for connection pooling and future adapter support
        self.session = requests.Session()
        
        # Mount HTTPAdapter with retry strategy if config is provided and retry is enabled
        if config:
            adapter = HTTPRetryAdapter.create_adapter(config)
            if adapter:
                self.session.mount("https://", adapter)
                self.session.mount("http://", adapter)

    def get(self, path: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Execute GET request."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        final_headers = {**self.headers, **(headers or {})}

        log_request(
            method="GET",
            url=url,
            params=params,
            headers=final_headers,
        )

        response = self.session.get(
            url, 
            headers=final_headers,
            params=params,
            timeout=self.timeout
        )
        log_response(response)
        return response
    
    def post(self, path: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Execute POST request."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        final_headers = {**self.headers, **(headers or {})}

        log_request(
            method="POST",
            url=url,
            params=params,
            headers=final_headers,
            body=body
        )

        response = self.session.post(
            url,
            headers=final_headers,
            params=params,
            timeout=self.timeout,
            json=body
        )
        log_response(response)
        return response
    
    def put(self, path: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Execute PUT request."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        final_headers = {**self.headers, **(headers or {})}

        log_request(
            method="PUT",
            url=url,
            params=params,
            headers=final_headers,
            body=body
        )

        response = self.session.put(
            url,
            headers=final_headers,
            params=params,
            timeout=self.timeout,
            json=body
        )
        log_response(response)
        return response
    
    def delete(self, path: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Execute DELETE request."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        final_headers = {**self.headers, **(headers or {})}

        log_request(
            method="DELETE",
            url=url,
            params=params,
            headers=final_headers,
        )

        response = self.session.delete(
            url, 
            headers=final_headers,
            params=params,
            timeout=self.timeout
        )
        log_response(response)
        return response
