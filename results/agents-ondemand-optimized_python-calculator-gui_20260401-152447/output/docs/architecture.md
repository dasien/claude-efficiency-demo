# Architecture Document: Python Tkinter GUI Calculator

**Date:** 2026-04-01
**Version:** 1.0

---

## 1. High-Level System Design

The calculator follows the **Model-View-Controller (MVC)** architectural pattern, split across two modules:

```
+-----------------------------------------------------+
|                   calculator.py                      |
|  (View + Controller: CalculatorApp class)            |
|                                                      |
|  - Tkinter window, widgets, layout                   |
|  - Event handlers (button clicks, keyboard input)    |
|  - Delegates all computation to CalculatorLogic      |
+----------------------------+------------------------+
                             |
                             | uses
                             v
+-----------------------------------------------------+
|               calculator_logic.py                    |
|  (Model: CalculatorLogic class)                      |
|                                                      |
|  - Expression building (append digits, operators)    |
|  - Expression evaluation                             |
|  - Error handling (returns error strings, no GUI)    |
|  - State management (current expression, result)     |
+-----------------------------------------------------+
```

### Data Flow

1. **User Input** -- User clicks a button or presses a key.
2. **Controller** -- The event handler in `CalculatorApp` identifies the action (digit, operator, equals, clear).
3. **Model** -- `CalculatorApp` calls the appropriate method on `CalculatorLogic` (e.g., `append_to_expression("5")`, `evaluate()`).
4. **Response** -- `CalculatorLogic` updates its internal state and returns the current display string.
5. **View** -- `CalculatorApp` updates the display widget with the returned string.

---

## 2. Module Definitions

### 2.1 calculator_logic.py -- CalculatorLogic Class

This module contains pure business logic with no GUI dependencies. It can be imported and tested independently.

```python
class CalculatorLogic:
    """Pure calculator logic: expression building, evaluation, and error handling.

    Attributes:
        expression (str): The current expression string being built.
    """

    def __init__(self) -> None:
        """Initialize with an empty expression."""
        ...

    def append_to_expression(self, value: str) -> str:
        """Append a character (digit, operator, or decimal point) to the expression.

        Args:
            value: A single character to append ('0'-'9', '.', '+', '-', '*', '/').

        Returns:
            The updated expression string for display.
        """
        ...

    def evaluate(self) -> str:
        """Evaluate the current expression and return the result as a string.

        Returns:
            The result as a string. Returns "Error" if evaluation fails
            (e.g., division by zero, syntax error). If the result is a
            whole number, returns it without a decimal point (e.g., "5" not "5.0").
        """
        ...

    def clear(self) -> str:
        """Clear the current expression and reset to initial state.

        Returns:
            An empty string for display.
        """
        ...

    def get_expression(self) -> str:
        """Return the current expression string.

        Returns:
            The current expression.
        """
        ...
```

**Design Decisions:**
- All methods return strings suitable for display. The GUI never needs to interpret or format the result.
- `evaluate()` catches all exceptions internally and returns "Error" rather than raising. This ensures the GUI layer never needs exception-handling logic for calculator operations.
- The expression is stored as a simple string. Python's `eval()` (or a safe subset) handles operator precedence naturally.

---

### 2.2 calculator.py -- CalculatorApp Class

This module contains the Tkinter GUI. It instantiates `CalculatorLogic` and delegates all computation to it.

```python
import tkinter as tk
from tkinter import ttk
from calculator_logic import CalculatorLogic


class CalculatorApp(tk.Tk):
    """Tkinter GUI calculator application.

    Uses CalculatorLogic for all computation. Handles layout,
    button creation, and event binding.

    Attributes:
        logic (CalculatorLogic): The calculator business logic instance.
        display_var (tk.StringVar): Variable bound to the display widget.
    """

    def __init__(self) -> None:
        """Initialize the calculator window, widgets, and event bindings."""
        ...

    def _create_widgets(self) -> None:
        """Create the display and all calculator buttons using grid layout."""
        ...

    def _bind_events(self) -> None:
        """Bind keyboard events to calculator actions."""
        ...

    def _on_button_click(self, value: str) -> None:
        """Handle a button click or keyboard input.

        Args:
            value: The button label or key character that was pressed.
        """
        ...

    def _update_display(self, text: str) -> None:
        """Update the display widget with the given text.

        Args:
            text: The string to show in the display.
        """
        ...
```

