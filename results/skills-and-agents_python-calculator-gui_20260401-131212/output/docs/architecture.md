# Calculator Application -- Architecture Document

**Date:** 2026-04-01
**Pattern:** Model-View-Controller (MVC)
**Language:** Python 3.x
**GUI Framework:** Tkinter

---

## 1. High-Level System Design

### 1.1 Architecture Overview

The application follows the Model-View-Controller (MVC) pattern implemented across two modules. The MVC boundaries are drawn as follows:

- **Model / Controller:** `calculator_logic.py` -- Contains the `CalculatorLogic` class, which owns all calculator state (the current expression, operands, operator, error flags) and all business logic (digit accumulation, operator handling, evaluation, clearing). This class never imports Tkinter and has no knowledge of the GUI.
- **View:** `calculator.py` -- Contains the `CalculatorApp` class, which owns the Tkinter window, all widgets, layout, styling, event binding, and display updates. It delegates every calculation-related action to a `CalculatorLogic` instance and reads back the display string to render.

### 1.2 Module Responsibilities

| Module | Class | Responsibility |
|---|---|---|
| `calculator_logic.py` | `CalculatorLogic` | Expression building, arithmetic evaluation, decimal handling, sign toggling, percentage calculation, error detection, state management |
| `calculator.py` | `CalculatorApp` | Window creation, widget layout, button rendering, keyboard binding, display synchronization, event routing to logic layer |

### 1.3 Data Flow

```
User Input (button click or keypress)
        |
        v
CalculatorApp (View)
  - Identifies the action (digit, operator, equals, clear, etc.)
  - Calls the corresponding method on CalculatorLogic
        |
        v
CalculatorLogic (Model/Controller)
  - Updates internal state (current value, pending operator, etc.)
  - Returns or exposes the new display string
        |
        v
CalculatorApp (View)
  - Reads get_display() from CalculatorLogic
  - Updates the Entry widget with the returned string
```

No data flows in the reverse direction. The logic layer never pushes updates to the view; the view always pulls the display value after each action.

---

## 2. Module Interface Definitions

### 2.1 `calculator_logic.py` -- `CalculatorLogic`

```python
class CalculatorLogic:
    """Pure business logic for a basic calculator. No GUI imports."""

    def __init__(self) -> None:
        """Initialize calculator to its default cleared state."""
        ...

    def add_digit(self, digit: str) -> None:
        """Append a digit ('0'-'9') to the current input buffer.

        Args:
            digit: A single character string, one of '0' through '9'.

        If the calculator is in an error state or has just completed
        an evaluation, this begins a new input sequence.
        """
        ...

    def add_decimal(self) -> None:
        """Append a decimal point to the current input buffer.

        If the current buffer already contains a decimal point,
        this call is ignored. If the buffer is empty or a new
        input sequence is starting, '0.' is used.
        """
        ...

    def add_operator(self, op: str) -> None:
        """Set the pending binary operator.

        Args:
            op: One of '+', '-', '*', '/'.

        If there is already a pending operator and a second operand
        has been entered, the pending operation is evaluated first
        (chaining behavior) before the new operator is stored.
        """
        ...

    def evaluate(self) -> str:
        """Evaluate the pending expression and return the display string.

        Returns:
            The string representation of the result, or an error
            message such as 'Error' for division by zero.

        After evaluation, the result becomes the first operand
        for potential chained operations.
        """
        ...

    def clear(self) -> None:
        """Reset the calculator to its initial state.

        Clears the current input buffer, pending operator,
        stored operand, and any error flags.
        """
        ...

    def toggle_sign(self) -> None:
        """Toggle the sign of the current input value between
        positive and negative. If the display is '0' or empty,
        this is a no-op.
        """
        ...

    def apply_percentage(self) -> None:
        """Divide the current input value by 100.

        Converts the current display value to its percentage
        equivalent (e.g., 50 becomes 0.5).
        """
        ...

    def get_display(self) -> str:
        """Return the current string to show on the calculator display.

        Returns:
            A string representing the current number, intermediate
            result, or error message. Integer results are returned
            without a trailing '.0' (e.g., '4' not '4.0').
        """
        ...
```

#### Internal State (private attributes, not part of public API)

| Attribute | Type | Purpose |
|---|---|---|
| `_current_input` | `str` | The digit string being built by the user |
| `_first_operand` | `float | None` | The left-hand operand of a pending operation |
| `_operator` | `str | None` | The pending binary operator (`+`, `-`, `*`, `/`) |
| `_should_reset_input` | `bool` | Flag indicating the next digit should start a new input buffer |
| `_error` | `bool` | Flag indicating the display is showing an error message |

### 2.2 `calculator.py` -- `CalculatorApp`

