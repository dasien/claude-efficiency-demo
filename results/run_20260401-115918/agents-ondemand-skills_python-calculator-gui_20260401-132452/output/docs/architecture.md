# Calculator Application -- Architecture Document

## 1. High-Level System Design

### 1.1 Pattern: Model-View-Controller (MVC)

The application follows an MVC pattern split across two files:

| Role       | File                  | Responsibility                                      |
|------------|-----------------------|-----------------------------------------------------|
| Model      | `calculator_logic.py` | Expression building, evaluation, state management   |
| View       | `calculator.py`       | Tkinter GUI layout, display rendering               |
| Controller | `calculator.py`       | Routes user input (clicks, keys) to model methods   |

The View and Controller are combined in a single file because, for an application this small, separating them into three files would add indirection without meaningful benefit. The critical separation -- business logic from GUI -- is preserved by isolating the model.

### 1.2 Data Flow

```
User Input (click / keypress)
        |
        v
CalculatorApp (View+Controller)
  - identifies the action (digit, operator, equals, clear)
  - calls the appropriate method on CalculatorLogic
        |
        v
CalculatorLogic (Model)
  - updates internal expression state
  - returns the current display string
        |
        v
CalculatorApp (View+Controller)
  - updates the Entry widget with the returned display string
```

All data flows in one direction through the controller. The model never imports `tkinter` and never writes to the display directly. The controller reads the model's state after each operation and pushes it to the view.

### 1.3 Module Dependency Graph

```
calculator.py  --->  calculator_logic.py
     |
     v
  tkinter (stdlib)
```

`calculator_logic.py` has zero dependencies beyond the Python standard library (no `tkinter`). This is a hard constraint that enables independent unit testing.

---

## 2. Module Interface Definitions

### 2.1 Model -- `calculator_logic.py`

```python
class CalculatorLogic:
    """Manages calculator expression state and evaluation.

    The expression is built incrementally as the user presses buttons.
    It is stored as a string (e.g. "12.5+3") and evaluated on demand.
    """

    def __init__(self) -> None:
        """Initialize with an empty expression and no error state."""
        ...

    def get_display(self) -> str:
        """Return the current string to show in the display.

        Returns:
            The current expression string, or "0" if the expression is empty.
        """
        ...

    def append_digit(self, digit: str) -> str:
        """Append a digit character ('0'-'9') to the expression.

        Args:
            digit: A single character string, one of '0' through '9'.

        Returns:
            The updated display string.
        """
        ...

    def append_decimal(self) -> str:
        """Append a decimal point to the current number in the expression.

        If the current number already contains a decimal point, this is a
        no-op. If the expression is empty or ends with an operator, '0.' is
        appended.

        Returns:
            The updated display string.
        """
        ...

    def append_operator(self, operator: str) -> str:
        """Append an arithmetic operator to the expression.

        Args:
            operator: One of '+', '-', '*', '/'.

        If the expression already ends with an operator, the previous
        operator is replaced. If the expression is empty, this is a no-op
        (except for '-', which starts a negative number).

        Returns:
            The updated display string.
        """
        ...

    def evaluate(self) -> str:
        """Evaluate the current expression and return the result.

        On success, the expression is replaced with the result so the user
        can continue calculating from that value.

        On failure (e.g. division by zero, malformed expression), an error
        message string is returned and the error flag is set. The next
        digit or clear operation resets the state.

        Returns:
            The result as a display string, or an error message such as
            "Error" or "Division by zero".
        """
        ...

    def clear(self) -> str:
        """Reset the calculator to its initial empty state.

        Returns:
            The display string after clearing (always "0").
        """
        ...

    def has_error(self) -> bool:
        """Return True if the last evaluation produced an error."""
        ...
```

### 2.2 View + Controller -- `calculator.py`

```python
import tkinter as tk
from tkinter import ttk
from calculator_logic import CalculatorLogic


class CalculatorApp(tk.Tk):
    """Tkinter-based calculator GUI.

    Creates the window, display, and button grid. Routes all user
    interactions to the CalculatorLogic model and updates the display
    with the result.
    """

    def __init__(self) -> None:
        """Initialize the main window, model, widgets, and event bindings."""
        ...

    def _create_widgets(self) -> None:
        """Build the display Entry and the button grid."""
        ...

    def _bind_events(self) -> None:
        """Bind keyboard events to calculator actions.

        Bindings:
            '0'-'9'     -> append_digit
            '.'         -> append_decimal
            '+','-','*','/' -> append_operator
            '<Return>', '=' -> evaluate
            '<Escape>', 'c', 'C' -> clear
            '<BackSpace>' -> (optional) delete last character
        """
        ...

    def _on_digit(self, digit: str) -> None:
        """Handle a digit button press or key press."""
        ...

    def _on_operator(self, operator: str) -> None:
        """Handle an operator button press or key press."""
        ...

    def _on_decimal(self) -> None:
        """Handle the decimal point button press or key press."""
        ...

    def _on_equals(self) -> None:
        """Handle the equals button press or Return key press."""
        ...

    def _on_clear(self) -> None:
        """Handle the clear button press or Escape key press."""
        ...

    def _update_display(self, text: str) -> None:
        """Replace the contents of the display Entry with the given text.

        Args:
            text: The string to display. If it is an error message,
                  the display color may change to indicate the error.
        """
        ...


def main() -> None:
    """Entry point. Instantiate CalculatorApp and start the Tkinter mainloop."""
    app = CalculatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
```

