import pytest
from utils.validators import assert_status, assert_required_keys, assert_response_time


class TestAuthentication:

    def test_valid_login_returns_token(self, client):
        response = client.post("/auth/token", json={"username": "test_user", "password": "test_pass"})
        assert_status(response, 200)
        data = response.json()
        assert_required_keys(data, ["access_token", "token_type", "expires_in"])

    def test_token_type_is_bearer(self, client):
        response = client.post("/auth/token", json={"username": "test_user", "password": "test_pass"})
        assert response.json()["token_type"].lower() == "bearer"

    def test_invalid_credentials_returns_401(self, client):
        response = client.post("/auth/token", json={"username": "wrong", "password": "wrong"})
        assert_status(response, 401)

    def test_missing_credentials_returns_400(self, client):
        response = client.post("/auth/token", json={})
        assert_status(response, 400)

    def test_auth_response_time(self, client):
        response = client.post("/auth/token", json={"username": "test_user", "password": "test_pass"})
        assert_response_time(response, max_ms=1000)

    def test_protected_endpoint_without_token_returns_401(self, client):
        response = client.get("/users")
        assert_status(response, 401)

    def test_protected_endpoint_with_invalid_token_returns_401(self, client):
        client.session.headers.update({"Authorization": "Bearer invalid_token_xyz"})
        response = client.get("/users")
        assert_status(response, 401)
        # Reset
        client.session.headers.pop("Authorization", None)

    def test_token_refresh(self, auth_client):
        response = auth_client.post("/auth/refresh")
        assert_status(response, 200)
        assert_required_keys(response.json(), ["access_token"])