```python
import tkinter as tk
from tkinter import ttk
from calculator_logic import CalculatorLogic


class CalculatorApp(tk.Tk):
    """Tkinter GUI for the calculator application."""

    def __init__(self) -> None:
        """Initialize the main window, logic instance, and all widgets."""
        ...

    def _create_widgets(self) -> None:
        """Create and grid-place all GUI widgets (display, buttons)."""
        ...

    def _create_button(
        self,
        text: str,
        row: int,
        col: int,
        colspan: int = 1,
        style: str = "default"
    ) -> ttk.Button:
        """Create a single button and place it in the grid.

        Args:
            text: The button label.
            row: Grid row (0-indexed, where row 0 is the display).
            col: Grid column (0-3).
            colspan: Number of columns the button spans.
            style: Visual style category ('default', 'operator', 'special').

        Returns:
            The created Button widget.
        """
        ...

    def _bind_events(self) -> None:
        """Bind keyboard events to their handler methods."""
        ...

    def _on_button_click(self, value: str) -> None:
        """Central dispatcher for all button clicks.

        Args:
            value: The label text of the clicked button.

        Routes the value to the appropriate CalculatorLogic method
        and then refreshes the display.
        """
        ...

    def _on_key_press(self, event: tk.Event) -> None:
        """Handle keyboard input events.

        Args:
            event: The Tkinter key event.

        Maps key symbols and characters to calculator actions:
        - Digits 0-9 -> add_digit
        - +, -, *, / -> add_operator
        - . -> add_decimal
        - Return/Enter, = -> evaluate
        - Escape, c/C -> clear
        """
        ...

    def _update_display(self) -> None:
        """Read get_display() from the logic layer and write it
        to the Entry widget. Clears the Entry first, then inserts
        the new value right-aligned.
        """
        ...
```

---

## 3. GUI Layout Specification

### 3.1 Window Properties

| Property | Value |
|---|---|
| Title | "Calculator" |
| Resizable | No (fixed size) |
| Default size | Approximately 300 x 400 pixels |
| Min size | 280 x 380 pixels |

### 3.2 Widget Hierarchy

```
tk.Tk (CalculatorApp)
 |
 +-- ttk.Entry (display)
 |     - row=0, column=0, columnspan=4
 |     - state: readonly
 |     - right-justified text
 |     - large font (e.g., 24pt)
 |
 +-- ttk.Button "C"       (row=1, col=0)
 +-- ttk.Button "+/-"     (row=1, col=1)   [toggle_sign]
 +-- ttk.Button "%"       (row=1, col=2)   [apply_percentage]
 +-- ttk.Button "/"       (row=1, col=3)   [operator]
 |
 +-- ttk.Button "7"       (row=2, col=0)
 +-- ttk.Button "8"       (row=2, col=1)
 +-- ttk.Button "9"       (row=2, col=2)
 +-- ttk.Button "*"       (row=2, col=3)   [operator]
 |
 +-- ttk.Button "4"       (row=3, col=0)
 +-- ttk.Button "5"       (row=3, col=1)
 +-- ttk.Button "6"       (row=3, col=2)
 +-- ttk.Button "-"       (row=3, col=3)   [operator]
 |
 +-- ttk.Button "1"       (row=4, col=0)
 +-- ttk.Button "2"       (row=4, col=1)
 +-- ttk.Button "3"       (row=4, col=2)
 +-- ttk.Button "+"       (row=4, col=3)   [operator]
 |
 +-- ttk.Button "0"       (row=5, col=0, columnspan=2)
 +-- ttk.Button "."       (row=5, col=2)
 +-- ttk.Button "="       (row=5, col=3)   [evaluate]
```

### 3.3 Grid Configuration

- **Columns 0-3:** Each configured with `weight=1` and `uniform="btn"` so all four columns share width equally.
- **Row 0 (display):** Given a larger `minsize` or weight to ensure the display is visually prominent.
- **Rows 1-5 (buttons):** Each configured with `weight=1` so buttons stretch vertically on resize (if resizing were enabled).
- **Padding:** Each button uses `padx=1, pady=1` for minimal gutters. The display uses `padx=5, pady=(10, 5)` for visual breathing room.
- **Sticky:** All buttons use `sticky="nsew"` to fill their cells. The display uses `sticky="ew"`.

### 3.4 Visual Style Categories

| Category | Applies To | Appearance |
|---|---|---|
| Digit | 0-9 | Default button style |
| Operator | +, -, *, /, = | Distinct background color (e.g., orange) to separate arithmetic actions |
| Special | C, +/-, % | Distinct background color (e.g., light gray) to indicate utility functions |
| Display | Entry widget | Large monospace or sans-serif font, right-aligned, readonly to prevent direct editing |

