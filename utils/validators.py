import jsonschema


def assert_status(response, expected_status):
    assert response.status_code == expected_status, (
        f"Expected {expected_status}, got {response.status_code}. Body: {response.text[:300]}"
    )


def assert_json_schema(data, schema):
    try:
        jsonschema.validate(instance=data, schema=schema)
    except jsonschema.ValidationError as e:
        raise AssertionError(f"Schema validation failed: {e.message}")


def assert_response_time(response, max_ms=2000):
    elapsed = response.elapsed.total_seconds() * 1000
    assert elapsed <= max_ms, f"Response too slow: {elapsed:.0f}ms (max {max_ms}ms)"


def assert_required_keys(data, keys):
    missing = [k for k in keys if k not in data]
    assert not missing, f"Missing keys in response: {missing}"


def assert_pagination(data):
    assert_required_keys(data, ["page", "per_page", "total", "data"])
    assert isinstance(data["data"], list), "Expected 'data' to be a list"
