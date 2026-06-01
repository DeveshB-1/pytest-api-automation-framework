import pytest
from utils.validators import assert_status, assert_response_time, assert_required_keys


class TestHealthEndpoints:

    def test_health_check_returns_200(self, client):
        response = client.get("/health")
        assert_status(response, 200)

    def test_health_response_time(self, client):
        response = client.get("/health")
        assert_response_time(response, max_ms=500)

    def test_health_payload_structure(self, client):
        response = client.get("/health")
        assert_status(response, 200)
        data = response.json()
        assert_required_keys(data, ["status", "version"])

    def test_health_status_is_ok(self, client):
        response = client.get("/health")
        data = response.json()
        assert data["status"] in ("ok", "healthy"), f"Unexpected status: {data['status']}"

    def test_readiness_check(self, client):
        response = client.get("/health/ready")
        assert_status(response, 200)

    def test_liveness_check(self, client):
        response = client.get("/health/live")
        assert_status(response, 200)
