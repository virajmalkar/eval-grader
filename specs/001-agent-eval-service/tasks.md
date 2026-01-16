---
description: "Task list for Agent Evaluation as a Service MVP implementation"
---

# Tasks: Agent Evaluation as a Service

**Input**: Design documents from `/specs/001-agent-eval-service/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

**Tests**: Backend contract tests required for all API endpoints. Integration tests for end-to-end flows. Frontend component tests for key UI features.

**Organization**: Tasks organized by user story (4 P1 stories, all critical for MVP) to enable parallel implementation within each story.

## Format: `[ID] [P?] [Story] Description with file path`

- **[P]**: Can run in parallel (different files, no blocking dependencies)
- **[Story]**: Which user story (US1, US2, US3, US4)
- **File paths**: Explicit locations per plan.md structure (backend/src/, frontend/src/)

## Path Conventions

- **Backend**: `backend/src/models/`, `backend/src/services/`, `backend/src/api/`, `backend/src/graders/`
- **Frontend**: `frontend/src/components/`, `frontend/src/pages/`, `frontend/src/services/`
- **Tests**: `backend/tests/contract/`, `backend/tests/integration/`, `backend/tests/unit/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, dependencies, and basic application structure

**Estimated Duration**: 1-2 hours

- [ ] T001 Create backend project structure per plan.md in backend/ directory
- [ ] T002 Create frontend project structure per plan.md in frontend/ directory
- [ ] T003 [P] Initialize Python environment and install backend dependencies (FastAPI, httpx, pytest, pydantic) in backend/requirements.txt
- [ ] T004 [P] Initialize Node.js project and install frontend dependencies (Vite, React, Vitest, @testing-library/react) in frontend/package.json
- [ ] T005 [P] Configure Python linting and formatting (black, flake8, isort) in backend/
- [ ] T006 [P] Configure JavaScript linting and formatting (ESLint, Prettier) in frontend/
- [ ] T007 Create FastAPI application entry point with middleware and error handlers in backend/main.py
- [ ] T008 [P] Create Vite configuration for frontend dev server and build in frontend/vite.config.js
- [ ] T009 [P] Setup environment configuration system for both backend (.env, config.py) and frontend (vite.config.js)
- [ ] T010 [P] Configure backend testing framework (pytest, pytest-asyncio) in backend/tests/conftest.py
- [ ] T011 [P] Configure frontend testing framework (Vitest, React Testing Library) in frontend/vitest.config.js
- [ ] T012 Create basic README.md with setup instructions and project overview
- [ ] T013 Create mock agent server for testing (backend/mock-agent-server.py)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user story work begins

**⚠️ CRITICAL**: No user story implementation can begin until this phase is complete

**Estimated Duration**: 2-3 hours

- [ ] T014 Implement in-memory storage abstraction in backend/src/services/storage.py (Storage base class)
- [ ] T015 [P] Implement TestCase model with validation in backend/src/models/test_case.py
- [ ] T016 [P] Implement EvaluationRun model with validation in backend/src/models/evaluation.py
- [ ] T017 [P] Implement EvaluationResult model with validation in backend/src/models/result.py
- [ ] T018 [P] Implement Grader model with validation in backend/src/models/grader.py
- [ ] T019 [P] Implement Score model with validation in backend/src/models/score.py
- [ ] T020 Implement abstract Grader interface in backend/src/graders/base.py
- [ ] T021 [P] Implement String-Match grader in backend/src/graders/string_match.py
- [ ] T022 [P] Implement TestCaseService in backend/src/services/test_case_service.py (CRUD operations)
- [ ] T023 [P] Implement GraderService in backend/src/services/grader_service.py (list and get graders)
- [ ] T024 [P] Implement StorageService in backend/src/services/storage_service.py (factory pattern for swappable storage)
- [ ] T025 [P] Create HTTP client wrapper for agent calls in backend/src/services/agent_client.py
- [ ] T026 Setup basic error handling and response utilities in backend/src/api/utils.py
- [ ] T027 [P] Create Pydantic request/response schemas in backend/src/api/schemas.py
- [ ] T028 [P] Setup frontend API client in frontend/src/services/api.js

