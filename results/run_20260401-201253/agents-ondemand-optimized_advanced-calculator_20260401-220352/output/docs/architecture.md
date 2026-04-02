# Advanced Calculator -- Architecture Document

**Version:** 1.0
**Date:** 2026-04-01
**Reference:** docs/requirements.md

---

## 1. Architectural Overview

The application follows the **Model-View-Controller (MVC)** pattern with strict separation between business logic and GUI code.

```
+-------------------+       +-------------------+       +-------------------+
|      View         | <---> |    Controller     | <---> |      Model        |
|  (gui/ package)   |       |    (app.py)       |       |  (logic/ package) |
+-------------------+       +-------------------+       +-------------------+
| base_view.py      |       | - Mode switching  |       | base_logic.py     |
| basic_view.py     |       | - Event routing   |       | basic_logic.py    |
| scientific_view.py|       | - Display updates |       | scientific_logic.py|
| programmer_view.py|       | - Keyboard binding|       | programmer_logic.py|
+-------------------+       +-------------------+       +-------------------+
```

**Data flow:** User input (button click or key press) flows from View to Controller. The Controller calls the appropriate Model method. The Model returns a result (or raises a CalculatorError). The Controller updates the View with the result.

---

## 2. File Structure

```
project/
├── calculator/
│   ├── __init__.py
│   ├── app.py                  # Controller: orchestrates Model and View
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── base_view.py        # Abstract base: display widget, common layout helpers
│   │   ├── basic_view.py       # Basic mode button grid
│   │   ├── scientific_view.py  # Scientific mode button grid
│   │   └── programmer_view.py  # Programmer mode button grid + base panel
│   └── logic/
│       ├── __init__.py
│       ├── base_logic.py       # Shared: memory, display formatting, expression parser
│       ├── basic_logic.py      # Basic arithmetic evaluation
│       ├── scientific_logic.py # Trig, log, power, root, factorial, constants
│       └── programmer_logic.py # Base conversion, bitwise ops, word size management
├── tests/
│   ├── __init__.py
│   ├── test_basic.py
│   ├── test_scientific.py
│   ├── test_programmer.py
│   ├── test_memory.py
│   └── test_mode_switch.py
├── main.py                     # Entry point: creates App and runs mainloop
└── requirements.txt            # pytest only
```

---

## 3. Model Layer (logic/)

### 3.1 base_logic.py -- BaseCalculator

The shared foundation for all calculator modes.

```python
class CalculatorError(Exception):
    """Raised for all user-facing calculator errors (div by zero, domain errors, etc.)."""
    pass

class BaseCalculator:
    """Shared state and operations for all calculator modes."""

    def __init__(self) -> None:
        self.current_input: str          # The digits the user is currently typing
        self.expression: list            # Tokens: numbers and operator strings
        self.memory: float               # Stored memory value
        self.has_memory: bool            # Whether memory indicator should show
        self.error_state: bool           # Whether the display is showing "Error"

    # --- Display formatting ---
    def format_number(self, value: float) -> str: ...
        # Integer results: no decimal point (5 not 5.0)
        # Float results: max 10 significant digits
        # Very large/small: scientific notation

    # --- Memory operations ---
    def memory_clear(self) -> None: ...
    def memory_recall(self) -> float: ...
    def memory_add(self, value: float) -> None: ...
    def memory_subtract(self, value: float) -> None: ...
    def memory_store(self, value: float) -> None: ...

    # --- Input management ---
    def append_digit(self, digit: str) -> str: ...
        # Handles leading-zero prevention (NI-4)
        # Handles single-decimal-point rule (NI-3)
    def append_decimal(self) -> str: ...
    def toggle_sign(self, value: float) -> float: ...
    def percentage(self, value: float) -> float: ...
    def backspace(self) -> str: ...
    def clear_entry(self) -> None: ...     # C: reset current input only
    def all_clear(self) -> None: ...       # AC: reset all state

    # --- Error recovery ---
    def clear_error(self) -> None: ...
```

### 3.2 Expression Parser (inside base_logic.py)

**Critical design decision:** The expression parser must NOT use Python's `eval()`. Instead, implement a proper recursive descent parser or shunting-yard algorithm that respects operator precedence.

