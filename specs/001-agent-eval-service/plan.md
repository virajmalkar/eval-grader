# Implementation Plan: Agent Evaluation as a Service

**Branch**: `001-agent-eval-service` | **Date**: 2026-01-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-agent-eval-service/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a lightweight web-based agent evaluation system where users can define test cases, run them against external agent endpoints, score responses using pluggable grading logic (starting with string-match), and view results through a single-page web UI. The system prioritizes simplicity and clarity through a minimal backend API, in-memory persistence, and explicit separation between test case management, execution, grading, and result visualization. No authentication layer in the initial build.

## Technical Context

**Language/Version**: Python 3.11 (backend), JavaScript ES2022 (frontend)  
**Primary Dependencies**: FastAPI (backend API), Vite + React (frontend), httpx (HTTP client for agent calls)  
**Storage**: In-memory dictionaries/maps (all data structures held in process memory; no database)  
**Testing**: pytest (backend unit/integration), Vitest + React Testing Library (frontend)  
**Target Platform**: Local development machine; single-process server accessible from browser  
**Project Type**: Web application (backend + frontend separation)  
**Performance Goals**: Sub-second API responses (< 500ms p95), concurrent evaluation runs supported, web UI interactive response (< 3s page load)  
**Constraints**: Single-process server (no horizontal scaling); in-memory storage means data loss on restart; agent timeouts of 30 seconds per request; no authentication/authorization  
**Scale/Scope**: MVP for ~10 concurrent users, support 100-1000 test cases per session, multiple concurrent evaluation runs

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Simplicity & Clarity First
✅ **PASS**: Backend exposes clear, simple REST endpoints with explicit purpose. Frontend uses standard Vite SPA patterns. In-memory storage eliminates complexity of database integration. No authentication layers. Clear separation between models, services, and API routes.

### II. Explicit Over Implicit
✅ **PASS**: All API contracts explicitly specify inputs/outputs. No magic configuration files (minimal config via environment variables only for agent timeout and ports). Grader interface is explicit - each grader implements clear contract. Error responses are explicit with status codes and messages.

### III. Minimal Dependencies
✅ **PASS**: FastAPI is lightweight and focused. Vite is minimal build tool (not full framework). In-memory storage means zero database dependencies. Only three primary dependencies listed. Standard library used extensively. httpx for HTTP client instead of requests (smaller footprint).

### IV. Deterministic Behavior
✅ **PASS**: All grading logic deterministic given same input. String-match grader is 100% deterministic. Evaluation results always same for same inputs (no randomization). Exception: agent endpoint responses not under our control, but we store them exactly as received.

### V. Separation of Concerns
✅ **PASS**: Clear layers: Models (data structure), Services (business logic), API (HTTP interface), Graders (pluggable scoring). Frontend components separated by feature (TestCaseManager, EvaluationRunner, ResultsViewer). No global state except in-memory storage module. Each layer has single responsibility.

### VI. Correctness & Testability
✅ **PASS**: Contract tests for each API endpoint. Integration tests for end-to-end flows (define → execute → grade → view). Unit tests for graders and services. All tests deterministic. In-memory storage makes tests fully deterministic. >85% coverage goal for critical paths.

### VII. Scalability Through Design
✅ **PASS**: While current MVP doesn't scale horizontally (in-memory), architecture allows switching to persistent storage later without changing business logic. Clear API contracts mean clients/backends can scale independently. Stateless API design (all state in storage abstraction). No premature optimization.

**Overall**: ✅ **GATE PASSED** - No violations. Architecture aligns with all seven principles.

## Project Structure

### Documentation (this feature)

```text
specs/001-agent-eval-service/
├── spec.md              # Feature specification (complete)
├── plan.md              # This file - implementation plan
├── research.md          # Phase 0 output - design research and decisions
├── data-model.md        # Phase 1 output - entity definitions and relationships
├── quickstart.md        # Phase 1 output - setup and basic usage
├── contracts/           # Phase 1 output - API contract specifications
│   ├── test-cases.md
│   ├── evaluations.md
│   ├── graders.md
│   └── results.md
└── checklists/
    └── requirements.md  # Spec quality validation
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/              # Data structures
│   │   ├── test_case.py
│   │   ├── evaluation.py
│   │   ├── grader.py
│   │   └── result.py
│   ├── services/            # Business logic
│   │   ├── test_case_service.py
│   │   ├── evaluation_service.py
│   │   ├── grader_service.py
│   │   └── storage.py
│   ├── graders/             # Pluggable grading implementations
│   │   ├── base.py
│   │   └── string_match.py
│   ├── api/                 # HTTP endpoints
│   │   ├── main.py
│   │   ├── test_cases.py
│   │   ├── evaluations.py
│   │   ├── graders.py
│   │   └── results.py
│   └── config.py            # Configuration (environment variables)
├── tests/
│   ├── contract/            # API contract tests
│   ├── integration/         # End-to-end flow tests
│   └── unit/                # Unit tests for services/graders
├── requirements.txt         # Python dependencies
└── main.py                  # Entry point

frontend/
├── src/
│   ├── components/
│   │   ├── TestCaseForm.jsx
│   │   ├── TestCaseList.jsx
│   │   ├── EvaluationRunner.jsx
│   │   ├── ResultsViewer.jsx
│   │   └── ResultsTable.jsx
│   ├── pages/
│   │   └── App.jsx
│   ├── services/
│   │   └── api.js           # HTTP client for backend
│   ├── styles/
│   │   └── App.css
│   └── main.jsx
├── index.html
├── vite.config.js
├── package.json
└── tests/
    └── vitest.config.js

README.md                       # Project documentation
.gitignore
```

**Structure Decision**: Web application with separate backend (Python/FastAPI) and frontend (JavaScript/Vite/React). This allows independent development, testing, and deployment of UI and API. Backend is stateless with in-memory storage abstraction (no external services). Frontend is single-page app accessing backend via REST API.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
