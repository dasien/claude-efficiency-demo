# Calculator Test Plan

## 1. Test Strategy

- **Unit tests** target `CalculatorLogic` directly — no GUI involvement.
- Tests use `pytest` for discovery, assertions, and fixtures.
- Each test creates a fresh `CalculatorLogic` instance via a pytest fixture.
- GUI integration testing is out of scope (Tkinter requires a display server); the architecture ensures all logic is testable via the model class.

## 2. Test Cases

### 2.1 Happy Path — Basic Operations

| ID | Description | Input Sequence | Expected Expression | Expected Result |
|----|-------------|---------------|-------------------|----------------|
| HP-1 | Single digit display | `1` | `"1"` | `"0"` |
| HP-2 | Multi-digit number | `1`, `2`, `3` | `"123"` | `"0"` |
| HP-3 | Addition | `5`, `+`, `3`, `=` | `"5+3="` | `"8"` |
| HP-4 | Subtraction | `9`, `-`, `4`, `=` | `"9-4="` | `"5"` |
| HP-5 | Multiplication | `6`, `*`, `7`, `=` | `"6*7="` | `"42"` |
| HP-6 | Division | `8`, `/`, `2`, `=` | `"8/2="` | `"4"` |
| HP-7 | Chained operations | `2`, `+`, `3`, `*`, `4`, `=` | `"2+3*4="` | `"14"` |
| HP-8 | Decimal number | `1`, `.`, `5`, `+`, `2`, `.`, `5`, `=` | `"1.5+2.5="` | `"4"` |
| HP-9 | Clear resets state | `5`, `+`, `3`, `C` | `""` | `"0"` |

### 2.2 Edge Cases

| ID | Description | Input Sequence | Expected Expression | Expected Result |
|----|-------------|---------------|-------------------|----------------|
| EC-1 | Multiple decimals in one number | `1`, `.`, `.`, `2` | `"1.2"` | `"0"` |
| EC-2 | Consecutive operators | `5`, `+`, `*` | `"5*"` | `"0"` |
| EC-3 | Equals with empty expression | `=` | `""` | `"0"` |
| EC-4 | Continue from result | `5`, `+`, `3`, `=`, `*`, `2`, `=` | `"8*2="` | `"16"` |
| EC-5 | New number after result | `5`, `+`, `3`, `=`, `9` | `"9"` | `"0"` |
| EC-6 | Clear after error | `5`, `/`, `0`, `=`, `C` | `""` | `"0"` |
| EC-7 | Digit after error | `5`, `/`, `0`, `=`, `3` | `"3"` | `"0"` |

### 2.3 Error Cases

| ID | Description | Input Sequence | Expected Result |
|----|-------------|---------------|----------------|
| ER-1 | Division by zero | `5`, `/`, `0`, `=` | `"Error"` |
| ER-2 | Division by zero (decimal) | `1`, `/`, `0`, `.`, `0`, `=` | `"Error"` |

### 2.4 Boundary Conditions

| ID | Description | Input Sequence | Validation |
|----|-------------|---------------|------------|
| BC-1 | Large numbers | `9`*10, `*`, `9`*10, `=` | Result is correct (Python handles big ints) |
| BC-2 | Small decimals | `0`, `.`, `0`, `0`, `1`, `+`, `0`, `.`, `0`, `0`, `2`, `=` | Result is `"0.003"` |
| BC-3 | Result formatting (whole) | `4`, `.`, `0`, `+`, `1`, `.`, `0`, `=` | Result is `"5"` not `"5.0"` |
| BC-4 | Result formatting (decimal) | `7`, `/`, `2`, `=` | Result is `"3.5"` |

### 2.5 Result Continuation

| ID | Description | Input Sequence | Expected Expression | Expected Result |
|----|-------------|---------------|-------------------|----------------|
| RC-1 | Operator after result | `3`, `+`, `2`, `=`, `+`, `1`, `=` | `"5+1="` | `"6"` |
| RC-2 | Digit after result starts fresh | `3`, `+`, `2`, `=`, `7` | `"7"` | `"0"` |

## 3. Testing Business Logic Independently

All tests interact only with `CalculatorLogic`:
```python
@pytest.fixture
def calc():
    return CalculatorLogic()

def test_addition(calc):
    calc.append_digit("5")
    calc.append_operator("+")
    calc.append_digit("3")
    calc.evaluate()
    assert calc.get_result() == "8"
```

No Tkinter imports, no window creation, no event simulation needed.

## 4. Coverage Goals

- **100% line coverage** of `calculator_logic.py`.
- All methods of `CalculatorLogic` tested.
- All edge cases from the requirements document covered.
- Error recovery paths (clear after error, digit after error) verified.
