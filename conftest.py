import os
import pytest
from utils.api_client import APIClient


@pytest.fixture(scope="session")
def client():
    return APIClient(env=os.getenv("ENV", "dev"))


@pytest.fixture(scope="session")
def auth_client(client):
    username = os.getenv("API_USERNAME", "test_user")
    password = os.getenv("API_PASSWORD", "test_pass")
    response = client.post("/auth/token", json={"username": username, "password": password})
    assert response.status_code == 200, f"Auth failed: {response.text}"
    token = response.json()["access_token"]
    client.set_auth_token(token)
    return client


@pytest.fixture
def sample_user():
    return {
        "name": "Test User",
        "email": "testuser@example.com",
        "role": "viewer",
    }
