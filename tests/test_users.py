import pytest
from utils.validators import (
    assert_status, assert_json_schema, assert_response_time,
    assert_required_keys, assert_pagination,
)

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email", "role", "created_at"],
    "properties": {
        "id":         {"type": "integer"},
        "name":       {"type": "string"},
        "email":      {"type": "string", "format": "email"},
        "role":       {"type": "string", "enum": ["admin", "editor", "viewer"]},
        "created_at": {"type": "string"},
    },
}


class TestUserEndpoints:

    def test_list_users_returns_200(self, auth_client):
        response = auth_client.get("/users")
        assert_status(response, 200)

    def test_list_users_pagination_structure(self, auth_client):
        response = auth_client.get("/users", params={"page": 1, "per_page": 10})
        assert_status(response, 200)
        assert_pagination(response.json())

    def test_list_users_response_time(self, auth_client):
        response = auth_client.get("/users")
        assert_response_time(response, max_ms=2000)

    def test_create_user_returns_201(self, auth_client, sample_user):
        response = auth_client.post("/users", json=sample_user)
        assert_status(response, 201)

    def test_create_user_response_schema(self, auth_client, sample_user):
        response = auth_client.post("/users", json=sample_user)
        assert_status(response, 201)
        assert_json_schema(response.json(), USER_SCHEMA)

    def test_create_user_missing_email_returns_400(self, auth_client):
        response = auth_client.post("/users", json={"name": "No Email"})
        assert_status(response, 400)

    def test_create_user_invalid_role_returns_400(self, auth_client, sample_user):
        bad_user = {**sample_user, "role": "superadmin"}
        response = auth_client.post("/users", json=bad_user)
        assert_status(response, 400)

    def test_get_user_by_id(self, auth_client, sample_user):
        created = auth_client.post("/users", json=sample_user)
        user_id = created.json()["id"]
        response = auth_client.get(f"/users/{user_id}")
        assert_status(response, 200)
        assert_json_schema(response.json(), USER_SCHEMA)

    def test_get_nonexistent_user_returns_404(self, auth_client):
        response = auth_client.get("/users/999999")
        assert_status(response, 404)

    def test_update_user(self, auth_client, sample_user):
        created = auth_client.post("/users", json=sample_user)
        user_id = created.json()["id"]
        response = auth_client.patch(f"/users/{user_id}", json={"name": "Updated Name"})
        assert_status(response, 200)
        assert response.json()["name"] == "Updated Name"

    def test_delete_user(self, auth_client, sample_user):
        created = auth_client.post("/users", json=sample_user)
        user_id = created.json()["id"]
        response = auth_client.delete(f"/users/{user_id}")
        assert_status(response, 204)

    def test_delete_user_is_idempotent(self, auth_client, sample_user):
        created = auth_client.post("/users", json=sample_user)
        user_id = created.json()["id"]
        auth_client.delete(f"/users/{user_id}")
        response = auth_client.delete(f"/users/{user_id}")
        assert response.status_code in (404, 204)

    def test_duplicate_email_returns_409(self, auth_client, sample_user):
        auth_client.post("/users", json=sample_user)
        response = auth_client.post("/users", json=sample_user)
        assert_status(response, 409)
