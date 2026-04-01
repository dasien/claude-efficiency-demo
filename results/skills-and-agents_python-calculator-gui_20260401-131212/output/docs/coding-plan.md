# Coding Plan: Python Tkinter Calculator Application

## Overview

A desktop calculator application built with Python and Tkinter. The project follows a strict separation of concerns: pure business logic in one module, GUI presentation in another, with comprehensive tests covering the logic layer.

---

## Project Structure

```
project/
    calculator_logic.py    # Business logic (pure Python, no GUI imports)
    calculator.py          # Tkinter GUI application
    test_calculator.py     # pytest tests for CalculatorLogic
    requirements.txt       # Dependencies
```

---

## Implementation Order

### Phase 1: calculator_logic.py (build first)

**Why first:** The logic module has zero dependencies on other project files. Building it first allows the GUI to be developed against a stable, tested interface. It also enables test-driven development -- tests can be written and passing before any GUI code exists.

### Phase 2: test_calculator.py (build alongside or immediately after logic)

**Why second:** Writing tests right after (or during) logic development validates correctness before the GUI layer adds complexity. All edge cases (division by zero, sign toggling, percentage, chained operations) are caught early.

### Phase 3: calculator.py (build last)

**Why last:** The GUI depends on `calculator_logic.py`. By this point the logic is complete and tested, so GUI development focuses purely on layout, event binding, and display updates without debugging arithmetic.

### Phase 4: requirements.txt (create at any point)

**Why flexible:** This is a single-line file. It can be created at any time.

---

## File-by-File Breakdown

### requirements.txt

```
pytest
```

Single dependency. Tkinter ships with the Python standard library and does not need to be listed.

---

### calculator_logic.py

**Class:** `CalculatorLogic`

**Responsibility:** Maintain calculator state and perform all arithmetic. No GUI imports, no print statements, no side effects beyond internal state.

**State attributes:**

| Attribute         | Type  | Purpose                                      |
|-------------------|-------|----------------------------------------------|
| `current_value`   | str   | The value currently being entered/displayed  |
| `first_operand`   | float | Stored left-hand operand                     |
| `operator`        | str   | Pending operator (+, -, *, /)                |
| `should_reset`    | bool  | Whether next digit input resets the display  |

**Public methods:**

| Method                  | Description                                                  |
|-------------------------|--------------------------------------------------------------|
| `input_digit(digit)`    | Append a digit (0-9) to current_value                        |
| `input_decimal()`       | Append a decimal point if not already present                |
| `input_operator(op)`    | Store current value as first_operand, store operator, prepare for second operand |
| `calculate()`           | Execute the pending operation and return the result string   |
| `clear()`               | Reset all state to initial values                            |
| `toggle_sign()`         | Negate the current value                                     |
| `percentage()`          | Divide current value by 100                                  |
| `get_display_value()`   | Return the current string to show on the display             |

**Edge cases to handle:**

- Division by zero: return an error string (e.g., "Error") rather than raising an exception
- Multiple decimal points: ignore subsequent decimal inputs if one exists
- Chained operations: pressing an operator after a previous operation should use the last result as the first operand
- Leading zeros: "00" should display as "0"
- Toggle sign on zero: should remain "0", not "-0"
- Percentage after operator: apply percentage relative to first operand if applicable

**Estimated complexity:** Medium. Approximately 80-120 lines. The state machine for chained operations and edge case handling requires careful logic.

---

### test_calculator.py

**Framework:** pytest

**Test organization:** One test function per behavior. Group related tests with descriptive names.

**Test cases to cover:**

| Category          | Test Cases                                                        |
|-------------------|-------------------------------------------------------------------|
| Digit input       | Single digit, multiple digits, leading zero suppression           |
| Decimal input     | Adding decimal, preventing duplicate decimals                     |
| Basic operations  | Addition, subtraction, multiplication, division                   |
| Division by zero  | Returns error string, calculator remains usable after error       |
| Clear             | Resets all state                                                  |
| Toggle sign       | Positive to negative, negative to positive, zero stays zero      |
| Percentage        | Converts current value to percentage                              |
| Chained ops       | 2 + 3 + 4 produces correct running total                         |
| Equals repeat     | Pressing equals without new input behaves predictably             |
| Display value     | Verify get_display_value returns correct string after each action |

**Estimated complexity:** Low-Medium. Approximately 60-100 lines. Each test is short but there are many cases.

---

### calculator.py

**Class:** `CalculatorApp` (inherits from `tk.Tk`)

**Responsibility:** Create the window, lay out widgets in a grid, bind button clicks and key presses to `CalculatorLogic` methods, and update the display.

**Imports:**

```python
import tkinter as tk
from calculator_logic import CalculatorLogic
```

**Constructor flow:**

1. Call `super().__init__()`
2. Set window title to "Calculator"
3. Set window geometry (approximately 300x400)
4. Disable window resizing or configure grid weights for responsive layout
5. Instantiate `self.logic = CalculatorLogic()`
6. Call `self._create_widgets()`
7. Call `self._bind_events()`

**Methods:**

| Method                        | Description                                           |
|-------------------------------|-------------------------------------------------------|
| `_create_widgets()`           | Build all buttons and the display Entry widget        |
| `_bind_events()`              | Bind keyboard shortcuts (digits, operators, Enter, Escape) |
| `_on_button_click(value)`     | Route a button press to the appropriate logic method  |
| `_update_display()`           | Read from logic.get_display_value() and set the Entry |

**Estimated complexity:** Medium. Approximately 100-150 lines. The grid layout is repetitive but straightforward. Event routing logic is simple since all real computation is delegated to CalculatorLogic.

