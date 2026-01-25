import logging 

logger = logging.getLogger(__name__)

SENSITIVE_HEADERS = {"authorization", "proxy-authorization"}

def sanitize_headers(headers: dict) -> dict:
    sanitized = {}
    for key, value in headers.items():
        if key.lower() in SENSITIVE_HEADERS:
            sanitized[key] = "***REDACTED***"
        else:
            sanitized[key] = value
    return sanitized

def log_request(method, url, params=None, headers=None, body=None):
    logger.info("%s %s", method, url)

    if params:
        logger.debug(f"Query params: {params}")

    if headers:
        safe_headers = sanitize_headers(headers)
        logger.debug("Headers: %s", safe_headers)
    
    if body:
        logger.debug(f"Request body: {body}")


def log_response(response):
    logger.info(f"Response status: {response.status_code}")
    if response.status_code == 204 or not response.content:
        logger.debug("Response body: <empty>")
    else:
        try:
            logger.debug(f"Response body: {response.json()}")
        except ValueError:
            logger.debug(f"Response body (text): {response.text}")