```python
class ExpressionParser:
    """Parses and evaluates mathematical expressions with operator precedence.

    Uses the shunting-yard algorithm to convert infix to postfix notation,
    then evaluates the postfix expression.

    Supported operators (in precedence order, low to high):
      - Addition (+), Subtraction (-)
      - Multiplication (*), Division (/)
      - Unary minus
      - Parentheses override precedence
    """

    PRECEDENCE: dict[str, int] = {
        "+": 1, "-": 1,
        "*": 2, "/": 2,
        "%": 2,           # Modulo (programmer mode)
    }

    def parse(self, tokens: list) -> float:
        """Evaluate a list of tokens (numbers and operator strings).

        Args:
            tokens: e.g. [2.0, "+", 3.0, "*", 4.0]

        Returns:
            The evaluated result.

        Raises:
            CalculatorError: On division by zero, mismatched parens, malformed input.
        """
        ...

    def _to_postfix(self, tokens: list) -> list: ...
    def _evaluate_postfix(self, postfix: list) -> float: ...
```

**Operator precedence rules:**
- `*` and `/` bind tighter than `+` and `-` (BA-5, BA-6)
- Parentheses override precedence (PA-2)
- Left-to-right associativity for equal-precedence operators

### 3.3 basic_logic.py -- BasicCalculator

```python
class BasicCalculator(BaseCalculator):
    """Basic mode: four-function arithmetic with expression parsing."""

    def add_operator(self, op: str) -> None:
        """Append an operator (+, -, *, /) to the expression."""
        ...

    def evaluate(self) -> float:
        """Evaluate the full expression and return the result.

        Raises:
            CalculatorError: On division by zero or malformed expression.
        """
        ...

    def get_expression_display(self) -> str:
        """Return the current expression as a string for the secondary display."""
        ...
```

### 3.4 scientific_logic.py -- ScientificCalculator

```python
class ScientificCalculator(BasicCalculator):
    """Scientific mode: extends Basic with trig, log, power, root, factorial, constants."""

    def __init__(self) -> None:
        super().__init__()
        self.angle_mode: str = "DEG"  # "DEG" or "RAD"
        self.paren_depth: int = 0

    # --- Angle mode ---
    def toggle_angle_mode(self) -> str: ...
    def _to_radians(self, value: float) -> float: ...
    def _from_radians(self, value: float) -> float: ...

    # --- Trigonometric (TR-1 through TR-6) ---
    def sin(self, value: float) -> float: ...
    def cos(self, value: float) -> float: ...
    def tan(self, value: float) -> float: ...
    def asin(self, value: float) -> float: ...
    def acos(self, value: float) -> float: ...
    def atan(self, value: float) -> float: ...
        # All raise CalculatorError for domain errors (e.g., asin(2), tan(90 deg))

    # --- Logarithmic (LG-1 through LG-3) ---
    def log10(self, value: float) -> float: ...
    def ln(self, value: float) -> float: ...
    def log2(self, value: float) -> float: ...
        # All raise CalculatorError for value <= 0

    # --- Power and Root (PW-1 through PW-8) ---
    def square(self, value: float) -> float: ...
    def cube(self, value: float) -> float: ...
    def power(self, base: float, exponent: float) -> float: ...  # Two-operand via expression
    def ten_to_x(self, value: float) -> float: ...
    def e_to_x(self, value: float) -> float: ...
    def sqrt(self, value: float) -> float: ...   # Raises CalculatorError for negative
    def cbrt(self, value: float) -> float: ...
    def reciprocal(self, value: float) -> float: ...  # Raises CalculatorError for zero

    # --- Constants (CO-1, CO-2) ---
    def get_pi(self) -> float: ...
    def get_e(self) -> float: ...

    # --- Factorial and Absolute Value (FA-1 through FA-4) ---
    def factorial(self, value: float) -> float: ...
        # Raises CalculatorError for negative or non-integer
        # Must handle up to n=170
    def absolute_value(self, value: float) -> float: ...

    # --- Parentheses (PA-1 through PA-4) ---
    def open_paren(self) -> None: ...
    def close_paren(self) -> None: ...
    def get_paren_depth(self) -> int: ...
```

**Design notes on unary vs. binary operations:**
- Unary operations (sin, cos, sqrt, x^2, n!, etc.) apply immediately to the current display value and replace it. They do NOT go into the expression token list.
- Binary operations (x^n, +, -, *, /) append the current value and the operator to the expression and await the second operand.
- Parentheses are inserted as tokens in the expression.

### 3.5 programmer_logic.py -- ProgrammerCalculator