---

## 3. GUI Layout Specification

### 3.1 Window Properties

| Property    | Value              |
|-------------|--------------------|
| Title       | "Calculator"       |
| Geometry    | 300 x 400 pixels   |
| Resizable   | Yes (both axes)    |
| Min size     | 250 x 350 pixels   |

### 3.2 Widget Hierarchy

```
CalculatorApp (tk.Tk)
  |
  +-- main_frame (ttk.Frame, padded container)
       |
       +-- display (ttk.Entry, read-only, row=0, columnspan=4)
       |
       +-- button_frame (ttk.Frame, row=1, columnspan=4)
            |
            +-- 20 buttons arranged in a 5-row x 4-column grid
```

### 3.3 Button Grid Layout

The button grid uses `grid()` geometry management. All columns have equal weight so they expand uniformly on resize. All buttons use `sticky="nsew"` to fill their cells.

```
Row 0:  [ C ]  [ (reserved) ]  [ (reserved) ]  [ / ]
Row 1:  [ 7 ]  [ 8 ]           [ 9 ]           [ * ]
Row 2:  [ 4 ]  [ 5 ]           [ 6 ]           [ - ]
Row 3:  [ 1 ]  [ 2 ]           [ 3 ]           [ + ]
Row 4:  [ 0 (colspan=2) ]      [ . ]           [ = ]
```

The reserved cells in Row 0 can remain empty or hold future features (e.g., backspace, sign toggle). The `0` button spans two columns to follow standard calculator convention.

### 3.4 Display Widget

- Widget type: `ttk.Entry`
- State: `readonly` (prevents direct typing; all input goes through event handlers)
- Font: Monospaced, large (e.g., `("Courier", 20)`)
- Text alignment: Right-justified (`justify="right"`)
- Spans all 4 columns at the top of the grid

---

## 4. Design Decisions and Rationale

### 4.1 Two Files, Not One or Three

**Decision**: Split into `calculator.py` and `calculator_logic.py`.

**Rationale**: A single file mixes testable logic with Tkinter code, making unit tests require a display server. Three files (separate view, controller, model) is unnecessary overhead for an application with one screen and five actions. Two files provide the critical benefit (testable model) without the cost of over-engineering.

### 4.2 String-Based Expression Building

**Decision**: The model builds the expression as a string (e.g., `"12+34.5"`) rather than using a token list or AST.

**Rationale**: For a four-function calculator, string concatenation is the simplest representation. Python's `eval()` (or a safe equivalent) can evaluate it directly. A token list or tree structure would be warranted for operator precedence beyond `*/+-`, parentheses, or multi-step undo, none of which are requirements here.

### 4.3 Model Returns Display Strings

**Decision**: Every model method returns the string to display, rather than requiring the controller to separately call `get_display()`.

**Rationale**: This reduces the chance of the view falling out of sync with the model. Every mutation returns the new state in a single call. The controller pattern becomes uniform: `self._update_display(self.logic.some_method(arg))`.

### 4.4 Error State as a Flag, Not an Exception

**Decision**: `evaluate()` returns an error string (e.g., `"Error"`) and sets an internal flag, rather than raising an exception.

**Rationale**: The controller does not need branching logic for error handling. It always does the same thing: display whatever string the model returns. The flag allows the model to auto-clear on the next digit input, which is standard calculator behavior. Exceptions would force try/except in every controller handler.

### 4.5 Safe Evaluation Instead of Raw `eval()`

**Decision**: The model must sanitize or restrict the expression before evaluating it. The recommended approach is to validate that the expression contains only digits, decimal points, and the four operators, then use `eval()` on the validated string. An alternative is to implement a simple parser.

**Rationale**: Raw `eval()` on arbitrary strings is a security risk in general-purpose applications. For this calculator, the expression is built character by character through the model's public API, so it is already constrained. An explicit validation step before `eval()` provides defense in depth.

