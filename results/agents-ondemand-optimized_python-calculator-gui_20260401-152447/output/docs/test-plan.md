# Test Plan: Python Tkinter GUI Calculator

**Date:** 2026-04-01
**Version:** 1.0

---

## 1. Test Strategy

### Approach

All automated tests target the `CalculatorLogic` class in `calculator_logic.py`. Because business logic is fully separated from the GUI (see `docs/architecture.md`), the logic can be tested by importing the class directly and calling its methods -- no Tkinter instantiation needed.

### What We Test

- **CalculatorLogic** -- All public methods: `append_to_expression()`, `evaluate()`, `clear()`, `get_expression()`.

### What We Do Not Test (Automated)

- **CalculatorApp (GUI)** -- Tkinter widget creation, layout, and rendering. These are verified through manual testing. The GUI is a thin layer that delegates to CalculatorLogic, so automated logic tests provide high confidence.

### Framework and Tools

- **pytest** as the test framework.
- **pytest.mark.parametrize** for testing multiple inputs with the same logic.
- No additional dependencies required.

### Running Tests

```bash
python3 -m pytest test_calculator.py -v
python3 -m pytest test_calculator.py -v --tb=short
python3 -m pytest test_calculator.py -k "test_division" -v
```

---

## 2. How to Test Business Logic Independently

The `CalculatorLogic` class has no GUI dependencies. Testing it requires only:

```python
from calculator_logic import CalculatorLogic

def test_example():
    logic = CalculatorLogic()
    logic.append_to_expression("2")
    logic.append_to_expression("+")
    logic.append_to_expression("3")
    result = logic.evaluate()
    assert result == "5"
```

Each test creates a fresh `CalculatorLogic` instance, builds an expression by calling `append_to_expression()` for each character, then calls `evaluate()` and asserts the result string. This pattern is used throughout.

### Helper Pattern

For readability, tests can use a helper to build expressions from a string:

```python
def build_expression(logic: CalculatorLogic, expr: str) -> None:
    """Append each character in expr to the logic instance."""
    for char in expr:
        logic.append_to_expression(char)
```

---

## 3. Test Cases

### 3.1 Happy Path -- Basic Operations

| Test Case ID | Description                          | Input Expression | Expected Result | Category   |
|--------------|--------------------------------------|------------------|-----------------|------------|
| HP-01        | Addition of two integers             | "2+3"            | "5"             | Happy path |
| HP-02        | Subtraction of two integers          | "9-4"            | "5"             | Happy path |
| HP-03        | Multiplication of two integers       | "6*7"            | "42"            | Happy path |
| HP-04        | Division of two integers (exact)     | "8/2"            | "4"             | Happy path |
| HP-05        | Division producing a float           | "7/2"            | "3.5"           | Happy path |
| HP-06        | Multi-digit numbers                  | "12+34"          | "46"            | Happy path |
| HP-07        | Floating-point addition              | "1.5+2.5"        | "4"             | Happy path |
| HP-08        | Floating-point subtraction           | "5.5-2.3"        | "3.2"           | Happy path |
| HP-09        | Mixed integer and float              | "3+1.5"          | "4.5"           | Happy path |
| HP-10        | Multiple operations                  | "2+3*4"          | "14"            | Happy path |
| HP-11        | Multiple additions                   | "1+2+3+4"        | "10"            | Happy path |
| HP-12        | Operator precedence (* before +)     | "2+3*4"          | "14"            | Happy path |
| HP-13        | Operator precedence (/ before -)     | "10-6/3"         | "8"             | Happy path |
| HP-14        | Single digit evaluation              | "5"              | "5"             | Happy path |
| HP-15        | Zero                                 | "0"              | "0"             | Happy path |

### 3.2 Expression Building