```python
class ProgrammerCalculator(BaseCalculator):
    """Programmer mode: integer arithmetic, base conversion, bitwise ops, word size."""

    WORD_SIZES: dict[int, tuple[int, int]] = {
        8:  (-128, 127),
        16: (-32768, 32767),
        32: (-2147483648, 2147483647),
        64: (-9223372036854775808, 9223372036854775807),
    }

    def __init__(self) -> None:
        super().__init__()
        self.base: int = 10           # 2, 8, 10, or 16
        self.word_size: int = 64      # 8, 16, 32, or 64
        self.value: int = 0           # Always stored internally as a Python int

    # --- Base conversion (NB-1 through NB-8) ---
    def set_base(self, base: int) -> str: ...
        # Returns the current value formatted in the new base
    def format_in_base(self, value: int, base: int) -> str: ...
    def get_all_bases(self, value: int) -> dict[str, str]: ...
        # Returns {"DEC": "255", "HEX": "FF", "OCT": "377", "BIN": "11111111"}
    def parse_input(self, digit: str) -> int: ...
        # Validates digit is legal for current base
    def get_valid_digits(self) -> set[str]: ...
        # Returns set of valid digit chars for the current base

    # --- Word size (WS-1 through WS-3) ---
    def set_word_size(self, bits: int) -> int: ...
        # Truncates current value to new word size
    def _apply_word_size(self, value: int) -> int: ...
        # Wraps value using two's complement for current word size
        # Algorithm: mask = (1 << bits) - 1
        #   value = value & mask
        #   if value >= (1 << (bits - 1)): value -= (1 << bits)

    # --- Bitwise operations (BW-1 through BW-6) ---
    def bitwise_and(self, a: int, b: int) -> int: ...
    def bitwise_or(self, a: int, b: int) -> int: ...
    def bitwise_xor(self, a: int, b: int) -> int: ...
    def bitwise_not(self, value: int) -> int: ...
    def left_shift(self, value: int, n: int) -> int: ...
    def right_shift(self, value: int, n: int) -> int: ...
        # All results go through _apply_word_size()

    # --- Integer arithmetic (PM-1 through PM-4) ---
    def integer_divide(self, a: int, b: int) -> int: ...
        # Truncating division (not floor): int(a / b)
    def modulo(self, a: int, b: int) -> int: ...

    # --- Overrides ---
    def evaluate(self) -> int: ...
        # Uses ExpressionParser but casts result to int and applies word size
```

**Key design decisions for Programmer mode:**
- All values are stored internally as Python `int` (arbitrary precision) but constrained through `_apply_word_size()` before display and after every operation.
- The `value` field is always a signed integer in two's complement interpretation.
- No decimal point input is allowed; the `append_decimal()` method is a no-op or raises an error.
- When switching TO programmer mode, float values are truncated via `int()`.

---

## 4. View Layer (gui/)

### 4.1 base_view.py -- BaseView

```python
class BaseView(ttk.Frame):
    """Shared GUI components: display area, memory row, common layout helpers."""

    def __init__(self, parent: tk.Widget, controller: "App") -> None:
        self.controller = controller  # Reference back to controller for callbacks

    def _create_display(self) -> None:
        """Create the expression line (secondary) and result display (primary)."""
        # Expression display: tk.Label, left-aligned, smaller font
        # Result display: tk.Label, right-aligned, large font
        ...

    def update_display(self, value: str, expression: str = "") -> None: ...
    def show_error(self, message: str = "Error") -> None: ...
    def show_memory_indicator(self, visible: bool) -> None: ...

    def _create_button(self, parent: tk.Widget, text: str, row: int, col: int,
                       command: callable, colspan: int = 1, style: str = "default") -> ttk.Button: ...
        # Helper to create a grid-placed button with consistent sizing
```

**Layout engine:** All views use `grid()` geometry manager. Each button occupies a cell in the grid. Multi-cell buttons (like `0`) use `columnspan`. Grid columns and rows are configured with `weight=1` for uniform sizing.

### 4.2 basic_view.py -- BasicView

Implements the Basic mode layout from requirements section 3.6:

```
+---------------------------------------+
|  [Expression display]                 |
|  [Result display          ]           |
+---------------------------------------+
| MC  | MR  | M+  | M-  | MS          |
+-----+-----+-----+-----+-------------+
|  C  | +/- |  %  |  /  |             |
+-----+-----+-----+-----+             |
|  7  |  8  |  9  |  *  |             |
+-----+-----+-----+-----+             |
|  4  |  5  |  6  |  -  |             |
+-----+-----+-----+-----+             |
|  1  |  2  |  3  |  +  |             |
+-----+-----+-----+-----+-------------+
|     0     |  .  |  =  |             |
+-----------+-----+-----+-------------+
```

