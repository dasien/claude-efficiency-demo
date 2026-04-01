# Test Plan: Python Tkinter GUI Calculator Application

## 1. Overview

This document defines the test plan for the calculator application's business logic layer, contained in `calculator_logic.py`. The GUI layer (Tkinter) is intentionally excluded from automated testing. All tests target the `CalculatorLogic` class directly.

## 2. Test Strategy

### 2.1 Approach

- **Framework**: pytest
- **Scope**: Unit tests for `CalculatorLogic` only. No GUI (Tkinter) testing is required.
- **Isolation**: Import and instantiate `CalculatorLogic` directly in test modules. The class contains no GUI dependencies and can be tested as a pure logic unit.
- **Coverage goal**: Greater than 90% line coverage on `calculator_logic.py`, measured with `pytest-cov`.

### 2.2 How to Test Business Logic Independently from the GUI

The calculator follows a separation-of-concerns pattern. The `CalculatorLogic` class owns all computation state and exposes it through `get_display()`. The Tkinter GUI is a thin layer that calls these methods and renders the display string.

To test without the GUI:

```python
from calculator_logic import CalculatorLogic

def test_basic_addition():
    calc = CalculatorLogic()
    calc.add_digit("2")
    calc.add_operator("+")
    calc.add_digit("3")
    result = calc.evaluate()
    assert result == "5"
```

No `tkinter` import is needed. No window is created. Tests run in any environment, including headless CI servers.

### 2.3 Test Execution

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=calculator_logic --cov-report=term-missing

# Run a specific category
pytest tests/ -v -k "happy_path"
```

### 2.4 Test File Structure

```
tests/
    conftest.py               # Shared fixtures (e.g., fresh CalculatorLogic instance)
    test_happy_path.py        # Basic operations, chained operations, decimals
    test_edge_cases.py        # Division by zero, multiple decimals, leading zeros, empty expr
    test_error_cases.py       # Invalid operations, overflow
    test_boundary.py          # Very large numbers, very small numbers, precision
```

### 2.5 Shared Fixtures

```python
# conftest.py
import pytest
from calculator_logic import CalculatorLogic

@pytest.fixture
def calc():
    """Return a fresh CalculatorLogic instance with all state cleared."""
    return CalculatorLogic()