**Design Decisions:**
- `CalculatorApp` inherits from `tk.Tk` to serve as the root window.
- A single `_on_button_click` method handles all inputs, routing to the appropriate `CalculatorLogic` method based on the value.
- `tk.StringVar` is used for the display to allow clean binding between the data and the Entry widget.

---

## 3. GUI Layout Specification

### Grid Layout

The calculator uses a 4-column grid layout. The display spans all 4 columns at the top.

```
+-------+-------+-------+-------+
|         Display (row 0)        |  <- Entry widget, columnspan=4
+-------+-------+-------+-------+
|   7   |   8   |   9   |   /   |  <- row 1
+-------+-------+-------+-------+
|   4   |   5   |   6   |   *   |  <- row 2
+-------+-------+-------+-------+
|   1   |   2   |   3   |   -   |  <- row 3
+-------+-------+-------+-------+
|   0   |   .   |   =   |   +   |  <- row 4
+-------+-------+-------+-------+
|              C (row 5)         |  <- Clear button, columnspan=4
+-------+-------+-------+-------+
```

### Grid Positions (row, column)

| Widget   | Row | Column | Columnspan | Sticky |
|----------|-----|--------|------------|--------|
| Display  |  0  |   0    |     4      |  ew    |
| 7        |  1  |   0    |     1      |  nsew  |
| 8        |  1  |   1    |     1      |  nsew  |
| 9        |  1  |   2    |     1      |  nsew  |
| /        |  1  |   3    |     1      |  nsew  |
| 4        |  2  |   0    |     1      |  nsew  |
| 5        |  2  |   1    |     1      |  nsew  |
| 6        |  2  |   2    |     1      |  nsew  |
| *        |  2  |   3    |     1      |  nsew  |
| 1        |  3  |   0    |     1      |  nsew  |
| 2        |  3  |   1    |     1      |  nsew  |
| 3        |  3  |   2    |     1      |  nsew  |
| -        |  3  |   3    |     1      |  nsew  |
| 0        |  4  |   0    |     1      |  nsew  |
| .        |  4  |   1    |     1      |  nsew  |
| =        |  4  |   2    |     1      |  nsew  |
| +        |  4  |   3    |     1      |  nsew  |
| C        |  5  |   0    |     4      |  nsew  |

### Widget Configuration

- **Display:** `ttk.Entry` with a large monospaced font (e.g., Courier 18), read-only state, right-justified text.
- **Buttons:** `ttk.Button` widgets with a readable font (e.g., Arial 14). Each button uses `command=lambda v=label: self._on_button_click(v)`.
- **Column/Row weights:** All columns have equal weight (weight=1). All button rows have equal weight (weight=1). The display row has weight=0 (fixed height).

---

## 4. Separation of Concerns Analysis

| Concern             | Responsible Module      | Details                                                  |
|---------------------|------------------------|----------------------------------------------------------|
| Expression building | `calculator_logic.py`  | Appending digits/operators to the expression string.     |
| Evaluation          | `calculator_logic.py`  | Parsing and computing the expression result.             |
| Error handling      | `calculator_logic.py`  | Catching exceptions, returning "Error" string.           |
| State management    | `calculator_logic.py`  | Tracking current expression, clearing state.             |
| Result formatting   | `calculator_logic.py`  | Converting float results to clean display strings.       |
| Window management   | `calculator.py`        | Creating the Tk root, setting title/size.                |
| Widget creation     | `calculator.py`        | Building Entry, Button, and Frame widgets.               |
| Layout              | `calculator.py`        | Grid positioning, column/row configuration.              |
| Event binding       | `calculator.py`        | Connecting button clicks and keyboard events to handlers.|
| Display updates     | `calculator.py`        | Writing text to the display Entry widget.                |

**Key principle:** `calculator_logic.py` has zero imports from `tkinter`. It can be tested, reused, or replaced independently. `calculator.py` contains zero arithmetic or expression-parsing logic.

