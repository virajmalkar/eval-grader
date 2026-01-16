# Data Model: Agent Evaluation as a Service

**Date**: 2026-01-15  
**Feature**: [001-agent-eval-service](./spec.md)  
**Purpose**: Define all data entities, relationships, and validation rules

---

## Entity Definitions

### Entity 1: TestCase

**Purpose**: Represents a single evaluation scenario with input and expected output

**Attributes**:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-----------|-------------|
| `id` | string (UUID) | Yes | Auto-generated, unique | Unique identifier; generated on creation |
| `input` | string | Yes | 1-10,000 chars | The text sent to the agent |
| `expected_output` | string | Yes | 1-10,000 chars | The correct/desired response |
| `description` | string | No | 0-500 chars | Human-readable explanation of this test case |
| `tags` | string[] | No | 0-10 tags max | Labels for organizing test cases (e.g., "critical", "edge-case") |
| `created_at` | datetime (ISO 8601) | Yes | Auto-generated | Timestamp when created |
| `modified_at` | datetime (ISO 8601) | Yes | Auto-updated | Timestamp of last modification |

**Validation Rules**:
- Input and expected_output MUST NOT be empty strings
- Input length MUST be between 1-10,000 characters (inclusive)
- Expected_output length MUST be between 1-10,000 characters (inclusive)
- Description length MUST NOT exceed 500 characters
- Each tag MUST be 1-50 characters alphanumeric + hyphen/underscore
- Modified_at MUST always be >= created_at

**State Transitions**:
- **Created**: New test case with initial values
- **Modified**: Fields updated; modified_at updated
- **Deleted**: Marked for deletion; persists in storage but not returned in listings

**Example**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "input": "What is the capital of France?",
  "expected_output": "Paris",
  "description": "Basic geography question",
  "tags": ["geography", "basic"],
  "created_at": "2026-01-15T10:30:00Z",
  "modified_at": "2026-01-15T10:30:00Z"
}
```

---

### Entity 2: EvaluationRun

**Purpose**: Represents a single execution of test cases against an agent endpoint

**Attributes**:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-----------|-------------|
| `id` | string (UUID) | Yes | Auto-generated, unique | Unique identifier for this run |
| `test_case_ids` | string[] | Yes | 1+ test cases | Array of TestCase IDs to evaluate |
| `agent_endpoint_url` | string (URL) | Yes | Valid HTTP(S) URL | URL where agent is deployed |
| `grader_ids` | string[] | Yes | 1+ graders | Array of Grader IDs to apply |
| `status` | enum | Yes | pending/running/completed/failed | Current execution status |
| `started_at` | datetime | No | Auto-set on start | When execution began |
| `completed_at` | datetime | No | Auto-set on completion | When execution ended |
| `result_count` | int | Yes | >= 0 | Number of results (count of test_case_ids × grader_ids scores) |
| `error_message` | string | No | 0-500 chars | If status=failed, details of failure |

**Validation Rules**:
- Test_case_ids MUST contain at least 1 ID
- Agent_endpoint_url MUST be valid HTTP or HTTPS URL
- Grader_ids MUST contain at least 1 ID
- Status MUST be one of: pending, running, completed, failed
- Completed_at can only be set if status is completed or failed
- Error_message required if status is failed

**State Transitions**:
1. **pending**: Newly created, not yet started
2. **running**: Execution in progress
3. **completed**: All results collected and graded
4. **failed**: Execution halted due to error (e.g., agent unreachable)

**Example**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440002",
  "test_case_ids": [
    "550e8400-e29b-41d4-a716-446655440001",
    "550e8400-e29b-41d4-a716-446655440003"
  ],
  "agent_endpoint_url": "https://api.agent.example.com/evaluate",
  "grader_ids": ["string-match"],
  "status": "completed",
  "started_at": "2026-01-15T10:35:00Z",
  "completed_at": "2026-01-15T10:35:15Z",
  "result_count": 2,
  "error_message": null
}
```

---

### Entity 3: EvaluationResult

**Purpose**: Represents the outcome of running a single test case in an evaluation run (stores agent response)

**Attributes**:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-----------|-------------|
| `id` | string (UUID) | Yes | Auto-generated, unique | Unique identifier for this result |
| `run_id` | string (UUID) | Yes | Foreign key to EvaluationRun | Which evaluation run this belongs to |
| `test_case_id` | string (UUID) | Yes | Foreign key to TestCase | Which test case this is for |
| `agent_response` | string | No | 0-10,000 chars | The actual response from the agent |
| `response_latency_ms` | int | No | >= 0 | Round-trip time to agent in milliseconds |
| `response_status` | enum | Yes | success/timeout/error | Was agent request successful? |
| `error_message` | string | No | 0-500 chars | If response_status=error, details |
| `created_at` | datetime | Yes | Auto-generated | When this result was recorded |

