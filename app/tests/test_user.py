from fastapi.testclient import TestClient
from app.main import app
from app import schema

client = TestClient(app)

def test_root():
    response = client.get('/')
    assert response.json().get("message") == "Hello"
    assert response.status_code == 200

def test_create_user():
    response = client.post("/users/", json={"email": "madel@gmail.com", "password": "password123"})
    
    new_user = schema.UserResponse(**response.json())
    assert new_user.email == "madel@gmail.com"
    assert response.status_code == 201