import pytest
from jose import jwt
from app import schema
from .test_database import client, session
from app.config import settings

@pytest.fixture
def test_user(client):
    user_data = {"email": "medo@gmail.com", "password": "password123"}
    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user

def test_create_user(client):
    response = client.post("/users/", json={"email": "madel@gmail.com", "password": "password123"})
    
    new_user = schema.UserResponse(**response.json())
    assert new_user.email == "madel@gmail.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_response = schema.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type == 'bearer'
    assert response.status_code == 200