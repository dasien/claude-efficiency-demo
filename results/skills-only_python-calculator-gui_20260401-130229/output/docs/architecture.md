# Calculator Application — Architecture Document

## 1. High-Level System Design

The application follows the **MVC (Model-View-Controller)** pattern with two modules:

```
┌─────────────────────────────────────────┐
│              calculator.py              │
│  ┌───────────┐      ┌───────────────┐  │
│  │  View      │      │  Controller   │  │
│  │ (Tkinter   │◄────►│ (Event        │  │
│  │  widgets)  │      │  handling)    │  │
│  └───────────┘      └──────┬────────┘  │
│                             │           │
│                     ┌───────▼────────┐  │
│                     │  Model         │  │
│                     │ (calculator_   │  │
│                     │  logic.py)     │  │
│                     └────────────────┘  │
└─────────────────────────────────────────┘
```

### Data Flow
1. **Input**: User presses a button or key → event fires.
2. **Controller**: Event handler in `CalculatorApp` interprets the input and calls the appropriate method on `CalculatorLogic`.
3. **Model**: `CalculatorLogic` updates its internal state and returns the new display value.
4. **View**: Controller updates the Tkinter display widget with the returned value.

## 2. Module Interface Definitions

### Module: `calculator_logic.py` (Model)

```python
class CalculatorLogic:
    """Pure business logic for a basic calculator. No GUI dependencies."""

    def __init__(self) -> None:
        """Initialize calculator to default state (display '0')."""

    def get_display(self) -> str:
        """Return the current display string."""

    def input_digit(self, digit: str) -> str:
        """Append a digit ('0'-'9') to the current number.
        Returns the updated display string."""

    def input_decimal(self) -> str:
        """Append a decimal point if not already present.
        Returns the updated display string."""

    def input_operator(self, operator: str) -> str:
        """Set the pending operator (+, -, *, /).
        If there is already a pending operation, evaluate it first.
        Returns the updated display string."""

    def input_equals(self) -> str:
        """Evaluate the pending operation.
        Returns the result display string, or 'Error' on failure."""

    def input_clear(self) -> str:
        """Reset all state. Returns '0'."""

    def input_backspace(self) -> str:
        """Remove the last digit from current input.
        Returns the updated display string."""
```

**Internal state:**
- `current_input: str` — the number currently being typed (as a string).
- `first_operand: float | None` — the stored first operand.
- `operator: str | None` — the pending operator.
- `result_displayed: bool` — whether the display is showing a result (next digit starts fresh).
- `last_operator: str | None` — for repeated `=` presses.
- `last_operand: float | None` — for repeated `=` presses.

### Module: `calculator.py` (View + Controller)

```python
class CalculatorApp:
    """Tkinter GUI calculator application."""

    def __init__(self, root: tk.Tk) -> None:
        """Build the GUI and bind events."""

    def _create_display(self) -> None:
        """Create the display widget at the top."""

    def _create_buttons(self) -> None:
        """Create the button grid."""

    def _on_button_click(self, value: str) -> None:
        """Handle a button click or key press. Routes to CalculatorLogic."""

    def _update_display(self, text: str) -> None:
        """Update the display widget with the given text."""

    def _bind_keyboard(self) -> None:
        """Bind keyboard events to calculator actions."""
```

## 3. GUI Layout Specification

### Widget Hierarchy
```
Tk (root window)
└── Frame (main_frame, padding)
    ├── Entry (display, row=0, columnspan=4)
    └── Buttons (rows 1-5, columns 0-3)
```

### Grid Layout (row, col)
```
Row 0: [Display ─────────────────────] (columnspan=4)
Row 1: [C (0,0)] [( (0,1)] [) (0,2)] [/ (0,3)]
Row 2: [7 (0,0)] [8 (0,1)] [9 (0,2)] [* (0,3)]
Row 3: [4 (0,0)] [5 (0,1)] [6 (0,2)] [- (0,3)]
Row 4: [1 (0,0)] [2 (0,1)] [3 (0,2)] [+ (0,3)]
Row 5: [0 (0,0, colspan=2)]  [. (0,2)] [= (0,3)]
```

### Styling
- Display: white background, right-aligned, large font (24pt), read-only.
- Number buttons: light gray background (`#f0f0f0`).
- Operator buttons: orange background (`#ff9500`), white text.
- Clear button: red background (`#ff3b30`), white text.
- Equals button: green background (`#34c759`), white text.

## 4. Design Decisions and Rationale

| Decision | Rationale |
|----------|-----------|
| Separate `calculator_logic.py` from GUI | Enables unit testing of all business logic without Tkinter. Follows separation of concerns. |
| MVC over MVP | Simpler for a small app. The controller and view coexist in one class since Tkinter naturally couples them. |
| String-based display state | Avoids float precision issues during input (user types "3.0", we keep "3.0" not `3.0`). Conversion to float happens only at evaluation time. |
| Left-to-right evaluation | Matches standard basic calculator behavior. Users expect `2 + 3 * 4 = 20`, not `14`. |
| `result_displayed` flag | Distinguishes "user is viewing a result" from "user is typing a number" so the next digit either starts fresh or appends. |
| Repeated equals support | Stores `last_operator` and `last_operand` so pressing `=` multiple times repeats the last operation — standard calculator behavior. |

## 5. Separation of Concerns

- **`calculator_logic.py`**: Zero imports from `tkinter`. Pure Python. All arithmetic, state management, and formatting live here. Every public method returns a `str` (the new display text). This module can be tested, reused, or replaced independently.
- **`calculator.py`**: Handles only GUI construction, event routing, and display updates. Contains no arithmetic or state logic. Delegates every action to `CalculatorLogic` and renders whatever string it returns.

## 6. Error Handling Strategy

1. **Division by zero**: `CalculatorLogic.input_equals()` catches `ZeroDivisionError` and returns `"Error"`.
2. **Invalid state**: Any unexpected error during evaluation is caught and returns `"Error"`.
3. **Error recovery**: When in error state, `input_clear()` resets everything. Digit/operator presses after an error also trigger a clear first.
4. **Display**: The GUI simply shows whatever string the logic returns — including `"Error"`. No message boxes or popups.

## 7. Event Handling Design

### Button Clicks
Each button is created with a `command` lambda that calls `_on_button_click(value)` with the button's label as the value. The handler routes based on value type:
- Digit → `logic.input_digit(value)`
- `.` → `logic.input_decimal()`
- Operator → `logic.input_operator(value)`
- `=` → `logic.input_equals()`
- `C` → `logic.input_clear()`

### Keyboard Bindings
Bound on the root window via `bind("<Key>", handler)`:
- `event.char` in `"0123456789"` → digit
- `event.char` in `"+-*/"` → operator
- `event.char == "."` → decimal
- `event.keysym == "Return"` or `event.char == "="` → equals
- `event.keysym == "Escape"` → clear
- `event.keysym == "BackSpace"` → backspace

### State Management
All state lives in `CalculatorLogic`. The GUI holds a single reference to the logic instance and has no calculator state of its own. This makes the state machine easy to reason about and test.
