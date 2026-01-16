"""
Contract test for PUT /api/test-cases/{id} (update)
"""
import pytest


@pytest.mark.asyncio
async def test_update_test_case_success(client, test_case_id):
    """Test updating a test case"""
    payload = {
        "input": "Updated input",
        "expected_output": "Updated output"
    }
    
    response = await client.put(f"/api/test-cases/{test_case_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["input"] == "Updated input"


@pytest.mark.asyncio
async def test_update_test_case_not_found(client):
    """Test updating a non-existent test case"""
    payload = {
        "input": "Updated input"
    }
    
    response = await client.put("/api/test-cases/nonexistent", json=payload)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_test_case_partial(client, test_case_id):
    """Test partial update of test case"""
    payload = {
        "description": "New description"
    }
    
    response = await client.put(f"/api/test-cases/{test_case_id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["description"] == "New description"
