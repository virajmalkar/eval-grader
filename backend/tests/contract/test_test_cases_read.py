"""
Contract test for GET /api/test-cases/{id} (read)
"""
import pytest


@pytest.mark.asyncio
async def test_get_test_case_success(client, test_case_id):
    """Test getting an existing test case"""
    response = await client.get(f"/api/test-cases/{test_case_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["id"] == test_case_id


@pytest.mark.asyncio
async def test_get_test_case_not_found(client):
    """Test getting a non-existent test case"""
    response = await client.get("/api/test-cases/nonexistent")
    assert response.status_code == 404
