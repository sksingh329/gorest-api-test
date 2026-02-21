import requests
from typing import Optional, Any, Dict
from core.utils.http_logger import log_request, log_response
from core.retry.retry_handler import RetryHandler
from core.retry.retry_config import DEFAULT_RETRY_CONFIG

class APIClient:
    def __init__(self, base_url: str, timeout: int = 30, headers: Optional[Dict[str, str]] = None):
        """
        Initialize API Client with session-based HTTP communication.
        
        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
            headers: Default headers to include in all requests
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = headers or {}
        
        # Initialize session for connection pooling
        self.session = requests.Session()
        
        # Initialize retry handler with default config
        self.retry_handler = RetryHandler(DEFAULT_RETRY_CONFIG)

    def get(self, path: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Execute GET request with automatic retry."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        final_headers = {**self.headers, **(headers or {})}

        log_request(
            method="GET",
            url=url,
            params=params,
            headers=final_headers,
        )

        response = self.retry_handler.execute(
            self.session.get,
            url,
            headers=final_headers,
            params=params,
            timeout=self.timeout
        )
        log_response(response)
        return response
    
    def post(self, path: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Execute POST request with automatic retry."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        final_headers = {**self.headers, **(headers or {})}

        log_request(
            method="POST",
            url=url,
            params=params,
            headers=final_headers,
            body=body
        )

        response = self.retry_handler.execute(
            self.session.post,
            url,
            headers=final_headers,
            params=params,
            timeout=self.timeout,
            json=body
        )
        log_response(response)
        return response
    
    def put(self, path: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Execute PUT request with automatic retry."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        final_headers = {**self.headers, **(headers or {})}

        log_request(
            method="PUT",
            url=url,
            params=params,
            headers=final_headers,
            body=body
        )

        response = self.retry_handler.execute(
            self.session.put,
            url,
            headers=final_headers,
            params=params,
            timeout=self.timeout,
            json=body
        )
        log_response(response)
        return response
    
    def delete(self, path: str, headers: Optional[Dict[str, str]] = None, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        """Execute DELETE request with automatic retry."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        final_headers = {**self.headers, **(headers or {})}

        log_request(
            method="DELETE",
            url=url,
            params=params,
            headers=final_headers,
        )

        response = self.retry_handler.execute(
            self.session.delete,
            url, 
            headers=final_headers,
            params=params,
            timeout=self.timeout
        )
        log_response(response)
        return response
