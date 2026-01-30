import pytest
import logging 
from application.payload.user_payload import user_create_payload


logger = logging.getLogger(__name__)

@pytest.fixture
def user_fixture(user_client):
    payload = user_create_payload()
    response = user_client.create_user(payload=payload)
    assert response.status_code == 201 
    response_body = response.json()
    user_id = response_body["id"]
    logger.info(f"Created user with ID: {user_id}")
    yield user_id
    user_client.delete_user(user_id=user_id)
    logger.info(f"Deleted user with ID: {user_id}")