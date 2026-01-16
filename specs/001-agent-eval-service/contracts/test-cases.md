# API Contract: Test Cases

**Date**: 2026-01-15  
**Purpose**: Define REST API for Test Case management (CRUD operations)

---

## Overview

Test Case endpoints allow users to create, read, update, and delete test case definitions. Test cases are immutable once used in an evaluation run (though they can still be edited, affecting future runs).

---

## Endpoints

### 1. Create Test Case

**Endpoint**: `POST /api/test-cases`

**Purpose**: Create a new test case

**Request Headers**:
```
Content-Type: application/json
```

**Request Body** (JSON):
```json
{
  "input": "What is the capital of France?",
  "expected_output": "Paris",
  "description": "Basic geography question",
  "tags": ["geography", "basic"]
}
```

**Request Validation**:
- `input`: Required, 1-10,000 characters
- `expected_output`: Required, 1-10,000 characters
- `description`: Optional, max 500 characters
- `tags`: Optional array, max 10 tags, each 1-50 chars

**Response: 201 Created**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "input": "What is the capital of France?",
    "expected_output": "Paris",
    "description": "Basic geography question",
    "tags": ["geography", "basic"],
    "created_at": "2026-01-15T10:30:00Z",
    "modified_at": "2026-01-15T10:30:00Z"
  },
  "error": null
}
```

**Error Responses**:

| Status | Scenario | Response |
|--------|----------|----------|
| 400 Bad Request | Missing required field | `{"success": false, "error": {"code": "MISSING_FIELD", "message": "Field 'input' is required"}}` |
| 400 Bad Request | Input too long | `{"success": false, "error": {"code": "INVALID_LENGTH", "message": "Input must be 1-10000 chars"}}` |
| 500 Internal Server Error | Server error | `{"success": false, "error": {"code": "INTERNAL_ERROR", "message": "..."}}` |

---

### 2. Get Test Case

**Endpoint**: `GET /api/test-cases/{id}`

**Purpose**: Retrieve a specific test case by ID

**Path Parameters**:
- `id`: UUID of test case

**Response: 200 OK**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "input": "What is the capital of France?",
    "expected_output": "Paris",
    "description": "Basic geography question",
    "tags": ["geography", "basic"],
    "created_at": "2026-01-15T10:30:00Z",
    "modified_at": "2026-01-15T10:30:00Z"
  },
  "error": null
}
```

**Error Responses**:

| Status | Scenario | Response |
|--------|----------|----------|
| 404 Not Found | Test case doesn't exist | `{"success": false, "error": {"code": "NOT_FOUND", "message": "Test case not found"}}` |

---

### 3. List Test Cases

**Endpoint**: `GET /api/test-cases`

**Purpose**: Retrieve all test cases

**Query Parameters** (all optional):
- `limit`: Max results (default: 100, max: 1000)
- `skip`: Number to skip (default: 0)
- `tag`: Filter by tag (partial match)

**Examples**:
- `GET /api/test-cases` - All test cases
- `GET /api/test-cases?tag=geography` - Only geography tagged
- `GET /api/test-cases?limit=10&skip=20` - Pagination

**Response: 200 OK**
```json
{
  "success": true,
  "data": {
    "test_cases": [
      {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "input": "What is the capital of France?",
        "expected_output": "Paris",
        "description": "Basic geography question",
        "tags": ["geography", "basic"],
        "created_at": "2026-01-15T10:30:00Z",
        "modified_at": "2026-01-15T10:30:00Z"
      },
      {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "input": "What is 2+2?",
        "expected_output": "4",
        "description": "Basic math",
        "tags": ["math"],
        "created_at": "2026-01-15T10:31:00Z",
        "modified_at": "2026-01-15T10:31:00Z"
      }
    ],
    "count": 2,
    "total": 42
  },
  "error": null
}
```

---

### 4. Update Test Case

**Endpoint**: `PUT /api/test-cases/{id}`

**Purpose**: Update an existing test case (all fields optional)

**Path Parameters**:
- `id`: UUID of test case

**Request Body** (JSON, all fields optional):
```json
{
  "input": "Updated input text",
  "expected_output": "Updated expected output",
  "description": "Updated description",
  "tags": ["updated", "tags"]
}
```

