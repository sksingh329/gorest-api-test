USERS_ENDPOINT = f"/users"
USER_ENDPOINT = "/users/{user_id}"

class UserClient:
    def __init__(self, api_client):
        self.api_client = api_client

    def list_user(self):
        return self.api_client.get(USERS_ENDPOINT)
    
    def create_user(self, payload):
        return self.api_client.post(USERS_ENDPOINT, body=payload)
    
    def get_user(self, user_id):
        return self.api_client.get(USER_ENDPOINT.format(user_id=user_id))
    
    def update_user(self, user_id, payload):
        return self.api_client.put(USER_ENDPOINT.format(user_id=user_id), body=payload)
    
    def delete_user(self, user_id):
        return self.api_client.delete(USER_ENDPOINT.format(user_id=user_id))