# Agent Evaluation Service

A comprehensive platform for evaluating AI agent responses against predefined test cases with extensible grading capabilities.

## Features

✅ **Test Case Management**: Create, read, update, and delete test cases with tags and descriptions
✅ **Async Evaluation Execution**: Run evaluations asynchronously against external agent endpoints
✅ **Pluggable Graders**: Extensible grading system with string-match MVP and per-result error isolation
✅ **Results Analysis**: Filter, analyze, and export evaluation results in JSON/CSV formats
✅ **Real-time Status**: Live feedback on evaluation progress with latency tracking
✅ **REST API**: Comprehensive API with contract-first design and Pydantic validation
✅ **Responsive UI**: React + Vite frontend with intuitive workflow

## Quick Start

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

Backend: http://localhost:8000

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

### Mock Agent (for testing)

```bash
cd backend
python mock_agent_server.py
```

Mock Agent: http://localhost:9000

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React/Vite)                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  TestCaseManager  │  EvaluationRunner  │  ResultsViewer  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP (JSON)
┌──────────────────────────┴──────────────────────────────────┐
│              Backend (FastAPI, Python)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Routes                                           │  │
│  │  ├── /api/test-cases (CRUD)                           │  │
│  │  ├── /api/evaluations (Create, Status, Results)      │  │
│  │  └── /api/graders (List, Get)                         │  │
│  └────────────────────┬─────────────────────────────────┘  │
│  ┌────────────────────┴─────────────────────────────────┐  │
│  │  Service Layer (Business Logic)                       │  │
│  │  ├── TestCaseService                                  │  │
│  │  ├── EvaluationService                                │  │
│  │  ├── GradingService (per-result isolation)           │  │
│  │  ├── AgentClient (async HTTP)                         │  │
│  │  ├── GraderService (factory pattern)                  │  │
│  │  └── StorageService (abstraction layer)               │  │
│  └────────────────────┬─────────────────────────────────┘  │
│  ┌────────────────────┴─────────────────────────────────┐  │
│  │  Models & Storage                                     │  │
│  │  ├── TestCase, EvaluationRun, EvaluationResult       │  │
│  │  ├── Grader, Score                                    │  │
│  │  └── InMemoryStorage (extensible to DB)               │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
         │                              │
         │ HTTP Calls                   │
         ▼                              ▼
    ┌─────────────┐               ┌──────────────┐
    │   External  │               │  StringMatch │
    │ Agent API   │               │   Grader     │
    └─────────────┘               └──────────────┘
```

## API Endpoints

### Test Cases
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/test-cases` | Create test case |
| GET | `/api/test-cases/{id}` | Get test case |
| GET | `/api/test-cases` | List test cases (paginated) |
| PUT | `/api/test-cases/{id}` | Update test case |
| DELETE | `/api/test-cases/{id}` | Delete test case |

### Evaluations
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/evaluations` | Create and start evaluation |
| GET | `/api/evaluations/{id}` | Get evaluation status |
| GET | `/api/evaluations` | List evaluations (paginated) |
| GET | `/api/evaluations/{id}/results` | Get results with scores |

### Graders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/graders` | List graders |
| GET | `/api/graders/{id}` | Get grader details |

## Data Models

### TestCase
```json
{
  "id": "uuid",
  "input": "string",
  "expected_output": "string",
  "description": "string",
  "tags": ["string"],
  "created_at": "ISO 8601 datetime",
  "modified_at": "ISO 8601 datetime"
}
```

### EvaluationRun
```json
{
  "id": "uuid",
  "test_case_ids": ["uuid"],
  "agent_endpoint_url": "string",
  "grader_ids": ["string"],
  "status": "pending|running|completed|failed",
  "result_count": "integer",
  "created_at": "ISO 8601 datetime",
  "modified_at": "ISO 8601 datetime"
}
```

### EvaluationResult
```json
{
  "id": "uuid",
  "run_id": "uuid",
  "test_case_id": "uuid",
  "agent_response": "string",
  "response_status": "success|error|timeout",
  "response_latency_ms": "integer",
  "error_message": "string|null",
  "scores": [
    {
      "id": "uuid",
      "result_id": "uuid",
      "grader_id": "string",
      "passed": "boolean",
      "score": "float (0-1)",
      "details": {"string": "any"}
    }
  ]
}
```

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run contract tests only
pytest tests/contract/

# Run integration tests only
pytest tests/integration/

# Run unit tests only
pytest tests/unit/
```

### Frontend Tests

```bash
cd frontend

# Run all tests
npm run test

# Run in watch mode
npm test -- --watch

# Run with coverage
npm test -- --coverage
```

## Development Workflow

1. **Create Test Cases**: Define what the agent should do
2. **Configure Agent**: Set agent endpoint URL
3. **Run Evaluation**: Execute test cases against agent
4. **Review Results**: Check scores, pass/fail rates, latencies
5. **Export Data**: Download results as JSON or CSV for analysis

## Graders

### String Match Grader
Performs case-insensitive string comparison with optional whitespace normalization.

**Config:**
```json
{
  "case_insensitive": true,
  "normalize_whitespace": false
}
```

### Adding Custom Graders

1. Create a new class extending `GraderInterface`:

```python
from src.graders.base import GraderInterface

class CustomGrader(GraderInterface):
    def grade(self, expected: str, actual: str, config: dict) -> dict:
        # Your grading logic
        return {
            "passed": expected == actual,
            "score": 1.0 if expected == actual else 0.0,
            "details": {}
        }
    
    def validate_config(self, config: dict) -> bool:
        return True
```

2. Register in `GraderService`:

```python
AVAILABLE_GRADERS = {
    "custom": CustomGrader(),
}
```

## Configuration

Backend configuration via environment variables:

```bash
BACKEND_HOST=localhost           # Server host
BACKEND_PORT=8000               # Server port
AGENT_TIMEOUT_SECONDS=30        # Agent call timeout
GRADER_TIMEOUT_SECONDS=5        # Grader timeout
TESTING=False                   # Enable testing mode
```

## Project Structure

```
agent-evaluator/
├── backend/
│   ├── src/
│   │   ├── api/          # HTTP endpoints
│   │   ├── graders/      # Grading implementations
│   │   ├── models/       # Data models
│   │   └── services/     # Business logic
│   ├── tests/
│   │   ├── contract/     # API contract tests
│   │   ├── integration/  # E2E workflow tests
│   │   └── unit/         # Unit tests
│   ├── main.py          # FastAPI app entry point
│   ├── mock_agent_server.py  # Mock agent for testing
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page layouts
│   │   ├── services/     # API client
│   │   └── styles/       # CSS
│   ├── tests/            # Component tests
│   ├── vite.config.js
│   └── package.json
└── README.md
```

## Performance

- **Agent Call Timeout**: 30 seconds
- **Grader Timeout**: 5 seconds per grader
- **Per-Result Error Isolation**: Individual grader failures don't cascade
- **Async Execution**: Evaluations run in background, API returns immediately

## Error Handling

- Global error handler with consistent response format
- Per-result error isolation (grader failures logged but don't fail entire run)
- Timeout handling for both agent calls and grader execution
- Validation errors with detailed messages

## Deployment

See [Backend README](./backend/README.md) and [Frontend README](./frontend/README.md) for deployment instructions.

Docker support coming in Phase 7 (Polish).

## License

See LICENSE file for details.

## Support

For issues, questions, or contributions, please refer to the project documentation or create an issue.

