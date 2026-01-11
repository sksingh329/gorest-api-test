import os
import requests
from faker import Faker


BASE_URL = "https://gorest.co.in/public/v2"
USERS_ENDPOINT = f"{BASE_URL}/users"
USER_ENDPOINT = f"{USERS_ENDPOINT}/{{user_id}}"
TOKEN = os.environ.get("API_TOKEN")

headers = {"Authorization": f"Bearer {TOKEN}"}


def test_list_user():
    response = requests.get(USERS_ENDPOINT)
    response_body = response.json()

    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response_body}")

    assert response.status_code == 200

def test_create_user():
    fake = Faker()
    username = fake.name_male()
    user_email = fake.email()
    user_gender = "male"
    user_status = "inactive"
    
    create_user_payload = {
        "name": username,
        "email": user_email,
        "gender": user_gender,
        "status": user_status
    }

    response = requests.post(url= USERS_ENDPOINT, headers= headers, json= create_user_payload)
    response_body = response.json()

    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response_body}")

    assert response.status_code == 201
    assert response_body["name"] == username
    assert response_body["email"] == user_email
    assert response_body["gender"] == user_gender
    assert response_body["status"] == user_status

def test_get_user():
    # Create User
    fake = Faker()
    create_user_payload = {
        "name": fake.name_male(),
        "email": fake.email(),
        "gender": "male",
        "status": "inactive"
    }

    create_user_response = requests.post(url= USERS_ENDPOINT, headers=headers, json=create_user_payload)
    create_user_response_body = create_user_response.json()
    user_id = create_user_response_body["id"]

    print(f"User ID: {user_id}")

    # Get user 
    get_user_response = requests.get(url=USER_ENDPOINT.format(user_id=user_id), headers=headers)
    get_user_response_body = get_user_response.json()

    assert get_user_response.status_code == 200
    assert get_user_response_body["id"] == user_id

def test_put_user():
    # Create User
    fake = Faker()
    create_user_payload = {
        "name": fake.name_male(),
        "email": fake.email(),
        "gender": "male",
        "status": "inactive"
    }

    create_user_response = requests.post(url= USERS_ENDPOINT, headers=headers, json=create_user_payload)
    create_user_response_body = create_user_response.json()
    user_id = create_user_response_body["id"]

    print(f"User ID: {user_id}")

    # Update user 
    update_user_payload = {
        "status": "active"
    }
    update_user_response = requests.put(url=USER_ENDPOINT.format(user_id=user_id), headers=headers, json=update_user_payload)
    update_user_response_body = update_user_response.json()
    
    print(f"Response Status Code: {update_user_response.status_code}")
    print(f"Response Body: {update_user_response_body}")

    assert update_user_response.status_code == 200
    assert update_user_response_body["id"] == user_id
    assert update_user_response_body["status"] == "active"

def test_delete_user():
    # Create User
    fake = Faker()
    create_user_payload = {
        "name": fake.name_male(),
        "email": fake.email(),
        "gender": "male",
        "status": "inactive"
    }

    create_user_response = requests.post(url= USERS_ENDPOINT, headers=headers, json=create_user_payload)
    create_user_response_body = create_user_response.json()
    user_id = create_user_response_body["id"]

    print(f"User ID: {user_id}")

    # Delete user 
    delete_user_response = requests.delete(url=USER_ENDPOINT.format(user_id=user_id), headers=headers)

    print(f"Response Status Code: {delete_user_response.status_code}")

    assert delete_user_response.status_code == 204

    # Get user to assert user is deleted 
    get_user_response = requests.get(url=USER_ENDPOINT.format(user_id=user_id), headers=headers)

    assert get_user_response.status_code == 404