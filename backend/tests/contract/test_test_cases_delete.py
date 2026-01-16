"""
Contract test for DELETE /api/test-cases/{id} (delete)
"""
import pytest


@pytest.mark.asyncio
async def test_delete_test_case_success(client, test_case_id):
    """Test deleting a test case"""
    response = await client.delete(f"/api/test-cases/{test_case_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_test_case_not_found(client):
    """Test deleting a non-existent test case"""
    response = await client.delete("/api/test-cases/nonexistent")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_test_case_verify_removed(client, test_case_id):
    """Test that deleted test case cannot be retrieved"""
    # First delete
    response = await client.delete(f"/api/test-cases/{test_case_id}")
    assert response.status_code == 204
    
    # Then verify it's gone
    response = await client.get(f"/api/test-cases/{test_case_id}")
    assert response.status_code == 404
