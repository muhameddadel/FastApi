from app import schema
from .test_database import client, session

def test_root(client):
    response = client.get('/')
    assert response.json().get("message") == "Hello"
    assert response.status_code == 200

def test_create_user(client):
    response = client.post("/users/", json={"email": "madel@gmail.com", "password": "password123"})
    
    new_user = schema.UserResponse(**response.json())
    assert new_user.email == "madel@gmail.com"
    assert response.status_code == 201


def test_login_user(client):
    response = client.post("/login", data={"username": "madel@gmail.com", "password": "password123"})

    assert response.status_code == 200