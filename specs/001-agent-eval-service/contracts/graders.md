# API Contract: Graders

**Date**: 2026-01-15  
**Purpose**: Define REST API for accessing grader definitions

---

## Overview

Grader endpoints allow users to discover available graders and understand how they work. Graders are managed by the system; users cannot create custom graders via API in MVP (only string-match is available initially).

---

## Endpoints

### 1. List Available Graders

**Endpoint**: `GET /api/graders`

**Purpose**: Retrieve all available graders

**Query Parameters** (all optional):
- `limit`: Max results (default: 50, max: 500)
- `skip`: Number to skip (default: 0)

**Response: 200 OK**
```json
{
  "success": true,
  "data": {
    "graders": [
      {
        "id": "string-match",
        "name": "String Match Grader",
        "description": "Exact or fuzzy string matching with case and whitespace options",
        "type": "string-match",
        "config_schema": {
          "type": "object",
          "properties": {
            "case_sensitive": {
              "type": "boolean",
              "description": "Whether to perform case-sensitive matching",
              "default": false
            },
            "normalize_whitespace": {
              "type": "boolean",
              "description": "Whether to normalize whitespace before matching",
              "default": true
            }
          }
        }
      }
    ],
    "count": 1,
    "total": 1
  },
  "error": null
}
```

**Grader Types** (MVP):

| ID | Name | Type | Purpose |
|---|---|------|---------|
| `string-match` | String Match Grader | string-match | Exact or case-insensitive/whitespace-insensitive text matching |

---

### 2. Get Grader Details

**Endpoint**: `GET /api/graders/{id}`

**Purpose**: Retrieve details and configuration schema for a specific grader

**Path Parameters**:
- `id`: Grader ID (e.g., "string-match")

**Response: 200 OK**
```json
{
  "success": true,
  "data": {
    "id": "string-match",
    "name": "String Match Grader",
    "description": "Exact or fuzzy string matching with case and whitespace options",
    "type": "string-match",
    "config_schema": {
      "type": "object",
      "properties": {
        "case_sensitive": {
          "type": "boolean",
          "description": "Whether to perform case-sensitive matching",
          "default": false
        },
        "normalize_whitespace": {
          "type": "boolean",
          "description": "Whether to normalize whitespace before matching",
          "default": true
        }
      },
      "required": []
    },
    "scoring_guide": {
      "1.0": "Response exactly matches expected output (within configured options)",
      "0.0": "Response does not match expected output"
    }
  },
  "error": null
}
```

**Error Responses**:

| Status | Scenario | Response |
|--------|----------|----------|
| 404 Not Found | Grader doesn't exist | `{"success": false, "error": {"code": "NOT_FOUND", "message": "Grader not found"}}` |

---

## Grader Configuration Reference

### String Match Grader

**ID**: `string-match`

**Description**: Compares agent response to expected output with configurable case sensitivity and whitespace normalization.

**Configuration Options**:

```json
{
  "case_sensitive": false,
  "normalize_whitespace": true
}
```

**Parameters**:
- `case_sensitive` (boolean, default: false): If false, "Paris" matches "paris"
- `normalize_whitespace` (boolean, default: true): If true, "Paris\n" matches "Paris"

**Scoring**:
- **1.0 (Pass)**: Actual response matches expected output per configuration
- **0.0 (Fail)**: No match

**Examples**:

Case 1: case_sensitive=false, normalize_whitespace=true
```
Expected: "Paris"
Actual:   "paris"
Result:   PASS (1.0) - case ignored
```

Case 2: case_sensitive=false, normalize_whitespace=true
```
Expected: "Paris"
Actual:   "  paris  \n"
Result:   PASS (1.0) - case ignored, whitespace normalized
```

Case 3: case_sensitive=true, normalize_whitespace=false
```
Expected: "Paris"
Actual:   "paris"
Result:   FAIL (0.0) - case mismatch
```

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
| NOT_FOUND | 404 | Grader not found |

---

## Contract Tests (pytest examples)

### Test: List graders
```python
def test_list_graders():
    response = client.get("/api/graders")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "graders" in data["data"]
    assert len(data["data"]["graders"]) > 0
    # Verify string-match grader exists
    grader_ids = [g["id"] for g in data["data"]["graders"]]
    assert "string-match" in grader_ids
```

### Test: Get grader details
```python
def test_get_grader_details():
    response = client.get("/api/graders/string-match")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["id"] == "string-match"
    assert "config_schema" in data["data"]
    assert "scoring_guide" in data["data"]
```

### Test: Get nonexistent grader
```python
def test_get_nonexistent_grader():
    response = client.get("/api/graders/nonexistent")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "NOT_FOUND"
```