**Validation Rules**:
- Response_status MUST be one of: success, timeout, error
- Agent_response and response_latency_ms only set if response_status=success
- Error_message required if response_status is timeout or error
- Agent_response length MUST NOT exceed 10,000 characters
- Response_latency_ms MUST be non-negative

**State Transitions**:
- **success**: Agent returned response; grading can proceed
- **timeout**: Agent didn't respond within 30 seconds; no grading attempted
- **error**: Agent returned error; no grading attempted

**Example**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440004",
  "run_id": "550e8400-e29b-41d4-a716-446655440002",
  "test_case_id": "550e8400-e29b-41d4-a716-446655440001",
  "agent_response": "Paris",
  "response_latency_ms": 245,
  "response_status": "success",
  "error_message": null,
  "created_at": "2026-01-15T10:35:01Z"
}
```

---

### Entity 4: Grader

**Purpose**: Represents a scoring mechanism; reusable across multiple evaluation runs

**Attributes**:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-----------|-------------|
| `id` | string | Yes | Must be unique; human-readable | Identifier (e.g., "string-match", "fuzzy-match") |
| `name` | string | Yes | 1-100 chars | Display name (e.g., "String Match Grader") |
| `description` | string | No | 0-500 chars | What this grader does |
| `type` | enum | Yes | string-match / custom-json | Grader category |
| `config` | object (JSON) | Yes | Valid grader config | Configuration for this grader |
| `created_at` | datetime | Yes | Auto-generated | When grader was created |

**Validation Rules**:
- ID MUST be alphanumeric + hyphen/underscore only
- Name MUST be 1-100 characters
- Type MUST be: string-match or custom-json
- Config schema depends on type (see below)
- Each grader must be valid JSON

**Grader Type 1: String Match**

Config schema:
```json
{
  "type": "string-match",
  "config": {
    "case_sensitive": boolean,     // default: false
    "normalize_whitespace": boolean // default: true
  }
}
```

Scoring:
- **Pass** (1.0): Actual response matches expected output (per config options)
- **Fail** (0.0): No match

**Grader Type 2: Custom JSON (Future)**

Config schema:
```json
{
  "type": "custom-json",
  "config": {
    "rules": [
      { "condition": "contains", "value": "keyword" },
      { "condition": "length_min", "value": 10 }
    ]
  }
}
```

**Built-in Graders** (pre-loaded at startup):

| ID | Name | Type | Purpose |
|---|---|------|---------|
| `string-match` | String Match | string-match | Exact/fuzzy text matching (MVP grader) |

**Example**:
```json
{
  "id": "string-match",
  "name": "String Match Grader",
  "description": "Exact or fuzzy string matching with case and whitespace options",
  "type": "string-match",
  "config": {
    "case_sensitive": false,
    "normalize_whitespace": true
  },
  "created_at": "2026-01-15T00:00:00Z"
}
```

---

### Entity 5: Score

**Purpose**: Represents the result of applying one grader to one evaluation result

**Attributes**:

| Field | Type | Required | Constraints | Description |
|-------|------|----------|-----------|-------------|
| `id` | string (UUID) | Yes | Auto-generated, unique | Unique identifier for this score |
| `result_id` | string (UUID) | Yes | Foreign key to EvaluationResult | Which result this score is for |
| `grader_id` | string | Yes | Foreign key to Grader | Which grader produced this score |
| `score_value` | float | No | 0.0 - 1.0 | Numeric score (0=fail, 1=pass); null if error |
| `score_status` | enum | Yes | pass/fail/error | Categorical result |
| `error_message` | string | No | 0-500 chars | If score_status=error, details |
| `created_at` | datetime | Yes | Auto-generated | When score was calculated |

**Validation Rules**:
- Score_value MUST be between 0.0 and 1.0 (inclusive) OR null
- Score_status MUST be one of: pass, fail, error
- If score_status is error, score_value MUST be null
- Error_message required if score_status is error
- Score_value should be set if score_status is not error

**Scoring Status**:
- **pass**: score_value >= 0.5 (grading succeeded)
- **fail**: 0.0 <= score_value < 0.5 (grading succeeded, scored as fail)
- **error**: score_value null (grading failed, e.g., timeout, exception)

**Example (Pass)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440005",
  "result_id": "550e8400-e29b-41d4-a716-446655440004",
  "grader_id": "string-match",
  "score_value": 1.0,
  "score_status": "pass",
  "error_message": null,
  "created_at": "2026-01-15T10:35:02Z"
}
```

**Example (Error)**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440006",
  "result_id": "550e8400-e29b-41d4-a716-446655440007",
  "grader_id": "custom-grader-1",
  "score_value": null,
  "score_status": "error",
  "error_message": "Grader timed out after 5 seconds",
  "created_at": "2026-01-15T10:35:03Z"
}
```

---

## Relationships

### ER Diagram (Text Format)

```
TestCase (1) --< (N) EvaluationResult
  |
  +-- Results reference test cases for expected output comparison

EvaluationRun (1) --< (N) EvaluationResult
  |
  +-- Results belong to exactly one run
  +-- Run tracks which test cases and graders were used

