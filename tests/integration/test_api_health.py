"""
Simple health check tests to verify integration test setup.
"""

import pytest
import httpx


API_BASE_URL = "http://localhost:8000"


@pytest.mark.asyncio
async def test_api_health():
    """Test that the API is running and healthy."""
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        response = await client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "ticketchain-api"


@pytest.mark.asyncio 
async def test_api_docs():
    """Test that API documentation is accessible."""
    async with httpx.AsyncClient(base_url=API_BASE_URL) as client:
        response = await client.get("/docs")
        assert response.status_code == 200
        assert "FastAPI" in response.text