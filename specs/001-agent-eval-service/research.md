# Research: Agent Evaluation as a Service

**Date**: 2026-01-15  
**Feature**: [001-agent-eval-service](./spec.md)  
**Purpose**: Resolve design questions and document architectural decisions

---

## Clarification 1: Custom Grader Definition Format

**Question**: How should users define custom grader logic?

**Decision**: JSON Rule-Based Definition (Option A) with planned extension for scripting

**Rationale**: 
- MVP must be **simple and explicit** per constitution principles
- JSON is straightforward to validate, store, and explain
- Reduces security concerns compared to arbitrary code execution
- Deterministic behavior guaranteed - no runtime execution surprises
- Easy for users to understand and debug without programming knowledge
- Minimal dependencies - uses only standard JSON parsing

**Implementation Approach**:
1. **Phase 0 (MVP)**: String-match grader only (no custom graders yet)
2. **Phase 1 (Future)**: Implement pluggable grader interface to support custom definitions
3. **Phase 2+ (Roadmap)**: JSON-based grader definitions with conditions/rules syntax

**Specification**:
```json
{
  "type": "string-match",
  "config": {
    "case_sensitive": false,
    "normalize_whitespace": false
  }
}
```

Future extensions:
```json
{
  "type": "custom-rules",
  "rules": [
    { "condition": "contains", "value": "keyword" },
    { "condition": "length_min", "value": 10 }
  ]
}
```

**Alternatives Considered**:
- **Python/JavaScript Functions**: Too complex for MVP; security concerns; requires runtime execution
- **Regex Patterns**: Too limited; only works for string matching
- **SQL/Query Syntax**: Overkill for initial graders; unfamiliar to most users

---

## Clarification 2: Custom Grader Error Handling Strategy

**Question**: How should the system handle errors in custom grader definitions or execution?

**Decision**: Per-Result Isolation (Option C) with strict validation

**Rationale**:
- **Correctness & Testability** (Constitution Principle VI): Individual grader failures should not cascade
- **Deterministic Behavior** (Principle IV): Clear, predictable error outcomes
- **Simplicity** (Principle I): Each result tracks its own scores independently
- Allows evaluation run to complete even if one grader fails on one result
- Provides clear visibility into which graders succeeded/failed per result

**Implementation Approach**:

1. **Pre-Execution Validation**:
   - Validate grader definition before use
   - Check for syntax errors, missing required fields
   - Fail fast if validation fails

2. **Per-Result Execution**:
   - Each grader evaluated independently per result
   - Grader timeout: 5 seconds (prevents infinite loops)
   - Errors captured: grader_id, result_id, error_message, error_type
   - Result score for that grader marked as "error" not "success"

3. **Result Storage**:
   - All scores stored, including failed grader attempts
   - Result metadata includes: scores_succeeded, scores_failed
   - Client UI shows which graders failed and why
   - Evaluation run completes successfully even if some graders fail

4. **Reporting**:
   - Evaluation results page shows grader success/failure for each result
   - Summary statistics: "95 responses graded, 3 grader errors"
   - Detailed error messages available in result detail view

**Alternatives Considered**:
- **Fail Safe - Validation Only**: Too strict; prevents any error recovery
- **Sandboxed Execution**: Adds complexity; unclear timeout/resource semantics for MVP
- **Strict Validation + Halt**: Stops entire evaluation on any error; poor UX

---

## Technology Stack Decisions

### Backend: Python + FastAPI

**Decision**: Python 3.11 + FastAPI

**Rationale**:
- FastAPI: Modern, minimal, with automatic OpenAPI documentation
- Native async support for concurrent evaluation runs
- Strong typing via Pydantic (aligns with "explicit" principle)
- Excellent test ecosystem (pytest, pytest-asyncio)

**Alternatives**: Django (too heavy), Flask (too minimal), Node.js/Express (less explicit typing)

### Frontend: JavaScript + Vite + React

**Decision**: Vite + React (vanilla JavaScript, no TypeScript for MVP)

**Rationale**:
- Vite: Fast, minimal build configuration, excellent DX
- React: Well-known component model, large ecosystem
- SPA pattern: Simple to reason about (all state in one JavaScript process)
- No TypeScript: Reduces friction for MVP; can add later if needed

**Alternatives**: Vue (similar choice; React more widely known), Next.js (too opinionated for simple SPA)

### Storage: In-Memory (Python Dictionaries)

**Decision**: All state stored in Python dictionaries/maps in backend process memory

**Rationale**:
- **Simplicity**: No external database complexity
- **Clarity**: All data visible in one place; easy to debug
- **Correctness**: Deterministic reads/writes; no consistency issues
- **MVP Scope**: Sufficient for demo with restart tolerance
- **Constitution Principle I**: Minimal dependencies

