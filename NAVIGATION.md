# Project Navigation Guide

Welcome to the Agent Evaluation Service repository! This guide helps you navigate all available resources.

## 📋 Quick Links

### For First-Time Users
1. [README.md](README.md) - Project overview and features
2. [USER_GUIDE.md](USER_GUIDE.md) - How to use the application
3. [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - For developers

### For Developers
1. [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - Architecture, common tasks, debugging
2. [backend/README.md](backend/README.md) - Backend setup and development
3. [frontend/README.md](frontend/README.md) - Frontend setup and development
4. [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Before going to production

### For Project Managers
1. [PHASE6_COMPLETE.md](PHASE6_COMPLETE.md) - Current phase status
2. [PHASE6_SUMMARY.md](PHASE6_SUMMARY.md) - What was completed in Phase 6
3. [specs/001-agent-eval-service/tasks.md](specs/001-agent-eval-service/tasks.md) - Task list with completion status

### For Operations/DevOps
1. [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Pre-deployment validation
2. [backend/README.md](backend/README.md) - Backend deployment
3. [frontend/README.md](frontend/README.md) - Frontend deployment

## 📂 Project Structure

```
agent-evaluator/
│
├── 📄 Main Documentation
│   ├── README.md                    # Project overview
│   ├── USER_GUIDE.md               # End-user documentation
│   ├── DEVELOPER_GUIDE.md          # Developer reference
│   ├── DEPLOYMENT_CHECKLIST.md     # Deployment validation
│   ├── PHASE6_SUMMARY.md           # What was completed (Phase 6)
│   └── PHASE6_COMPLETE.md          # Phase 6 status report
│
├── backend/                         # Python/FastAPI backend
│   ├── src/
│   │   ├── api/                    # HTTP endpoints
│   │   │   ├── test_cases.py       # Test case endpoints
│   │   │   ├── evaluations.py      # Evaluation endpoints
│   │   │   ├── graders.py          # Grader endpoints
│   │   │   ├── schemas.py          # Pydantic schemas
│   │   │   └── utils.py            # Response utilities
│   │   ├── models/                 # Data models
│   │   │   ├── test_case.py
│   │   │   ├── evaluation.py
│   │   │   ├── grader.py
│   │   │   └── score.py
│   │   ├── services/               # Business logic
│   │   │   ├── test_case_service.py
│   │   │   ├── evaluation_service.py
│   │   │   ├── grading_service.py
│   │   │   ├── agent_client.py
│   │   │   ├── grader_service.py
│   │   │   ├── storage_service.py
│   │   │   └── storage.py
│   │   ├── graders/                # Grading implementations
│   │   │   ├── base.py             # GraderInterface
│   │   │   └── string_match.py     # String match grader
│   │   └── config.py               # Configuration
│   ├── tests/
│   │   ├── contract/               # API contract tests
│   │   ├── integration/            # E2E workflow tests
│   │   ├── unit/                   # Unit tests
│   │   └── conftest.py             # Pytest fixtures
│   ├── main.py                     # FastAPI app entry point
│   ├── mock_agent_server.py        # Mock agent for testing
│   ├── requirements.txt            # Python dependencies
│   ├── README.md                   # Backend documentation
│   └── .env.example                # Environment template
│
├── frontend/                        # React/Vite frontend
│   ├── src/
│   │   ├── components/             # React components
│   │   │   ├── TestCaseForm.jsx
│   │   │   ├── TestCaseList.jsx
│   │   │   ├── EvaluationRunner.jsx
│   │   │   ├── ResultsViewer.jsx   # Phase 6: New
│   │   │   └── GraderSelector.jsx
│   │   ├── pages/                  # Page layouts
│   │   │   ├── App.jsx
│   │   └── TestCaseManager.jsx
│   │   ├── services/
│   │   │   └── api.js              # API client
│   │   ├── styles/
│   │   │   └── App.css
│   │   └── main.jsx                # React entry point
│   ├── tests/
│   │   └── components/             # Component tests
│   │       └── ResultsViewer.test.jsx  # Phase 6: New
│   ├── package.json                # Node dependencies
│   ├── vite.config.js              # Vite configuration
│   ├── vitest.config.js            # Vitest configuration
│   ├── README.md                   # Frontend documentation
│   └── index.html                  # HTML entry point
│
└── specs/001-agent-eval-service/   # Specification documents
    ├── spec.md                     # User stories & requirements
    ├── plan.md                     # Architecture & design
    ├── data-model.md               # Entity relationships
    ├── research.md                 # Technical decisions
    ├── quickstart.md               # Integration guide
    ├── tasks.md                    # Task list & progress
    ├── checklists/                 # Completion checklists
    └── contracts/                  # API specifications
```

## 🚀 Quick Start

### For New Developers
```bash
# 1. Read the overview
cat README.md

# 2. Read developer guide
cat DEVELOPER_GUIDE.md

# 3. Setup backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# 4. Setup frontend (new terminal)
cd frontend
npm install
npm run dev

# 5. Run mock agent (new terminal)
cd backend
python mock_agent_server.py
```

### For End Users
```bash
1. Read USER_GUIDE.md
2. Access application at http://localhost:5173
3. Start by creating test cases
4. Run evaluations
5. View and export results
```

### For Operations
```bash
1. Read DEPLOYMENT_CHECKLIST.md
2. Follow pre-deployment validation steps
3. Deploy backend to production
4. Deploy frontend to static hosting
5. Monitor and maintain
```

## 📊 Project Status

| Phase | Component | Status | Notes |
|-------|-----------|--------|-------|
| 1 | Setup | ✅ Complete | Infrastructure ready |
| 2 | Foundational | ✅ Complete | Models and services |
| 3 | US1 Test Cases | ✅ Complete | CRUD endpoints |
| 4 | US2 Execution | ✅ Complete | Async evaluation |
| 5 | US3 Grading | ✅ Complete | Extensible graders |
| 6 | US4 Results | ✅ Complete | Results viewer (Phase 6) |
| 7 | Polish | ⏳ Not Started | Logging, Docker, CI/CD |

**Current**: MVP Complete (All 4 user stories working)  
**Next Phase**: Polish & Deployment

## 📚 Key Documentation

### Understanding the Project
- [README.md](README.md) - What is this project?
- [specs/001-agent-eval-service/spec.md](specs/001-agent-eval-service/spec.md) - User stories & requirements
- [specs/001-agent-eval-service/plan.md](specs/001-agent-eval-service/plan.md) - Architecture & design

### Using the Application
- [USER_GUIDE.md](USER_GUIDE.md) - How to use features
- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - How to extend it

### Setting Up Environments
- [backend/README.md](backend/README.md) - Backend setup
- [frontend/README.md](frontend/README.md) - Frontend setup
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Production setup

### Development Reference
- [specs/001-agent-eval-service/data-model.md](specs/001-agent-eval-service/data-model.md) - Data schemas
- [specs/001-agent-eval-service/contracts/](specs/001-agent-eval-service/contracts/) - API specs
- [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) - Development guide

### Project Progress
- [PHASE6_COMPLETE.md](PHASE6_COMPLETE.md) - Current status
- [PHASE6_SUMMARY.md](PHASE6_SUMMARY.md) - What was delivered
- [specs/001-agent-eval-service/tasks.md](specs/001-agent-eval-service/tasks.md) - Task tracking

## 🎯 Common Tasks

### I want to...

**...understand the project**
→ Read [README.md](README.md)

**...use the application**
→ Read [USER_GUIDE.md](USER_GUIDE.md)

**...develop a new feature**
→ Read [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) and backend/frontend READMEs

**...deploy to production**
→ Follow [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

**...add a custom grader**
→ See DEVELOPER_GUIDE.md → "Add a New Grader" section

**...add a new API endpoint**
→ See DEVELOPER_GUIDE.md → "Add a New Endpoint" section

**...add a new React component**
→ See DEVELOPER_GUIDE.md → "Add a New Component" section

**...understand the data model**
→ Read [specs/001-agent-eval-service/data-model.md](specs/001-agent-eval-service/data-model.md)

**...see API specifications**
→ Browse [specs/001-agent-eval-service/contracts/](specs/001-agent-eval-service/contracts/)

**...check project progress**
→ Read [PHASE6_COMPLETE.md](PHASE6_COMPLETE.md)

## 💻 Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Backend | Python | 3.11 |
| Backend Framework | FastAPI | 0.104.1 |
| Backend HTTP | httpx | 0.25.2 |
| Frontend Framework | React | 18.2.0 |
| Frontend Build | Vite | 5.0.8 |
| Data Validation | Pydantic | 2.5.0 |
| Testing (Backend) | pytest | 7.4.3 |
| Testing (Frontend) | Vitest | 1.1.0 |

## 🔗 Important Links

- **Local Backend**: http://localhost:8000
- **Local Frontend**: http://localhost:5173
- **Backend Docs**: http://localhost:8000/docs
- **Mock Agent**: http://localhost:9000
- **GitHub**: [Link to repo]
- **Issue Tracker**: [Link to issues]

## ✅ Verification

To verify everything is set up correctly:

```bash
# Backend
cd backend && pytest && python -m uvicorn main:app --reload

# Frontend
cd frontend && npm test && npm run build

# Both running:
# Backend: http://localhost:8000 (API)
# Frontend: http://localhost:5173 (UI)
# Mock: http://localhost:9000 (Testing)
```

## 📞 Support & Communication

| Need | Resource |
|------|----------|
| Feature question | USER_GUIDE.md |
| Technical question | DEVELOPER_GUIDE.md |
| Bug report | GitHub Issues |
| Deployment help | DEPLOYMENT_CHECKLIST.md |
| Architecture clarification | specs/plan.md + DEVELOPER_GUIDE.md |

## 🎓 Learning Path

### For New Team Members (1-2 hours)
1. Read [README.md](README.md) (10 min)
2. Read [USER_GUIDE.md](USER_GUIDE.md) (20 min)
3. Try the application locally (20 min)
4. Read [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) (30 min)
5. Browse code structure (20 min)

### For Contributors (2-4 hours)
1. Complete "For New Team Members" path above
2. Read [PHASE6_COMPLETE.md](PHASE6_COMPLETE.md) (20 min)
3. Read backend & frontend READMEs (30 min)
4. Review specs/plan.md (30 min)
5. Explore test files (30 min)
6. Try implementing a small feature (1-2 hours)

---

**Last Updated**: 2026-01-16 (Phase 6)  
**Maintainer**: Development Team  
**Status**: MVP Complete ✅