---

## Widget Layout Plan

All widgets use `grid()` layout. The main window has 4 columns and 6 rows.

### Grid Configuration

- All 4 columns have equal weight (weight=1) so buttons resize evenly
- Row 0 (display) has weight=1 to absorb extra vertical space
- All button rows (1-5) have equal weight

### Grid Map

```
+-------------------+----------+----------+----------+
| Row 0: Display (Entry)                             |
| row=0, col=0, columnspan=4, sticky="nsew"          |
+-------------------+----------+----------+----------+
| Row 1:                                             |
|  C                |   +/-    |    %     |    /     |
|  row=1,col=0      | row=1,   | row=1,   | row=1,  |
|                   | col=1    | col=2    | col=3   |
+-------------------+----------+----------+----------+
| Row 2:                                             |
|  7                |    8     |    9     |    *     |
|  row=2,col=0      | row=2,   | row=2,   | row=2,  |
|                   | col=1    | col=2    | col=3   |
+-------------------+----------+----------+----------+
| Row 3:                                             |
|  4                |    5     |    6     |    -     |
|  row=3,col=0      | row=3,   | row=3,   | row=3,  |
|                   | col=1    | col=2    | col=3   |
+-------------------+----------+----------+----------+
| Row 4:                                             |
|  1                |    2     |    3     |    +     |
|  row=4,col=0      | row=4,   | row=4,   | row=4,  |
|                   | col=1    | col=2    | col=3   |
+-------------------+----------+----------+----------+
| Row 5:                                             |
|  0 (columnspan=2)           |    .     |    =     |
|  row=5,col=0, colspan=2     | row=5,   | row=5,  |
|                              | col=2    | col=3   |
+-------------------+----------+----------+----------+
```

### Widget Details

| Widget   | Type       | Row | Column | Columnspan | Sticky | Notes                              |
|----------|------------|-----|--------|------------|--------|------------------------------------|
| Display  | tk.Entry   | 0   | 0      | 4          | nsew   | Right-aligned text, read-only state, large font |
| C        | tk.Button  | 1   | 0      | 1          | nsew   | Calls logic.clear()                |
| +/-      | tk.Button  | 1   | 1      | 1          | nsew   | Calls logic.toggle_sign()          |
| %        | tk.Button  | 1   | 2      | 1          | nsew   | Calls logic.percentage()           |
| /        | tk.Button  | 1   | 3      | 1          | nsew   | Calls logic.input_operator("/")    |
| 7        | tk.Button  | 2   | 0      | 1          | nsew   | Calls logic.input_digit("7")      |
| 8        | tk.Button  | 2   | 1      | 1          | nsew   | Calls logic.input_digit("8")      |
| 9        | tk.Button  | 2   | 2      | 1          | nsew   | Calls logic.input_digit("9")      |
| *        | tk.Button  | 2   | 3      | 1          | nsew   | Calls logic.input_operator("*")   |
| 4        | tk.Button  | 3   | 0      | 1          | nsew   | Calls logic.input_digit("4")      |
| 5        | tk.Button  | 3   | 1      | 1          | nsew   | Calls logic.input_digit("5")      |
| 6        | tk.Button  | 3   | 2      | 1          | nsew   | Calls logic.input_digit("6")      |
| -        | tk.Button  | 3   | 3      | 1          | nsew   | Calls logic.input_operator("-")   |
| 1        | tk.Button  | 4   | 0      | 1          | nsew   | Calls logic.input_digit("1")      |
| 2        | tk.Button  | 4   | 1      | 1          | nsew   | Calls logic.input_digit("2")      |
| 3        | tk.Button  | 4   | 2      | 1          | nsew   | Calls logic.input_digit("3")      |
| +        | tk.Button  | 4   | 3      | 1          | nsew   | Calls logic.input_operator("+")   |
| 0        | tk.Button  | 5   | 0      | 2          | nsew   | Calls logic.input_digit("0")      |
| .        | tk.Button  | 5   | 2      | 1          | nsew   | Calls logic.input_decimal()        |
| =        | tk.Button  | 5   | 3      | 1          | nsew   | Calls logic.calculate()            |

### Keyboard Bindings

| Key              | Action                     |
|------------------|----------------------------|
| 0-9              | input_digit()              |
| .                | input_decimal()            |
| + - * /          | input_operator()           |
| Enter or =       | calculate()                |
| Escape           | clear()                    |
| Backspace        | (optional) delete last digit |

---

## Dependencies Between Modules

```
calculator.py  --->  calculator_logic.py
     |
     v
  tkinter (stdlib)

test_calculator.py  --->  calculator_logic.py
     |
     v
   pytest (requirements.txt)
```

- `calculator_logic.py` depends on nothing (pure Python, no imports beyond stdlib math if needed)
- `calculator.py` depends on `calculator_logic.py` and `tkinter`
- `test_calculator.py` depends on `calculator_logic.py` and `pytest`
- There are no circular dependencies

---

## Complexity Summary

| Component            | Estimated Lines | Complexity | Notes                                    |
|----------------------|-----------------|------------|------------------------------------------|
| calculator_logic.py  | 80-120          | Medium     | State management and edge cases          |
| test_calculator.py   | 60-100          | Low-Medium | Many small, independent test functions   |
| calculator.py        | 100-150         | Medium     | Repetitive grid layout, simple routing   |
| requirements.txt     | 1               | Trivial    | Single dependency                        |
| **Total**            | **241-371**     | **Medium** | Well within single-developer scope       |
