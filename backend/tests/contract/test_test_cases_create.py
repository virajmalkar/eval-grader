"""
Contract test for POST /api/test-cases (create)
"""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_test_case_success(client):
    """Test creating a test case successfully"""
    payload = {
        "input": "What is the capital of France?",
        "expected_output": "Paris",
        "description": "Basic geography",
        "tags": ["geography"]
    }
    
    response = await client.post("/api/test-cases", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["input"] == "What is the capital of France?"
    assert data["data"]["expected_output"] == "Paris"
    assert data["data"]["id"] is not None


@pytest.mark.asyncio
async def test_create_test_case_missing_required_field(client):
    """Test creating a test case without required field"""
    payload = {
        "input": "What is the capital of France?"
        # missing expected_output
    }
    
    response = await client.post("/api/test-cases", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_test_case_empty_input(client):
    """Test creating a test case with empty input"""
    payload = {
        "input": "",
        "expected_output": "Paris"
    }
    
    response = await client.post("/api/test-cases", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_test_case_input_too_long(client):
    """Test creating a test case with input exceeding max length"""
    payload = {
        "input": "x" * 10001,
        "expected_output": "Paris"
    }
    
    response = await client.post("/api/test-cases", json=payload)
    assert response.status_code == 422
