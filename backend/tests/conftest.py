"""
Pytest configuration and fixtures for backend tests
"""
import pytest
from pathlib import Path
import sys
from httpx import AsyncClient
import asyncio

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import app after path setup
from main import app
from src.services.storage_service import StorageService
from src.services.test_case_service import TestCaseService


@pytest.fixture
def mock_test_case():
    """Fixture for a sample test case"""
    return {
        "id": "test-1",
        "input": "What is 2+2?",
        "expected_output": "4",
        "description": "Basic arithmetic",
        "tags": ["math"],
        "created_at": "2026-01-15T10:00:00Z",
        "modified_at": "2026-01-15T10:00:00Z"
    }


@pytest.fixture
def mock_evaluation_run():
    """Fixture for a sample evaluation run"""
    return {
        "id": "run-1",
        "test_case_ids": ["test-1", "test-2"],
        "agent_endpoint_url": "http://localhost:9000/evaluate",
        "grader_ids": ["string-match"],
        "status": "pending",
        "started_at": None,
        "completed_at": None,
        "result_count": 0,
        "error_message": None
    }


@pytest.fixture
async def client():
    """Async HTTP test client"""
    # Reset storage before each test
    StorageService.reset_storage()
    
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client


@pytest.fixture
async def test_case_id(client):
    """Create a test case and return its ID"""
    payload = {
        "input": "What is 2+2?",
        "expected_output": "4",
        "description": "Basic math"
    }
    response = await client.post("/api/test-cases", json=payload)
    test_case = response.json()["data"]
    return test_case["id"]