---

## 5. Separation of Concerns Analysis

### 5.1 What the Model Knows

- The current expression string
- Whether an error has occurred
- Rules for valid expression construction (e.g., no double decimals)
- How to evaluate an arithmetic expression

### 5.2 What the Model Does NOT Know

- That Tkinter exists
- How the display renders text
- What buttons exist or how they are laid out
- Whether input comes from mouse clicks or keyboard
- Window dimensions, fonts, colors, or any visual property

### 5.3 What the View/Controller Knows

- How to create and arrange Tkinter widgets
- How to bind keyboard events to handler methods
- That a `CalculatorLogic` instance exists and has specific methods

### 5.4 What the View/Controller Does NOT Know

- How expressions are stored internally
- How evaluation works
- Any arithmetic rules

### 5.5 Testing Implications

Because of this separation:

- **`calculator_logic.py`** can be tested with plain `pytest` in a headless environment. No display server, no Tkinter imports, no GUI fixtures. Example:

  ```python
  def test_addition():
      logic = CalculatorLogic()
      logic.append_digit("2")
      logic.append_operator("+")
      logic.append_digit("3")
      assert logic.evaluate() == "5"
  ```

- **`calculator.py`** can be tested for layout and integration with `tkinter.Tk()` fixtures if desired, but this is optional. The critical business logic is already covered by model tests.

---

## 6. Error Handling Strategy

### 6.1 Error Sources

| Error Condition        | Example Input   | Model Behavior                          |
|------------------------|-----------------|-----------------------------------------|
| Division by zero       | `5/0=`          | Return `"Division by zero"`             |
| Malformed expression   | `5+=` (edge)    | Return `"Error"`                        |
| Overflow               | Very large nums | Return `"Error"` or scientific notation |

### 6.2 Error Display

Errors are shown in the same display Entry widget used for normal output. No dialog boxes or pop-ups are used for calculation errors. This keeps the interaction flow uninterrupted.

When the model's `has_error()` returns `True`, the controller may optionally change the display text color to red (via `ttk.Style` or direct widget configuration) to provide a visual cue.

### 6.3 Error Recovery

After an error state:

- Pressing any **digit** clears the error and starts a new expression with that digit.
- Pressing **C (clear)** returns to the initial `"0"` state.
- Pressing an **operator** clears the error and is ignored (the user must start with a digit).

This behavior is managed entirely within the model via the `has_error()` flag. The controller does not need conditional logic for error recovery.

---

## 7. Event Handling Design

### 7.1 Button Click Events

Each button is created with a `command` callback that delegates to the appropriate controller method. Callbacks are bound at widget creation time using `lambda` or `functools.partial` to pass the button's value.

```python
# Example: creating a digit button
btn = ttk.Button(frame, text="7", command=lambda: self._on_digit("7"))
```

### 7.2 Keyboard Input Events

Keyboard bindings are registered on the root window via `bind()`. Each key event handler extracts the relevant character and delegates to the same controller methods used by button clicks.

| Key(s)                | Handler           |
|-----------------------|-------------------|
| `0-9`                 | `_on_digit`       |
| `.`                   | `_on_decimal`     |
| `+`, `-`, `*`, `/`   | `_on_operator`    |
| `<Return>`, `=`       | `_on_equals`      |
| `<Escape>`, `c`, `C` | `_on_clear`       |

Keyboard and button events converge on the same controller methods, ensuring identical behavior regardless of input source.

### 7.3 State Management

All mutable state resides in the `CalculatorLogic` instance. The GUI holds no shadow copies of the expression or result. The single source of truth is always the model. The controller's update cycle is:

1. Receive event (button or key).
2. Call one model method.
3. Take the returned string and put it in the display.

There is no state synchronization problem because there is only one copy of the state.

### 7.4 Event Flow Diagram

```
[Button "7" clicked]  ---command--->  _on_digit("7")
[Key "7" pressed]     ---bind--->     _on_digit("7")
                                           |
                                           v
                                  logic.append_digit("7")
                                           |
                                           v
                                  returns "7" (display string)
                                           |
                                           v
                                  _update_display("7")
                                           |
                                           v
                                  Entry widget shows "7"
```

---

## 8. File Summary

| File                  | Lines (est.) | Purpose                                |
|-----------------------|--------------|----------------------------------------|
| `calculator_logic.py` | 60-90        | Model: expression state and evaluation |
| `calculator.py`       | 100-150      | View + Controller: GUI and input routing |
| `test_calculator.py`  | 80-120       | Unit tests for `CalculatorLogic`       |

Total estimated size: under 400 lines for the complete application including tests.
