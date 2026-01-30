import logging
from application.payload.user_payload import create_user_payload, user_create_payload


logger = logging.getLogger(__name__)


def test_list_user(user_client):
    response = user_client.list_user()
    assert response.status_code == 200

def test_create_user(user_client):
    payload = create_user_payload(status="inactive")

    response = user_client.create_user(payload=payload)
    response_body = response.json()

    assert response.status_code == 201
    assert response_body["name"] == payload["name"]
    assert response_body["email"] == payload["email"]
    assert response_body["gender"] == payload["gender"]
    assert response_body["status"] == payload["status"]

    user_id = response_body["id"]

    logger.info(f"User ID: {user_id}")

    if user_id:
        user_client.delete_user(user_id=user_id)
