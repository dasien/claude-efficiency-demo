# Test Plan: Python Tkinter Calculator

## 1. Overview

This document defines the test strategy and test cases for the calculator application.
The system under test is the `CalculatorLogic` class in `calculator_logic.py`, which
encapsulates all arithmetic and display logic independently of the Tkinter GUI layer.

## 2. Test Strategy

### 2.1 Scope

- **In scope:** Unit testing of `CalculatorLogic` public methods.
- **Out of scope:** GUI rendering, Tkinter widget behavior, visual layout, and manual
  click interactions. The GUI is a thin pass-through layer that delegates entirely to
  `CalculatorLogic`, so testing the logic class in isolation provides sufficient
  confidence in application correctness.

### 2.2 Framework and Tooling

| Tool    | Purpose                          |
|---------|----------------------------------|
| pytest  | Test runner and assertion library |
| coverage / pytest-cov | Code coverage measurement |

### 2.3 How to Test Business Logic Independently from the GUI

`CalculatorLogic` is a plain Python class with no dependency on Tkinter or any UI
framework. Tests instantiate it directly:

```python
from calculator_logic import CalculatorLogic

def test_example():
    calc = CalculatorLogic()
    calc.append_digit("3")
    calc.append_operator("+")
    calc.append_digit("4")
    result = calc.evaluate()
    assert result == "7"
```

No window, event loop, or widget reference is required. Each test creates a fresh
instance so that tests remain independent of one another.

### 2.4 Coverage Goals

| Module              | Target |
|---------------------|--------|
| calculator_logic.py | 90%+   |

Run coverage with:

```
pytest --cov=calculator_logic --cov-report=term-missing tests/
```

### 2.5 Test File Location

All tests reside in `tests/test_calculator_logic.py`.

---

## 3. Test Cases

Every test case follows a consistent format:

- **ID** -- unique identifier
- **Description** -- what is being verified
- **Steps** -- sequence of method calls
- **Expected Output** -- return value of the final call and/or observable state

### 3.1 Happy Path -- Basic Arithmetic

| ID | Description | Steps | Expected Output |
|----|-------------|-------|-----------------|
| HP-01 | Single-digit addition | `append_digit("2")`, `append_operator("+")`, `append_digit("3")`, `evaluate()` | `"5"` |
| HP-02 | Single-digit subtraction | `append_digit("9")`, `append_operator("-")`, `append_digit("4")`, `evaluate()` | `"5"` |
| HP-03 | Single-digit multiplication | `append_digit("3")`, `append_operator("*")`, `append_digit("7")`, `evaluate()` | `"21"` |
| HP-04 | Single-digit division | `append_digit("8")`, `append_operator("/")`, `append_digit("2")`, `evaluate()` | `"4"` |
| HP-05 | Multi-digit operands | `append_digit("1")`, `append_digit("2")`, `append_operator("+")`, `append_digit("3")`, `append_digit("4")`, `evaluate()` | `"46"` |
| HP-06 | get_display reflects current entry | `append_digit("5")`, `get_display()` | `"5"` |
| HP-07 | Division producing decimal result | `append_digit("7")`, `append_operator("/")`, `append_digit("2")`, `evaluate()` | `"3.5"` |

### 3.2 Chained Operations

| ID | Description | Steps | Expected Output |
|----|-------------|-------|-----------------|
| CH-01 | Three-term addition | `append_digit("1")`, `append_operator("+")`, `append_digit("2")`, `append_operator("+")`, `append_digit("3")`, `evaluate()` | `"6"` |
| CH-02 | Mixed operators | `append_digit("5")`, `append_operator("+")`, `append_digit("3")`, `append_operator("*")`, `append_digit("2")`, `evaluate()` | Result depends on evaluation strategy (left-to-right: `"16"`, or standard precedence: `"11"`) |
| CH-03 | Evaluate then continue | `append_digit("2")`, `append_operator("+")`, `append_digit("3")`, `evaluate()` (returns `"5"`), `append_operator("+")`, `append_digit("1")`, `evaluate()` | `"6"` |

### 3.3 Decimal Numbers

