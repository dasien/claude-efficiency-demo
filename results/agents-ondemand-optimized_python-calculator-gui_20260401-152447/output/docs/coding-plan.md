# Coding Plan: Python Tkinter GUI Calculator

**Date:** 2026-04-01
**Version:** 1.0

---

## 1. Implementation Order

The modules are built in dependency order: foundational logic first, then the GUI that depends on it, then tests that validate the logic.

| Order | Module                  | Rationale                                                     |
|-------|-------------------------|---------------------------------------------------------------|
| 1     | `calculator_logic.py`   | Pure logic with no dependencies. Must exist before the GUI can use it. Can be tested immediately after creation. |
| 2     | `test_calculator.py`    | Validates calculator_logic.py before building the GUI on top of it. Catches logic bugs early. |
| 3     | `calculator.py`         | Depends on calculator_logic.py. Built last because it integrates the logic into the GUI. |

---

## 2. File-by-File Breakdown

### 2.1 calculator_logic.py

**Purpose:** All calculator business logic. No GUI imports.

**Contents:**

```
class CalculatorLogic:
    - __init__(self) -> None
        Initialize self.expression = ""

    - append_to_expression(self, value: str) -> str
        Append a digit, operator, or decimal to the expression.
        Return the updated expression string.

    - evaluate(self) -> str
        Evaluate the expression using a safe eval approach.
        Sanitize input (only allow 0-9, ., +, -, *, /, spaces, parentheses).
        On success: return result as string (integer format if whole number).
        On failure: set expression to "Error" and return "Error".

    - clear(self) -> str
        Reset expression to "".
        Return "".

    - get_expression(self) -> str
        Return the current expression string.
```

**Key Implementation Details:**
- Expression sanitization: verify all characters in expression are in the allowed set before calling `eval()`.
- Result formatting: if `result == int(result)`, return `str(int(result))`, else return `str(result)`.
- After evaluation, store the result string as the new expression so it can be used for chaining.
- After an error, the expression is set to "" internally so that the next input starts fresh (or the user presses C).

**Estimated Complexity:** Low. Approximately 40-60 lines of code.

---

### 2.2 test_calculator.py

**Purpose:** Unit tests for CalculatorLogic using pytest.

**Contents:**

```
import pytest
from calculator_logic import CalculatorLogic

class TestBasicOperations:
    - test_addition
    - test_subtraction
    - test_multiplication
    - test_division
    - test_integer_result_display
    - test_float_result_display

class TestExpressionBuilding:
    - test_append_single_digit
    - test_append_multiple_digits
    - test_append_operator
    - test_append_decimal
    - test_build_full_expression

class TestEdgeCases:
    - test_division_by_zero
    - test_empty_expression
    - test_consecutive_operators
    - test_trailing_operator
    - test_leading_operator
    - test_multiple_decimal_points
    - test_very_large_numbers
    - test_very_small_numbers

class TestClear:
    - test_clear_resets_expression
    - test_clear_after_error

class TestChaining:
    - test_chain_after_result
    - test_operator_after_result

Parametrized tests for operator coverage.
```

**Estimated Complexity:** Medium. Approximately 100-150 lines of code.

---

### 2.3 calculator.py

**Purpose:** Tkinter GUI. Entry point for the application.

**Contents:**

```
import tkinter as tk
from tkinter import ttk
from calculator_logic import CalculatorLogic

class CalculatorApp(tk.Tk):
    - __init__(self) -> None
        Call super().__init__()
        Set title, geometry, min size.
        Create self.logic = CalculatorLogic()
        Create self.display_var = tk.StringVar()
        Call _create_widgets()
        Call _bind_events()

    - _create_widgets(self) -> None
        Create display Entry (row 0, columnspan 4).
        Create button grid (rows 1-5) using nested loop over BUTTON_LAYOUT.
        Configure row/column weights.

    - _bind_events(self) -> None
        Bind <Key> event on root for keyboard input.

    - _on_button_click(self, value: str) -> None
        Route to logic.append_to_expression(), logic.evaluate(), or logic.clear().
        Call _update_display() with the result.

    - _on_key_press(self, event: tk.Event) -> None
        Map keyboard characters and keysyms to _on_button_click() calls.

    - _update_display(self, text: str) -> None
        Set self.display_var to the given text.

BUTTON_LAYOUT constant:
    [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"],
        ["C"]   # spans 4 columns
    ]

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
```

