# Calculator Application — Test Plan

## 1. Test Strategy

### Unit Tests (Primary Focus)
All business logic lives in `calculator_logic.py` and can be tested without Tkinter.
Tests instantiate `CalculatorLogic` directly and call its methods, asserting on returned strings.

### Integration Testing (Manual)
GUI integration is verified manually by running the application.
The clean separation means that if the logic tests pass, the GUI only needs to be verified for correct wiring (display updates, button routing).

### What We Do NOT Test Automatically
- Tkinter widget rendering (requires display server, brittle).
- Visual appearance (font sizes, colors, layout).
- Keyboard bindings (tested manually).

## 2. Test Cases

### 2.1 Happy Path — Basic Operations

| ID | Input Sequence | Expected Result | Description |
|----|---------------|-----------------|-------------|
| HP-1 | `2`, `+`, `3`, `=` | `"5"` | Basic addition |
| HP-2 | `1`, `0`, `-`, `4`, `=` | `"6"` | Subtraction |
| HP-3 | `3`, `*`, `7`, `=` | `"21"` | Multiplication |
| HP-4 | `8`, `/`, `2`, `=` | `"4"` | Division |
| HP-5 | `2`, `+`, `3`, `*`, `4`, `=` | `"14"` | Operator precedence (2+12=14) |
| HP-6 | `1`, `.`, `5`, `+`, `2`, `.`, `5`, `=` | `"4"` | Decimal addition |
| HP-7 | `0`, `.`, `1`, `+`, `0`, `.`, `2`, `=` | `"0.3"` | Small decimal addition |

### 2.2 Display Behavior

| ID | Input Sequence | Expected Display | Description |
|----|---------------|-----------------|-------------|
| DB-1 | (no input) | `"0"` | Initial state shows "0" |
| DB-2 | `5` | `"5"` | Single digit |
| DB-3 | `1`, `2`, `3` | `"123"` | Multi-digit number |
| DB-4 | `5`, `+`, `3` | `"5+3"` | Expression building |

### 2.3 Edge Cases

| ID | Input Sequence | Expected Result | Description |
|----|---------------|-----------------|-------------|
| EC-1 | `5`, `/`, `0`, `=` | `"Error"` | Division by zero |
| EC-2 | `3`, `.`, `2`, `.`, `1` | `"3.21"` (second `.` ignored) | Multiple decimals |
| EC-3 | `+`, `5`, `=` | `"5"` | Leading operator |
| EC-4 | `5`, `+`, `=` | Error or `"5"` | Trailing operator |
| EC-5 | `=` (empty) | `"0"` | Evaluate empty expression |
| EC-6 | `5`, `+`, `+`, `3`, `=` | `"8"` | Consecutive operators (replace) |
| EC-7 | `1`, `0`, `0`, `0`, `0`, `0`, `*`, `1`, `0`, `0`, `0`, `0`, `0`, `=` | `"10000000000"` | Large numbers |
| EC-8 | `0`, `.`, `0`, `0`, `1`, `+`, `0`, `.`, `0`, `0`, `2`, `=` | `"0.003"` | Small decimals |

### 2.4 Error Cases

| ID | Input Sequence | Expected Result | Description |
|----|---------------|-----------------|-------------|
| ER-1 | `5`, `/`, `0`, `=` | `"Error"` | Division by zero |
| ER-2 | `*`, `*`, `=` | `"Error"` | Invalid expression |
| ER-3 | `/`, `=` | `"Error"` or `"0"` | Operator-only expression |

### 2.5 State Management

| ID | Input Sequence | Expected Result | Description |
|----|---------------|-----------------|-------------|
| SM-1 | `2`, `+`, `3`, `=`, `C` | `"0"` | Clear after evaluation |
| SM-2 | `2`, `+`, `3`, `=`, `+`, `4`, `=` | `"9"` | Chain: result + new op |
| SM-3 | `2`, `+`, `3`, `=`, `5` | `"5"` | New digit after eval starts fresh |
| SM-4 | `1`, `2`, `3`, backspace | `"12"` | Backspace removes last char |
| SM-5 | `5`, backspace | `"0"` | Backspace to empty shows "0" |

### 2.6 Boundary Conditions

| ID | Input Sequence | Expected Result | Description |
|----|---------------|-----------------|-------------|
| BC-1 | `9`, `9`, `9`, ..., `*`, `9`, `9`, `9`, ..., `=` | Large number (no crash) | Very large result |
| BC-2 | `1`, `/`, `3`, `=` | `"0.333333333333"` or similar | Repeating decimal |
| BC-3 | `0`, `+`, `0`, `=` | `"0"` | Zero plus zero |

## 3. Testing Business Logic Independently

All tests import `CalculatorLogic` from `calculator_logic.py` and exercise it via its public API:

```python
from calculator_logic import CalculatorLogic

def test_basic_addition():
    calc = CalculatorLogic()
    calc.add_character("2")
    calc.add_character("+")
    calc.add_character("3")
    result = calc.evaluate()
    assert result == "5"
```

No Tkinter import is needed anywhere in the test file.

## 4. Coverage Goals

| Module | Target Coverage | Notes |
|--------|----------------|-------|
| `calculator_logic.py` | 95%+ | All public methods and edge cases. |
| `calculator.py` | Not measured | GUI code tested manually. |

### Running Tests
```bash
python3 -m pytest test_calculator.py -v
python3 -m pytest test_calculator.py -v --tb=short
```