**Response: 200 OK**
```json
{
  "success": true,
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "input": "Updated input text",
    "expected_output": "Updated expected output",
    "description": "Updated description",
    "tags": ["updated", "tags"],
    "created_at": "2026-01-15T10:30:00Z",
    "modified_at": "2026-01-15T10:35:00Z"
  },
  "error": null
}
```

**Error Responses**:

| Status | Scenario | Response |
|--------|----------|----------|
| 404 Not Found | Test case doesn't exist | `{"success": false, "error": {"code": "NOT_FOUND", "message": "Test case not found"}}` |
| 400 Bad Request | Validation failure | `{"success": false, "error": {"code": "INVALID_INPUT", "message": "..."}}` |

**Behavior**: `modified_at` automatically updated to current time

---

### 5. Delete Test Case

**Endpoint**: `DELETE /api/test-cases/{id}`

**Purpose**: Delete a test case

**Path Parameters**:
- `id`: UUID of test case

**Response: 204 No Content**
```
(empty body)
```

**Error Responses**:

| Status | Scenario | Response |
|--------|----------|----------|
| 404 Not Found | Test case doesn't exist | `{"success": false, "error": {"code": "NOT_FOUND", "message": "Test case not found"}}` |

**Behavior**: 
- Soft delete recommended (mark as deleted, don't remove)
- Results for this test case remain in storage for historical reference
- Deleted test cases not returned in list queries

---

## Response Format Standard

All responses follow this structure:

**Success** (all endpoints):
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

**Error** (all endpoints):
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

**Standard HTTP Status Codes**:
- `200 OK`: Request succeeded, response has data
- `201 Created`: Resource created successfully
- `204 No Content`: Request succeeded, no content returned
- `400 Bad Request`: Invalid input or validation error
- `404 Not Found`: Resource doesn't exist
- `500 Internal Server Error`: Server-side error

---

## Error Codes

| Code | HTTP | Meaning |
|------|------|---------|
| MISSING_FIELD | 400 | Required field not provided |
| INVALID_LENGTH | 400 | Field length outside allowed range |
| INVALID_INPUT | 400 | Input fails validation |
| DUPLICATE_ID | 400 | ID already exists (only on POST) |
| NOT_FOUND | 404 | Resource not found |
| INTERNAL_ERROR | 500 | Unexpected server error |

---

## Contract Tests (pytest examples)

### Test: Create valid test case
```python
def test_create_test_case_success():
    response = client.post("/api/test-cases", json={
        "input": "test input",
        "expected_output": "expected",
        "description": "desc",
        "tags": ["tag1"]
    })
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["id"]
    assert data["data"]["input"] == "test input"
    assert data["data"]["expected_output"] == "expected"
```

### Test: Create test case with missing input
```python
def test_create_test_case_missing_input():
    response = client.post("/api/test-cases", json={
        "expected_output": "expected"
    })
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "MISSING_FIELD"
```

### Test: List test cases with pagination
```python
def test_list_test_cases_pagination():
    # Create 5 test cases first
    for i in range(5):
        client.post("/api/test-cases", json={
            "input": f"input {i}",
            "expected_output": f"output {i}"
        })
    
    # Get first 2
    response = client.get("/api/test-cases?limit=2&skip=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["test_cases"]) == 2
    assert data["data"]["total"] == 5
```

### Test: Update test case
```python
def test_update_test_case():
    # Create
    create_response = client.post("/api/test-cases", json={
        "input": "original input",
        "expected_output": "original output"
    })
    test_case_id = create_response.json()["data"]["id"]
    
    # Update
    update_response = client.put(f"/api/test-cases/{test_case_id}", json={
        "input": "updated input"
    })
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["data"]["input"] == "updated input"
    assert data["data"]["expected_output"] == "original output"  # Unchanged
```

### Test: Delete test case
```python
def test_delete_test_case():
    # Create
    create_response = client.post("/api/test-cases", json={
        "input": "test",
        "expected_output": "test"
    })
    test_case_id = create_response.json()["data"]["id"]
    
    # Delete
    delete_response = client.delete(f"/api/test-cases/{test_case_id}")
    assert delete_response.status_code == 204
    
    # Verify deleted
    get_response = client.get(f"/api/test-cases/{test_case_id}")
    assert get_response.status_code == 404
```

