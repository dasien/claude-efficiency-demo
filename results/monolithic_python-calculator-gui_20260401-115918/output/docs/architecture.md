# Calculator Application — Architecture Document

## 1. High-Level System Design

The application follows an **MVC-inspired** pattern with two modules:

```
┌─────────────────────────────────────────┐
│           calculator.py (View)          │
│  ┌───────────────┐  ┌───────────────┐  │
│  │   Display      │  │  Button Grid  │  │
│  └───────┬───────┘  └───────┬───────┘  │
│          │    User Events    │          │
│          └────────┬──────────┘          │
│                   ▼                     │
│          CalculatorApp (Controller)     │
│                   │                     │
└───────────────────┼─────────────────────┘
                    │ delegates
                    ▼
┌─────────────────────────────────────────┐
│      calculator_logic.py (Model)        │
│                                         │
│  CalculatorLogic                        │
│  - expression: str                      │
│  - add_character(char) -> str           │
│  - evaluate() -> str                    │
│  - clear() -> str                       │
│  - backspace() -> str                   │
└─────────────────────────────────────────┘
```

**Data Flow:**
1. User presses a button or key.
2. `CalculatorApp` receives the event and calls the appropriate method on `CalculatorLogic`.
3. `CalculatorLogic` updates its internal state and returns the new display string.
4. `CalculatorApp` updates the display widget with the returned string.

## 2. Module Interface Definitions

### calculator_logic.py — `CalculatorLogic`

```python
class CalculatorLogic:
    """Pure business logic for the calculator. No GUI dependencies."""

    def __init__(self) -> None:
        """Initialize with empty expression."""

    @property
    def display_text(self) -> str:
        """Return the current display string."""

    def add_character(self, char: str) -> str:
        """Append a digit, decimal, or operator to the expression.

        Handles validation:
        - Prevents multiple consecutive operators (replaces previous).
        - Prevents multiple decimal points in a single number.

        Returns: Updated display string.
        """

    def evaluate(self) -> str:
        """Evaluate the current expression.

        Returns: Result as a string, or 'Error' on failure.
        """

    def clear(self) -> str:
        """Reset to initial state.

        Returns: '0'
        """

    def backspace(self) -> str:
        """Remove the last character from the expression.

        Returns: Updated display string.
        """
```

### calculator.py — `CalculatorApp`

```python
class CalculatorApp(tk.Tk):
    """Tkinter GUI for the calculator."""

    def __init__(self) -> None:
        """Set up window, create widgets, bind events."""

    def _create_widgets(self) -> None:
        """Create the display and button grid."""

    def _bind_events(self) -> None:
        """Bind keyboard events to handler methods."""

    def _update_display(self, text: str) -> None:
        """Update the display widget with the given text."""

    def _on_button_click(self, value: str) -> None:
        """Handle a button press (digit, operator, =, C)."""

    def _on_key_press(self, event: tk.Event) -> None:
        """Handle keyboard input, delegating to _on_button_click."""
```

## 3. GUI Layout Specification

### Widget Hierarchy
```
Tk (CalculatorApp)
└── main_frame (ttk.Frame)
    ├── display_var (tk.StringVar) — bound to display entry
    ├── display (ttk.Entry) — row 0, col 0-3, sticky="ew"
    └── buttons (ttk.Button) — rows 1-5, cols 0-3
```

### Grid Layout

| Row | Col 0   | Col 1   | Col 2   | Col 3   |
|-----|---------|---------|---------|---------|
| 0   | Display (columnspan=4)              |
| 1   | C       | (       | )       | /       |
| 2   | 7       | 8       | 9       | *       |
| 3   | 4       | 5       | 6       | -       |
| 4   | 1       | 2       | 3       | +       |
| 5   | 0 (columnspan=2)    | .       | =       |

- All columns have equal weight for uniform sizing.
- Buttons use `sticky="nsew"` to fill their cells.
- Padding: 2px between buttons.

## 4. Design Decisions and Rationale

| Decision | Rationale |
|----------|-----------|
| Separate `calculator_logic.py` | Enables unit testing of all calculation logic without Tkinter. Pure functions with string I/O are trivially testable. |
| Expression-based (not register-based) | Simpler to implement. Users see the full expression, which matches modern calculator UX. Python's `eval`-like parsing handles precedence naturally. |
| Use Python `ast.literal_eval` or custom parsing instead of raw `eval` | `eval()` is a security risk. We use a restricted evaluator that only allows numbers and arithmetic operators. |
| `ttk` widgets over plain `tk` | Modern appearance with minimal effort. |
| Fixed window size | Calculator layout is fixed; resizing adds complexity without value. |
| `StringVar` for display | Two-way binding keeps display in sync with state automatically. |

## 5. Separation of Concerns

| Concern | Module | Details |
|---------|--------|---------|
| Expression building | `calculator_logic.py` | Validates and constructs the expression string. |
| Evaluation | `calculator_logic.py` | Parses and computes the result. No GUI knowledge. |
| Input validation | `calculator_logic.py` | Prevents invalid sequences (double operators, double decimals). |
| Display rendering | `calculator.py` | Updates the `ttk.Entry` widget. |
| Event routing | `calculator.py` | Maps button clicks and key presses to logic methods. |
| Window management | `calculator.py` | Title, size, grid layout. |

**Key principle:** `calculator_logic.py` has zero imports from `tkinter`. It is a pure Python module that accepts strings and returns strings.

## 6. Error Handling Strategy

| Error | Detection | User Feedback |
|-------|-----------|---------------|
| Division by zero | `ZeroDivisionError` caught in `evaluate()` | Display shows "Error" |
| Invalid expression (e.g., `3*/`) | `Exception` caught in `evaluate()` | Display shows "Error" |
| Syntax error | `SyntaxError` / `ValueError` caught in `evaluate()` | Display shows "Error" |
| Recovery from error | Any new digit input after "Error" | Clears error and starts fresh |

All exceptions are caught within `CalculatorLogic.evaluate()`. The GUI layer never sees exceptions — it only receives strings.

## 7. Event Handling Design

### Button Clicks
Each button is created with a `command` parameter bound to a lambda that calls `_on_button_click(value)`.

### Keyboard Input
`bind_all('<Key>', _on_key_press)` captures all keyboard input. The handler maps:
- `0-9`, `.`, `+`, `-`, `*`, `/` -> `add_character()`
- `Return`, `=` -> `evaluate()`
- `Escape`, `c`, `C` -> `clear()`
- `BackSpace` -> `backspace()`

### State Management
- `CalculatorLogic` holds the single source of truth: `_expression` (str) and `_last_was_eval` (bool).
- `_last_was_eval` tracks whether the last action was evaluation, so the next digit starts fresh while an operator continues from the result.
