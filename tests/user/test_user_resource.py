from application.payload.user_payload import user_create_payload, user_update_payload

def test_get_user(user_client, user_fixture):
    user_id = user_fixture
    response = user_client.get_user(user_id=user_id)
    assert response.status_code == 200

def test_update_user(user_client, user_fixture):
    # Update user status to active
    payload = user_update_payload(status="active")
    user_id = user_fixture
    response = user_client.update_user(user_id=user_id, payload=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "active"

def test_delete_user(user_client):
    # Create a user to delete
    payload = user_create_payload()
    create_response = user_client.create_user(payload=payload)
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    # Now delete the user
    delete_response = user_client.delete_user(user_id=user_id)
    assert delete_response.status_code == 204

    # Verify deletion
    get_response = user_client.get_user(user_id=user_id)
    assert get_response.status_code == 404

def test_create_user_fails_with_duplicate_email(user_client, user_fixture):
    # Get the email of the existing user
    existing_user_id = user_fixture
    existing_user_response = user_client.get_user(user_id=existing_user_id)
    existing_email = existing_user_response.json()["email"]

    # Attempt to create a new user with the same email
    payload = user_create_payload(email=existing_email)
    response = user_client.create_user(payload=payload)
    assert response.status_code == 422