- Button `0` uses `columnspan=2`.
- Memory row is a separate frame above the main grid.
- Operator buttons (+, -, *, /) get a distinct style (e.g., orange background).
- The `=` button gets a highlighted style.

### 4.3 scientific_view.py -- ScientificView

Extends the layout with 5 additional columns on the left for scientific functions (see requirements section 4.7). Includes:
- A Deg/Rad toggle indicator in the top-right area.
- Parenthesis depth counter near the `(` `)` buttons.

### 4.4 programmer_view.py -- ProgrammerView

Implements the Programmer mode layout from requirements section 5.6. Includes:
- Base conversion panel (HEX/DEC/OCT/BIN values displayed simultaneously).
- Base selector radio buttons (DEC, HEX, OCT, BIN).
- Word size selector dropdown or radio buttons (8, 16, 32, 64).
- Hex digit buttons A-F (enabled/disabled based on current base).
- Bitwise operation buttons (AND, OR, XOR, NOT, LSH, RSH).
- The decimal point button is disabled/hidden.

**Dynamic button state:** When the base changes, the View calls a method that enables/disables digit and hex buttons. The Controller mediates this -- the View asks the Model for `get_valid_digits()` and updates button states accordingly.

---

## 5. Controller Layer (app.py)

```python
class App(tk.Tk):
    """Main application controller. Manages mode switching and event routing."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Calculator")

        # Models (one per mode, memory is shared via base class)
        self.basic_calc = BasicCalculator()
        self.scientific_calc = ScientificCalculator()
        self.programmer_calc = ProgrammerCalculator()
        self.active_calc: BaseCalculator = self.basic_calc

        # Views (created lazily or all at once, only one visible)
        self.basic_view: BasicView
        self.scientific_view: ScientificView
        self.programmer_view: ProgrammerView
        self.active_view: BaseView

        self._create_menu()
        self._bind_keyboard()
        self._switch_mode("basic")

    # --- Mode switching ---
    def _switch_mode(self, mode: str) -> None:
        """Switch between 'basic', 'scientific', 'programmer'.

        Steps:
        1. Get the current display value from the active model.
        2. Hide the current view.
        3. Transfer the value to the new model:
           - Basic <-> Scientific: preserve float value (MS-3).
           - To Programmer: truncate to int (MS-4).
           - From Programmer: preserve int value as float (MS-5).
        4. Transfer memory state (MF-7): copy memory and has_memory.
        5. Show the new view.
        6. Resize the window (MS-6).
        7. Update the display.
        """
        ...

    # --- Event routing ---
    def on_digit(self, digit: str) -> None: ...
    def on_operator(self, op: str) -> None: ...
    def on_equals(self) -> None: ...
    def on_clear(self) -> None: ...
    def on_all_clear(self) -> None: ...
    def on_backspace(self) -> None: ...
    def on_memory(self, action: str) -> None: ...       # "MC", "MR", "M+", "M-", "MS"
    def on_scientific(self, func: str) -> None: ...     # "sin", "cos", "sqrt", etc.
    def on_programmer(self, func: str) -> None: ...     # "AND", "OR", "NOT", etc.
    def on_base_change(self, base: int) -> None: ...
    def on_word_size_change(self, bits: int) -> None: ...

    # --- Keyboard handling ---
    def _bind_keyboard(self) -> None:
        """Bind keyboard shortcuts per requirements section 6.

        Uses self.bind_all() for global keys (digits, operators, Enter, Escape, Backspace).
        Uses mode-aware dispatch: e.g., parentheses only work in Scientific mode.
        Mode switch shortcuts: Ctrl+1, Ctrl+2, Ctrl+3.
        """
        ...

    # --- Display update (central) ---
    def _update_display(self) -> None:
        """Pull current value and expression from the active model and push to the active view."""
        ...

    def _handle_error(self, error: CalculatorError) -> None:
        """Display 'Error' on the view and set the model's error state."""
        ...
```

### 5.1 Event Flow Example

**User presses `2`, `+`, `3`, `*`, `4`, `=` in Basic mode:**

