# Calculator Application — Test Plan

## 1. Test Strategy

### Scope
- **Unit tests**: All public methods of `CalculatorLogic` — tested directly without any GUI.
- **Integration**: GUI is NOT tested in automated tests (Tkinter requires a display server). Manual verification only.

### Approach
- Import `CalculatorLogic` and call methods in sequence, asserting `get_display()` or return values.
- Use `pytest.mark.parametrize` for operations with multiple input sets.
- Each test gets a fresh `CalculatorLogic` instance via a pytest fixture.

### Coverage Goal
- 100% branch coverage of `calculator_logic.py`.
- Every edge case from the requirements document has a corresponding test.

## 2. Test Cases

### 2.1 Happy Path — Digit Input

| ID | Description | Steps | Expected Display |
|----|-------------|-------|-----------------|
| D1 | Single digit | `input_digit("5")` | `"5"` |
| D2 | Multi-digit number | `input_digit("1")`, `input_digit("2")`, `input_digit("3")` | `"123"` |
| D3 | Leading zero replaced | `input_digit("0")`, `input_digit("5")` | `"5"` |
| D4 | Zero stays as zero | `input_digit("0")` | `"0"` |

### 2.2 Happy Path — Decimal Input

| ID | Description | Steps | Expected Display |
|----|-------------|-------|-----------------|
| DC1 | Basic decimal | `input_digit("3")`, `input_decimal()`, `input_digit("5")` | `"3.5"` |
| DC2 | Leading decimal | `input_decimal()`, `input_digit("5")` | `"0.5"` |

### 2.3 Happy Path — Arithmetic Operations

| ID | Description | Steps | Expected Display |
|----|-------------|-------|-----------------|
| A1 | Addition | `5 + 3 =` | `"8"` |
| A2 | Subtraction | `10 - 3 =` | `"7"` |
| A3 | Multiplication | `4 * 3 =` | `"12"` |
| A4 | Division | `10 / 4 =` | `"2.5"` |
| A5 | Division exact | `10 / 2 =` | `"5"` |
| A6 | Negative result | `3 - 5 =` | `"-2"` |

### 2.4 Happy Path — Clear and Backspace

| ID | Description | Steps | Expected Display |
|----|-------------|-------|-----------------|
| CL1 | Clear resets | `5 + 3`, `input_clear()` | `"0"` |
| CL2 | Clear after result | `5 + 3 =`, `input_clear()` | `"0"` |
| BS1 | Backspace digit | `input_digit("1")`, `input_digit("2")`, `input_backspace()` | `"1"` |
| BS2 | Backspace to zero | `input_digit("5")`, `input_backspace()` | `"0"` |

### 2.5 Edge Cases

| ID | Description | Steps | Expected Display |
|----|-------------|-------|-----------------|
| E1 | Multiple decimals ignored | `3`, `.`, `.`, `5` | `"3.5"` |
| E2 | Operator replacement | `5`, `+`, `-`, `3`, `=` | `"2"` |
| E3 | Equals with no op | `input_digit("5")`, `input_equals()` | `"5"` |
| E4 | Chained operations | `5`, `+`, `3`, `*`, (shows `8`), `2`, `=` | `"16"` |
| E5 | Repeated equals | `5`, `+`, `3`, `=`, `=`, `=` | `"8"`, `"11"`, `"14"` |
| E6 | Digit after result | `5`, `+`, `3`, `=`, `9` | `"9"` (fresh input) |
| E7 | Operator after result | `5`, `+`, `3`, `=`, `+`, `2`, `=` | `"10"` |
| E8 | Backspace on zero | `input_backspace()` | `"0"` |
| E9 | Decimal only | `input_decimal()` | `"0."` |
| E10 | Large numbers | `99999999 * 99999999 =` | `"9999999800000001"` |

### 2.6 Error Cases

| ID | Description | Steps | Expected Display |
|----|-------------|-------|-----------------|
| ER1 | Division by zero | `5`, `/`, `0`, `=` | `"Error"` |
| ER2 | Clear after error | `5 / 0 =`, `input_clear()` | `"0"` |
| ER3 | Digit after error | `5 / 0 =`, `input_digit("3")` | `"3"` |

### 2.7 Boundary Conditions

| ID | Description | Steps | Expected Display |
|----|-------------|-------|-----------------|
| B1 | Very small decimal | `0.0001 + 0.0002 =` | `"0.0003"` |
| B2 | Zero + zero | `0 + 0 =` | `"0"` |
| B3 | Multiply by zero | `5 * 0 =` | `"0"` |

## 3. Testing Business Logic Independently

All tests import only `calculator_logic.CalculatorLogic`. No Tkinter imports are needed. The test file can run in headless environments (CI servers, containers) without a display server.

Pattern for each test:
```python
def test_example(calc):
    calc.input_digit("5")
    calc.input_operator("+")
    calc.input_digit("3")
    result = calc.input_equals()
    assert result == "8"
```

## 4. Coverage Goals

| Module | Target | Method |
|--------|--------|--------|
| `calculator_logic.py` | 100% line + branch | `pytest --cov=calculator_logic --cov-branch` |
| `calculator.py` | Manual testing only | Launch app and verify visually |
