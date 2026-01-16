# Quickstart: True/False Checker Grader

**Purpose**: Get a working True/False grader implementation quickly  
**Target**: Developers implementing Phase 2 tasks  
**Status**: Design Phase

## Overview

The True/False Checker grader evaluates agent responses against expected boolean values. It supports multiple boolean formats (true/false, yes/no, 1/0) and integrates seamlessly with the existing grader infrastructure.

## Quick Reference

### Grader ID
```
"true-false"
```

### Default Aliases
- **True**: "true", "True", "TRUE", "yes", "Yes", "YES", "1"
- **False**: "false", "False", "FALSE", "no", "No", "NO", "0"

### Usage Pattern

```python
from src.graders.true_false import TrueFalseGrader

# Create with defaults
grader = TrueFalseGrader()

# Grade a response
result = grader.grade(agent_response="yes", expected_output="true")
# → {"passed": true, "score": 1.0, "details": {...}}
```

## Implementation Structure

### Files to Create

1. **`backend/src/graders/true_false.py`** (~150 lines)
   - TrueFalseGrader class
   - Inherits from GraderInterface
   - Implements grade() and validate_config()

2. **`backend/tests/unit/test_true_false_grader.py`** (~200 lines)
   - Unit tests for all grading scenarios
   - Edge case tests
   - Configuration validation tests

### Files to Modify

1. **`backend/src/graders/__init__.py`**
   - Add: `from .true_false import TrueFalseGrader`

2. **`backend/src/services/grader_service.py`**
   - Register grader: `"true-false": TrueFalseGrader("true-false")`

### No Changes Required

- ✅ API endpoints (auto-discovered)
- ✅ Frontend components (auto-discovers via API)
- ✅ Storage layer (grader is stateless)
- ✅ Evaluation service (already supports any grader)

## Implementation Checklist

### Phase 2A: Core Implementation

- [ ] Create `src/graders/true_false.py` with TrueFalseGrader class
- [ ] Implement `__init__()` with config parsing
- [ ] Implement `grade()` method with all scenarios
- [ ] Implement `validate_config()` method
- [ ] Update `src/graders/__init__.py` to export TrueFalseGrader
- [ ] Register in `src/services/grader_service.py`
- [ ] Verify grader appears in GET /api/graders

### Phase 2B: Unit Testing

- [ ] Create `tests/unit/test_true_false_grader.py`
- [ ] Test exact boolean matching (true→true, false→false, etc.)
- [ ] Test alias recognition (yes→true, no→false, 1→true, 0→false)
- [ ] Test case insensitivity (TRUE→true, yes→true, etc.)
- [ ] Test whitespace normalization (" true "→"true", etc.)
- [ ] Test invalid responses (score=0.0, passed=false)
- [ ] Test custom aliases configuration
- [ ] Test case sensitivity option
- [ ] Test edge cases (empty string, None, etc.)
- [ ] Verify all details fields populated

### Phase 2C: Integration Testing

- [ ] Add true-false grader test case to integration tests
- [ ] Verify grader selectable in frontend GraderSelector
- [ ] Verify full evaluation workflow with true-false grader
- [ ] Test evaluation results display correctly
- [ ] Manual end-to-end test in UI

## Code Organization

### TrueFalseGrader Class Structure

```python
class TrueFalseGrader(GraderInterface):
    """Boolean value matcher with multi-format support"""
    
    def __init__(self, grader_id="true-false", config=None):
        """Initialize with optional custom configuration"""
        # Extract and cache config values
    
    def validate_config(self) -> bool:
        """Validate configuration keys and structure"""
        # Check recognized keys
        # Validate aliases dict if present
        # Validate case_sensitive bool if present
    
    def _normalize(self, text: str) -> str:
        """Normalize text for comparison"""
        # Strip whitespace
        # Apply case normalization if needed
    
    def _interpret_boolean(self, value: str) -> tuple[str|None, str]:
        """Interpret string as boolean"""
        # Normalize input
        # Check against aliases
        # Return (boolean_value, original_value) or (None, original_value)
    
    def grade(self, agent_response: str, expected_output: str) -> dict:
        """Grade response against expected boolean"""
        # Normalize inputs
        # Interpret both as booleans
        # Compare and score
        # Return detailed result
```

### Test Structure

