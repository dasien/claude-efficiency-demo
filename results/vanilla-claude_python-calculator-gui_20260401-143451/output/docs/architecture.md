# Calculator Architecture Document

## 1. High-Level System Design

The application follows a **Model-View-Controller (MVC)** pattern with two modules:

```
┌─────────────────────────────────────────┐
│              calculator.py              │
│         (View + Controller)             │
│                                         │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │   View      │  │   Controller     │  │
│  │ (Tkinter    │◄─┤ (Event handlers, │  │
│  │  widgets)   │  │  key bindings)   │  │
│  └─────────────┘  └───────┬──────────┘  │
│                           │              │
└───────────────────────────┼──────────────┘
                            │ calls
                            ▼
              ┌──────────────────────────┐
              │   calculator_logic.py    │
              │       (Model)            │
              │                          │
              │  CalculatorLogic class   │
              │  - expression state      │
              │  - evaluation            │
              │  - input validation      │
              └──────────────────────────┘
```

### Data Flow
1. User presses a button or key -> Controller receives event.
2. Controller calls appropriate method on `CalculatorLogic`.
3. `CalculatorLogic` updates internal state and returns display values.
4. Controller updates the View (expression and result labels).

## 2. Module Interface Definitions

### calculator_logic.py — `CalculatorLogic` class

```python
class CalculatorLogic:
    """Pure business logic for the calculator. No GUI dependencies."""

    def __init__(self) -> None:
        """Initialize with empty expression and result '0'."""

    def get_expression(self) -> str:
        """Return the current expression string."""

    def get_result(self) -> str:
        """Return the current result string."""

    def append_digit(self, digit: str) -> None:
        """Append a digit (0-9) to the current expression.
        If the previous action was evaluate, start a new expression.
        """

    def append_decimal(self) -> None:
        """Append a decimal point if the current number doesn't have one."""

    def append_operator(self, operator: str) -> None:
        """Append an operator (+, -, *, /).
        If the last character is already an operator, replace it.
        If called after evaluation, continue from the result.
        """

    def evaluate(self) -> None:
        """Evaluate the current expression.
        Sets the result to the computed value, or 'Error' on failure.
        """

    def clear(self) -> None:
        """Reset expression and result to initial state."""
```

### calculator.py — `CalculatorApp` class

```python
class CalculatorApp:
    """Tkinter GUI for the calculator."""

    def __init__(self, root: tk.Tk) -> None:
        """Set up the window, displays, buttons, and key bindings."""

    def _create_display(self) -> None:
        """Create expression and result display labels."""

    def _create_buttons(self) -> None:
        """Create the button grid."""

    def _update_display(self) -> None:
        """Sync the display labels with CalculatorLogic state."""

    def _on_button_click(self, value: str) -> None:
        """Handle a button click or key press for a given value."""

    def _on_key_press(self, event: tk.Event) -> None:
        """Map keyboard events to calculator actions."""
```

## 3. GUI Layout Specification

### Widget Hierarchy
```
Tk (root window)
├── Frame (display_frame)
│   ├── Label (expression_label)  — shows expression
│   └── Label (result_label)      — shows result
└── Frame (button_frame)
    └── Grid of Button widgets (5 rows x 4 columns)
```

### Grid Positions
```
         Col 0    Col 1    Col 2    Col 3
Row 0:   C                          /
Row 1:   7        8        9        *
Row 2:   4        5        6        -
Row 3:   1        2        3        +
Row 4:   0 (span 2)       .        =
```

- `C` button spans columns 0-2 (columnspan=3).
- `0` button spans columns 0-1 (columnspan=2).
- `=` button occupies row 4, column 3.

## 4. Design Decisions and Rationale

| Decision | Rationale |
|----------|-----------|
| Separate `CalculatorLogic` class | Enables unit testing without Tkinter; clean separation of concerns. |
| Expression-based evaluation | Users see what they've typed; uses Python `eval()` internally with sanitization for simplicity. |
| Replace consecutive operators | Prevents invalid expressions like `5 + * 3`; last operator wins. |
| Result continuation | After `=`, pressing an operator continues from the result — standard calculator UX. |
| `eval()` with restricted input | Only digits, operators, decimal points, and parentheses are allowed in the expression string. Input is validated before `eval()` is called. |

## 5. Separation of Concerns

- **`calculator_logic.py`**: Contains all state management and computation. Has zero imports from `tkinter`. Can be tested with pure Python unit tests.
- **`calculator.py`**: Contains all GUI code. Delegates all logic to `CalculatorLogic`. Handles event routing and display updates only.

This separation means:
- Business logic can be reused with a different UI (e.g., CLI, web).
- Tests cover the logic without needing a display server or GUI mocking.

## 6. Error Handling Strategy

1. **Division by zero**: Python raises `ZeroDivisionError` during `eval()`. Caught in `evaluate()`, result set to `"Error"`.
2. **Invalid expression**: Any `Exception` during `eval()` sets result to `"Error"`.
3. **Recovery from error**: `clear()` resets state. Pressing a digit after an error also starts fresh.
4. **Input prevention**: `append_decimal()` checks if the current number already has a decimal. `append_operator()` replaces consecutive operators.

## 7. Event Handling Design

### Button Clicks
Each button is created with a `command` callback that calls `_on_button_click(value)` where `value` is the button's label (`"1"`, `"+"`, `"="`, `"C"`, etc.).

### Keyboard Input
`root.bind("<Key>", self._on_key_press)` captures all key events. The handler maps:
- `0-9`, `.` -> `append_digit` / `append_decimal`
- `+`, `-`, `*`, `/` -> `append_operator`
- `Return`, `Enter`, `=` -> `evaluate`
- `Escape`, `c`, `C` -> `clear`
- `BackSpace` -> handled if needed

### State Management
`CalculatorLogic` maintains:
- `_expression: str` — the current expression being built.
- `_result: str` — the current displayed result (`"0"` initially).
- `_evaluated: bool` — flag indicating the last action was evaluation (for continuation logic).
