import os
import pytest
import logging
from core.api.api_client import APIClient
from application.user_client import UserClient


BASE_URL = "https://gorest.co.in/public/v2"


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler()],
        force=True,
    )

    # Reduce noise from libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)

    logging.info("=== Test session started ===")
    yield
    logging.info("=== Test session finished ===")

@pytest.fixture(scope="session")
def auth_headers():
    token = os.getenv("API_TOKEN")
    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture
def api_client(auth_headers):
    return APIClient(
        base_url=BASE_URL, 
        timeout=20,
        headers=auth_headers
    )

@pytest.fixture
def user_client(api_client):
    return UserClient(api_client=api_client)