| Test Case ID | Description                          | Action Sequence               | Expected Display | Category   |
|--------------|--------------------------------------|-------------------------------|------------------|------------|
| EB-01        | Append single digit                  | append("5")                   | "5"              | Building   |
| EB-02        | Append multiple digits               | append("1"), append("2")      | "12"             | Building   |
| EB-03        | Append digit then operator           | append("5"), append("+")      | "5+"             | Building   |
| EB-04        | Append decimal                       | append("1"), append(".")      | "1."             | Building   |
| EB-05        | Build full expression                | append each char of "12+34"   | "12+34"          | Building   |
| EB-06        | get_expression returns current state | append("7"), get_expression() | "7"              | Building   |

### 3.3 Clear Functionality

| Test Case ID | Description                          | Action Sequence                          | Expected Result | Category |
|--------------|--------------------------------------|------------------------------------------|-----------------|----------|
| CL-01        | Clear empties expression             | append("123"), clear()                   | ""              | Clear    |
| CL-02        | Clear after partial expression       | append("5+"), clear()                    | ""              | Clear    |
| CL-03        | Clear after evaluation               | append("2+3"), evaluate(), clear()       | ""              | Clear    |
| CL-04        | Clear after error                    | append("5/0"), evaluate(), clear()       | ""              | Clear    |
| CL-05        | Input works after clear              | append("5"), clear(), append("3"), eval  | "3"             | Clear    |
| CL-06        | Input works after error then clear   | append("1/0"), eval, clear, append("2+3"), eval | "5"     | Clear    |

### 3.4 Result Chaining

| Test Case ID | Description                          | Action Sequence                              | Expected Result | Category |
|--------------|--------------------------------------|----------------------------------------------|-----------------|----------|
| RC-01        | Operator after result                | "2+3" -> eval -> append("+") -> append("4") -> eval | "9"     | Chaining |
| RC-02        | Digit after result starts fresh      | "2+3" -> eval -> append("7")                 | "57" or "7"     | Chaining |
| RC-03        | Multiple chains                      | "1+1" -> eval -> "+1" -> eval -> "+1" -> eval| "4"             | Chaining |

Note: The behavior for RC-02 (digit after result) should be defined in implementation -- either appending to the result string or starting fresh. The test should match whichever behavior is implemented.

### 3.5 Edge Cases

| Test Case ID | Description                          | Input Expression | Expected Result | Category   |
|--------------|--------------------------------------|------------------|-----------------|------------|
| EC-01        | Division by zero                     | "5/0"            | "Error"         | Edge case  |
| EC-02        | Division by zero in complex expr     | "3+5/0"          | "Error"         | Edge case  |
| EC-03        | Empty expression evaluation          | "" (just eval)   | "Error" or ""   | Edge case  |
| EC-04        | Consecutive operators                | "5++3"           | "Error"         | Edge case  |
| EC-05        | Trailing operator                    | "5+"             | "Error"         | Edge case  |
| EC-06        | Leading operator (plus)              | "+5"             | "5" or "Error"  | Edge case  |
| EC-07        | Leading operator (minus/negative)    | "-5"             | "-5" or "Error" | Edge case  |
| EC-08        | Multiple decimal points              | "1.2.3"          | "Error"         | Edge case  |
| EC-09        | Decimal without leading digit        | ".5+.5"          | "1" or "Error"  | Edge case  |
| EC-10        | Operator only                        | "+"              | "Error"         | Edge case  |
| EC-11        | Multiple operators in a row          | "5*/3"           | "Error"         | Edge case  |

### 3.6 Boundary Conditions

