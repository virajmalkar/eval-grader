"""
Contract test for GET /api/test-cases (list)
"""
import pytest


@pytest.mark.asyncio
async def test_list_test_cases_success(client):
    """Test listing test cases"""
    response = await client.get("/api/test-cases")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_list_test_cases_with_pagination(client):
    """Test listing test cases with pagination"""
    response = await client.get("/api/test-cases?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert len(data["data"]) <= 10


@pytest.mark.asyncio
async def test_list_test_cases_invalid_limit(client):
    """Test listing test cases with invalid limit"""
    response = await client.get("/api/test-cases?skip=0&limit=0")
    assert response.status_code == 422
