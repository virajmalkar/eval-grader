<!-- 
SYNC IMPACT REPORT - Constitution v1.0.0
==========================================
Initial Constitution Creation - 2026-01-15

Version Change: N/A (Initial creation)
New Principles Added:
  1. Simplicity & Clarity First
  2. Explicit Over Implicit
  3. Minimal Dependencies
  4. Deterministic Behavior
  5. Separation of Concerns
  6. Correctness & Testability
  7. Scalability Through Design

Templates Status:
  ✅ plan-template.md: No updates required (already Constitution-aware)
  ✅ spec-template.md: No updates required (already Constitution-aware)
  ✅ tasks-template.md: No updates required (already Constitution-aware)
  ✅ README.md: Can reference constitution for project values

No deferred items. All principles fully specified.
-->

# Agent Evaluator Constitution

## Core Principles

### I. Simplicity & Clarity First
Every component MUST be understandable by a single developer within 10 minutes of reading the code. Complex logic MUST be broken into smaller, transparent functions with explicit purpose. Avoid clever solutions in favor of straightforward, readable implementations that prioritize maintainability over compactness.

### II. Explicit Over Implicit
Code MUST make behavior obvious through clear naming, explicit types, and documented assumptions. Magic values, implicit side effects, and unclear variable names are forbidden. Configuration MUST be explicit and visible (never buried in environment-only logic). When trade-offs arise between "concise" and "explicit," choose explicit.

### III. Minimal Dependencies
External dependencies MUST solve a critical problem that cannot reasonably be implemented internally. Every new dependency requires documented justification. Prefer small, focused libraries over large frameworks. Standard library capabilities MUST be evaluated before adding external packages. Keep the dependency tree flat and auditable.

### IV. Deterministic Behavior
All functionality MUST produce consistent, reproducible results given identical inputs. Non-determinism (random seeds, timing-dependent logic, ordering issues) MUST be confined to intentional interfaces and clearly marked. Tests MUST verify deterministic behavior through explicit input-output assertions. For demo purposes, all results MUST be reproducible and explainable.

### V. Separation of Concerns
Each module MUST have a single, well-defined responsibility. Business logic MUST be isolated from I/O, configuration, and infrastructure concerns. Services MUST not depend on global state. Interface contracts MUST be explicit and enforced through testing. Layering violations during code review MUST be rejected.

### VI. Correctness & Testability
Correctness MUST be verified through tests before feature completion. Contract tests verify component boundaries; integration tests verify workflows. Test coverage for critical paths MUST exceed 85%. Edge cases and error conditions MUST be explicitly tested. Tests MUST be runnable in isolation and deterministic.

### VII. Scalability Through Design
Scalability MUST be achieved through architecture, not through heroic optimizations. Systems MUST scale vertically and horizontally through clear interfaces. Performance constraints MUST be explicit and documented. Avoid premature optimization; optimize only for measured bottlenecks with clear justification.

## Quality Standards

### Code Review Gate
Every merge MUST satisfy:
- [ ] Single Responsibility: Module has one clear purpose
- [ ] Explicit Behavior: No hidden logic; names are precise
- [ ] Testability: Critical paths have contract tests
- [ ] No Hidden Dependencies: All external calls documented
- [ ] Deterministic: Same input → same output guaranteed

### Testing Discipline
- Contract tests for every public interface
- Integration tests for multi-component workflows
- Unit tests for business logic and edge cases
- All tests MUST be deterministic and runnable in isolation
- Flaky tests MUST be treated as critical bugs

## Development Workflow

### Feature Implementation
1. Write specification with acceptance criteria and user scenarios
2. Write contract tests (RED phase)
3. Implement feature (GREEN phase)
4. Refactor for clarity and maintainability (REFACTOR phase)
5. Review against constitution principles
6. Merge and document

### Complexity Justification
When complexity cannot be avoided (e.g., performance-critical path), ALL of the following MUST be documented:
- Why simplicity alone is insufficient
- What problem the complexity solves
- Explicit acceptance criteria for the complexity trade-off
- Link to approved architectural decision
- Maintenance plan for ongoing clarity

## Governance

**This constitution supersedes all other development practices.** All PRs, designs, and architectural decisions MUST align with these principles. When ambiguity arises, ask: "Will this code be understood by a new team member in 10 minutes?"

**Amendment Process:**
- Major changes (new principles, removed principles): Requires team consensus and documentation
- Minor clarifications: Document rationale and version bump
- All amendments MUST update `LAST_AMENDED_DATE` and increment `CONSTITUTION_VERSION`

**Compliance Verification:**
- Code review explicitly checks each principle from the Quality Standards section
- Architecture reviews reference applicable principles
- Documentation MUST link design decisions to supporting principles

**Version**: 1.0.0 | **Ratified**: 2026-01-15 | **Last Amended**: 2026-01-15
