# Feature Specification: True/False Checker Grader

**Feature Branch**: `002-true-false-grader`  
**Created**: January 15, 2026  
**Status**: Draft  
**Input**: User description: "Add another grader which is True/False checker"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Create and Configure True/False Grader (Priority: P1)

Evaluators need to create a new grader instance that validates whether agent responses are boolean True/False values matching expected outcomes. This enables binary classification evaluation workflows where agents must produce correct true/false determinations.

**Why this priority**: Core feature that enables the grader's basic functionality. Without this, the grader cannot be used at all.

**Independent Test**: Can create and configure a True/False grader instance, and when grading, it correctly classifies responses as "passed" (correct boolean) or "failed" (wrong boolean). This alone delivers value for binary evaluation scenarios.

**Acceptance Scenarios**:

1. **Given** a True/False grader is instantiated with default config, **When** no config is provided, **Then** the grader initializes with case-insensitive matching for "true", "false", "yes", "no" variants
2. **Given** a configured True/False grader, **When** validate_config() is called, **Then** configuration is valid if all config keys are recognized
3. **Given** a grader with custom config mapping, **When** instantiated with custom true/false aliases, **Then** the grader accepts and uses those custom aliases for matching

---

### User Story 2 - Grade Exact Boolean Matches (Priority: P1)

Evaluators need the grader to evaluate agent responses against expected boolean values, with responses considered passed only when they match the expected boolean (case-insensitive).

**Why this priority**: Core grading functionality that directly evaluates responses. All evaluation workflows depend on this.

**Independent Test**: Provide expected value (e.g., "true") and agent response (e.g., "True"), grader returns passed=true and score=1.0. Provides immediate feedback on grading capability.

**Acceptance Scenarios**:

1. **Given** expected output "true" and agent response "true", **When** graded, **Then** result is passed=true, score=1.0
2. **Given** expected output "false" and agent response "false", **When** graded, **Then** result is passed=true, score=1.0
3. **Given** expected output "true" and agent response "false", **When** graded, **Then** result is passed=false, score=0.0
4. **Given** expected output "false" and agent response "true", **When** graded, **Then** result is passed=false, score=0.0
5. **Given** expected output "true" and agent response "TRUE" (uppercase), **When** graded with case_insensitive=true, **Then** result is passed=true, score=1.0

---

### User Story 3 - Handle Multiple Boolean Aliases (Priority: P1)

Evaluators need the grader to recognize common boolean representations (true/false, yes/no, 1/0) so agents can respond in their natural format while still being correctly evaluated.

**Why this priority**: Core functionality - restricting to only "true/false" would reject valid boolean responses like "yes/no" or "1/0", limiting real-world usability.

**Independent Test**: Provide response "yes" when expecting "true", grader recognizes these as equivalent booleans and returns passed=true. Alone, this validates cross-format boolean handling.

**Acceptance Scenarios**:

1. **Given** expected "true" and response "yes", **When** graded with alias mapping enabled, **Then** result is passed=true (yes maps to true)
2. **Given** expected "false" and response "no", **When** graded with alias mapping enabled, **Then** result is passed=true (no maps to false)
3. **Given** expected "true" and response "1", **When** graded with numeric aliases enabled, **Then** result is passed=true (1 maps to true)
4. **Given** expected "false" and response "0", **When** graded with numeric aliases enabled, **Then** result is passed=true (0 maps to false)

---

### User Story 4 - Provide Detailed Grading Information (Priority: P2)

Evaluators need detailed grading metadata for analysis, including normalized values, boolean interpretation, and explanation of why a response passed or failed.

**Why this priority**: Important for debugging and understanding grading decisions, but doesn't prevent using the grader (P1 stories provide basic value).

**Independent Test**: Grade a response and inspect the details object to confirm it contains expected, actual, normalized boolean values, and clear explanation of the grading decision.

**Acceptance Scenarios**:

1. **Given** a graded response, **When** inspecting the details object, **Then** it contains "expected_bool", "actual_bool", "match_status", and "reason" fields
2. **Given** mismatched response, **When** details are examined, **Then** reason explains why booleans didn't match
3. **Given** response that doesn't parse as boolean, **When** details are examined, **Then** reason explains the parsing failure

### Edge Cases

- What happens when agent response is not a valid boolean (e.g., "maybe", "unknown")? → Should return passed=false with reason "Response does not represent a boolean value"
- How does system handle whitespace around boolean values (e.g., " true ", "  false  ")? → Should normalize/strip whitespace and treat as valid booleans
- What if both expected and actual responses are invalid booleans? → Should return passed=false with appropriate reason
- What happens with empty strings or null values? → Should return passed=false with reason "Empty or null response"

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: Grader MUST inherit from GraderInterface and implement all abstract methods (grade, validate_config)
- **FR-002**: Grader MUST accept boolean values in multiple formats: "true"/"false", "True"/"False", "yes"/"no", "1"/"0" 
- **FR-003**: Grader MUST perform case-insensitive boolean matching (by default)
- **FR-004**: Grader MUST return dict with "passed" (bool), "score" (float 0.0-1.0), and "details" (dict) structure
- **FR-005**: Grader MUST assign score=1.0 when booleans match and score=0.0 when they don't match
- **FR-006**: Grader MUST accept optional config with "aliases" (dict mapping custom values to true/false) and "case_sensitive" (bool) flags
- **FR-007**: Grader MUST normalize whitespace (strip leading/trailing spaces) from responses automatically
- **FR-008**: Grader MUST provide details object containing normalized_expected, normalized_actual, match_status, and reason fields
- **FR-009**: Grader MUST handle invalid boolean values gracefully by returning passed=false with clear reason
- **FR-010**: Grader MUST be registered in grader service and available via GET /api/graders endpoint
- **FR-011**: Grader config validation MUST accept recognized config keys: aliases, case_sensitive

### Key Entities *(include if feature involves data)*

- **BooleanValue**: Represents a value that can be interpreted as true or false
  - Canonical forms: true, false
  - String aliases: "true", "false", "True", "False", "yes", "no", "Yes", "No", "1", "0"
  - Attributes: original_value, normalized_value, is_boolean_interpretable, reason_if_invalid

- **GradingResult**: Standard grading output structure
  - passed: bool (true if booleans match)
  - score: float (1.0 for match, 0.0 for mismatch or invalid)
  - details: dict with explanation and normalized values

## Success Criteria *(mandatory)*

1. True/False grader is available in grader list at `/api/graders` endpoint alongside StringMatchGrader
2. Grader correctly evaluates 100% of test cases with exact boolean matching (true→true, false→false, true→false both return expected results)
3. Grader recognizes all common boolean aliases (yes/no, 1/0) and treats them as equivalent to true/false
4. Grader handles edge cases gracefully without errors (invalid values, whitespace, empty strings)
5. All grader responses include proper details object with explanation and normalized values
6. Grader can be selected in frontend GraderSelector component for use in evaluation workflows
7. Integration tests validate grading behavior across all boolean formats and edge cases
8. Configuration validation accepts only recognized keys and provides clear error messages

## Assumptions

- Default behavior should be case-insensitive (matches real-world agent responses better)
- Whitespace normalization should happen automatically (improves robustness)
- Default aliases should include common boolean representations (yes/no, 1/0) to maximize compatibility
- Config parameter format should follow StringMatchGrader pattern (dict with optional keys)
- Grader ID should be "true-false" to match naming pattern with "string-match"
- Integration with existing infrastructure (grader service, storage, API) requires minimal changes following established patterns