---

## 5. Error Handling Strategy

All errors are handled gracefully and displayed in the GUI. The application never crashes from user input.

### Error Flow

```
User Input -> CalculatorLogic.evaluate()
                  |
                  +-- try: eval(expression)
                  |       |
                  |       +-- Success: return formatted result string
                  |
                  +-- except (SyntaxError, ZeroDivisionError, ...):
                          |
                          +-- return "Error"
                              |
                              v
                  CalculatorApp._update_display("Error")
```

### Error Cases Handled

| Error Condition       | Example Input | CalculatorLogic Returns | Recovery                        |
|-----------------------|---------------|-------------------------|---------------------------------|
| Division by zero      | "5/0"         | "Error"                 | User presses C to clear.        |
| Invalid syntax        | "5++3"        | "Error"                 | User presses C to clear.        |
| Empty expression      | "" (nothing)  | "Error" or ""           | User presses C to clear.        |
| Trailing operator     | "5+"          | "Error"                 | User presses C to clear.        |
| Malformed decimal     | "1.2.3"       | "Error"                 | User presses C to clear.        |
| Overflow              | Very large    | "Error" or large number | User presses C to clear.        |

### Safety of eval()

The `evaluate()` method must sanitize the expression before using Python's `eval()`. Only characters in the set `0-9 . + - * / ( )` should be permitted. Any other characters must be rejected, returning "Error". This prevents code injection through the calculator display.

---

## 6. Event Handling Design

### Button Click Events

Each button is created with a `command` parameter that calls `_on_button_click(value)` where `value` is the button's label string.

```python
# Button creation pattern
for label in ["7", "8", "9", "/"]:
    btn = ttk.Button(frame, text=label,
                     command=lambda v=label: self._on_button_click(v))
```

### Keyboard Events

Keyboard bindings are set on the root window so they work regardless of which widget has focus.

| Key(s)               | Action                           |
|-----------------------|----------------------------------|
| 0-9                   | Append digit to expression       |
| + - * /               | Append operator to expression    |
| .                     | Append decimal point             |
| Enter / Return        | Evaluate expression              |
| Escape                | Clear expression                 |
| BackSpace             | Clear expression                 |

```python
# Keyboard binding pattern
self.bind('<Key>', self._on_key_press)

def _on_key_press(self, event: tk.Event) -> None:
    if event.char in '0123456789.+-*/':
        self._on_button_click(event.char)
    elif event.keysym == 'Return':
        self._on_button_click('=')
    elif event.keysym in ('Escape', 'BackSpace'):
        self._on_button_click('C')
```

### State Management

The `CalculatorLogic` instance is the single source of truth for calculator state. The GUI reads from it after every action and updates the display accordingly.

```
[Button Click / Key Press]
        |
        v
_on_button_click(value)
        |
        +-- value in "0123456789.+-*/" --> logic.append_to_expression(value)
        +-- value == "="               --> logic.evaluate()
        +-- value == "C"               --> logic.clear()
        |
        v
_update_display(result_string)
```

---

## 7. Design Decisions and Rationale

| Decision | Rationale |
|----------|-----------|
| MVC pattern with two files | Keeps the codebase simple while maintaining full separation of concerns. Two files is appropriate for this scale of project. |
| Expression stored as a string | Simple to build incrementally and display. Python's `eval()` handles precedence naturally. |
| `eval()` for evaluation | Avoids building a custom expression parser for a calculator with standard operations. Input sanitization mitigates safety concerns. |
| Methods return display strings | The GUI never interprets results -- it simply displays what the logic returns. This eliminates formatting logic in the view. |
| Single `_on_button_click` handler | Centralizes input routing in one method rather than separate handlers per button. Reduces code duplication. |
| `tk.StringVar` for display | Provides clean data binding between the model's output and the Entry widget. |
| Keyboard events on root window | Ensures keyboard input works regardless of focus state. Users do not need to click the display first. |
| No third-party dependencies | Tkinter is part of the Python standard library. The project runs anywhere Python is installed. |
| Integer display for whole results | "5" is cleaner than "5.0" for the user. The logic layer handles this formatting. |