**Checkpoint**: Foundation complete - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Define and Manage Test Cases (Priority: P1) 🎯 MVP

**Goal**: Enable users to create, read, update, and delete test cases that define agent evaluation scenarios

**Independent Test**: CRUD operations on test cases via UI and API work correctly; test cases persist in storage

**Architecture**: REST CRUD endpoints map to TestCaseService; UI components map to React components

### Contract Tests for US1 (REQUIRED - run first)

- [ ] T029 [P] [US1] Contract test for POST /api/test-cases (create) in backend/tests/contract/test_test_cases_create.py
- [ ] T030 [P] [US1] Contract test for GET /api/test-cases/{id} (read) in backend/tests/contract/test_test_cases_read.py
- [ ] T031 [P] [US1] Contract test for GET /api/test-cases (list) in backend/tests/contract/test_test_cases_list.py
- [ ] T032 [P] [US1] Contract test for PUT /api/test-cases/{id} (update) in backend/tests/contract/test_test_cases_update.py
- [ ] T033 [P] [US1] Contract test for DELETE /api/test-cases/{id} (delete) in backend/tests/contract/test_test_cases_delete.py

### Backend Implementation for US1

- [ ] T034 [US1] Implement POST /api/test-cases endpoint in backend/src/api/test_cases.py
- [ ] T035 [US1] Implement GET /api/test-cases/{id} endpoint in backend/src/api/test_cases.py
- [ ] T036 [US1] Implement GET /api/test-cases (with pagination/filtering) endpoint in backend/src/api/test_cases.py
- [ ] T037 [US1] Implement PUT /api/test-cases/{id} endpoint in backend/src/api/test_cases.py
- [ ] T038 [US1] Implement DELETE /api/test-cases/{id} endpoint in backend/src/api/test_cases.py
- [ ] T039 [P] [US1] Add validation and error handling to TestCaseService in backend/src/services/test_case_service.py
- [ ] T040 [P] [US1] Add logging to test case operations in backend/src/services/test_case_service.py

### Frontend Implementation for US1

- [ ] T041 [P] [US1] Create TestCaseForm component for creating/editing test cases in frontend/src/components/TestCaseForm.jsx
- [ ] T042 [P] [US1] Create TestCaseList component for viewing test cases in frontend/src/components/TestCaseList.jsx
- [ ] T043 [P] [US1] Create TestCaseManager page component in frontend/src/pages/TestCaseManager.jsx
- [ ] T044 [US1] Implement API integration in TestCaseForm (POST and PUT) in frontend/src/components/TestCaseForm.jsx
- [ ] T045 [US1] Implement API integration in TestCaseList (GET list, GET detail) in frontend/src/components/TestCaseList.jsx
- [ ] T046 [US1] Implement delete functionality in TestCaseList component in frontend/src/components/TestCaseList.jsx
- [ ] T047 [P] [US1] Add form validation and error messages in frontend/src/components/TestCaseForm.jsx
- [ ] T048 [P] [US1] Add loading states and spinners to TestCaseList component in frontend/src/components/TestCaseList.jsx

### Integration Tests for US1

- [ ] T049 [US1] Integration test for complete test case lifecycle (create → read → update → delete) in backend/tests/integration/test_test_case_lifecycle.py
- [ ] T050 [P] [US1] Integration test for test case list pagination in backend/tests/integration/test_test_case_list_pagination.py

### Unit Tests for US1

- [ ] T051 [P] [US1] Unit tests for TestCaseService CRUD methods in backend/tests/unit/test_test_case_service.py
- [ ] T052 [P] [US1] Component tests for TestCaseForm in frontend/tests/TestCaseForm.test.jsx
- [ ] T053 [P] [US1] Component tests for TestCaseList in frontend/tests/TestCaseList.test.jsx

**Checkpoint**: User Story 1 complete - test case management fully functional, tested, and working end-to-end

---

## Phase 4: User Story 2 - Execute Evaluation Runs (Priority: P1)

**Goal**: Enable users to run test cases against external agent endpoints and collect responses

