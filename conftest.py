import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid

import os
from dotenv import load_dotenv

from app.main import app
from app.database import Base
from app.main import get_db

engine = create_engine(os.getenv("DATABASE_URL"))
print(os.getenv("DATABASE_URL"))

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture(scope="function")
def generate_category(client):
    name = f"test_name_{uuid.uuid4().hex}"
    response = client.post(
        "/categories/",
        json={"name": name}
    )
    assert response.status_code == 200
    assert response.json()["name"] == name

    yield response.json()

    response = client.delete(f"/categories/{response.json()["id"]}")
    assert response.status_code == 204
