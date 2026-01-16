# API Contract: Evaluations

**Date**: 2026-01-15  
**Purpose**: Define REST API for running and managing evaluation executions

---

## Overview

Evaluation endpoints allow users to start evaluation runs, monitor their status, and retrieve results. An evaluation run executes a set of test cases against an external agent endpoint and applies graders to score the responses.

---

## Endpoints

### 1. Create Evaluation Run

**Endpoint**: `POST /api/evaluations`

**Purpose**: Start a new evaluation run

**Request Body** (JSON):
```json
{
  "test_case_ids": ["550e8400-e29b-41d4-a716-446655440001", "550e8400-e29b-41d4-a716-446655440002"],
  "agent_endpoint_url": "https://api.agent.example.com/evaluate",
  "grader_ids": ["string-match"]
}
```

**Request Validation**:
- `test_case_ids`: Required, array of valid test case IDs, 1+ items
- `agent_endpoint_url`: Required, valid HTTP(S) URL
- `grader_ids`: Required, array of valid grader IDs, 1+ items

**Response: 201 Created**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440010",
    "test_case_ids": ["550e8400-e29b-41d4-a716-446655440001", "550e8400-e29b-41d4-a716-446655440002"],
    "agent_endpoint_url": "https://api.agent.example.com/evaluate",
    "grader_ids": ["string-match"],
    "status": "running",
    "started_at": "2026-01-15T10:35:00Z",
    "completed_at": null,
    "result_count": 0,
    "error_message": null
  },
  "error": null
}
```

**Behavior**:
- Run begins immediately (async execution)
- Status starts as "running"
- Results are populated as responses arrive
- This endpoint returns immediately; use polling or webhooks to monitor

**Error Responses**:

| Status | Scenario | Response |
|--------|----------|----------|
| 400 Bad Request | Invalid test case ID | `{"success": false, "error": {"code": "INVALID_TEST_CASE_ID", "message": "Test case not found"}}` |
| 400 Bad Request | Invalid grader ID | `{"success": false, "error": {"code": "INVALID_GRADER_ID", "message": "Grader not found"}}` |
| 400 Bad Request | Invalid URL | `{"success": false, "error": {"code": "INVALID_URL", "message": "Agent endpoint URL must be valid HTTP(S)"}}` |
| 400 Bad Request | Missing field | `{"success": false, "error": {"code": "MISSING_FIELD", "message": "..."}}` |

---

### 2. Get Evaluation Run Status

**Endpoint**: `GET /api/evaluations/{id}`

**Purpose**: Retrieve status and progress of an evaluation run

**Path Parameters**:
- `id`: UUID of evaluation run

**Response: 200 OK**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440010",
    "test_case_ids": ["550e8400-e29b-41d4-a716-446655440001", "550e8400-e29b-41d4-a716-446655440002"],
    "agent_endpoint_url": "https://api.agent.example.com/evaluate",
    "grader_ids": ["string-match"],
    "status": "completed",
    "started_at": "2026-01-15T10:35:00Z",
    "completed_at": "2026-01-15T10:35:15Z",
    "result_count": 2,
    "error_message": null
  },
  "error": null
}
```

**Status Values**:
- `pending`: Not yet started (should be rare)
- `running`: Currently executing
- `completed`: All results collected and graded
- `failed`: Execution halted due to error

**Error Responses**:

| Status | Scenario | Response |
|--------|----------|----------|
| 404 Not Found | Run doesn't exist | `{"success": false, "error": {"code": "NOT_FOUND", "message": "Evaluation run not found"}}` |

---

### 3. List Evaluation Runs

**Endpoint**: `GET /api/evaluations`

**Purpose**: Retrieve all evaluation runs

**Query Parameters** (all optional):
- `limit`: Max results (default: 50, max: 500)
- `skip`: Number to skip (default: 0)
- `status`: Filter by status (pending/running/completed/failed)

**Examples**:
- `GET /api/evaluations` - All runs
- `GET /api/evaluations?status=completed` - Only completed runs
- `GET /api/evaluations?limit=10&skip=20` - Pagination

**Response: 200 OK**
```json
{
  "success": true,
  "data": {
    "evaluations": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440010",
        "test_case_ids": ["550e8400-e29b-41d4-a716-446655440001", "550e8400-e29b-41d4-a716-446655440002"],
        "agent_endpoint_url": "https://api.agent.example.com/evaluate",
        "grader_ids": ["string-match"],
        "status": "completed",
        "started_at": "2026-01-15T10:35:00Z",
        "completed_at": "2026-01-15T10:35:15Z",
        "result_count": 2,
        "error_message": null
      }
    ],
    "count": 1,
    "total": 5
  },
  "error": null
}
```

---

### 4. Get Evaluation Results

**Endpoint**: `GET /api/evaluations/{id}/results`

**Purpose**: Retrieve all results and scores for a completed evaluation run

**Path Parameters**:
- `id`: UUID of evaluation run

**Query Parameters** (all optional):
- `limit`: Max results (default: 100, max: 1000)
- `skip`: Number to skip (default: 0)

