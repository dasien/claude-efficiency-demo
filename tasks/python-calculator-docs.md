Build a Python command-line calculator application. You must complete each phase in order, producing the required document or artifact before moving to the next phase.

## Phase 1: Requirements Document

Write a `docs/requirements.md` that captures:
- Functional requirements (what the calculator must do)
- Non-functional requirements (performance, usability, error handling)
- User interface specification (input format, output format, REPL behavior)
- Edge cases and boundary conditions to handle
- Acceptance criteria for each requirement

The calculator must support: addition (+), subtraction (-), multiplication (*), division (/), input in the format `<number> <operator> <number>` (e.g., `5 + 3`), a REPL loop (quit/exit to stop), integer and floating-point numbers, and graceful error handling.

## Phase 2: Architecture Document

Write a `docs/architecture.md` that includes:
- High-level system design (modules, responsibilities, data flow)
- Module interface definitions (function signatures with types)
- Design decisions and rationale (why this structure over alternatives)
- Separation of concerns analysis (how business logic is isolated from I/O)
- Error handling strategy (exception types, where errors are caught vs raised)

## Phase 3: Coding Plan

Write a `docs/coding-plan.md` that specifies:
- Implementation order (which modules/functions to build first and why)
- File-by-file breakdown of what each file contains
- Dependencies between modules
- Estimated complexity per component

## Phase 4: Test Plan

Write a `docs/test-plan.md` that covers:
- Test strategy (unit tests, integration tests, what framework)
- Test cases organized by category: happy path, edge cases, error cases, boundary conditions
- Expected inputs and outputs for each test case
- Coverage goals

## Phase 5: Implementation

Implement the calculator following your architecture and coding plan:
- `calculator.py` — main application code
- `requirements.txt` — Python dependencies

## Phase 6: Test Implementation and Execution

Implement and run the tests following your test plan:
- `test_calculator.py` — pytest test suite
- Run all tests and verify they pass

Use `python3` (not `python`) for all commands.
