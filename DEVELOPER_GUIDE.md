# Developer Quick Reference

## Project Overview
Agent Evaluation Service - MVP for evaluating AI agent responses against test cases with extensible grading.

## Technology Stack
- **Backend**: Python 3.11, FastAPI 0.104.1, httpx (async HTTP)
- **Frontend**: React 18.2.0, Vite 5.0.8, JavaScript ES2022
- **Testing**: pytest (backend), Vitest (frontend)
- **Storage**: In-memory (migration-ready to database)

## Quick Commands

### Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload              # Start server (localhost:8000)
pytest                                  # Run all tests
pytest --cov=src                        # Run with coverage
python mock_agent_server.py             # Start mock agent (localhost:9000)
black src/ tests/ && flake8 src/ tests/ # Format & lint
```

### Frontend
```bash
cd frontend
npm install
npm run dev                   # Start dev server (localhost:5173)
npm run build                 # Build for production
npm test                      # Run tests
npm run test:coverage         # Run tests with coverage
npm run lint                  # Run ESLint
npm run format                # Run Prettier
```

## Directory Structure

```
backend/
├── src/
│   ├── api/           # HTTP endpoints
│   │   ├── test_cases.py
│   │   ├── evaluations.py
│   │   ├── graders.py
│   │   ├── schemas.py
│   │   └── utils.py
│   ├── models/        # Data models
│   │   ├── test_case.py
│   │   ├── evaluation.py
│   │   ├── grader.py
│   │   └── score.py
│   ├── services/      # Business logic
│   │   ├── test_case_service.py
│   │   ├── evaluation_service.py
│   │   ├── grading_service.py
│   │   ├── agent_client.py
│   │   ├── grader_service.py
│   │   ├── storage_service.py
│   │   └── storage.py
│   ├── graders/       # Grading implementations
│   │   ├── base.py
│   │   └── string_match.py
│   └── config.py      # Configuration
├── tests/
│   ├── contract/      # API contract tests (5 files, 20 tests)
│   ├── integration/   # E2E workflow tests
│   ├── unit/          # Unit tests
│   └── conftest.py    # pytest fixtures
├── main.py            # FastAPI app entry point
└── mock_agent_server.py

frontend/
├── src/
│   ├── components/    # React components
│   │   ├── TestCaseForm.jsx
│   │   ├── TestCaseList.jsx
│   │   ├── EvaluationRunner.jsx
│   │   ├── ResultsViewer.jsx
│   │   └── GraderSelector.jsx
│   ├── pages/         # Page layouts
│   │   ├── App.jsx
│   │   └── TestCaseManager.jsx
│   ├── services/      # API client
│   │   └── api.js
│   ├── styles/        # CSS
│   │   └── App.css
│   └── main.jsx       # React entry point
├── tests/             # Component tests
│   ├── components/
│   └── ...
└── vite.config.js
```

## Key APIs

### Test Case API
```bash
POST /api/test-cases              # Create
GET /api/test-cases/{id}          # Get
GET /api/test-cases               # List (skip, limit)
PUT /api/test-cases/{id}          # Update
DELETE /api/test-cases/{id}       # Delete
```

### Evaluation API
```bash
POST /api/evaluations             # Create and start
GET /api/evaluations/{id}         # Get status
GET /api/evaluations              # List (skip, limit)
GET /api/evaluations/{id}/results # Get results with scores
```

### Grader API
```bash
GET /api/graders                  # List graders
GET /api/graders/{id}             # Get grader details
```

## Component Hierarchy

```
App.jsx
├── TestCaseManager
│   ├── TestCaseForm
│   └── TestCaseList
├── EvaluationRunner
│   └── GraderSelector
└── ResultsViewer
    └── (Results table with filtering & export)
```

## Data Flow

```
1. Create Test Cases
   └─> TestCaseForm → POST /api/test-cases → TestCaseList

2. Run Evaluation
   └─> EvaluationRunner → POST /api/evaluations → Poll GET /api/evaluations/{id}