**Estimated Complexity:** Medium. Approximately 80-120 lines of code.

---

## 3. Dependencies Between Modules

```
calculator.py  ----imports---->  calculator_logic.py
test_calculator.py  ----imports---->  calculator_logic.py
```

- `calculator_logic.py` has **zero dependencies** (no imports from other project files, no third-party packages).
- `calculator.py` depends on `calculator_logic.py` and `tkinter` (standard library).
- `test_calculator.py` depends on `calculator_logic.py` and `pytest`.

There are no circular dependencies.

---

## 4. Widget Layout Plan

### Button Grid (4-column layout)

All buttons use `sticky="nsew"` so they expand to fill their grid cell.

```
Row 0:  [         Display Entry (columnspan=4)         ]
Row 1:  [ 7 (0,0) ] [ 8 (0,1) ] [ 9 (0,2) ] [ / (0,3) ]
Row 2:  [ 4 (1,0) ] [ 5 (1,1) ] [ 6 (1,2) ] [ * (1,3) ]
Row 3:  [ 1 (2,0) ] [ 2 (2,1) ] [ 3 (2,2) ] [ - (2,3) ]
Row 4:  [ 0 (3,0) ] [ . (3,1) ] [ = (3,2) ] [ + (3,3) ]
Row 5:  [              C (columnspan=4)                  ]
```

Note: Grid row numbers in the actual code are offset by 1 because the display occupies row 0.

### Button Creation Strategy

Use a nested loop over `BUTTON_LAYOUT` to create buttons programmatically:

```python
BUTTON_LAYOUT = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
]

for row_idx, row in enumerate(BUTTON_LAYOUT):
    for col_idx, label in enumerate(row):
        btn = ttk.Button(frame, text=label,
                         command=lambda v=label: self._on_button_click(v))
        btn.grid(row=row_idx + 1, column=col_idx, sticky="nsew", padx=1, pady=1)

# Clear button separately (spans all columns)
clear_btn = ttk.Button(frame, text="C",
                       command=lambda: self._on_button_click("C"))
clear_btn.grid(row=5, column=0, columnspan=4, sticky="nsew", padx=1, pady=1)
```

### Column and Row Weight Configuration

```python
for col in range(4):
    self.columnconfigure(col, weight=1)
for row in range(1, 6):  # button rows
    self.rowconfigure(row, weight=1)
self.rowconfigure(0, weight=0)  # display row: fixed height
```

---

## 5. Estimated Complexity Per Component

| Component             | Lines of Code | Complexity | Notes                                       |
|-----------------------|---------------|------------|---------------------------------------------|
| `calculator_logic.py` | 40-60         | Low        | Simple string manipulation and eval.        |
| `calculator.py`       | 80-120        | Medium     | Grid layout, event binding, widget creation.|
| `test_calculator.py`  | 100-150       | Medium     | Many test cases, but each is simple.        |
| **Total**             | **220-330**   | Low-Medium | Small project, clean separation.            |

### Risk Areas

| Risk                          | Mitigation                                               |
|-------------------------------|----------------------------------------------------------|
| `eval()` safety               | Strict character whitelist before evaluation.            |
| Floating-point display quirks | Format results: use int display when result is whole.    |
| Keyboard focus issues         | Bind keys on root window, not individual widgets.        |
| State after error              | Clear resets all state; error sets expression to "Error". |
