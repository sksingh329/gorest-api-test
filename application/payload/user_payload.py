from faker import Faker 

fake = Faker()

def user_create_payload(
    *,
    name=None,
    email=None,
    gender="male",
    status="inactive"
):
    return {
        "name": name or fake.name_male(),
        "email": email or fake.email(),
        "gender": gender,
        "status": status
    }

def user_update_payload(
    *,
    name=None,
    email=None,
    gender=None,
    status=None,
):
    payload = {}

    if name is not None:
        payload["name"] = name
    if email is not None:
        payload["email"] = email
    if gender is not None:
        payload["gender"] = gender
    if status is not None:
        payload["status"] = status

    return payload
