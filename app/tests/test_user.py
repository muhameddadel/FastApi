from fastapi.testclient import TestClient
from app.main import app
from app import schema
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db
from app.database import Base


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
app.dependency_overrides[get_db] = override_get_db


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