**Response: 200 OK**
```json
{
  "success": true,
  "data": {
    "evaluation_id": "550e8400-e29b-41d4-a716-446655440010",
    "results": [
      {
        "result_id": "550e8400-e29b-41d4-a716-446655440020",
        "test_case_id": "550e8400-e29b-41d4-a716-446655440001",
        "test_case_input": "What is the capital of France?",
        "test_case_expected": "Paris",
        "agent_response": "The capital of France is Paris.",
        "response_status": "success",
        "response_latency_ms": 245,
        "scores": [
          {
            "grader_id": "string-match",
            "grader_name": "String Match",
            "score_value": 0.0,
            "score_status": "fail",
            "error_message": null
          }
        ]
      },
      {
        "result_id": "550e8400-e29b-41d4-a716-446655440021",
        "test_case_id": "550e8400-e29b-41d4-a716-446655440002",
        "test_case_input": "What is 2+2?",
        "test_case_expected": "4",
        "agent_response": "4",
        "response_status": "success",
        "response_latency_ms": 120,
        "scores": [
          {
            "grader_id": "string-match",
            "grader_name": "String Match",
            "score_value": 1.0,
            "score_status": "pass",
            "error_message": null
          }
        ]
      }
    ],
    "summary": {
      "total_results": 2,
      "successful_responses": 2,
      "failed_responses": 0,
      "grader_pass_counts": {
        "string-match": 1
      },
      "grader_fail_counts": {
        "string-match": 1
      },
      "average_latency_ms": 182.5
    }
  },
  "error": null
}
```

**Error Responses**:

| Status | Scenario | Response |
|--------|----------|----------|
| 404 Not Found | Run doesn't exist | `{"success": false, "error": {"code": "NOT_FOUND", "message": "Evaluation run not found"}}` |

---

## Response Format Standard

All responses follow the standard format:

**Success**:
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

**Error**:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

---

## Error Codes

| Code | HTTP | Meaning |
|------|------|---------|
| INVALID_TEST_CASE_ID | 400 | Test case doesn't exist |
| INVALID_GRADER_ID | 400 | Grader doesn't exist |
| INVALID_URL | 400 | Agent endpoint URL invalid |
| MISSING_FIELD | 400 | Required field not provided |
| NOT_FOUND | 404 | Evaluation run not found |
| INTERNAL_ERROR | 500 | Unexpected server error |

---

## Behavior Notes

### Asynchronous Execution

Evaluation runs execute asynchronously. The `POST /api/evaluations` endpoint returns immediately with `status: "running"`. The frontend should:
1. Poll `GET /api/evaluations/{id}` every 1-2 seconds to check status
2. When `status` changes to "completed" or "failed", fetch results with `GET /api/evaluations/{id}/results`

### Agent Endpoint Error Handling

If the agent endpoint is unreachable or times out:
- Individual result stored with `response_status: "error"`
- Error message captured: "Connection refused" or "Timeout after 30 seconds"
- Remaining test cases continue to be executed
- Evaluation run completes with `status: "completed"` (partial results)

### Grader Error Handling

If a grader fails on a result:
- Score stored with `score_status: "error"`
- Error message captured: "Grader timeout" or error details
- Other graders continue processing the result
- Evaluation run completes successfully

### Result Completeness

A result for test case T with graders G1, G2, G3 has:
- 1 EvaluationResult entity
- 3 Score entities (one per grader, each may be pass/fail/error)

Summary statistics count successes:
- "successful_responses": Results with response_status=success
- "grader_pass_counts": Count of scores with score_status=pass per grader

---

## Contract Tests (pytest examples)

### Test: Create evaluation run
```python
def test_create_evaluation_run():
    # Assume test cases and graders exist
    response = client.post("/api/evaluations", json={
        "test_case_ids": ["tc-001", "tc-002"],
        "agent_endpoint_url": "https://agent.example.com/api",
        "grader_ids": ["string-match"]
    })
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] in ["pending", "running"]
```

### Test: Get evaluation status
```python
def test_get_evaluation_status():
    # Create run
    create_response = client.post("/api/evaluations", json={
        "test_case_ids": ["tc-001"],
        "agent_endpoint_url": "https://agent.example.com/api",
        "grader_ids": ["string-match"]
    })
    run_id = create_response.json()["data"]["id"]
    
    # Poll status
    response = client.get(f"/api/evaluations/{run_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["id"] == run_id
    assert data["data"]["status"] in ["pending", "running", "completed", "failed"]
```

### Test: List evaluations
```python
def test_list_evaluations():
    response = client.get("/api/evaluations")
    assert response.status_code == 200
    data = response.json()
    assert "evaluations" in data["data"]
    assert "count" in data["data"]
    assert "total" in data["data"]
```

### Test: Get evaluation results
```python
def test_get_evaluation_results():
    # Create and complete run (mock agent)
    create_response = client.post("/api/evaluations", json={
        "test_case_ids": ["tc-001"],
        "agent_endpoint_url": "https://agent.example.com/api",
        "grader_ids": ["string-match"]
    })
    run_id = create_response.json()["data"]["id"]
    
    # Wait for completion (in real scenario)
    # Get results
    response = client.get(f"/api/evaluations/{run_id}/results")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data["data"]
    assert "summary" in data["data"]
```

