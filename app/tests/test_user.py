import pytest
from jose import jwt
from app import schema
from app.config import settings


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongmail@gmail.com', 'password123', 403),
    ('medo@gmail.com', 'wrongpass', 403),
    ('wrongmail@gmail.com', 'wrongpass', 403),
    (None, 'password123', 422),
    ('medo@gmail.com', None, 422),
])

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


def test_incorrect_login(test_user, client, email, password, status_code):
    response = client.post('/login', data={"username": email, 'password': password})
    
    assert response.status_code == status_code
    assert response.json().get('detail') == 'Invalid Credentials'

