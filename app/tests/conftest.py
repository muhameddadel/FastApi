from fastapi.testclient import TestClient
import pytest
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    # sqlalchemy
    Base.metadata.create_all(bind=engine)
    Base.metadata.drop_all(bind=engine)
    # alembic
    # comand.upgrade("head")
    # comand.downgrade("head")
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "medo@gmail.com", "password": "password123"}
    response = client.post("/users/", json=user_data)

    assert response.status_code == 201

    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers, 
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def test_posts(test_user, session):
    posts_data = [{
        "title": "title one", 
        "content": "content one", 
        "user_id": test_user['id'],
    },
    {
        "title": "title two", 
        "content": "content two", 
        "user_id": test_user['id'],
    }, 
    {
        "title": "title three", 
        "content": "content three", 
        "user_id": test_user['id'],
    }]

    def create_post_model(post):
        return models.Posts(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    # session.add_all([models.Posts(title="title one", content="content one", user_id=test_user['id']),
    #                 models.Posts(title="title two", content="content two", user_id=test_user['id']), 
    #                 models.Posts(title="title three", content="content three", user_id=test_user['id'])])
    session.commit()
    all_posts = session.query(models.Posts).all()
    return all_posts