**Independent Test**: Can create evaluation run, send test inputs to agent endpoint, collect responses, and retrieve results

**Architecture**: EvaluationService orchestrates execution; agent_client handles HTTP calls; UI shows progress and results

### Contract Tests for US2 (REQUIRED - run first)

- [ ] T054 [P] [US2] Contract test for POST /api/evaluations (create run) in backend/tests/contract/test_evaluations_create.py
- [ ] T055 [P] [US2] Contract test for GET /api/evaluations/{id} (get status) in backend/tests/contract/test_evaluations_status.py
- [ ] T056 [P] [US2] Contract test for GET /api/evaluations (list runs) in backend/tests/contract/test_evaluations_list.py
- [ ] T057 [P] [US2] Contract test for GET /api/evaluations/{id}/results (get results) in backend/tests/contract/test_evaluations_results.py

### Backend Implementation for US2

- [ ] T058 [US2] Implement EvaluationService orchestration logic in backend/src/services/evaluation_service.py
- [ ] T059 [US2] Implement async execution loop for sending test inputs to agent in backend/src/services/evaluation_service.py
- [ ] T060 [P] [US2] Implement response collection and storage in backend/src/services/evaluation_service.py
- [ ] T061 [P] [US2] Implement agent timeout handling (30 second timeout, error capture) in backend/src/services/agent_client.py
- [ ] T062 [P] [US2] Implement agent error handling in backend/src/services/agent_client.py
- [ ] T063 [US2] Implement POST /api/evaluations endpoint in backend/src/api/evaluations.py
- [ ] T064 [US2] Implement GET /api/evaluations/{id} endpoint in backend/src/api/evaluations.py
- [ ] T065 [US2] Implement GET /api/evaluations (list with filtering) endpoint in backend/src/api/evaluations.py
- [ ] T066 [US2] Implement GET /api/evaluations/{id}/results endpoint (with summary stats) in backend/src/api/evaluations.py
- [ ] T067 [P] [US2] Add logging for evaluation run progress in backend/src/services/evaluation_service.py
- [ ] T068 [P] [US2] Add error handling and status tracking in backend/src/services/evaluation_service.py

### Frontend Implementation for US2

- [ ] T069 [P] [US2] Create EvaluationRunner component for configuring runs in frontend/src/components/EvaluationRunner.jsx
- [ ] T070 [P] [US2] Create EvaluationProgress component for showing run progress in frontend/src/components/EvaluationProgress.jsx
- [ ] T071 [US2] Implement API integration in EvaluationRunner (POST to create run) in frontend/src/components/EvaluationRunner.jsx
- [ ] T072 [US2] Implement polling logic for monitoring run status (GET /api/evaluations/{id}) in frontend/src/components/EvaluationProgress.jsx
- [ ] T073 [P] [US2] Add form validation for agent endpoint URL in frontend/src/components/EvaluationRunner.jsx
- [ ] T074 [P] [US2] Add UI feedback for errors during agent calls in frontend/src/components/EvaluationProgress.jsx
- [ ] T075 [P] [US2] Implement test case selector in EvaluationRunner component in frontend/src/components/EvaluationRunner.jsx

### Integration Tests for US2

- [ ] T076 [US2] Integration test for complete evaluation run with mock agent in backend/tests/integration/test_evaluation_run_complete.py
- [ ] T077 [P] [US2] Integration test for agent timeout handling in backend/tests/integration/test_evaluation_agent_timeout.py
- [ ] T078 [P] [US2] Integration test for agent error handling in backend/tests/integration/test_evaluation_agent_error.py

### Unit Tests for US2

- [ ] T079 [P] [US2] Unit tests for EvaluationService execution logic in backend/tests/unit/test_evaluation_service.py
- [ ] T080 [P] [US2] Unit tests for agent_client HTTP calls in backend/tests/unit/test_agent_client.py
- [ ] T081 [P] [US2] Component tests for EvaluationRunner in frontend/tests/EvaluationRunner.test.jsx
- [ ] T082 [P] [US2] Component tests for EvaluationProgress in frontend/tests/EvaluationProgress.test.jsx

