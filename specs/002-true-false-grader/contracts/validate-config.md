# Contract: Validate Configuration

**Method**: `TrueFalseGrader.validate_config() -> bool`  
**Type**: Public Interface Contract  
**Status**: Design Phase

## Summary

The validate_config method verifies that the grader's configuration is valid and recognizes all config keys. Returns bool (never raises exceptions).

## Method Signature

```python
def validate_config(self) -> bool:
    """
    Validate grader configuration.
    
    Returns:
        True if config is valid, False otherwise.
        
    Note: This method logs warnings for unknown keys but doesn't raise exceptions.
    It allows partial initialization with defaults for unrecognized settings.
    """
```

## Validation Rules

### Valid Configuration Checks

1. **Config type**: `config` must be dict or None
   - If None → valid (uses defaults)
   - If not dict → invalid, return False

2. **Config keys**: All keys must be in recognized set
   - Recognized keys: ["aliases", "case_sensitive"]
   - Unknown keys → log warning, continue (not blocking)
   - Return False only if blocking errors found

3. **Aliases structure** (if present):
   - Must be dict type
   - Must have "true" key with list value
   - Must have "false" key with list value
   - Each value must be list of strings
   - Invalid → return False

4. **Case sensitivity** (if present):
   - Must be bool type
   - Invalid → return False

### Validation Scenarios

#### Valid Configurations

**Default (no config)**:
```python
grader = TrueFalseGrader("true-false")  # config={}
validate_config() → True
```

**Custom aliases**:
```python
config = {
    "aliases": {
        "true": ["yep", "affirmative"],
        "false": ["nope", "negative"]
    }
}
grader = TrueFalseGrader("true-false", config)
validate_config() → True
```

**Case sensitive**:
```python
config = {"case_sensitive": True}
grader = TrueFalseGrader("true-false", config)
validate_config() → True
```

**All options**:
```python
config = {
    "aliases": {
        "true": ["yes"],
        "false": ["no"]
    },
    "case_sensitive": True
}
grader = TrueFalseGrader("true-false", config)
validate_config() → True
```

#### Invalid Configurations

**Non-dict aliases**:
```python
config = {"aliases": ["true", "false"]}  # Should be dict
validate_config() → False
# Reason: aliases is list, not dict
```

**Missing "true" in aliases**:
```python
config = {
    "aliases": {
        "false": ["no"]
        # Missing "true" key
    }
}
validate_config() → False
# Reason: aliases must have both "true" and "false" keys
```

**Non-list alias values**:
```python
config = {
    "aliases": {
        "true": "yes",     # Should be list
        "false": ["no"]
    }
}
validate_config() → False
# Reason: alias values must be lists
```

**Non-bool case_sensitive**:
```python
config = {"case_sensitive": "false"}  # Should be bool
validate_config() → False
# Reason: case_sensitive must be bool
```

**Unknown config key** (non-blocking):
```python
config = {
    "aliases": {"true": ["yes"], "false": ["no"]},
    "max_length": 100  # Unknown key
}
validate_config() → True
# Logs warning: "Unknown config key: max_length"
# But returns True (unknown keys don't block)
```

## Return Value Contracts

| Config State | Return Value | Behavior |
|---|---|---|
| config=None or {} | True | Uses defaults |
| All keys valid and well-formed | True | Configuration accepted |
| Unknown key present | True | Logs warning, continues |
| Invalid key type (e.g., aliases not dict) | False | Validation fails |
| Missing required alias key (true/false) | False | Validation fails |
| Invalid value type (e.g., bool not for case_sensitive) | False | Validation fails |

## Logging Behavior

**Warning Level** (non-blocking):
```
logger.warning(f"Unknown config key: {key}")
```
Logged for each unknown key, but validation continues.

**No Info/Debug** (validation should be silent on success)

**No Exceptions** (all errors handled with return False)

## Usage Context

The validate_config method is called during initialization to ensure the grader can start with the provided configuration. It provides defensive programming without blocking operation.

**Initialization Pattern**:
```python
def __init__(self, grader_id: str = "true-false", config: Optional[Dict] = None):
    super().__init__(grader_id, config)
    
    # Extract and cache config values
    self.case_sensitive = self.config.get("case_sensitive", False)
    self._parse_aliases()
    
    # Validate configuration
    if not self.validate_config():
        logger.warning(f"Configuration validation failed for {grader_id}")
        # Continue anyway with defaults for failed parts
```

## Success Criteria

✅ Default config (no args) passes validation  
✅ Valid aliases config passes validation  
✅ Valid case_sensitive config passes validation  
✅ Combined valid config passes validation  
✅ Unknown keys logged but validation passes  
✅ Missing alias keys → validation fails  
✅ Wrong type for case_sensitive → validation fails  
✅ No exceptions raised → returns bool always  
✅ False return enables graceful degradation to defaults  