```python
class TestTrueFalseGrader:
    
    def test_exact_match_true(self):
        # Expected: true, Response: true → passed=true
    
    def test_exact_match_false(self):
        # Expected: false, Response: false → passed=true
    
    def test_mismatch(self):
        # Expected: true, Response: false → passed=false
    
    def test_case_insensitive_true(self):
        # Expected: true, Response: TRUE → passed=true
    
    def test_alias_yes_to_true(self):
        # Expected: true, Response: yes → passed=true
    
    def test_alias_no_to_false(self):
        # Expected: false, Response: no → passed=true
    
    def test_numeric_1_to_true(self):
        # Expected: true, Response: 1 → passed=true
    
    def test_invalid_response(self):
        # Expected: true, Response: maybe → passed=false
    
    def test_empty_response(self):
        # Expected: true, Response: "" → passed=false
    
    def test_whitespace_normalization(self):
        # Expected: " true ", Response: "  yes  " → passed=true
    
    def test_custom_aliases(self):
        # Config: {"aliases": {"true": ["yep"], "false": ["nope"]}}
        # Response: yep → Treated as true
    
    def test_details_structure(self):
        # Result has all required details fields
    
    def test_validate_config_default(self):
        # No config provided → validate_config() returns True
    
    def test_validate_config_invalid_aliases(self):
        # Invalid aliases dict → validate_config() returns False
```

## Example Workflows

### Workflow 1: Basic Grading (No Config)

```python
grader = TrueFalseGrader()

# Test 1: Match
result = grader.grade("true", "true")
assert result["passed"] == True
assert result["score"] == 1.0

# Test 2: Mismatch
result = grader.grade("false", "true")
assert result["passed"] == False
assert result["score"] == 0.0

# Test 3: Alias
result = grader.grade("yes", "true")
assert result["passed"] == True
```

### Workflow 2: Custom Aliases

```python
config = {
    "aliases": {
        "true": ["affirmative", "correct"],
        "false": ["incorrect", "wrong"]
    }
}
grader = TrueFalseGrader(config=config)

result = grader.grade("affirmative", "true")
assert result["passed"] == True

result = grader.grade("incorrect", "false")
assert result["passed"] == True
```

### Workflow 3: Case Sensitive Mode

```python
config = {"case_sensitive": True}
grader = TrueFalseGrader(config=config)

# Case must match exactly (or be in aliases)
result = grader.grade("TRUE", "true")
# → passed=false (TRUE not in aliases by default when case_sensitive=true)
```

### Workflow 4: Integration with Evaluation

```python
# In evaluation flow
test_case = TestCase(
    question="Is 2+2=4?",
    expected_output="true"
)

grader = grader_service.get_grader("true-false")
agent_response = "yes"  # Agent's answer

result = grader.grade(agent_response, test_case.expected_output)
# → {"passed": true, "score": 1.0, "details": {...}}

# Store result
grading_result = {
    "test_case_id": test_case.id,
    "grader_id": "true-false",
    "grading_result": result
}
```

## Testing Validation

All tests should verify:

1. ✅ Return value structure is correct
2. ✅ Score is 0.0 or 1.0 (no partial credit)
3. ✅ passed bool matches score (true if 1.0, false if 0.0)
4. ✅ Details object always populated
5. ✅ Reason field is non-empty and descriptive
6. ✅ Original values preserved in details
7. ✅ No exceptions raised on edge cases

## Common Issues & Solutions

### Issue: "Grader not in /api/graders"
**Solution**: Verify registration in grader_service.py and __init__.py import added

### Issue: "Alias not recognized"
**Solution**: Verify aliases are exact strings in config (case-sensitive within dict)

### Issue: "Case sensitive returns unexpected results"
**Solution**: Remember case_sensitive=True requires exact alias match; True is not same as true

### Issue: "Invalid response still shows in details"
**Solution**: Check details.actual_bool is None for invalid responses (expected behavior)

## Success Indicators

When complete, you should be able to:

1. ✅ Select "True/False" grader in frontend GraderSelector
2. ✅ Create test case with boolean expected_output
3. ✅ Run evaluation with True/False grader
4. ✅ See grading results in UI with correct score/passed status
5. ✅ View detailed explanation of grading decision
6. ✅ All unit tests passing (100% coverage on grader logic)
7. ✅ Integration test validating full workflow
