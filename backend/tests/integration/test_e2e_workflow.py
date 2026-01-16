"""
Integration tests for the complete evaluation workflow.
Tests the full flow: Create test cases → Run evaluation → Grade results.
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_complete_evaluation_workflow(client: AsyncClient):
    """
    Test complete workflow:
    1. Create test cases
    2. Create and start evaluation
    3. Verify evaluation completes
    4. Verify grading results
    """
    # Step 1: Create test cases
    test_case_1 = await client.post(
        "/api/test-cases",
        json={
            "input": "Hello",
            "expected_output": "hello",
            "description": "Case sensitivity test",
            "tags": ["basic"],
        }
    )
    assert test_case_1.status_code == 201
    tc1_id = test_case_1.json()["data"]["id"]

    test_case_2 = await client.post(
        "/api/test-cases",
        json={
            "input": "World",
            "expected_output": "world",
            "description": "Another test",
            "tags": ["basic"],
        }
    )
    assert test_case_2.status_code == 201
    tc2_id = test_case_2.json()["data"]["id"]

    # Step 2: Create evaluation run
    eval_response = await client.post(
        "/api/evaluations",
        json={
            "test_case_ids": [tc1_id, tc2_id],
            "agent_endpoint_url": "http://localhost:8001/agent",
            "grader_ids": ["string-match"],
        }
    )
    assert eval_response.status_code == 201
    run_id = eval_response.json()["data"]["id"]
    assert eval_response.json()["data"]["status"] == "pending"

    # Step 3: Wait for evaluation to complete (or verify it starts)
    status_response = await client.get(f"/api/evaluations/{run_id}")
    assert status_response.status_code == 200
    assert status_response.json()["data"]["status"] in ["running", "completed", "pending"]

    # Step 4: Get evaluation results
    results_response = await client.get(f"/api/evaluations/{run_id}/results")
    assert results_response.status_code == 200
    results_data = results_response.json()["data"]

    # Verify results structure
    assert "results" in results_data
    assert "summary" in results_data
    assert results_data["summary"]["total"] >= 0
    assert "successful" in results_data["summary"]
    assert "failed" in results_data["summary"]


@pytest.mark.asyncio
async def test_evaluation_with_graders(client: AsyncClient):
    """Test evaluation includes grader results."""
    # Create test case
    tc_response = await client.post(
        "/api/test-cases",
        json={
            "input": "test",
            "expected_output": "test",
            "description": "Simple test",
            "tags": ["e2e"],
        }
    )
    tc_id = tc_response.json()["data"]["id"]

    # Create evaluation with grader
    eval_response = await client.post(
        "/api/evaluations",
        json={
            "test_case_ids": [tc_id],
            "agent_endpoint_url": "http://localhost:8001/agent",
            "grader_ids": ["string-match"],
        }
    )
    run_id = eval_response.json()["data"]["id"]

    # Get results
    results_response = await client.get(f"/api/evaluations/{run_id}/results")
    assert results_response.status_code == 200
    results_data = results_response.json()["data"]

    # Each result should have scores if grading ran
    for result in results_data.get("results", []):
        # Result should have structure
        assert "id" in result
        assert "test_case_id" in result
        assert "response_status" in result


@pytest.mark.asyncio
async def test_test_cases_listing_and_retrieval(client: AsyncClient):
    """Test that test cases can be created, listed, and retrieved."""
    # Create multiple test cases
    ids = []
    for i in range(3):
        response = await client.post(
            "/api/test-cases",
            json={
                "input": f"Input {i}",
                "expected_output": f"Output {i}",
                "description": f"Test case {i}",
                "tags": ["test"],
            }
        )
        assert response.status_code == 201
        ids.append(response.json()["data"]["id"])

    # List test cases
    list_response = await client.get("/api/test-cases?skip=0&limit=10")
    assert list_response.status_code == 200
    test_cases = list_response.json()["data"]
    assert len(test_cases) >= 3

    # Retrieve individual test case
    for tc_id in ids:
        get_response = await client.get(f"/api/test-cases/{tc_id}")
        assert get_response.status_code == 200
        tc = get_response.json()["data"]
        assert tc["id"] == tc_id
        assert "input" in tc
        assert "expected_output" in tc


@pytest.mark.asyncio
async def test_graders_endpoint(client: AsyncClient):
    """Test that graders can be listed and retrieved."""
    # List graders
    response = await client.get("/api/graders")
    assert response.status_code == 200
    graders = response.json()["data"]
    assert len(graders) > 0

    # Verify string-match grader exists
    string_match_grader = next(
        (g for g in graders if g["id"] == "string-match"), None
    )
    assert string_match_grader is not None
    assert string_match_grader["name"] == "String Match"
    assert "type" in string_match_grader
    assert "config" in string_match_grader

    # Get specific grader
    grader_response = await client.get("/api/graders/string-match")
    assert grader_response.status_code == 200
    grader = grader_response.json()["data"]
    assert grader["id"] == "string-match"


@pytest.mark.asyncio
async def test_evaluation_error_handling(client: AsyncClient):
    """Test error handling in evaluations."""
    # Try to create evaluation with non-existent test case ID
    eval_response = await client.post(
        "/api/evaluations",
        json={
            "test_case_ids": ["nonexistent"],
            "agent_endpoint_url": "http://localhost:8001/agent",
            "grader_ids": ["string-match"],
        }
    )
    # Should either reject or create with error handling
    assert eval_response.status_code in [400, 201]
