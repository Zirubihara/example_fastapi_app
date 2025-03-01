from fastapi.testclient import TestClient


def test_health_check(client: TestClient, api_v1_prefix: str):
    """Test health check endpoint."""
    response = client.get(f"{api_v1_prefix}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"} 