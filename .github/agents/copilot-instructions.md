# agent-evaluator Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-15

## Active Technologies
- Python 3.11 + FastAPI 0.104.1 (existing), Pydantic 2.5.0 (existing) (002-true-false-grader)
- InMemoryStorage (existing - no new storage needed) (002-true-false-grader)

- Python 3.11 (backend), JavaScript ES2022 (frontend) + FastAPI (backend API), Vite + React (frontend), httpx (HTTP client for agent calls) (001-agent-eval-service)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.11 (backend), JavaScript ES2022 (frontend): Follow standard conventions

## Recent Changes
- 002-true-false-grader: Added Python 3.11 + FastAPI 0.104.1 (existing), Pydantic 2.5.0 (existing)

- 001-agent-eval-service: Added Python 3.11 (backend), JavaScript ES2022 (frontend) + FastAPI (backend API), Vite + React (frontend), httpx (HTTP client for agent calls)

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