---

## 4. Design Decisions and Rationale

### 4.1 Two-File Structure

**Decision:** Split the project into exactly two files: `calculator_logic.py` and `calculator.py`.

**Rationale:** This is the minimum viable separation for MVC in a small application. A single file would entangle GUI and logic, making unit testing of arithmetic behavior require Tkinter. Three or more files (e.g., a separate controller) would add indirection without meaningful benefit at this scale. Two files give us one fully testable pure-Python module and one GUI module.

### 4.2 CalculatorLogic Owns the Display String

**Decision:** The logic layer produces the formatted display string via `get_display()`, rather than returning raw numeric values for the view to format.

**Rationale:** Display formatting is a business concern in a calculator. Decisions like "show '0' not ''" and "show '3' not '3.0'" and "show 'Error' on division by zero" are logic decisions, not presentation decisions. Keeping them in the logic layer ensures consistent behavior regardless of the UI and makes them trivially testable.

### 4.3 Entry Widget in Readonly State

**Decision:** The display is a `ttk.Entry` widget set to `readonly` state, not a `Label` or an editable `Entry`.

**Rationale:** An `Entry` supports text selection (useful for copying results) and right-justification via `justify="right"`. Setting it to `readonly` prevents direct keyboard editing while still allowing programmatic updates through the `textvariable` or by toggling state for inserts. A `Label` would not support text selection.

### 4.4 Operator Chaining via Implicit Evaluation

**Decision:** When the user presses an operator while a previous operation is pending, the pending operation is evaluated first.

**Rationale:** This matches the behavior of standard pocket calculators and macOS/Windows calculator apps. The sequence `3 + 5 * 2 =` produces `16` (i.e., `(3+5)*2`), not `13`. Users of basic calculators expect left-to-right evaluation, not algebraic precedence.

### 4.5 Keyboard Input via bind on Root Window

**Decision:** Keyboard events are bound on the root `Tk` window, not on individual widgets.

**Rationale:** The calculator should respond to keyboard input regardless of which widget has focus. Binding on the root window ensures global capture. The `_on_key_press` handler maps key symbols to actions and delegates to the same logic methods as button clicks.

### 4.6 No External Dependencies

**Decision:** The application uses only the Python standard library (Tkinter).

**Rationale:** A basic calculator has no need for third-party packages. Tkinter ships with all standard CPython distributions. This eliminates dependency management and makes the application trivially portable.

---

## 5. Separation of Concerns Analysis

### 5.1 Boundary Definition

The boundary between business logic and GUI is the public interface of `CalculatorLogic`. The following table shows which concerns live where:

| Concern | Owner | Justification |
|---|---|---|
| Accumulating digits into a number string | `CalculatorLogic` | This is expression-building logic |
| Deciding whether to append or replace on digit press | `CalculatorLogic` | State-dependent logic (post-evaluate reset) |
| Performing arithmetic operations | `CalculatorLogic` | Pure computation |
| Formatting the result (int vs float display) | `CalculatorLogic` | Display semantics are a calculator concern |
| Producing error messages for invalid operations | `CalculatorLogic` | Error detection is logic |
| Creating and laying out widgets | `CalculatorApp` | Pure GUI concern |
| Translating button clicks to method calls | `CalculatorApp` | Event routing is a view concern |
| Translating key presses to method calls | `CalculatorApp` | Event routing is a view concern |
| Writing the display string into the Entry widget | `CalculatorApp` | Widget manipulation is a GUI concern |
| Visual styling (colors, fonts, padding) | `CalculatorApp` | Presentation concern |

### 5.2 Testability Implications

Because `CalculatorLogic` has zero GUI dependencies, it can be tested entirely with standard `unittest` or `pytest` assertions:

```python
def test_addition():
    calc = CalculatorLogic()
    calc.add_digit("3")
    calc.add_operator("+")
    calc.add_digit("4")
    result = calc.evaluate()
    assert result == "7"

def test_division_by_zero():
    calc = CalculatorLogic()
    calc.add_digit("5")
    calc.add_operator("/")
    calc.add_digit("0")
    result = calc.evaluate()
    assert result == "Error"
```

No Tkinter window needs to be instantiated, no event loop needs to run, and no display needs to be rendered. This is the primary benefit of the separation.

---

## 6. Error Handling Strategy

### 6.1 Categories of Errors

