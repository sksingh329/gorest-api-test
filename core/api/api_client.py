import requests
from core.utils.http_logger import log_request, log_response

class APIClient:
    def __init__(self, base_url, timeout=30, headers=None):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = headers or {}

    def get(self, path, headers=None, params=None):
        url = f"{self.base_url}/{path.lstrip('/')}"
        final_headers = {**self.headers, **(headers or {})}

        log_request(
            method="GET",
            url=url,
            params=params,
            headers=final_headers,
        )

        response = requests.get(
            url, 
            headers=final_headers,
            params=params,
            timeout=self.timeout
        )
        log_response(response)
        return response
    
    def post(self, path, headers=None, params=None, body=None):
        url = f"{self.base_url}/{path.lstrip('/')}"
        final_headers = {**self.headers, **(headers or {})}

        log_request(
            method="POST",
            url=url,
            params=params,
            headers=final_headers,
            body=body
        )

        response = requests.post(
            url,
            headers=final_headers,
            params=params,
            timeout=self.timeout,
            json=body
        )
        log_response(response)
        return response
    
    def put(self, path, headers=None, params=None, body=None):
        url = f"{self.base_url}/{path.lstrip('/')}"
        final_headers = {**self.headers, **(headers or {})}

        log_request(
            method="PUT",
            url=url,
            params=params,
            headers=final_headers,
            body=body
        )

        response = requests.put(
            url,
            headers=final_headers,
            params=params,
            timeout=self.timeout,
            json=body
        )
        log_response(response)
        return response
    
    def delete(self, path, headers=None, params=None):
        url = f"{self.base_url}/{path.lstrip('/')}"
        final_headers = {**self.headers, **(headers or {})}

        log_request(
            method="DELETE",
            url=url,
            params=params,
            headers=final_headers,
        )

        response = requests.delete(
            url, 
            headers=final_headers,
            params=params,
            timeout=self.timeout
        )
        log_response(response)
        return response