```

---

## 3. Test Cases

### 3.1 Happy Path

#### 3.1.1 Basic Arithmetic Operations

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| HP-01 | Single digit addition | `add_digit("2")`, `add_operator("+")`, `add_digit("3")`, `evaluate()` | `"5"` |
| HP-02 | Single digit subtraction | `add_digit("9")`, `add_operator("-")`, `add_digit("4")`, `evaluate()` | `"5"` |
| HP-03 | Single digit multiplication | `add_digit("6")`, `add_operator("*")`, `add_digit("7")`, `evaluate()` | `"42"` |
| HP-04 | Single digit division | `add_digit("8")`, `add_operator("/")`, `add_digit("2")`, `evaluate()` | `"4"` |
| HP-05 | Multi-digit number addition | `add_digit("1")`, `add_digit("2")`, `add_operator("+")`, `add_digit("3")`, `add_digit("4")`, `evaluate()` | `"46"` |
| HP-06 | Display updates after each digit | `add_digit("1")`, check `get_display()` returns `"1"`, `add_digit("2")`, check `get_display()` returns `"12"` | Display reflects accumulated digits |

#### 3.1.2 Chained Operations

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| HP-07 | Two additions in sequence | `2 + 3 + 4 =` | `"9"` |
| HP-08 | Mixed operators | `5 + 3 * 2 =` | Result depends on whether operator precedence is respected or left-to-right evaluation is used; document actual behavior |
| HP-09 | Evaluate then continue | `2 + 3 =` (result `"5"`), then `+ 1 =` | `"6"` |
| HP-10 | Multiple evaluations | `2 + 3 =`, then `=` again | Verify consistent behavior (either repeats last operation or holds result) |

#### 3.1.3 Decimal Numbers

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| HP-11 | Simple decimal addition | `1.5 + 2.5 =` | `"4"` or `"4.0"` (document actual format) |
| HP-12 | Decimal multiplication | `0.1 * 0.2 =` | `"0.02"` |
| HP-13 | Leading zero decimal | `add_decimal()`, `add_digit("5")`, check `get_display()` | `"0.5"` |
| HP-14 | Integer and decimal mixed | `3 + 1.5 =` | `"4.5"` |

#### 3.1.4 Clear

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| HP-15 | Clear resets display | `add_digit("5")`, `clear()`, `get_display()` | `"0"` or `""` (document actual) |
| HP-16 | Clear mid-expression | `5 + 3`, `clear()`, `2 + 1 =` | `"3"` |

#### 3.1.5 Toggle Sign

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| HP-17 | Negate a positive number | `add_digit("5")`, `toggle_sign()`, `get_display()` | `"-5"` |
| HP-18 | Double toggle returns to positive | `add_digit("5")`, `toggle_sign()`, `toggle_sign()`, `get_display()` | `"5"` |
| HP-19 | Negate then evaluate | `-5 + 10 =` | `"5"` |

#### 3.1.6 Percent

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| HP-20 | Basic percent | `add_digit("5")`, `add_digit("0")`, `add_percent()`, `get_display()` | `"0.5"` |
| HP-21 | Percent in expression | `200 + 10% =` | Result depends on implementation (could be `"200.1"` or `"220"`); document actual behavior |

---

### 3.2 Edge Cases

#### 3.2.1 Division by Zero

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| EC-01 | Divide by zero | `5 / 0 =` | Returns an error string (e.g., `"Error"`, `"Infinity"`, or `"Cannot divide by zero"`) |
| EC-02 | Divide by zero mid-chain | `10 / 0 + 5 =` | Error state; verify application does not crash |

#### 3.2.2 Multiple Decimal Points

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| EC-03 | Two decimals in one number | `add_digit("1")`, `add_decimal()`, `add_decimal()`, `add_digit("5")` | Second decimal is ignored; display shows `"1.5"` |
| EC-04 | Decimal in second operand | `1.2 + 3.4 =` | `"4.6"` (decimals work independently per operand) |

#### 3.2.3 Leading Zeros

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| EC-05 | Multiple leading zeros | `add_digit("0")`, `add_digit("0")`, `add_digit("5")` | Display shows `"5"` (leading zeros stripped) or `"005"` (document actual) |
| EC-06 | Zero before decimal | `add_digit("0")`, `add_decimal()`, `add_digit("1")` | `"0.1"` |

#### 3.2.4 Empty Expression

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| EC-07 | Evaluate with no input | `evaluate()` immediately on fresh instance | Returns `"0"` or `""` without error |
| EC-08 | Evaluate after clear | `5 + 3 =`, `clear()`, `evaluate()` | Returns `"0"` or `""` without error |

#### 3.2.5 Operator Without Operand

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| EC-09 | Operator first | `add_operator("+")`, `add_digit("5")`, `evaluate()` | Treats as `0 + 5 = 5` or ignores the operator; no crash |
| EC-10 | Consecutive operators | `add_digit("5")`, `add_operator("+")`, `add_operator("-")` | Second operator replaces the first, or last one wins |
| EC-11 | Trailing operator | `5 +` then `evaluate()` | Returns `"5"` or error; no crash |

---

### 3.3 Error Cases

#### 3.3.1 Invalid Operations

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| ER-01 | Invalid digit character | `add_digit("a")` | Ignored or raises ValueError; no crash, display unchanged |
| ER-02 | Invalid operator | `add_operator("^")` | Ignored or raises ValueError; no crash |
| ER-03 | Empty string digit | `add_digit("")` | Ignored; no crash |

#### 3.3.2 Overflow

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| ER-04 | Multiplication causing large result | Multiply large numbers (e.g., `99999999 * 99999999`) | Returns valid result or `"Error"`/`"Overflow"`; no unhandled exception |
| ER-05 | Repeated multiplication | Start with `2`, repeatedly `* 2 =` many times | Handles gracefully; no crash |

---

### 3.4 Boundary Conditions

#### 3.4.1 Very Large Numbers

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| BC-01 | Large integer addition | `999999999999999 + 1 =` | `"1000000000000000"` |
| BC-02 | Large number display | Enter 20+ digits | Verify `get_display()` returns full number or truncates gracefully |

#### 3.4.2 Very Small Numbers

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| BC-03 | Small decimal result | `1 / 3 =` | Returns a reasonable decimal representation (e.g., `"0.3333333333"`) |
| BC-04 | Subtraction near zero | `0.0001 - 0.0001 =` | `"0"` |

#### 3.4.3 Floating-Point Precision

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| BC-05 | Classic float issue | `0.1 + 0.2 =` | `"0.3"` (not `"0.30000000000000004"`); verify rounding behavior |
| BC-06 | Repeating decimal | `1 / 3 * 3 =` | `"1"` or close to `"1"`; document actual precision handling |
| BC-07 | Large minus large | `1000000.01 - 1000000 =` | `"0.01"` |

#### 3.4.4 Sign and Percent Boundaries

| ID | Description | Steps | Expected Result |
|----|-------------|-------|-----------------|
| BC-08 | Toggle sign on zero | `add_digit("0")`, `toggle_sign()` | `"0"` (not `"-0"`) |
| BC-09 | Percent of zero | `add_digit("0")`, `add_percent()` | `"0"` |
| BC-10 | Percent of negative | `add_digit("5")`, `toggle_sign()`, `add_percent()` | `"-0.05"` |

---

## 4. Coverage Goals

| Module | Target | Measurement |
|--------|--------|-------------|
| `calculator_logic.py` | > 90% line coverage | `pytest --cov=calculator_logic --cov-report=term-missing` |

All public methods of `CalculatorLogic` must be exercised by at least one test. Every branch in conditional logic (e.g., division-by-zero guard, duplicate-decimal guard) must be covered.

### Coverage Gaps to Watch

- Error/exception handling branches inside `evaluate()`.
- Guard clauses in `add_decimal()` (rejecting a second decimal point).
- State transitions when operators are entered without a preceding digit.
- `toggle_sign()` behavior when the display is empty or zero.
- `add_percent()` behavior on edge values (zero, negative).

## 5. Risks and Assumptions

- **Assumption**: `CalculatorLogic` has no dependency on `tkinter` or any GUI module. If it does, the import will fail in headless CI and the test strategy must be revised.
- **Assumption**: `evaluate()` returns a string, not a numeric type. All assertions compare strings.
- **Risk**: Floating-point formatting may vary across Python versions. Tests for precision (BC-05, BC-06, BC-07) should allow for minor formatting differences or pin the Python version in CI.
- **Risk**: The class may use `eval()` internally for expression parsing. If so, additional security-oriented tests should be added to verify that arbitrary code cannot be injected through `add_digit()` or `add_operator()`.
