"""
Test middleware functionality.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_middleware_adds_custom_headers(client: TestClient) -> None:
    """Test that middleware adds custom headers to responses."""
    response = client.get("/")

    # Check status code
    assert response.status_code == 200

    # Check that custom headers are present
    assert "X-Process-Time" in response.headers
    assert "X-Request-ID" in response.headers

    # Verify X-Process-Time is a valid float string
    process_time = response.headers["X-Process-Time"]
    assert float(process_time) >= 0.0

    # Verify X-Request-ID is a valid UUID string
    request_id = response.headers["X-Request-ID"]
    assert len(request_id) == 36  # UUID4 format
    assert request_id.count("-") == 4


def test_middleware_preserves_response_content(client: TestClient) -> None:
    """Test that middleware doesn't modify response content."""
    response = client.get("/")

    # Check that response content is preserved
    assert response.status_code == 200
    # The root endpoint returns a simple string message
    response_data = response.json()
    assert response_data == "Hellow World!"


def test_middleware_handles_different_endpoints(client: TestClient) -> None:
    """Test middleware works with different endpoints."""
    # Test a non-existent endpoint to avoid database dependencies
    response = client.get("/non-existent")

    # Should have middleware headers regardless of endpoint status
    assert "X-Process-Time" in response.headers
    assert "X-Request-ID" in response.headers
    assert response.status_code == 404

    # Request IDs should be unique for different requests
    response2 = client.get("/another-non-existent")
    assert response.headers["X-Request-ID"] != response2.headers["X-Request-ID"]


def test_middleware_handles_post_requests(client: TestClient) -> None:
    """Test middleware works with POST requests."""
    # Test a non-existent POST endpoint to avoid database dependencies
    test_data = {
        "name": "Test Data",
        "description": "Test data for middleware testing",
    }

    response = client.post("/non-existent/", json=test_data)

    # Should have middleware headers even for non-existent endpoints
    assert "X-Process-Time" in response.headers
    assert "X-Request-ID" in response.headers
    assert response.status_code == 404

    # Process time should be reasonable (less than 1 second for this simple operation)
    process_time = float(response.headers["X-Process-Time"])
    assert process_time < 1.0


def test_middleware_timing_accuracy(client: TestClient) -> None:
    """Test that process time measurement is reasonably accurate."""
    import time

    # Make multiple requests and check timing consistency
    times: list[float] = []
    for _ in range(3):
        start = time.time()
        response = client.get("/")
        end = time.time()

        middleware_time = float(response.headers["X-Process-Time"])
        actual_time = end - start

        # Middleware time should be less than or equal to actual time
        # (it measures internal processing, not network overhead)
        assert middleware_time <= actual_time
        times.append(middleware_time)

    # All times should be positive
    assert all(t > 0 for t in times)


def test_middleware_error_handling(client: TestClient) -> None:
    """Test middleware behavior with non-existent endpoints."""
    response = client.get("/non-existent-endpoint")

    # Even 404 responses should have middleware headers
    assert response.status_code == 404
    assert "X-Process-Time" in response.headers
    assert "X-Request-ID" in response.headers