| Test Case ID | Description                          | Input Expression        | Expected Result       | Category  |
|--------------|--------------------------------------|-------------------------|-----------------------|-----------|
| BC-01        | Very large result                    | "999999999*999999999"   | "999999998000000001"  | Boundary  |
| BC-02        | Very small float                     | "0.0000001+0.0000002"  | "3e-07" or "0.0000003"| Boundary  |
| BC-03        | Result is exactly zero               | "5-5"                   | "0"                   | Boundary  |
| BC-04        | Negative result                      | "3-7"                   | "-4"                  | Boundary  |
| BC-05        | Long expression                      | "1+1+1+1+1+1+1+1+1+1"  | "10"                  | Boundary  |
| BC-06        | Floating-point whole number result   | "2.0+3.0"              | "5"                   | Boundary  |
| BC-07        | Divide to many decimal places        | "10/3"                  | "3.3333333333333335" (or similar) | Boundary |
| BC-08        | Multiply by zero                     | "12345*0"              | "0"                   | Boundary  |
| BC-09        | Add zero                             | "42+0"                 | "42"                  | Boundary  |

### 3.7 Error Recovery

| Test Case ID | Description                          | Action Sequence                          | Expected Result | Category |
|--------------|--------------------------------------|------------------------------------------|-----------------|----------|
| ER-01        | Error then clear then valid expr     | "1/0" -> eval -> clear -> "2+3" -> eval  | "5"             | Recovery |
| ER-02        | Multiple errors then recovery        | "a" -> eval -> clear -> "/0" -> eval -> clear -> "4+4" -> eval | "8" | Recovery |
| ER-03        | Clear during error shows empty       | "5/0" -> eval -> clear                   | ""              | Recovery |

---

## 4. Parametrized Test Suggestions

The following groups of test cases are ideal for `@pytest.mark.parametrize`:

### Basic Operations (parametrized)

```python
@pytest.mark.parametrize("expression, expected", [
    ("2+3", "5"),
    ("9-4", "5"),
    ("6*7", "42"),
    ("8/2", "4"),
    ("7/2", "3.5"),
    ("2+3*4", "14"),
    ("10-6/3", "8"),
    ("1+2+3+4", "10"),
])
def test_basic_operations(expression: str, expected: str) -> None:
    logic = CalculatorLogic()
    for char in expression:
        logic.append_to_expression(char)
    assert logic.evaluate() == expected
```

### Error Cases (parametrized)

```python
@pytest.mark.parametrize("expression", [
    "5/0",
    "5++3",
    "5+",
    "+",
    "5*/3",
    "1.2.3",
])
def test_error_cases(expression: str) -> None:
    logic = CalculatorLogic()
    for char in expression:
        logic.append_to_expression(char)
    assert logic.evaluate() == "Error"
```

---

## 5. Coverage Goals

| Component             | Target Coverage | Notes                                          |
|-----------------------|-----------------|-------------------------------------------------|
| `calculator_logic.py` | 100%            | All methods, all branches, all error paths.    |
| `calculator.py`       | Not measured     | GUI code is tested manually, not automated.    |

### Coverage Measurement

```bash
python3 -m pytest test_calculator.py -v --cov=calculator_logic --cov-report=term-missing
```

### Definition of Done

- All test cases in this plan are implemented and passing.
- Coverage of `calculator_logic.py` is 100% (line and branch).
- No test depends on another test's state (all tests use fresh `CalculatorLogic` instances).
- Tests run in under 1 second total.

---

## 6. Manual Testing Checklist (GUI)

These items require manual verification since they involve Tkinter rendering and interaction:

- [ ] Window opens with title "Calculator".
- [ ] Display is visible at the top, spanning full width.
- [ ] All 16 buttons are visible and labeled correctly.
- [ ] Clicking number buttons updates the display.
- [ ] Clicking operator buttons updates the display.
- [ ] Clicking "=" evaluates and shows the result.
- [ ] Clicking "C" clears the display.
- [ ] Keyboard digits 0-9 work.
- [ ] Keyboard operators +, -, *, / work.
- [ ] Keyboard Enter triggers evaluation.
- [ ] Keyboard Escape or Backspace triggers clear.
- [ ] Window resizes and buttons scale proportionally.
- [ ] Error messages ("Error") appear in the display, not as pop-ups or crashes.
- [ ] After an error, pressing "C" restores normal operation.