3. Grade Results
   └─> Evaluation Service → GradingService → Per-result isolation

4. View Results
   └─> ResultsViewer → GET /api/evaluations/{id}/results → Display table

5. Export
   └─> JSON/CSV export (client-side)
```

## Common Tasks

### Add a New Endpoint
1. Create schema in `backend/src/api/schemas.py`
2. Create route in `backend/src/api/{resource}.py`
3. Add service method in `backend/src/services/{service}.py`
4. Write contract test in `backend/tests/contract/`

### Add a New Component
1. Create component in `frontend/src/components/{Component}.jsx`
2. Add API calls to `frontend/src/services/api.js` if needed
3. Write component test in `frontend/tests/components/{Component}.test.jsx`
4. Add styling to `frontend/src/styles/App.css`

### Add a New Grader
1. Create class extending `GraderInterface` in `backend/src/graders/`
2. Implement `grade()` and `validate_config()` methods
3. Register in `GraderService.AVAILABLE_GRADERS`
4. Add tests

### Run Tests
```bash
# Backend
pytest                           # All tests
pytest tests/contract/           # Contract tests only
pytest tests/integration/        # Integration tests only
pytest -k test_name              # Specific test
pytest --cov=src --cov-report=html

# Frontend
npm test                         # All tests
npm test -- --watch             # Watch mode
npm test -- --coverage          # Coverage report
```

## Configuration

### Backend (.env)
```
BACKEND_HOST=localhost
BACKEND_PORT=8000
AGENT_TIMEOUT_SECONDS=30
GRADER_TIMEOUT_SECONDS=5
TESTING=False
```

### Frontend (vite.config.js)
- Dev server: localhost:5173
- Proxy: /api → localhost:8000
- Build output: dist/

## Response Format

All API responses follow the pattern:
```json
{
  "status": "success|error",
  "message": "Human readable message",
  "data": {...}
}
```

## Error Codes
- 200: Success
- 201: Created
- 400: Bad request (validation)
- 404: Not found
- 500: Server error

## Performance Tuning

- Agent timeout: 30 seconds (configurable)
- Grader timeout: 5 seconds (configurable)
- Results polling: 3 seconds (frontend)
- Results pagination: 50 items default (future)

## Debugging

### Backend
```python
# Add logging
import logging
logger = logging.getLogger(__name__)
logger.info("Debug message")

# Print to console during testing
print("Debug value:", variable)
```

### Frontend
```javascript
// Console logging
console.log('Debug value:', value);
console.error('Error:', error);

// React DevTools
// Install React DevTools browser extension
```

## Dependencies

### Backend Key Packages
- `fastapi` - Web framework
- `httpx` - Async HTTP client
- `pydantic` - Data validation
- `pytest` - Testing framework
- `black` - Code formatter

### Frontend Key Packages
- `react` - UI library
- `vite` - Build tool
- `vitest` - Testing framework
- `@testing-library/react` - Component testing

## Documentation Files
- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)
- [Root README](./README.md)
- [Phase 6 Summary](./PHASE6_SUMMARY.md)
- [Spec](./specs/001-agent-eval-service/spec.md)
- [Plan](./specs/001-agent-eval-service/plan.md)
- [Data Model](./specs/001-agent-eval-service/data-model.md)

## Quick Debug Checklist

- [ ] Are services running? (Backend on 8000, Frontend on 5173)
- [ ] Mock agent running? (localhost:9000 for testing)
- [ ] Environment variables set? (.env file)
- [ ] Dependencies installed? (pip/npm)
- [ ] Tests passing? (pytest/npm test)
- [ ] ESLint/Prettier happy? (npm run lint/format)
- [ ] Database clean? (in-memory storage resets on restart)

## Next Phase (Phase 7 - Polish)

Remaining work for production readiness:
- [ ] Add comprehensive logging
- [ ] Docker setup (Dockerfile, docker-compose)
- [ ] CI/CD workflows (.github/workflows/)
- [ ] Additional documentation
- [ ] Performance optimization
- [ ] Security hardening
- [ ] Deployment guide
