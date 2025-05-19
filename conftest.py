import pytest
from sqlalchemy import create_engine
import uuid

import os

engine = create_engine(os.getenv("DATABASE_URL"))
print(os.getenv("DATABASE_URL"))


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