| ID | Description | Steps | Expected Output |
|----|-------------|-------|-----------------|
| DC-01 | Simple decimal entry | `append_digit("1")`, `append_decimal()`, `append_digit("5")` | display is `"1.5"` |
| DC-02 | Decimal addition | `append_digit("1")`, `append_decimal()`, `append_digit("5")`, `append_operator("+")`, `append_digit("2")`, `append_decimal()`, `append_digit("5")`, `evaluate()` | `"4.0"` or `"4"` |
| DC-03 | Leading decimal (0.5) | `append_decimal()`, `append_digit("5")` | display is `"0.5"` or `".5"` |
| DC-04 | Multiple decimal points ignored | `append_digit("1")`, `append_decimal()`, `append_digit("2")`, `append_decimal()`, `append_digit("3")` | display is `"1.23"` -- second decimal has no effect |

### 3.4 Error Cases

| ID | Description | Steps | Expected Output |
|----|-------------|-------|-----------------|
| ER-01 | Division by zero | `append_digit("5")`, `append_operator("/")`, `append_digit("0")`, `evaluate()` | Error string displayed (e.g., `"Error"`); `has_error()` returns `True` |
| ER-02 | has_error is False normally | `append_digit("1")`, `append_operator("+")`, `append_digit("1")`, `evaluate()` | `has_error()` returns `False` |
| ER-03 | Error state auto-recovery on new digit | `append_digit("5")`, `append_operator("/")`, `append_digit("0")`, `evaluate()`, `append_digit("3")` | `has_error()` returns `False`; display is `"3"` |
| ER-04 | Clear after error recovers | `append_digit("5")`, `append_operator("/")`, `append_digit("0")`, `evaluate()`, `clear()` | returns `"0"`; `has_error()` returns `False` |

### 3.5 Consecutive Operators (Last Wins)

| ID | Description | Steps | Expected Output |
|----|-------------|-------|-----------------|
| CO-01 | Replace operator | `append_digit("5")`, `append_operator("+")`, `append_operator("-")`, `append_digit("3")`, `evaluate()` | `"2"` -- the minus replaced the plus |
| CO-02 | Triple operator replacement | `append_digit("4")`, `append_operator("+")`, `append_operator("*")`, `append_operator("-")`, `append_digit("1")`, `evaluate()` | `"3"` -- only the final minus is applied |

### 3.6 Clear Behavior

| ID | Description | Steps | Expected Output |
|----|-------------|-------|-----------------|
| CL-01 | Clear resets to zero | `append_digit("9")`, `append_digit("9")`, `clear()` | returns `"0"` |
| CL-02 | Clear mid-expression | `append_digit("5")`, `append_operator("+")`, `append_digit("3")`, `clear()` | returns `"0"`; subsequent `evaluate()` should not crash |
| CL-03 | Clear then new expression | `append_digit("1")`, `clear()`, `append_digit("2")`, `append_operator("+")`, `append_digit("3")`, `evaluate()` | `"5"` |

### 3.7 Boundary Conditions

| ID | Description | Steps | Expected Output |
|----|-------------|-------|-----------------|
| BD-01 | Large number addition | `append_digit` for `"999999999"`, `append_operator("+")`, `append_digit("1")`, `evaluate()` | `"1000000000"` |
| BD-02 | Very small decimal | `append_digit("1")`, `append_operator("/")`, `append_digit` for `"3"`, `evaluate()` | A decimal representation (e.g., `"0.3333333333333333"`) -- verify no crash |
| BD-03 | Leading zeros | `append_digit("0")`, `append_digit("0")`, `append_digit("5")` | display is `"5"` or `"005"` -- document actual behavior; no crash |
| BD-04 | Empty expression evaluation | (fresh instance) `evaluate()` | returns `"0"` or a safe default; no crash; `has_error()` is `False` |
| BD-05 | Evaluate with only operator | `append_operator("+")`, `evaluate()` | No crash; returns a safe value; `has_error()` may be `True` or `False` depending on implementation |

---

## 4. Test Execution

### 4.1 Running the Full Suite

```
pytest tests/test_calculator_logic.py -v
```

### 4.2 Running with Coverage

```
pytest --cov=calculator_logic --cov-report=term-missing tests/test_calculator_logic.py
```

### 4.3 Running a Single Category

Use pytest marker or keyword filtering:

```
pytest tests/test_calculator_logic.py -v -k "decimal"
```

---

## 5. Pass / Fail Criteria

- All tests in sections 3.1 through 3.7 pass.
- Code coverage on `calculator_logic.py` meets or exceeds 90%.
- No test produces an unhandled exception.
