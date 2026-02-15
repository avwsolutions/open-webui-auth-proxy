import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello World"}

def test_post_root(client):
    payload = {"name": "test"}
    response = client.post("/", json=payload)

    assert response.status_code == 200
    assert response.get_json() == {"received": payload}
