Build a Python GUI calculator application using Tkinter. You must complete each phase in order, producing the required document or artifact before moving to the next phase.

## Phase 1: Requirements Document

Write a `docs/requirements.md` that captures:
- Functional requirements (what the calculator must do)
- Non-functional requirements (performance, usability, error handling)
- GUI specification (window layout, button placement, display behavior)
- Edge cases and boundary conditions to handle
- Acceptance criteria for each requirement

The calculator must support: addition (+), subtraction (-), multiplication (*), division (/), a display showing the current expression and result, number buttons (0-9) and a decimal point button, operator buttons, an equals button to evaluate, a clear button to reset, keyboard input support (typing numbers and operators), integer and floating-point numbers, and graceful error handling shown in the display (not crashes).

## Phase 2: Architecture Document

Write a `docs/architecture.md` that includes:
- High-level system design (MVC/MVP pattern, modules, responsibilities, data flow)
- Module interface definitions (class and function signatures with types)
- GUI layout specification (grid layout, widget hierarchy)
- Design decisions and rationale (why this structure over alternatives)
- Separation of concerns analysis (how business logic is isolated from GUI code)
- Error handling strategy (how errors are displayed to the user)
- Event handling design (button clicks, keyboard input, state management)

## Phase 3: Coding Plan

Write a `docs/coding-plan.md` that specifies:
- Implementation order (which modules/classes to build first and why)
- File-by-file breakdown of what each file contains
- Dependencies between modules
- Widget layout plan (row/column grid positions)
- Estimated complexity per component

## Phase 4: Test Plan

Write a `docs/test-plan.md` that covers:
- Test strategy (unit tests for logic, integration approach for GUI)
- Test cases organized by category: happy path, edge cases, error cases, boundary conditions
- Expected inputs and outputs for each test case
- How to test business logic independently from the GUI
- Coverage goals

## Phase 5: Implementation

Implement the calculator following your architecture and coding plan:
- `calculator.py` — main application code (GUI + logic)
- `calculator_logic.py` — business logic separated from GUI (if your architecture calls for it)
- `requirements.txt` — Python dependencies

## Phase 6: Test Implementation and Execution

Implement and run the tests following your test plan:
- `test_calculator.py` — pytest test suite (testing business logic, not GUI)
- Run all tests and verify they pass

Use `python3` (not `python`) for all commands.
