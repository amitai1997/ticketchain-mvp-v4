"""Unit tests for main API endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_root_endpoint(client):
    """Test the root endpoint returns expected response."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello from TicketChain API",
        "status": "healthy"
    }


def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ticketchain-api"
    assert data["version"] == "0.1.0"