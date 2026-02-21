import os
import pytest
import logging
from dotenv import load_dotenv
from core.api.api_client import APIClient
from application.user_client import UserClient
from tests.environment_variables import EnvironmentVariables

# Load .env file at import time so env vars are available to all fixtures.
# Existing OS env vars take precedence (override=False), making CI secrets
# automatically win over local .env values.
load_dotenv(override=False)


def pytest_addoption(parser):
    """Register --env CLI option for pytest."""
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help=f"Environment to run tests against. Options: {', '.join(EnvironmentVariables.get_all_environments())}"
    )


@pytest.fixture(scope="session")
def environment(request) -> str:
    """Get selected environment from CLI option."""
    return request.config.getoption("--env")


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
def auth_headers(environment: str) -> dict:
    """Build Authorization headers using the token for the active environment."""
    token = EnvironmentVariables.get_api_token(environment)
    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture
def api_client(auth_headers, environment):
    base_url = EnvironmentVariables.get_base_url(environment)
    return APIClient(
        base_url=base_url, 
        timeout=20,
        headers=auth_headers
    )

@pytest.fixture
def user_client(api_client):
    return UserClient(api_client=api_client)