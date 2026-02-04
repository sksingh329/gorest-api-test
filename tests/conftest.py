import os
import pytest
import logging
from core.api.api_client import APIClient
from application.user_client import UserClient
from tests.environment_variables import EnvironmentVariables
from core.config.config_manager import ConfigManager


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


@pytest.fixture(scope="session")
def config(environment: str) -> ConfigManager:
    """Initialize and load configuration for selected environment."""
    return ConfigManager(env=environment, config_path="config.ini")


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
def api_client(auth_headers, environment, config):
    base_url = EnvironmentVariables.get_base_url(environment)
    return APIClient(
        base_url=base_url, 
        timeout=config.get_timeout(),
        headers=auth_headers,
        config=config
    )

@pytest.fixture
def user_client(api_client):
    return UserClient(api_client=api_client)