1. View button `2` fires `controller.on_digit("2")`.
2. Controller calls `basic_calc.append_digit("2")`. Model updates `current_input = "2"`.
3. Controller calls `_update_display()`. View shows `2`.
4. View button `+` fires `controller.on_operator("+")`.
5. Controller calls `basic_calc.add_operator("+")`. Model pushes `2.0` and `"+"` to `expression`.
6. Controller calls `_update_display()`. Expression line shows `2 +`.
7. ...repeat for `3`, `*`, `4`...
8. View button `=` fires `controller.on_equals()`.
9. Controller calls `basic_calc.evaluate()`. Model's ExpressionParser evaluates `[2.0, "+", 3.0, "*", 4.0]` respecting precedence: `3*4=12`, then `2+12=14`. Returns `14.0`.
10. Controller calls `basic_calc.format_number(14.0)` which returns `"14"`.
11. Controller calls `view.update_display("14", "2 + 3 * 4 =")`.

**Error flow:** If the parser raises `CalculatorError` (e.g., division by zero), the Controller catches it in a try/except and calls `_handle_error()`, which shows "Error" on the display and sets `model.error_state = True`. The next digit press calls `model.clear_error()` first.

---

## 6. Key Design Decisions

### 6.1 Expression Evaluation -- No eval()

The expression parser uses the **shunting-yard algorithm** to convert infix tokens to postfix, then evaluates the postfix stack. This ensures:
- Correct operator precedence without relying on Python's eval().
- No security risk from arbitrary code execution.
- Clean error reporting for malformed expressions.
- Easy extension for programmer-mode operators (AND, OR, XOR, LSH, RSH, MOD).

The parser operates on a list of tokens (floats and operator strings), not raw character strings. Tokenization happens during input (each digit press builds a number, each operator press finalizes the current number and appends both).

### 6.2 Memory Management

Memory is stored as a `float` on `BaseCalculator`. When switching modes, the Controller copies `memory` and `has_memory` from the old model to the new model. This satisfies MF-7 (memory persists across mode switches) without requiring a shared singleton.

### 6.3 Mode Switching

Each mode has its own Model instance. The Controller transfers state (current value, memory) during switches. This keeps each model clean and avoids conditional logic inside a single model class.

**Value transfer rules:**
- Basic to Scientific (or reverse): copy `float` value directly.
- Any mode to Programmer: `int(current_value)` -- truncation per MS-4.
- Programmer to any mode: `float(current_int_value)` -- per MS-5.

### 6.4 Error Propagation

All model-layer errors raise `CalculatorError` with a descriptive message. The Controller catches these uniformly and displays "Error" on the View. The View never catches exceptions. The model never imports tkinter.

### 6.5 Two's Complement Word Size

In Programmer mode, every operation result passes through `_apply_word_size()`, which uses bitmask arithmetic:

```python
def _apply_word_size(self, value: int) -> int:
    bits = self.word_size
    mask = (1 << bits) - 1
    value = value & mask
    if value >= (1 << (bits - 1)):
        value -= (1 << bits)
    return value
```

This correctly handles overflow wrapping (e.g., 127 + 1 = -128 in 8-bit).

### 6.6 Unary vs. Binary Scientific Operations

- **Unary operations** (sin, cos, sqrt, x^2, n!, |x|, log, ln, etc.) are applied immediately to the current display value. They do not enter the expression -- they transform the current operand in place.
- **Binary operations** (x^n, +, -, *, /) push the first operand and operator to the expression and wait for the second operand.
- This mirrors the behavior of standard desktop calculators.

### 6.7 Window Sizing

Each mode defines a preferred window size:
- Basic: approximately 320 x 480 pixels.
- Scientific: approximately 560 x 480 pixels (wider for extra button columns).
- Programmer: approximately 560 x 560 pixels (wider and taller for base panel and extra rows).

The Controller calls `self.geometry()` during mode switches per MS-6.

---

## 7. Dependencies Between Modules

```
main.py
  └── calculator/app.py (Controller)
        ├── calculator/logic/basic_logic.py
        │     └── calculator/logic/base_logic.py (inherits)
        ├── calculator/logic/scientific_logic.py
        │     └── calculator/logic/basic_logic.py (inherits)
        ├── calculator/logic/programmer_logic.py
        │     └── calculator/logic/base_logic.py (inherits)
        ├── calculator/gui/basic_view.py
        │     └── calculator/gui/base_view.py (inherits)
        ├── calculator/gui/scientific_view.py
        │     └── calculator/gui/base_view.py (inherits)
        └── calculator/gui/programmer_view.py
              └── calculator/gui/base_view.py (inherits)
```

**Rule:** The `logic/` package never imports from `gui/`. The `gui/` package never imports from `logic/`. Only `app.py` imports from both. This satisfies NF-5 and NF-12.
