# Contract: Create/Register True/False Grader

**Endpoint**: Not directly exposed (internal registration)  
**Type**: System Integration Contract  
**Status**: Design Phase

## Summary

The True/False grader is registered in the grader service at system startup and becomes available via the existing `/api/graders` endpoint. No new endpoint is created.

## Registration Flow

**Location**: `backend/src/services/grader_service.py` (existing)

**Current Pattern** (with StringMatchGrader):
```python
# In grader_service.py __init__
self.graders = {
    "string-match": StringMatchGrader("string-match")
}
```

**New Pattern** (adding TrueFalseGrader):
```python
# In grader_service.py __init__
from src.graders.true_false import TrueFalseGrader

self.graders = {
    "string-match": StringMatchGrader("string-match"),
    "true-false": TrueFalseGrader("true-false")
}
```

## API Contract: GET /api/graders

**Existing Endpoint** (no changes needed)

### Request

```http
GET /api/graders HTTP/1.1
Host: localhost:8000
Content-Type: application/json
```

### Response (200 OK)

```json
{
  "graders": [
    {
      "id": "string-match",
      "name": "String Match",
      "description": "Exact string matching with optional normalization"
    },
    {
      "id": "true-false",
      "name": "True/False",
      "description": "Boolean value matching with support for multiple formats"
    }
  ]
}
```

## Grader Metadata

Each grader MUST provide:

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `id` | string | "true-false" | Unique identifier, must match grader instance ID |
| `name` | string | "True/False" | Human-readable display name |
| `description` | string | "Boolean..." | Short description of grader purpose |

## Configuration Contract

**Grader ID**: `"true-false"`

**Default Configuration**:
```json
{
  "aliases": {
    "true": ["true", "True", "TRUE", "yes", "Yes", "YES", "1"],
    "false": ["false", "False", "FALSE", "no", "No", "NO", "0"]
  },
  "case_sensitive": false
}
```

**Custom Configuration Example**:
```json
{
  "aliases": {
    "true": ["yep", "affirmative"],
    "false": ["nope", "negative"]
  },
  "case_sensitive": true
}
```

## Integration Points

1. **Grader Service** (`src/services/grader_service.py`)
   - Import TrueFalseGrader from `src.graders.true_false`
   - Register in `graders` dict with ID "true-false"
   - No other changes needed (service already handles auto-discovery)

2. **API Endpoint** (`src/api/graders.py`)
   - No changes needed (automatically includes all graders from service)
   - GET /api/graders already returns all registered graders

3. **Evaluation Service** (`src/services/evaluation_service.py`)
   - No changes needed (already supports any registered grader by ID)
   - Existing grader selection logic applies unchanged

4. **Frontend** (`frontend/src/components/GraderSelector.jsx`)
   - No changes needed (auto-discovers graders from API)
   - True/False grader automatically appears in selector dropdown

## Error Handling

**Invalid Configuration**:
- If unknown config keys provided → Grader logs warning but initializes with defaults for unrecognized keys
- If aliases dict missing "true" or "false" key → ValueError raised
- If case_sensitive is not bool → TypeError raised

**Invalid Grading**:
- If agent_response not parseable as boolean → score=0.0, passed=false, details.reason explains
- If expected_output not parseable as boolean → score=0.0, passed=false (should not happen with valid TestCase)

## Success Criteria

✅ Grader ID "true-false" appears in GET /api/graders response  
✅ Grader can be selected during evaluation creation  
✅ Grader metadata accurate and descriptive  
✅ Configuration defaults handle common boolean formats  
✅ No breaking changes to existing grader API  