EvaluationResult (1) --< (N) Score
  |
  +-- One result has multiple scores (one per grader)

Grader (1) --< (N) Score
  |
  +-- Each grader can score multiple results
  +-- Graders are reusable across runs
```

### Relationship Rules

**TestCase ↔ EvaluationResult**:
- Relationship: TestCase (1) → (N) EvaluationResult
- Constraint: EvaluationResult.test_case_id is foreign key to TestCase.id
- Cascade: Deleting TestCase may invalidate related results (soft delete recommended)
- Cardinality: One test case can be run multiple times in different runs

**EvaluationRun ↔ EvaluationResult**:
- Relationship: EvaluationRun (1) → (N) EvaluationResult
- Constraint: EvaluationResult.run_id references EvaluationRun.id
- Cascade: Deleting run should delete associated results
- Cardinality: Exactly one run per result

**EvaluationResult ↔ Score**:
- Relationship: EvaluationResult (1) → (N) Score
- Constraint: Score.result_id references EvaluationResult.id
- Cardinality: One result has exactly (count of graders applied) scores
- Cascade: Deleting result should delete associated scores

**Grader ↔ Score**:
- Relationship: Grader (1) → (N) Score
- Constraint: Score.grader_id references Grader.id
- Cardinality: One grader can score many results
- Reusability: Same grader used across multiple runs

---

## Data Constraints & Invariants

### Global Invariants (must always be true)

1. **Score Completeness**: For every combination of (EvaluationResult, Grader) in a run, exactly one Score MUST exist
2. **Result Integrity**: Every EvaluationResult MUST have a valid test_case_id and run_id
3. **Run Integrity**: Every EvaluationRun with status=completed MUST have result_count > 0
4. **Agent Response Consistency**: If response_status=success, agent_response MUST be non-null
5. **Error Consistency**: If response_status ≠ success, error_message MUST be non-null

### Temporal Invariants

1. **Timestamp Ordering**: created_at ≤ modified_at for all entities
2. **Run Timing**: started_at ≤ completed_at
3. **No Future Dates**: All timestamps MUST be ≤ current time

---

## Data Volume Expectations

**MVP Scale**:
- 100-1000 test cases per session
- 10-100 evaluation runs per session
- Concurrent runs: 1-5 simultaneous
- Graders: 1-3 available
- Expected memory: <100MB for typical session

**Storage Cleanup**:
- In-memory storage lost on server restart
- Session isolation: Each server start has fresh storage
- Manual data export via API (JSON/CSV) before restart if persistence needed

---

## Example: Full Evaluation Flow Data

**Scenario**: User creates 2 test cases, runs them both against an agent with 1 grader

**Data State After Completion**:

```
TestCase #1
├── id: tc-001
├── input: "What is 2+2?"
└── expected_output: "4"

TestCase #2
├── id: tc-002
├── input: "What is the color of grass?"
└── expected_output: "green"

EvaluationRun
├── id: run-001
├── test_case_ids: [tc-001, tc-002]
├── grader_ids: [string-match]
└── status: completed

EvaluationResult #1
├── id: result-001
├── run_id: run-001
├── test_case_id: tc-001
├── agent_response: "The answer is 4"
├── response_status: success
└── Score
    ├── grader_id: string-match
    ├── score_status: fail (response "The answer is 4" ≠ expected "4")
    └── score_value: 0.0

EvaluationResult #2
├── id: result-002
├── run_id: run-001
├── test_case_id: tc-002
├── agent_response: "green"
├── response_status: success
└── Score
    ├── grader_id: string-match
    ├── score_status: pass (response "green" = expected "green")
    └── score_value: 1.0
```

**Summary Metrics**:
- Total results: 2
- Successful responses: 2/2 (100%)
- Grader pass rate: 1/2 (50%)
- Failed grader reason: Response didn't match exactly (fuzzy matching could improve this)

---

## Implementation Notes

### UUID Generation
- Use Python `uuid.uuid4()` for auto-generation
- Store as string (UUID.hex format)
- Example: `550e8400e29b41d4a716446655440000`

### Datetime Handling
- Store as ISO 8601 format: `2026-01-15T10:30:00Z`
- Use UTC timezone always
- Python: `datetime.datetime.utcnow().isoformat() + 'Z'`

### JSON Serialization
- Use Pydantic models for validation
- Serialize all entities to JSON for API responses
- Deserialize from JSON on API input

---

## Future Extensibility

This data model supports future enhancements without breaking changes:

1. **Custom Graders**: Add new grader types; reuse Score/Grader entities
2. **Persistence**: Replace in-memory storage; data model unchanged
3. **User Accounts**: Add user_id field to TestCase/EvaluationRun (optional for MVP)
4. **Audit Trail**: Add created_by, modified_by to entities
5. **Batch Operations**: Support archiving old runs without deletion
6. **Metrics**: Pre-calculate aggregated metrics for reporting

