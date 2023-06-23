from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get('/')
    assert response.json().get("message") == "Hello"
    assert response.status_code == 200