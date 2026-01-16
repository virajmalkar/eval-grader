# Quickstart: Agent Evaluation as a Service

**Date**: 2026-01-15  
**Purpose**: Get up and running with the agent evaluation system in 5 minutes

---

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- git
- A text editor or IDE
- A shell/terminal

---

## 1. Clone and Setup (2 minutes)

### Clone the repository
```bash
cd /path/to/agent-evaluator
git checkout 001-agent-eval-service
```

### Setup backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Setup frontend
```bash
cd ../frontend
npm install
```

---

## 2. Start the Application (1 minute)

### Terminal 1: Start backend server
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Terminal 2: Start frontend dev server
```bash
cd frontend
npm run dev
```

Expected output:
```
> dev
> vite

  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

### Open browser
Navigate to `http://localhost:5173` - you should see the Agent Evaluator UI

---

## 3. Create Your First Test Case (1 minute)

1. Click **"Create Test Case"** button
2. Fill in the form:
   - **Input**: "What is the capital of France?"
   - **Expected Output**: "Paris"
   - **Description**: "Basic geography test"
   - **Tags**: geography, basic
3. Click **"Save"**
4. Create a second test case:
   - **Input**: "What is 2 + 2?"
   - **Expected Output**: "4"
   - **Description**: "Basic math"
   - **Tags**: math, basic

You should now see 2 test cases in the list.

---

## 4. Run an Evaluation (1 minute)

### Option A: Using a Mock Agent (Recommended for Demo)

1. Click **"New Evaluation Run"**
2. Configure:
   - **Select Test Cases**: Check both test cases
   - **Agent Endpoint**: `http://localhost:8001/evaluate`
   - **Graders**: Select "String Match"
3. Click **"Run Evaluation"**
4. In another terminal, start the mock agent:
   ```bash
   cd /path/to/agent-evaluator
   python mock-agent-server.py
   ```
5. Watch the evaluation progress in real-time

### Option B: Using a Real Agent

If you have an actual agent endpoint available:

1. Click **"New Evaluation Run"**
2. Enter your agent endpoint URL (e.g., `https://api.yourcompany.com/agent/evaluate`)
3. Select test cases and graders
4. Click **"Run Evaluation"**

---

## 5. View Results

Once evaluation completes:

1. **Results Dashboard**: Shows pass rate and aggregate statistics
2. **Results Table**: Each row is one test case result with:
   - Input text
   - Expected output
   - Agent's actual response
   - Score from each grader
3. **Detail View**: Click a row to see detailed side-by-side comparison

---

## API Usage Examples

### Create a Test Case (curl)
```bash
curl -X POST http://localhost:8000/api/test-cases \
  -H "Content-Type: application/json" \
  -d '{
    "input": "What is the capital of France?",
    "expected_output": "Paris",
    "description": "Geography test",
    "tags": ["geography"]
  }'
```

### List Test Cases
```bash
curl http://localhost:8000/api/test-cases
```

### Create Evaluation Run
```bash
curl -X POST http://localhost:8000/api/evaluations \
  -H "Content-Type: application/json" \
  -d '{
    "test_case_ids": ["<test_case_id_1>", "<test_case_id_2>"],
    "agent_endpoint_url": "http://localhost:8001/evaluate",
    "grader_ids": ["string-match"]
  }'
```

### Get Evaluation Results
```bash
curl http://localhost:8000/api/evaluations/<run_id>/results
```

### List Available Graders
```bash
curl http://localhost:8000/api/graders
```

---

## Project Structure

```
backend/
├── src/
│   ├── models/          # Data structures (TestCase, EvaluationRun, etc.)
│   ├── services/        # Business logic (CRUD, evaluation orchestration)
│   ├── graders/         # Grading implementations
│   ├── api/             # HTTP endpoints
│   └── config.py        # Configuration
├── tests/
│   ├── contract/        # API contract tests
│   ├── integration/     # End-to-end flow tests
│   └── unit/            # Unit tests
└── main.py             # Application entry point

frontend/
├── src/
│   ├── components/      # React components (forms, tables, etc.)
│   ├── pages/           # Page layouts
│   ├── services/        # API client
│   └── styles/          # CSS
├── index.html           # Entry point
└── vite.config.js       # Build configuration
```

---

## Testing

### Backend Tests
```bash
cd backend
pytest                           # Run all tests
pytest tests/contract/          # Run contract tests only
pytest tests/integration/       # Run integration tests
pytest -v                       # Verbose output
pytest --cov=src                # Coverage report
```

### Frontend Tests
```bash
cd frontend
npm run test                    # Run all tests
npm run test -- --coverage      # Coverage report
```

---

## Configuration

### Backend Environment Variables

Create `backend/.env`:
```
AGENT_TIMEOUT_SECONDS=30
API_PORT=8000
LOG_LEVEL=INFO
```

### Frontend Configuration

Create `frontend/.env`:
```
VITE_API_URL=http://localhost:8000
VITE_ENV=development
```

---

## Troubleshooting

### Backend won't start
```
ERROR: Address already in use
```
**Solution**: Backend already running or port 8000 in use. Try:
```bash
lsof -i :8000              # Find what's using port 8000
kill -9 <PID>              # Kill the process
```

### Agent endpoint unreachable
```
Connection refused to http://localhost:8001/evaluate
```
**Solution**: Start the mock agent server in a separate terminal:
```bash
python mock-agent-server.py
```

### Frontend won't load
```
Could not connect to backend API
```
**Solution**: Verify backend is running (`http://localhost:8000` should work) and check `VITE_API_URL` is correct.

### Test cases not saving
**Solution**: In-memory storage is session-specific. Server restart clears data. Export results first if needed.

---

## Next Steps

1. **Explore the UI**: Create more test cases, run evaluations, review results
2. **Test the API**: Use curl or Postman to interact with endpoints directly
3. **Read the specifications**:
   - [Feature Specification](./spec.md) - User stories and requirements
   - [Data Model](./data-model.md) - Entity definitions and relationships
   - [API Contracts](./contracts/) - Detailed endpoint specifications
4. **Review the code**: Start with `backend/main.py` and `frontend/src/pages/App.jsx`
5. **Add custom graders** (future): See architecture in [research.md](./research.md)

---

## File Locations

| What | Where |
|------|-------|
| Specifications | `specs/001-agent-eval-service/` |
| Backend source | `backend/src/` |
| Backend tests | `backend/tests/` |
| Frontend source | `frontend/src/` |
| Frontend tests | `frontend/tests/` |
| API contracts | `specs/001-agent-eval-service/contracts/` |
| Data model | `specs/001-agent-eval-service/data-model.md` |

---

## Getting Help

- **API Documentation**: Generated at `http://localhost:8000/docs` (FastAPI Swagger UI)
- **Test Contracts**: See `specs/001-agent-eval-service/contracts/`
- **Feature Spec**: See `specs/001-agent-eval-service/spec.md`
- **Code Comments**: Check inline comments in source files

---

## Demo Workflow

**Complete end-to-end demo (5 minutes)**:

1. Start servers (backend + frontend)
2. Create 3 test cases:
   - Geography: "What is the capital of France?" → "Paris"
   - Math: "What is 2+2?" → "4"
   - Spelling: "Spell 'hello'" → "h-e-l-l-o"
3. Create evaluation run with all 3 test cases
4. Start mock agent in separate terminal
5. Watch evaluation progress
6. View results dashboard
7. Click into one result to see detail view
8. Download/export results as JSON

This demonstrates all four core features:
✅ Define test cases  
✅ Run evaluations  
✅ Score responses  
✅ View results in web UI
