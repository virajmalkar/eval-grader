# Agent Evaluation Service - Backend

FastAPI-based backend for the Agent Evaluation Service.

## Setup

### Prerequisites
- Python 3.11+
- pip

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment template:
```bash
cp .env.example .env
```

### Running the Server

```bash
uvicorn main:app --reload
```

Server will be available at `http://localhost:8000`

API documentation available at `http://localhost:8000/docs`

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src

# Specific test file
pytest tests/unit/test_example.py

# Contract tests only
pytest tests/contract/
```

### Code Quality

```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/

# Type checking
mypy src/

# Sort imports
isort src/ tests/
```

## Project Structure

- `src/models/` - Data models
- `src/services/` - Business logic
- `src/api/` - HTTP endpoints
- `src/graders/` - Grading implementations
- `tests/contract/` - API contract tests
- `tests/integration/` - End-to-end tests
- `tests/unit/` - Unit tests

## Mock Agent Server

For development and testing, a mock agent server is included:

```bash
python mock_agent_server.py
```

Available at `http://localhost:9000/evaluate`

## API Endpoints

### Test Cases
- `POST /api/test-cases` - Create test case
- `GET /api/test-cases/{id}` - Get test case
- `GET /api/test-cases` - List test cases
- `PUT /api/test-cases/{id}` - Update test case
- `DELETE /api/test-cases/{id}` - Delete test case

### Evaluations
- `POST /api/evaluations` - Create and start evaluation
- `GET /api/evaluations/{id}` - Get evaluation status
- `GET /api/evaluations` - List evaluations
- `GET /api/evaluations/{id}/results` - Get evaluation results with scores

### Graders
- `GET /api/graders` - List available graders
- `GET /api/graders/{id}` - Get grader details

## Integration Tests

The project includes comprehensive integration tests that validate the complete workflow:

```bash
# Run integration tests only
pytest tests/integration/

# Run all tests
pytest
```

Integration tests cover:
- Complete evaluation workflow (create test cases → run evaluation → grade)
- Evaluation with graders
- Test case CRUD operations
- Grader endpoints
- Error handling

## Architecture

### Service Layer
- **TestCaseService**: CRUD operations for test cases
- **EvaluationService**: Orchestrates evaluation execution and integrates with grading
- **GradingService**: Applies graders to evaluation results with per-result isolation
- **AgentClient**: Async HTTP calls to external agent endpoints
- **GraderService**: Factory for grader instances
- **StorageService**: Abstracts storage implementation (in-memory, extensible to database)

### Graders
The grading system is extensible. Currently includes:
- **StringMatchGrader**: Case-insensitive string matching with optional whitespace normalization

New graders can be added by:
1. Creating a class that extends `GraderInterface`
2. Implementing the `grade()` method
3. Registering in `GraderService`

### Error Handling
- Per-result error isolation: Individual grader failures don't cascade
- Timeout handling: 30s for agent calls, 5s for graders
- Global error handler with consistent response format

