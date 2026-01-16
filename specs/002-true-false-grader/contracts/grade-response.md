# Contract: Grade Response

**Method**: `TrueFalseGrader.grade(agent_response: str, expected_output: str) -> Dict[str, Any]`  
**Type**: Public Interface Contract  
**Status**: Design Phase

## Summary

The grade method evaluates agent responses against expected boolean values, returning a standardized grading result with score and detailed explanation.

## Method Signature

```python
def grade(self, agent_response: str, expected_output: str) -> Dict[str, Any]:
    """
    Grade a response using boolean matching.
    
    Args:
        agent_response: The response from the agent (e.g., "true", "yes", "1")
        expected_output: The expected boolean value (e.g., "true", "false")
    
    Returns:
        {
            "passed": bool,
            "score": float (0.0-1.0),
            "details": {
                "expected_bool": str,      # "true" or "false"
                "actual_bool": str|None,   # "true", "false", or None
                "match_status": str,       # "match", "mismatch", "invalid_response"
                "reason": str,             # Human-readable explanation
                "expected_original": str,  # Original input before normalization
                "actual_original": str     # Original input before normalization
            }
        }
    """
```

## Processing Algorithm

1. **Input Normalization**
   - Strip whitespace from both inputs
   - Store original values for details
   - If case_sensitive=False, convert to lowercase

2. **Boolean Interpretation**
   - Check normalized agent_response against true_aliases
   - Check normalized agent_response against false_aliases
   - Check normalized expected_output against true_aliases
   - Check normalized expected_output against false_aliases
   - If either doesn't match any alias → invalid

3. **Comparison**
   - If both valid: compare booleans (true/false)
   - If agent_response invalid: passed=false
   - If expected_output invalid: passed=false (unexpected but handled)

4. **Score Assignment**
   - passed=true → score=1.0
   - passed=false → score=0.0

5. **Details Construction**
   - Populate all required fields
   - Provide clear reason for pass/fail

## Return Value Contracts

### Success Case (Booleans Match)

**Input**: expected="true", response="yes"

```python
{
    "passed": True,
    "score": 1.0,
    "details": {
        "expected_bool": "true",
        "actual_bool": "true",
        "match_status": "match",
        "reason": "Expected and actual values match",
        "expected_original": "true",
        "actual_original": "yes"
    }
}
```

### Mismatch Case (Different Booleans)

**Input**: expected="true", response="false"

```python
{
    "passed": False,
    "score": 0.0,
    "details": {
        "expected_bool": "true",
        "actual_bool": "false",
        "match_status": "mismatch",
        "reason": "Expected true but got false",
        "expected_original": "true",
        "actual_original": "false"
    }
}
```

### Invalid Response Case

**Input**: expected="true", response="maybe"

```python
{
    "passed": False,
    "score": 0.0,
    "details": {
        "expected_bool": "true",
        "actual_bool": None,
        "match_status": "invalid_response",
        "reason": "Response 'maybe' does not represent a boolean value",
        "expected_original": "true",
        "actual_original": "maybe"
    }
}
```

### Empty Response Case

**Input**: expected="true", response=""

```python
{
    "passed": False,
    "score": 0.0,
    "details": {
        "expected_bool": "true",
        "actual_bool": None,
        "match_status": "invalid_response",
        "reason": "Empty or null response",
        "expected_original": "true",
        "actual_original": ""
    }
}
```

### Whitespace Normalization Case

**Input**: expected=" true ", response="  Yes  " (with case_sensitive=False)

```python
{
    "passed": True,
    "score": 1.0,
    "details": {
        "expected_bool": "true",
        "actual_bool": "true",
        "match_status": "match",
        "reason": "Expected and actual values match",
        "expected_original": " true ",
        "actual_original": "  Yes  "
    }
}
```

### Custom Aliases Case

**Input**: expected="true", response="yep"  
**Config**: `{"aliases": {"true": ["yep"], "false": ["nope"]}}`

```python
{
    "passed": True,
    "score": 1.0,
    "details": {
        "expected_bool": "true",
        "actual_bool": "true",
        "match_status": "match",
        "reason": "Expected and actual values match",
        "expected_original": "true",
        "actual_original": "yep"
    }
}
```

## Type Guarantees

- **returned["passed"]** is always bool (never None)
- **returned["score"]** is always float in [0.0, 1.0] (never NaN)
- **returned["details"]** is always dict with all required keys
- **returned["details"]["actual_bool"]** can be "true", "false", or None (invalid)
- **returned["details"]["match_status"]** is always one of: "match", "mismatch", "invalid_response"
- **returned["details"]["reason"]** is always non-empty string

## Determinism Guarantee

- Same (agent_response, expected_output) inputs with same grader config → identical output
- No randomness, timing-dependent behavior, or state mutations
- Thread-safe (no shared state modifications)

## Error Handling

**No Exceptions Raised**:
- Invalid inputs → score=0.0, details.reason explains issue
- Unknown boolean format → score=0.0, details.reason explains
- Edge cases (None, empty string) → handled gracefully with informative reason

**Logging**:
- No logging in grade() method (kept clean)
- Validation failures logged in validate_config() method

## Success Criteria

✅ Booleans match (same format) → passed=true, score=1.0  
✅ Booleans match (different formats) → passed=true, score=1.0  
✅ Booleans mismatch → passed=false, score=0.0  
✅ Invalid response → passed=false, score=0.0, reason explains  
✅ Whitespace handled → normalized before comparison  
✅ Custom aliases work → recognized as valid booleans  
✅ Details always populated → all fields present and valid  
✅ No exceptions → edge cases handled gracefully  