**Checkpoint**: User Story 2 complete - evaluation execution fully functional with error handling

---

## Phase 5: User Story 3 - Score Responses with Graders (Priority: P1)

**Goal**: Enable grading of collected responses using pluggable graders starting with string-match

**Independent Test**: Responses can be scored by graders; scores stored and retrieved correctly; error handling for grader failures

**Architecture**: GradingService applies graders to results; per-result error isolation; Score entities capture outcomes

### Contract Tests for US3 (REQUIRED - run first)

- [ ] T083 [P] [US3] Contract test for GET /api/graders (list graders) in backend/tests/contract/test_graders_list.py
- [ ] T084 [P] [US3] Contract test for GET /api/graders/{id} (get grader details) in backend/tests/contract/test_graders_get.py

### Backend Implementation for US3

- [ ] T085 [US3] Implement GradingService orchestration in backend/src/services/grading_service.py
- [ ] T086 [US3] Implement grading loop (apply all graders to all results) in backend/src/services/grading_service.py
- [ ] T087 [P] [US3] Implement per-result error isolation (grader failure doesn't stop others) in backend/src/services/grading_service.py
- [ ] T088 [P] [US3] Implement grader timeout handling (5 second timeout per grader) in backend/src/services/grading_service.py
- [ ] T089 [P] [US3] Implement error capture and storage in backend/src/services/grading_service.py
- [ ] T090 [US3] Implement Score storage and retrieval in backend/src/services/grading_service.py
- [ ] T091 [US3] Implement aggregate metrics calculation (pass rates, per-grader stats) in backend/src/services/grading_service.py
- [ ] T092 [US3] Implement POST /api/graders (list graders) endpoint in backend/src/api/graders.py
- [ ] T093 [US3] Implement GET /api/graders/{id} endpoint (grader details with schema) in backend/src/api/graders.py
- [ ] T094 [P] [US3] Add logging for grading progress in backend/src/services/grading_service.py

### Frontend Implementation for US3

- [ ] T095 [P] [US3] Create GraderSelector component for choosing which graders to apply in frontend/src/components/GraderSelector.jsx
- [ ] T096 [US3] Integrate GraderSelector into EvaluationRunner in frontend/src/components/EvaluationRunner.jsx
- [ ] T097 [P] [US3] Display grader selection in evaluation configuration in frontend/src/components/EvaluationRunner.jsx

### Integration Tests for US3

- [ ] T098 [US3] Integration test for complete grading workflow in backend/tests/integration/test_grading_complete.py
- [ ] T099 [P] [US3] Integration test for per-result error isolation in backend/tests/integration/test_grading_error_isolation.py
- [ ] T100 [P] [US3] Integration test for grader timeout handling in backend/tests/integration/test_grading_timeout.py

### Unit Tests for US3

- [ ] T101 [P] [US3] Unit tests for GradingService in backend/tests/unit/test_grading_service.py
- [ ] T102 [P] [US3] Unit tests for StringMatchGrader in backend/tests/unit/test_string_match_grader.py
- [ ] T103 [P] [US3] Unit tests for metrics calculation in backend/tests/unit/test_metrics_calculation.py
- [ ] T104 [P] [US3] Component tests for GraderSelector in frontend/tests/GraderSelector.test.jsx

**Checkpoint**: User Story 3 complete - grading functional with proper error handling

---

## Phase 6: User Story 4 - View Evaluation Results in Web UI (Priority: P1)

**Goal**: Enable users to view, filter, and analyze evaluation results through web dashboard

**Independent Test**: Results dashboard displays correctly; filtering works; detail views show complete information; export functions work

**Architecture**: ResultsViewer components consume evaluation data; ResultsTable shows all results; ResultsDetail shows side-by-side comparison

### Contract Tests for US4 (REQUIRED - results already covered by US2, focus on UI data needs)

- [X] T105 [P] [US4] Integration test for UI data retrieval and rendering with results in backend/tests/integration/test_e2e_workflow.py

### Backend Implementation for US4

- [ ] T106 [US4] Implement results export to JSON in backend/src/api/evaluations.py
- [ ] T107 [US4] Implement results export to CSV in backend/src/api/evaluations.py
- [ ] T108 [P] [US4] Add result filtering by date range in backend/src/services/evaluation_service.py
- [ ] T109 [P] [US4] Add result filtering by tags in backend/src/services/evaluation_service.py

### Frontend Implementation for US4

- [X] T110 [P] [US4] Create ResultsViewer component for overall results dashboard in frontend/src/components/ResultsViewer.jsx
- [ ] T111 [P] [US4] Create ResultsTable component for displaying results in tabular form in frontend/src/components/ResultsTable.jsx
- [ ] T112 [P] [US4] Create ResultsDetail component for side-by-side detail view in frontend/src/components/ResultsDetail.jsx
- [ ] T113 [US4] Create ResultsFilters component for filtering by date/tags in frontend/src/components/ResultsFilters.jsx
- [X] T114 [US4] Implement API integration in ResultsViewer (GET /api/evaluations/{id}/results) in frontend/src/components/ResultsViewer.jsx
- [ ] T115 [US4] Implement filtering logic in ResultsFilters in frontend/src/components/ResultsFilters.jsx
- [ ] T116 [P] [US4] Implement sorting by column in ResultsTable in frontend/src/components/ResultsTable.jsx
- [ ] T117 [P] [US4] Implement row detail expansion in ResultsTable in frontend/src/components/ResultsTable.jsx
- [X] T118 [US4] Implement export to JSON functionality in ResultsViewer in frontend/src/components/ResultsViewer.jsx
- [X] T119 [US4] Implement export to CSV functionality in ResultsViewer in frontend/src/components/ResultsViewer.jsx
- [ ] T120 [P] [US4] Add pagination to ResultsTable for large result sets in frontend/src/components/ResultsTable.jsx
- [X] T121 [P] [US4] Add loading states and error messages in frontend/src/components/ResultsViewer.jsx
- [X] T122 [US4] Create App.jsx routing structure to navigate between test cases, runner, and results pages in frontend/src/pages/App.jsx

### Integration Tests for US4

- [ ] T123 [US4] Integration test for results export to JSON in backend/tests/integration/test_results_export_json.py
- [ ] T124 [P] [US4] Integration test for results export to CSV in backend/tests/integration/test_results_export_csv.py

### Unit Tests for US4

- [X] T125 [P] [US4] Component tests for ResultsViewer in frontend/tests/components/ResultsViewer.test.jsx
- [ ] T126 [P] [US4] Component tests for ResultsTable in frontend/tests/ResultsTable.test.jsx
- [ ] T127 [P] [US4] Component tests for ResultsDetail in frontend/tests/ResultsDetail.test.jsx
- [ ] T128 [P] [US4] Component tests for ResultsFilters in frontend/tests/ResultsFilters.test.jsx

**Checkpoint**: User Story 4 complete - results visualization and analysis fully functional

### Frontend Polish

- [ ] T136 [P] Add comprehensive error handling and user-friendly error messages in frontend/src/
- [ ] T137 [P] Implement responsive CSS for mobile/tablet viewing in frontend/src/styles/
- [ ] T138 [P] Add accessibility features (ARIA labels, keyboard navigation) in frontend/src/components/
- [ ] T139 [P] Create frontend component documentation in frontend/
- [ ] T140 Create frontend test coverage report (target >80%) in frontend/
- [ ] T141 [P] Create frontend development guide in frontend/README.md
- [ ] T142 [P] Add CI/CD configuration for frontend tests (.github/workflows/frontend-tests.yml)

### Integration & Deployment

- [ ] T143 Create comprehensive end-to-end test (all 4 user stories together) in backend/tests/integration/test_e2e_complete_workflow.py
- [ ] T144 [P] Test concurrent evaluation runs (simulated 3+ simultaneous runs) in backend/tests/integration/test_concurrent_runs.py
- [ ] T145 [P] Test with large result sets (1000+ test cases) in backend/tests/integration/test_large_datasets.py
- [ ] T146 Create Dockerfile for backend in backend/Dockerfile
- [ ] T147 [P] Create Dockerfile for frontend in frontend/Dockerfile
- [ ] T148 [P] Create docker-compose.yml for local development in docker-compose.yml
- [ ] T149 Create production deployment guide in DEPLOYMENT.md
- [ ] T150 [P] Create troubleshooting guide in TROUBLESHOOTING.md

### Documentation

- [ ] T151 Update main README.md with feature overview, architecture, and quick start
- [ ] T152 [P] Create API reference documentation from contract files in docs/API.md
- [ ] T153 [P] Create data model documentation in docs/DATA_MODEL.md
- [ ] T154 [P] Create architecture decision record in docs/ARCHITECTURE.md
- [ ] T155 [P] Create development workflow guide in docs/DEVELOPMENT.md
- [ ] T156 [P] Create changelog for version 0.1.0 in CHANGELOG.md

---

## Dependency Graph & Parallelization Strategy

### Critical Path (Must Complete Sequentially)
```
Setup (Phase 1) → Foundational (Phase 2) → US1 (Phase 3) → US2 (Phase 4) → US3 (Phase 5) → US4 (Phase 6) → Polish (Phase 7)
```

### Phase 3 (US1) - Parallelizable Tasks
```
[T029-T033] Contract tests (write concurrently)
  ↓
[T034-T038] API endpoints (can develop in parallel, different files)
  ↓
[T039-T040] Service layer (depends on models, can run with endpoints)
  ↓
[T041-T048] Frontend components (parallel with backend)
  ↓
[T049-T053] Integration/unit tests (parallel, different modules)
```

### Phase 4 (US2) - Parallelizable Tasks
```
[T054-T057] Contract tests (parallel)
  ↓
[T058-T062] Backend service & client (can develop in parallel)
  ↓
[T063-T066] API endpoints (parallel)
  ↓
[T069-T075] Frontend components (parallel with backend)
  ↓
[T076-T082] Tests (parallel)
```

### Phase 5 (US3) - Parallelizable Tasks
```
[T083-T084] Contract tests (parallel)
  ↓
[T085-T091] Backend grading service (sequential dependency)
  ↓
[T092-T093] API endpoints (parallel)
  ↓
[T095-T097] Frontend grader selection (parallel with backend)
  ↓
[T098-T104] Tests (parallel)
```

### Phase 6 (US4) - Parallelizable Tasks
```
[T110-T112] Frontend result components (parallel, independent)
  ↓
[T113-T122] Frontend integration & features (can be parallelized)
  ↓
[T123-T128] Tests (parallel)
```

### Phase 7 (Polish) - Highly Parallelizable
- [T129-T142] Backend and Frontend polish can run in parallel
- [T143-T145] Integration tests (parallel)
- [T146-T148] Deployment config (parallel)
- [T151-T156] Documentation (parallel)

---

## Parallelization Examples

### Example 1: US1 Implementation (Phase 3)
**Can do in parallel**:
- Developer A: T034-T038 (API endpoints) + T039-T040 (service layer) = Backend API
- Developer B: T041-T048 (UI components) = Frontend
- Developer C: T029-T033 (contract tests) + T049-T053 (integration tests) = Test suite

**Sequential dependency**: Models (T015 from Phase 2) → Services → API

### Example 2: Across Multiple Stories (After Phase 2)
Once Phase 2 foundational is complete:
- Team A develops US1 (Phases 3)
- Team B develops US2 (Phase 4)
- Team C develops US3 (Phase 5)
- Team D develops US4 (Phase 6)
- Team E works on Polish (Phase 7)

These can run in strict sequence OR with some overlap:
- After US1 foundation tests pass, US2 can START (not necessarily finish)
- If US1 service layer completes early, US2 backend can begin

---

## Task Statistics

### By Phase
| Phase | Tasks | Duration | Status |
|-------|-------|----------|--------|
| Phase 1: Setup | 13 | 1-2 hrs | Foundation |
| Phase 2: Foundational | 15 | 2-3 hrs | Blocking |
| Phase 3: US1 (Test Cases) | 25 | 3-4 hrs | MVP |
| Phase 4: US2 (Execution) | 29 | 4-5 hrs | MVP |
| Phase 5: US3 (Grading) | 22 | 3-4 hrs | MVP |
| Phase 6: US4 (Results) | 19 | 3-4 hrs | MVP |
| Phase 7: Polish | 28 | 2-3 hrs | Enhancement |
| **Total** | **151** | **18-25 hrs** | **Complete** |

### By Category
- Backend Implementation: ~45 tasks
- Frontend Implementation: ~35 tasks
- Testing (contract/integration/unit): ~45 tasks
- Documentation/DevOps: ~26 tasks

### By Story (MVP Only)
- US1 (Test Cases): 25 tasks
- US2 (Execution): 29 tasks
- US3 (Grading): 22 tasks
- US4 (Results): 19 tasks
- **MVP Total**: 95 tasks (excludes Setup/Foundational/Polish)

---

## Suggested MVP Scope

**For Minimum Viable Demo (8-12 hours)**:
1. Complete Phase 1 (Setup) - 2 hours
2. Complete Phase 2 (Foundational) - 2 hours
3. Complete Phase 3 (US1 - Test Cases) - 2-3 hours
4. Complete Phase 4 (US2 - Execution) - 2-3 hours
5. Complete Phase 5 (US3 - Grading) - 2-3 hours

**Result**: Can define test cases, run evaluations, and score responses. Web UI for test case management. Results via API.

**Optional additions (for full feature demo)**:
- Complete Phase 6 (US4 - Results UI) - adds web-based results dashboard
- Polish phase for production-ready features

---

## Independent Testability Per Story

Each user story can be developed, tested, and demonstrated independently:

✅ **US1 Standalone**: Create test cases via UI/API. Verify CRUD operations work. Demo: "I can create, edit, view, delete test cases"

✅ **US2 Standalone**: Run test cases against mock agent. Collect responses. Verify end-to-end execution. Demo: "I can run 10 tests and get results back"

✅ **US3 Standalone**: Score collected responses with string-match grader. Verify scores are correct. Demo: "I can grade responses and see pass/fail"

✅ **US4 Standalone**: View results in dashboard, filter, export. Verify UI displays correctly. Demo: "I can see all results, filter by tags, and export to CSV"

**All 4 stories together**: Complete end-to-end workflow from test creation to results analysis

---

## Quality Gates

### Before Phase Completion
- [ ] All contract tests in phase passing (RED → GREEN → REFACTOR)
- [ ] Integration tests for critical workflows passing
- [ ] Unit test coverage >85% for business logic
- [ ] No NEEDS CLARIFICATION items remaining
- [ ] Constitution principles verified (all 7 passing)

### Before Merge/Release
- [ ] All 151 tasks completed and working
- [ ] Full end-to-end test (E2E) passing
- [ ] Performance tests: <500ms API p95, <3s UI load
- [ ] Security: no hardcoded secrets, environment-based config
- [ ] Documentation: all components documented, README complete
- [ ] Deployment tested: docker-compose up works

---

## Architecture Verification Checklist

### Constitution Alignment (Verify Before Merge)

- [ ] **Simplicity**: All components <200 lines (refactor if larger), clear interfaces
- [ ] **Explicit**: All configs explicit (no magic), error messages clear, no implicit behavior
- [ ] **Minimal Dependencies**: Only FastAPI, Vite, React (no bloat), standard lib used
- [ ] **Deterministic**: Graders repeatable, no randomization, same input = same output
- [ ] **Separation of Concerns**: Models, Services, API, Graders are isolated layers
- [ ] **Correctness**: Tests passing, coverage >85%, edge cases handled
- [ ] **Scalability**: Storage abstraction allows swap to database, stateless API design

---

## Next Steps After Task Completion

1. **Deploy**: Use Dockerfile/docker-compose for containerized deployment
2. **Monitor**: Add metrics/logging for production tracking
3. **Extend**: Add custom graders, database storage, authentication
4. **Scale**: Horizontal scaling with message queue for evaluation runs
5. **Integrate**: Connect to actual agent services or CI/CD pipelines