| Error Condition | Detection Point | User-Facing Behavior |
|---|---|---|
| Division by zero | `evaluate()` in `CalculatorLogic` | Display shows "Error" |
| Overflow (extremely large results) | `evaluate()` in `CalculatorLogic` | Display shows "Error" |
| Invalid float conversion | `evaluate()` in `CalculatorLogic` | Display shows "Error" |
| Multiple decimal points | `add_decimal()` in `CalculatorLogic` | Input silently ignored |
| Operator with no operand | `add_operator()` in `CalculatorLogic` | Operator replaces previous or uses current display as first operand |
| Equals with incomplete expression | `evaluate()` in `CalculatorLogic` | Displays current value unchanged |

### 6.2 Error State Management

When `evaluate()` encounters an error (division by zero, overflow, etc.):

1. The `_error` flag is set to `True`.
2. `get_display()` returns the string `"Error"`.
3. Any subsequent digit input (`add_digit`) clears the error state and begins fresh input.
4. Any subsequent `clear()` call resets the entire calculator.
5. Operator presses while in error state are ignored.

### 6.3 Implementation Approach

Errors are caught using Python's standard exception handling within `evaluate()`:

```python
def evaluate(self) -> str:
    try:
        result = self._compute(self._first_operand, self._operator, second)
        # Format and store result
    except ZeroDivisionError:
        self._error = True
        return "Error"
    except (OverflowError, ValueError):
        self._error = True
        return "Error"
```

The logic layer never raises exceptions to the GUI layer. All error conditions are trapped internally and expressed as display strings. This means the GUI layer does not need try/except blocks around logic calls.

---

## 7. Event Handling Design

### 7.1 Button Click Flow

Each button is created with a `command` parameter bound to a lambda or partial that calls `_on_button_click(value)`:

```python
button = ttk.Button(
    self,
    text="7",
    command=lambda v="7": self._on_button_click(v)
)
```

The `_on_button_click` method acts as a dispatcher:

```
_on_button_click(value):
    if value is a digit (0-9):
        self.logic.add_digit(value)
    elif value is an operator (+, -, *, /):
        self.logic.add_operator(value)
    elif value == ".":
        self.logic.add_decimal()
    elif value == "=":
        self.logic.evaluate()
    elif value == "C":
        self.logic.clear()
    elif value == "+/-":
        self.logic.toggle_sign()
    elif value == "%":
        self.logic.apply_percentage()

    self._update_display()
```

Every code path ends with `_update_display()`, which reads `get_display()` and writes the result to the Entry widget. This guarantees the display is always synchronized with the logic state.

### 7.2 Keyboard Input Mapping

Keyboard events are bound on the root window in `_bind_events()`:

```python
def _bind_events(self) -> None:
    self.bind("<Key>", self._on_key_press)
```

The `_on_key_press` handler maps keys as follows:

| Key(s) | Action |
|---|---|
| `0` - `9` (keysym or char) | `add_digit(char)` |
| `+`, `-`, `*`, `/` | `add_operator(char)` |
| `.` | `add_decimal()` |
| `Return`, `KP_Enter`, `=` | `evaluate()` |
| `Escape`, `c`, `C` | `clear()` |
| `BackSpace` | Remove last character from input (optional enhancement) |

After dispatching, `_on_key_press` calls `_update_display()` and returns `"break"` to prevent the keystroke from propagating to the Entry widget (which is readonly but should not receive focus-driven input).

### 7.3 State Management Summary

All mutable state resides in `CalculatorLogic`. The GUI layer holds no calculator state of its own -- it is purely reactive. The state transitions within `CalculatorLogic` follow this model:

```
                         add_digit()
    CLEARED  --------------------------->  BUILDING_INPUT
       ^                                       |
       |  clear()                              | add_operator()
       |                                       v
       |                                OPERATOR_PENDING
       |                                       |
       |                                       | add_digit()
       |                                       v
       |                                BUILDING_SECOND_INPUT
       |                                       |
       |         evaluate()                    | evaluate()
       |<--------------------------------------+--------> RESULT_DISPLAYED
       |                                                      |
       |  clear()                             add_operator()  |
       |<-------------------------+                           |
                                  |                           v
                                  +--- OPERATOR_PENDING <-----+
                                        (chaining)

    Any state --[error]--> ERROR_STATE --[add_digit or clear]--> CLEARED/BUILDING_INPUT
```

This state machine is implicit in the flag values (`_should_reset_input`, `_error`, `_operator`, `_first_operand`) rather than implemented as an explicit enum. This is appropriate for the small number of states involved.

---

## 8. File Structure

```
project/
    calculator_logic.py    # CalculatorLogic class (pure Python, no GUI)
    calculator.py          # CalculatorApp class (Tkinter GUI, imports calculator_logic)
    test_calculator.py     # Unit tests for CalculatorLogic (no GUI required)
```

`calculator.py` serves as the application entry point:

```python
if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
```

No `requirements.txt` is needed as the application uses only the Python standard library.
