# Data Model: True/False Checker Grader

**Phase**: 1 - Design & Contracts  
**Date**: 2026-01-15  
**Status**: Complete

## Entities & State

### 1. TrueFalseGrader

**Responsibility**: Validate boolean responses and compute grading scores

**Configuration**:
```python
config: Dict[str, Any] = {
    "aliases": {          # Optional: custom boolean mappings
        "true": ["true", "True", "yes", "Yes", "1"],
        "false": ["false", "False", "no", "No", "0"]
    },
    "case_sensitive": bool = False  # Optional: enforce case sensitivity
}
```

**State**:
- `grader_id: str = "true-false"`
- `config: Dict[str, Any]` (initialized from constructor)
- `case_sensitive: bool` (extracted from config)
- `true_aliases: List[str]` (parsed and cached from config)
- `false_aliases: List[str]` (parsed and cached from config)

**Behavior**:

1. **Initialization** (`__init__`)
   - Accept grader_id and optional config dict
   - Parse aliases from config (use defaults if not provided)
   - Cache case_sensitive flag
   - Raise ValueError if config contains unrecognized keys

2. **Configuration Validation** (`validate_config()`)
   - Check all config keys are in ["aliases", "case_sensitive"]
   - If aliases provided, verify it's a dict with "true" and "false" keys
   - Return True if valid, log warnings for unknown keys
   - Never raise exceptions (returns False for invalid)

3. **Boolean Value Normalization** (internal)
   - Strip whitespace from input
   - Apply case normalization if case_sensitive=False
   - Return normalized string

4. **Boolean Interpretation** (internal)
   - Check normalized value against true_aliases
   - If match found, return ("true", original_value)
   - Check normalized value against false_aliases
   - If match found, return ("false", original_value)
   - If no match, return (None, original_value) → invalid

5. **Grading** (`grade(agent_response: str, expected_output: str)`)
   - Normalize both inputs
   - Interpret expected_output as boolean
   - Interpret agent_response as boolean
   - Compare booleans (match = True, else False)
   - Return grading result (see below)

### 2. GradingResult

**Output Structure** (returned from `grade()`):
```python
{
    "passed": bool,          # True if booleans match, False otherwise
    "score": float,          # 1.0 if passed, 0.0 if not
    "details": {
        "expected_bool": str,          # "true" or "false"
        "actual_bool": str|None,       # "true", "false", or None if invalid
        "match_status": str,           # "match", "mismatch", or "invalid_response"
        "reason": str,                 # Human-readable explanation
        "expected_original": str,      # Original expected input before normalization
        "actual_original": str         # Original agent response before normalization
    }
}
```

**Details Field Logic**:
- If both booleans are valid and match: `match_status="match"`, `reason="Expected and actual values match"`, `passed=true`
- If both booleans are valid but don't match: `match_status="mismatch"`, `reason="Expected <expected_bool> but got <actual_bool>"`, `passed=false`
- If expected valid but actual invalid: `match_status="invalid_response"`, `reason="Response '<actual_original>' does not represent a boolean value"`, `passed=false`
- If expected invalid (should not happen in normal flow): `match_status="invalid_expected"`, `reason="Expected value '<expected_original>' is not a valid boolean"`, `passed=false`
- If response is empty/null: `match_status="invalid_response"`, `reason="Empty or null response"`, `passed=false`

### 3. BooleanAliases (Configuration Schema)

**Structure**:
```python
{
    "true": ["true", "True", "TRUE", "yes", "Yes", "YES", "1"],
    "false": ["false", "False", "FALSE", "no", "No", "NO", "0"]
}
```

**Rules**:
- Keys MUST be lowercase "true" or "false"
- Values MUST be lists of strings
- Each alias should be pre-normalized (case-handling delegated to case_sensitive flag)
- Aliases are case-sensitive within this dict (case_sensitive flag applies later)

## Entity Relationships

```
TrueFalseGrader
  ├─ inherits from: GraderInterface
  ├─ creates: GradingResult
  └─ uses: BooleanAliases (from config)

GraderInterface (defined in base.py)
  ├─ abstract method: grade() → GradingResult
  ├─ abstract method: validate_config() → bool
  └─ implemented by: StringMatchGrader, TrueFalseGrader

grader_service (existing)
  └─ registers: [StringMatchGrader, TrueFalseGrader]
     └─ provides via: GET /api/graders
```

## Validation Rules

### TrueFalseGrader Initialization
1. grader_id MUST be string (default: "true-false")
2. config MUST be dict or None
3. If config provided, keys MUST be subset of ["aliases", "case_sensitive"]
4. If "aliases" in config, MUST be dict with "true" and "false" keys
5. If "case_sensitive" in config, MUST be bool

### GradingResult Structure
1. "passed" MUST be bool
2. "score" MUST be float in range [0.0, 1.0]
3. "details" MUST be dict with required keys: expected_bool, actual_bool, match_status, reason
4. "reason" MUST be human-readable string
5. "match_status" MUST be one of: "match", "mismatch", "invalid_response", "invalid_expected"

## State Mutations

**Immutable** (no state changes after initialization):
- grader_id (set once in __init__)
- case_sensitive (set once in __init__)
- Alias mappings (set once in __init__)

All methods are stateless (no side effects, deterministic).

## Edge Cases & Boundary Conditions

1. **Empty/Null Inputs**
   - agent_response = "" → invalid, score=0.0
   - agent_response = None → invalid, score=0.0
   - agent_response = "   " (whitespace only) → invalid after normalization, score=0.0

2. **Ambiguous Inputs**
   - agent_response = "yes" when expected = "true" → valid match (alias), score=1.0
   - agent_response = "1" when expected = "false" → invalid match, score=0.0

3. **Case Sensitivity**
   - case_sensitive=False, agent_response="TRUE" when expected="true" → match, score=1.0
   - case_sensitive=True, agent_response="TRUE" when expected="true" → no match (unless True in aliases), score=0.0

4. **Custom Aliases**
   - config = {"aliases": {"true": ["yep"], "false": ["nope"]}}
   - agent_response = "yep" when expected = "true" → match, score=1.0

5. **Invalid Boolean Values**
   - agent_response = "maybe" → invalid, score=0.0, reason explains non-match
   - agent_response = "42" → invalid, score=0.0
   - agent_response = "on" (not in aliases) → invalid, score=0.0

## Assumptions

1. Inputs are always strings (agent responses and expected outputs from TestCase)
2. GraderInterface is the correct abstraction point (not modifying)
3. grader_service auto-discovers graders (registration is the only requirement)
4. Default aliases cover 90%+ of real-world cases
5. No persistence needed (grader is stateless)
6. Boolean semantics are platform-independent (true/false have universal meaning)