**Known Limitations**:
- Data lost on server restart
- Single process (no horizontal scaling)
- Not suitable for production use
- Easy migration path: Replace `storage.py` with database adapter later

---

## Grader Architecture Design

### Core Abstraction: Grader Interface

**Base Grader Class**:
```python
class Grader:
    """Base interface for all graders"""
    def __init__(self, config: dict):
        self.config = config
    
    def grade(self, actual: str, expected: str) -> GradeResult:
        """Score a single response.
        
        Args:
            actual: Agent response text
            expected: Expected output text
            
        Returns:
            GradeResult with score and status
        """
        raise NotImplementedError
```

**String Match Implementation**:
```python
class StringMatchGrader(Grader):
    """Exact or fuzzy string matching grader"""
    def grade(self, actual: str, expected: str) -> GradeResult:
        case_sensitive = self.config.get('case_sensitive', False)
        normalize_whitespace = self.config.get('normalize_whitespace', False)
        # Implementation: compare strings, return Pass/Fail
```

**Benefits**:
- **Clear separation of concerns** (Principle V): Graders isolated from scoring logic
- **Extensible**: Adding new graders doesn't change existing code
- **Testable**: Each grader has deterministic contract
- **Explicit**: Contract clearly defined in base class

---

## Execution Flow Design

### Evaluation Run: 4-Phase Process

**Phase 1: Initialization**
- Load test cases
- Validate agent endpoint URL
- Load graders
- Create empty results collection

**Phase 2: Execution**
- For each test case:
  - Send input to agent endpoint
  - Capture response + latency + any errors
  - Store result

**Phase 3: Grading**
- For each result:
  - For each grader:
    - Call grader.grade(actual, expected)
    - Store score (or error if grader fails)

**Phase 4: Aggregation**
- Calculate summary statistics
- Count pass/fail by grader
- Compute overall metrics

**Design Rationale**:
- **Separation of concerns**: Execution, grading, aggregation are independent
- **Deterministic**: Same input always produces same result
- **Error resilience**: Phase 3 grader failures don't affect other phases
- **Observable**: Each phase can be logged and inspected independently

---

## Data Persistence Strategy

### In-Memory Storage Abstraction

**Design Pattern**: Storage module provides unified interface; implementation swappable

```python
# src/services/storage.py
class Storage:
    def save_test_case(self, test_case: TestCase) -> str:
        """Store test case, return ID"""
    
    def get_test_case(self, id: str) -> Optional[TestCase]:
        """Retrieve test case by ID"""
    
    def list_test_cases(self) -> List[TestCase]:
        """List all test cases"""
    
    def delete_test_case(self, id: str) -> bool:
        """Delete test case, return success"""
```

**MVP Implementation**: Python dictionaries with UUID keys
```python
class InMemoryStorage(Storage):
    def __init__(self):
        self._test_cases = {}  # id -> TestCase
        self._evaluations = {}  # id -> EvaluationRun
        self._results = {}     # id -> EvaluationResult
        self._graders = {}     # id -> Grader
```

**Migration Path**: Implement `DatabaseStorage(Storage)` class later without changing API consumers

---

## API Design Philosophy

### REST Conventions

- **Test Cases**: `/api/test-cases` (CRUD operations)
- **Evaluations**: `/api/evaluations` (create run, get status)
- **Results**: `/api/evaluations/{id}/results` (retrieve scores)
- **Graders**: `/api/graders` (list available, get definition)

### Explicit Response Format

All responses include explicit structure:
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

Error responses:
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Test case input required"
  }
}
```

**Rationale**: Clear success/failure semantics; explicit error reporting; no ambiguity

---

## Testing Strategy

### Unit Tests (Graders, Services)
- **String Match Grader**: Test all config variations
- **Storage**: CRUD operations for all entity types
- **Evaluation Service**: Logic for run initialization, result aggregation

### Integration Tests
- Full flow: Create test case → Execute → Grade → View results
- Error scenarios: Agent timeout, grader failure, invalid input
- Concurrent evaluation runs

### Contract Tests
- Each API endpoint tested independently
- Valid inputs → expected outputs
- Invalid inputs → appropriate error responses
- Response structure verification

---

## Conclusion

This research document provides the foundation for Phase 1 (data model, API contracts, quickstart) with all architectural decisions justified and explicitly documented. The design prioritizes:

1. **Simplicity**: In-memory storage, minimal dependencies, clear abstractions
2. **Clarity**: Explicit APIs, pluggable graders, clear error messages
3. **Correctness**: Deterministic grading, per-result error handling
4. **Testability**: Contract testing, isolated components, repeatable results
5. **Constitution Alignment**: All seven principles supported by design

Ready for Phase 1 detailed design.
