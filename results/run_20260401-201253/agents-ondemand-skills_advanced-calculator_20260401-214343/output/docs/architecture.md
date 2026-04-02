# Advanced Calculator -- Architecture Document

**Version:** 1.0
**Date:** 2026-04-01
**Based on:** requirements.md v1.0

---

## 1. High-Level System Design

The application follows the **Model-View-Controller (MVC)** pattern with a strict
dependency rule: the GUI (View) depends on the Logic (Model), never the reverse.
The Controller layer lives in `app.py` and coordinates between them.

```
+-------------------+       +-------------------+       +-------------------+
|       VIEW        |       |    CONTROLLER     |       |       MODEL       |
|                   |       |                   |       |                   |
|  base_view.py     | ----> |    app.py         | ----> |  base_logic.py    |
|  basic_view.py    |       |                   |       |  basic_logic.py   |
|  scientific_view.py       |  (orchestrates    |       |  scientific_logic |
|  programmer_view.py       |   mode switching, |       |  programmer_logic |
|                   |       |   event routing)  |       |                   |
+-------------------+       +-------------------+       +-------------------+
     Tkinter widgets          Binds View to Model         Pure Python, no GUI
```

**Dependency direction:** View -> Controller -> Model. The Model never imports
from View or Controller. The Controller never imports from View (it receives
callbacks, not references to widget internals).

### 1.1 Communication Flow

1. User presses a button or key in the View.
2. The View calls a Controller callback (a plain Python callable).
3. The Controller invokes the appropriate Model method.
4. The Model computes the result and returns a `DisplayState` data object.
5. The Controller passes the `DisplayState` to the View for rendering.

The View never calls Model methods directly. The Model never updates the View
directly. All communication passes through the Controller.

---

## 2. File Structure

```
project/
├── calculator/
│   ├── __init__.py
│   ├── app.py                  # Controller: mode switching, event routing
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── base_view.py        # Abstract base: display panel, common layout
│   │   ├── basic_view.py       # Basic mode button grid
│   │   ├── scientific_view.py  # Scientific mode button grid
│   │   └── programmer_view.py  # Programmer mode button grid + base panel
│   └── logic/
│       ├── __init__.py
│       ├── base_logic.py       # Abstract base + memory + display formatting
│       ├── basic_logic.py      # Arithmetic expression evaluation
│       ├── scientific_logic.py # Trig, log, power, root, factorial, constants
│       └── programmer_logic.py # Base conversion, bitwise ops, word size
├── tests/
│   ├── __init__.py
│   ├── test_basic.py
│   ├── test_scientific.py
│   ├── test_programmer.py
│   ├── test_memory.py
│   └── test_mode_switch.py
├── main.py                     # Entry point: python3 main.py
└── requirements.txt            # pytest (testing only)
```

---

## 3. Module Interfaces -- Logic Layer

All logic classes are pure Python. They never import tkinter. They accept
primitive values (strings, ints, floats) and return data objects. This makes
them fully unit-testable.

### 3.1 Data Transfer Objects

These are plain dataclasses used to communicate state from Model to Controller
to View. They live in `base_logic.py`.

```python
# calculator/logic/base_logic.py

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List


class Mode(Enum):
    BASIC = "basic"
    SCIENTIFIC = "scientific"
    PROGRAMMER = "programmer"


class AngleUnit(Enum):
    DEG = "deg"
    RAD = "rad"


class NumberBase(Enum):
    DEC = 10
    HEX = 16
    OCT = 8
    BIN = 2


class WordSize(Enum):
    BITS_8 = 8
    BITS_16 = 16
    BITS_32 = 32
    BITS_64 = 64


@dataclass
class DisplayState:
    """Immutable snapshot of everything the View needs to render."""
    main_display: str           # The primary number/result string
    expression_display: str     # The expression line (e.g. "2 + 3 *")
    error: bool                 # True if main_display shows an error
    memory_indicator: bool      # True if memory contains a nonzero value

    # Scientific-specific
    angle_unit: AngleUnit = AngleUnit.DEG
    paren_depth: int = 0

    # Programmer-specific
    number_base: NumberBase = NumberBase.DEC
    word_size: WordSize = WordSize.BITS_64
    hex_value: str = ""
    dec_value: str = ""
    oct_value: str = ""
    bin_value: str = ""


@dataclass
class ButtonEnabledState:
    """Which buttons should be enabled/disabled in the current state.
    Used primarily by Programmer mode to disable invalid digit buttons."""
    digits: dict[str, bool] = field(default_factory=dict)
    # key = button label, value = enabled
    hex_digits: dict[str, bool] = field(default_factory=dict)
    decimal_point: bool = True
```

### 3.2 BaseLogic -- Abstract Base Class

```python
# calculator/logic/base_logic.py (continued)

from abc import ABC, abstractmethod


class BaseLogic(ABC):
    """Shared interface and state for all calculator modes.

    Subclasses implement mode-specific behavior. The base class owns:
    - Memory storage (MC, MR, M+, M-, MS)
    - Display formatting (integer vs float, scientific notation)
    - Input buffer management
    - Error state
    """

    def __init__(self) -> None:
        self._memory: float = 0.0
        self._current_input: str = "0"
        self._expression: str = ""
        self._error: bool = False
        self._new_input: bool = True  # next digit replaces display

    # ── Memory operations (shared across all modes) ──────────────

    def memory_clear(self) -> DisplayState: ...
    def memory_recall(self) -> DisplayState: ...
    def memory_add(self) -> DisplayState: ...
    def memory_subtract(self) -> DisplayState: ...
    def memory_store(self) -> DisplayState: ...

    @property
    def has_memory(self) -> bool:
        """True if memory contains a nonzero value."""
        return self._memory != 0.0

    # ── Input operations ─────────────────────────────────────────

    def input_digit(self, digit: str) -> DisplayState: ...
    def input_decimal(self) -> DisplayState: ...
    def input_sign_toggle(self) -> DisplayState: ...
    def input_backspace(self) -> DisplayState: ...

    # ── Clear operations ─────────────────────────────────────────

    def clear_entry(self) -> DisplayState: ...
    def clear_all(self) -> DisplayState: ...

    # ── Evaluation ───────────────────────────────────────────────

    @abstractmethod
    def evaluate(self) -> DisplayState:
        """Evaluate the current expression and return the result."""
        ...

    # ── State export (for mode switching) ────────────────────────

    def get_current_value(self) -> float:
        """Return the current numeric value for mode-switch handoff."""
        ...

    def set_current_value(self, value: float) -> DisplayState:
        """Set the current value (received from mode-switch handoff)."""
        ...

    # ── Display formatting (shared) ──────────────────────────────

    @staticmethod
    def format_number(value: float) -> str:
        """Format a number for display.

        Rules (from requirements DI-1 through DI-5):
        - Integers display without decimal point: 5 not 5.0
        - Floats display with max 10 significant digits
        - Very large/small numbers use scientific notation
        """
        ...

    # ── Snapshot ─────────────────────────────────────────────────

    @abstractmethod
    def get_display_state(self) -> DisplayState:
        """Build and return the current DisplayState for the View."""
        ...
```

### 3.3 BasicLogic

```python
# calculator/logic/basic_logic.py

from calculator.logic.base_logic import BaseLogic, DisplayState


class BasicLogic(BaseLogic):
    """Basic mode: four arithmetic operators with correct precedence.

    Expression evaluation strategy:
    - Expressions are stored as a list of tokens (numbers and operators).
    - On evaluate(), the token list is processed in two passes:
      1. First pass: resolve * and / (left to right).
      2. Second pass: resolve + and - (left to right).
    - This avoids eval() and gives full control over error handling.
    """

    def __init__(self) -> None:
        super().__init__()
        self._tokens: list = []       # e.g. [2.0, "+", 3.0, "*", 4.0]
        self._pending_op: str = ""    # operator waiting for second operand

    def input_operator(self, op: str) -> DisplayState:
        """Handle +, -, *, / button press.

        Args:
            op: One of "+", "-", "*", "/".

        Returns:
            Updated DisplayState.
        """
        ...

    def input_percent(self) -> DisplayState:
        """Divide current value by 100 (requirement NI-6)."""
        ...

    def evaluate(self) -> DisplayState:
        """Evaluate the token list with correct operator precedence.

        Implements requirements BA-5 and BA-6.
        Division by zero produces an error state (ER-1).
        """
        ...

    def get_display_state(self) -> DisplayState: ...
```

### 3.4 ScientificLogic

```python
# calculator/logic/scientific_logic.py

from calculator.logic.basic_logic import BasicLogic
from calculator.logic.base_logic import DisplayState, AngleUnit


class ScientificLogic(BasicLogic):
    """Scientific mode: extends BasicLogic with advanced math functions.

    Inherits all basic arithmetic. Adds:
    - Trigonometric functions (sin, cos, tan, asin, acos, atan)
    - Logarithmic functions (log, ln, log2)
    - Power and root functions (x^2, x^3, x^n, 10^x, e^x, sqrt, cbrt, 1/x)
    - Constants (pi, e)
    - Factorial, absolute value
    - Parenthesized sub-expressions

    Angle mode (DEG/RAD) affects trig function input/output.
    """

    def __init__(self) -> None:
        super().__init__()
        self._angle_unit: AngleUnit = AngleUnit.DEG
        self._paren_depth: int = 0
        self._paren_stacks: list = []  # stack of saved expression states

    # ── Angle mode ───────────────────────────────────────────────

    def toggle_angle_unit(self) -> DisplayState:
        """Toggle between DEG and RAD. Does not change the current value."""
        ...

    @property
    def angle_unit(self) -> AngleUnit: ...

    # ── Trigonometric functions ──────────────────────────────────

    def trig_sin(self) -> DisplayState: ...
    def trig_cos(self) -> DisplayState: ...
    def trig_tan(self) -> DisplayState: ...
    def trig_asin(self) -> DisplayState: ...
    def trig_acos(self) -> DisplayState: ...
    def trig_atan(self) -> DisplayState: ...

    # ── Logarithmic functions ────────────────────────────────────

    def log_base10(self) -> DisplayState: ...
    def log_natural(self) -> DisplayState: ...
    def log_base2(self) -> DisplayState: ...

    # ── Power and root functions ─────────────────────────────────

    def power_square(self) -> DisplayState: ...
    def power_cube(self) -> DisplayState: ...
    def power_n(self) -> DisplayState:
        """Begin x^n operation. Waits for second operand then evaluate."""
        ...
    def power_10x(self) -> DisplayState: ...
    def power_ex(self) -> DisplayState: ...
    def root_square(self) -> DisplayState: ...
    def root_cube(self) -> DisplayState: ...
    def reciprocal(self) -> DisplayState: ...

    # ── Constants ────────────────────────────────────────────────

    def insert_pi(self) -> DisplayState: ...
    def insert_e(self) -> DisplayState: ...

    # ── Factorial and absolute value ─────────────────────────────

    def factorial(self) -> DisplayState: ...
    def absolute_value(self) -> DisplayState: ...

    # ── Parentheses ──────────────────────────────────────────────

    def open_paren(self) -> DisplayState: ...
    def close_paren(self) -> DisplayState: ...

    def get_display_state(self) -> DisplayState: ...
```

### 3.5 ProgrammerLogic

```python
# calculator/logic/programmer_logic.py

from calculator.logic.base_logic import (
    BaseLogic, DisplayState, ButtonEnabledState,
    NumberBase, WordSize,
)


class ProgrammerLogic(BaseLogic):
    """Programmer mode: integer-only arithmetic in multiple bases.

    Key design decisions:
    - Internal value is always stored as a Python int.
    - The int is masked to the current word size on every mutation
      using two's complement arithmetic.
    - Display conversion to HEX/OCT/BIN is done at display time.
    - Base switching only changes the display, not the stored value.
    - Word size switching masks the existing value to the new size.

    Does NOT inherit from BasicLogic because:
    - No floating-point support.
    - No operator precedence (simple left-to-right evaluation).
    - Completely different operator set (bitwise ops).
    """

    def __init__(self) -> None:
        super().__init__()
        self._value: int = 0
        self._number_base: NumberBase = NumberBase.DEC
        self._word_size: WordSize = WordSize.BITS_64
        self._pending_op: str = ""
        self._operand: int = 0

    # ── Base switching ───────────────────────────────────────────

    def set_base(self, base: NumberBase) -> DisplayState:
        """Switch display base. Value is preserved, display changes."""
        ...

    @property
    def number_base(self) -> NumberBase: ...

    # ── Word size ────────────────────────────────────────────────

    def set_word_size(self, size: WordSize) -> DisplayState:
        """Change word size. Value is masked to new size."""
        ...

    @property
    def word_size(self) -> WordSize: ...

    def _mask_to_word_size(self, value: int) -> int:
        """Apply two's complement masking for current word size.

        Example for 8-bit:
            value & 0xFF gives unsigned bits.
            If high bit set, subtract 2^8 to get signed representation.

        This implements requirements WS-2 and WS-3.
        """
        ...

    # ── Input (base-aware) ───────────────────────────────────────

    def input_digit(self, digit: str) -> DisplayState:
        """Accept a digit valid for the current base (0-9, A-F)."""
        ...

    def input_decimal(self) -> DisplayState:
        """No-op in Programmer mode (requirement PM-3)."""
        ...

    # ── Arithmetic operators (integer-only) ──────────────────────

    def input_operator(self, op: str) -> DisplayState:
        """Handle +, -, *, /, MOD.

        Programmer mode uses simple left-to-right evaluation
        (no operator precedence). Each operator immediately evaluates
        the pending operation if one exists.
        """
        ...

    def evaluate(self) -> DisplayState:
        """Evaluate pending operation. Integer division truncates (PM-2)."""
        ...

    # ── Bitwise operators ────────────────────────────────────────

    def bitwise_and(self) -> DisplayState:
        """Begin AND operation. Waits for second operand."""
        ...

    def bitwise_or(self) -> DisplayState: ...
    def bitwise_xor(self) -> DisplayState: ...

    def bitwise_not(self) -> DisplayState:
        """Immediate unary NOT on current value."""
        ...

    def bitwise_lshift(self) -> DisplayState:
        """Begin left shift. Waits for second operand."""
        ...

    def bitwise_rshift(self) -> DisplayState:
        """Begin arithmetic right shift. Waits for second operand."""
        ...

    # ── Base conversion display ──────────────────────────────────

    def _format_in_base(self, value: int, base: NumberBase) -> str:
        """Format an integer for display in the given base.

        HEX: uppercase, no prefix (e.g. "FF")
        DEC: standard integer string (e.g. "255")
        OCT: no prefix (e.g. "377")
        BIN: no prefix, grouped in 4-bit nibbles (e.g. "1111 1111")
        """
        ...

    def get_all_bases(self) -> dict[str, str]:
        """Return current value in all four bases for the conversion panel.

        Returns:
            {"HEX": "FF", "DEC": "255", "OCT": "377", "BIN": "11111111"}
        """
        ...

    # ── Button enable/disable state ──────────────────────────────

    def get_button_enabled_state(self) -> ButtonEnabledState:
        """Return which digit/hex buttons are enabled for current base.

        BIN: only 0, 1
        OCT: only 0-7
        DEC: only 0-9
        HEX: 0-9 and A-F
        """
        ...

    # ── State export (for mode switching) ────────────────────────

    def get_current_value(self) -> float:
        """Return current int as float for mode-switch handoff."""
        return float(self._value)

    def set_current_value(self, value: float) -> DisplayState:
        """Accept value from mode switch; truncates to int (MS-4)."""
        ...

    def get_display_state(self) -> DisplayState: ...
```

---

## 4. GUI Design

### 4.1 Base View

`base_view.py` defines the shared GUI skeleton that all modes use.

```
BaseView (tkinter.Frame)
├── display_frame (Frame)
│   ├── expression_label (Label)     # secondary display: "2 + 3 *"
│   ├── main_label (Label)           # primary display: "14"
│   └── indicator_frame (Frame)      # "M" indicator, "Deg/Rad", etc.
└── button_frame (Frame)             # populated by subclass
```

**BaseView responsibilities:**
- Create and manage the display panel (shared by all modes).
- Provide `update_display(state: DisplayState)` method.
- Provide `set_callbacks(callbacks: dict[str, Callable])` to wire buttons.
- Manage the button_frame placeholder that subclasses populate.

**BaseView interface:**

```python
# calculator/gui/base_view.py

import tkinter as tk
from typing import Callable, Optional


class BaseView(tk.Frame):
    """Abstract base for all calculator mode views."""

    def __init__(self, parent: tk.Widget) -> None: ...

    def update_display(self, state) -> None:
        """Update all display elements from a DisplayState object."""
        ...

    def set_callbacks(self, callbacks: dict[str, Callable]) -> None:
        """Wire button presses to controller callbacks.

        Args:
            callbacks: Maps action names to callables.
                Example: {"digit_0": fn, "op_add": fn, "evaluate": fn, ...}
        """
        ...

    def build_buttons(self) -> None:
        """Subclasses override to populate self.button_frame."""
        ...

    def destroy_buttons(self) -> None:
        """Remove all widgets from button_frame (used during mode switch)."""
        ...
```

### 4.2 Basic View Layout

```
+---------------------------------------+
|  expression_label                     |   <- Label, right-aligned, smaller font
|  main_label                           |   <- Label, right-aligned, large font
|  [M]                                  |   <- memory indicator, left-aligned
+---------------------------------------+
| MC  | MR  | M+  | M-  | MS          |   <- row 0 (memory row)
+-----+-----+-----+-----+-------------+
|  C  | +/- |  %  |  /  |             |   <- row 1
+-----+-----+-----+-----+             |
|  7  |  8  |  9  |  *  |             |   <- row 2
+-----+-----+-----+-----+             |
|  4  |  5  |  6  |  -  |             |   <- row 3
+-----+-----+-----+-----+             |
|  1  |  2  |  3  |  +  |             |   <- row 4
+-----+-----+-----+-----+-------------+
|     0     |  .  |  =  | Backspace   |   <- row 5 (0 spans 2 cols)
+-----------+-----+-----+-------------+

Grid: 5 columns x 6 rows (memory row + 5 button rows)
Button 0 uses columnspan=2.
Window size: approximately 320 x 480 pixels.
```

### 4.3 Scientific View Layout

Scientific mode adds five columns of function buttons to the left of the
basic grid and a Deg/Rad toggle in the indicator area.

```
+-----------------------------------------------------------+
|  expression_label                                         |
|  main_label                              [Deg] [paren: 2] |
|  [M]                                                      |
+-----------------------------------------------------------+
| MC  | MR  | M+  | M-  | MS                               |
+-----+-----+-----+-----+-----+-----+-----+-----+----------+
|  (  |  )  | x^2 | x^3 | x^n |  C  | +/- |  %  |  /     |
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
| sin | cos | tan | sqr | cbr |  7  |  8  |  9  |  *      |
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
|asin |acos |atan | 10x | e^x |  4  |  5  |  6  |  -      |
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
| n!  | |x| | log | ln  |log2 |  1  |  2  |  3  |  +      |
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
| pi  |  e  | 1/x |     |     |     0     |  .  |  =      |
+-----+-----+-----+-----+-----+-----------+-----+---------+

Grid: 9 columns x 7 rows (memory row + 6 button rows)
Window size: approximately 560 x 520 pixels.
```

### 4.4 Programmer View Layout

Programmer mode replaces the scientific functions with hex digit buttons,
bitwise operators, a base selector, and a base conversion panel.

```
+-----------------------------------------------------------+
|  expression_label                                         |
|  main_label                              [Word: 64-bit]   |
+-----------------------------------------------------------+
|  HEX: FF     DEC: 255     OCT: 377     BIN: 11111111     |  <- conversion panel
+-----------------------------------------------------------+
|  (o) DEC   (o) HEX   (o) OCT   (o) BIN                  |  <- radio buttons
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
|  A  |  B  |  C  |  D  |  E  |  F  | AND | OR  |  AC     |
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
| NOT | XOR | LSH | RSH |     |  C  | +/- | MOD |  /      |
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
|     |     |     |     |     |  7  |  8  |  9  |  *      |
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
|     |     |     |     |     |  4  |  5  |  6  |  -      |
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
|     |     |     |     |     |  1  |  2  |  3  |  +      |
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
|                               |     0     |  = |  <x     |
+-------------------------------+-----------+----+---------+

Grid: 9 columns x 8 rows (conversion + base selector + 6 button rows)
Window size: approximately 560 x 580 pixels.
```

The conversion panel is a read-only frame (four Labels) that updates on every
state change to show all four base representations simultaneously.

The base selector is a row of four tkinter Radiobuttons sharing an IntVar.

The word size selector is a dropdown (OptionMenu) or a row of Radiobuttons
in the indicator area of the display panel.

---

## 5. Controller Design (app.py)

The Controller is the `CalculatorApp` class. It owns the tkinter root window,
the menu bar, the current logic instance, and the current view instance.

```python
# calculator/app.py

import tkinter as tk
from calculator.logic.base_logic import Mode, DisplayState
from calculator.logic.basic_logic import BasicLogic
from calculator.logic.scientific_logic import ScientificLogic
from calculator.logic.programmer_logic import ProgrammerLogic
from calculator.gui.basic_view import BasicView
from calculator.gui.scientific_view import ScientificView
from calculator.gui.programmer_view import ProgrammerView


class CalculatorApp:
    """Main controller. Manages mode switching and event routing."""

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._mode: Mode = Mode.BASIC
        self._logic: BasicLogic | ScientificLogic | ProgrammerLogic = None
        self._view: BasicView | ScientificView | ProgrammerView = None
        self._memory: float = 0.0  # preserved across mode switches

        self._build_menu()
        self._switch_mode(Mode.BASIC)
        self._bind_keyboard()

    def _build_menu(self) -> None:
        """Create the menu bar with mode selection."""
        ...

    def _switch_mode(self, new_mode: Mode) -> None:
        """Switch between calculator modes.

        Steps:
        1. Read current value and memory from existing logic (if any).
        2. Destroy current view.
        3. Instantiate new logic for the target mode.
        4. Transfer memory to new logic.
        5. Transfer current value:
           - Basic <-> Scientific: preserve float value (MS-3).
           - Any -> Programmer: truncate to int (MS-4).
           - Programmer -> Any: preserve int as float (MS-5).
        6. Instantiate new view.
        7. Wire callbacks from view to controller methods.
        8. Resize window.
        9. Render initial display state.
        """
        ...

    def _resize_window(self, mode: Mode) -> None:
        """Resize to appropriate dimensions for the mode."""
        ...

    def _build_callbacks(self) -> dict[str, callable]:
        """Build the callback dictionary for the current mode.

        Returns a dict mapping action names to bound methods:
        {
            "digit_0": lambda: self._on_digit("0"),
            "digit_1": lambda: self._on_digit("1"),
            ...
            "op_add": lambda: self._on_operator("+"),
            "evaluate": self._on_evaluate,
            "clear_entry": self._on_clear_entry,
            "clear_all": self._on_clear_all,
            "memory_clear": self._on_memory_clear,
            ...
        }
        """
        ...

    def _refresh_display(self) -> None:
        """Get DisplayState from logic and push to view."""
        state = self._logic.get_display_state()
        self._view.update_display(state)

    # ── Event handlers ───────────────────────────────────────────

    def _on_digit(self, digit: str) -> None:
        self._logic.input_digit(digit)
        self._refresh_display()

    def _on_operator(self, op: str) -> None:
        self._logic.input_operator(op)
        self._refresh_display()

    def _on_evaluate(self) -> None:
        self._logic.evaluate()
        self._refresh_display()

    # ... similar one-liner handlers for every action ...

    def _bind_keyboard(self) -> None:
        """Bind keyboard events to the root window. See section 6."""
        ...
```

---

## 6. Event Handling Design

### 6.1 Button Events

Each View subclass creates tkinter Button widgets in `build_buttons()`. Each
button is bound to a callback name from the callbacks dictionary:

```python
# Example inside basic_view.py build_buttons():
btn = tk.Button(self.button_frame, text="7",
                command=self._callbacks["digit_7"])
```

The callbacks dictionary is set by the Controller via `set_callbacks()` before
`build_buttons()` is called. The View never knows what the callbacks do -- it
just invokes them.

### 6.2 Keyboard Events

All keyboard bindings are registered on the root window by the Controller in
`_bind_keyboard()`. This centralizes input handling and avoids focus issues.

```python
def _bind_keyboard(self) -> None:
    root = self._root

    # Digit keys
    for d in "0123456789":
        root.bind(d, lambda e, digit=d: self._on_digit(digit))

    # Operators
    root.bind("+", lambda e: self._on_operator("+"))
    root.bind("-", lambda e: self._on_operator("-"))
    root.bind("*", lambda e: self._on_operator("*"))
    root.bind("/", lambda e: self._on_operator("/"))

    # Enter/Return = evaluate
    root.bind("<Return>", lambda e: self._on_evaluate())
    root.bind("<KP_Enter>", lambda e: self._on_evaluate())

    # Escape = All Clear
    root.bind("<Escape>", lambda e: self._on_clear_all())

    # Backspace
    root.bind("<BackSpace>", lambda e: self._on_backspace())

    # Mode switching
    root.bind("<Control-Key-1>", lambda e: self._switch_mode(Mode.BASIC))
    root.bind("<Control-Key-2>", lambda e: self._switch_mode(Mode.SCIENTIFIC))
    root.bind("<Control-Key-3>", lambda e: self._switch_mode(Mode.PROGRAMMER))

    # Programmer-specific (conditionally handled inside handlers)
    root.bind("&", lambda e: self._on_bitwise("AND"))
    root.bind("|", lambda e: self._on_bitwise("OR"))
    root.bind("^", lambda e: self._on_bitwise("XOR"))
    root.bind("~", lambda e: self._on_bitwise("NOT"))

    # Hex digits (conditionally handled in _on_digit)
    for c in "abcdefABCDEF":
        root.bind(c, lambda e, ch=c: self._on_digit(ch.upper()))

    # Parentheses (Scientific mode only, checked inside handler)
    root.bind("(", lambda e: self._on_open_paren())
    root.bind(")", lambda e: self._on_close_paren())
```

Mode-specific keys (hex digits, parentheses, bitwise operators) are always
bound but the handler methods check `self._mode` and silently ignore
inapplicable keys. This avoids rebinding on every mode switch.

### 6.3 Event Flow Diagram

```
  [User presses "7" on keyboard]
            |
            v
  root.bind("7") fires lambda
            |
            v
  CalculatorApp._on_digit("7")
            |
            v
  self._logic.input_digit("7")       <-- pure Python, no GUI
            |
            v
  returns None (mutates logic state)
            |
            v
  CalculatorApp._refresh_display()
            |
            v
  self._logic.get_display_state()     <-- returns DisplayState
            |
            v
  self._view.update_display(state)    <-- updates tkinter Labels
            |
            v
  [Display shows "7"]
```

---

## 7. Mode Switching Design

### 7.1 State Transfer

When switching modes, the Controller:

1. Reads the current numeric value from the old logic via `get_current_value()`.
2. Reads the memory value from the old logic (`_memory` attribute).
3. Creates a new logic instance for the target mode.
4. Transfers memory: `new_logic._memory = old_memory`.
5. Transfers the value via `new_logic.set_current_value(value)`.

The expression and pending operations are intentionally discarded. Only the
current numeric value and memory survive a mode switch.

### 7.2 Value Conversion Rules

| From | To | Conversion |
|------|----|------------|
| Basic | Scientific | Pass float as-is (MS-3) |
| Scientific | Basic | Pass float as-is (MS-3) |
| Basic/Scientific | Programmer | `int(value)` -- truncate toward zero (MS-4) |
| Programmer | Basic/Scientific | `float(int_value)` -- exact (MS-5) |

### 7.3 View Swap

```python
def _switch_mode(self, new_mode: Mode) -> None:
    # 1. Save state from current logic
    if self._logic is not None:
        old_value = self._logic.get_current_value()
        old_memory = self._logic._memory
    else:
        old_value = 0.0
        old_memory = 0.0

    # 2. Destroy old view
    if self._view is not None:
        self._view.destroy()

    # 3. Create new logic
    if new_mode == Mode.BASIC:
        self._logic = BasicLogic()
    elif new_mode == Mode.SCIENTIFIC:
        self._logic = ScientificLogic()
    elif new_mode == Mode.PROGRAMMER:
        self._logic = ProgrammerLogic()

    # 4. Transfer state
    self._logic._memory = old_memory
    self._logic.set_current_value(old_value)

    # 5. Create new view
    view_cls = {
        Mode.BASIC: BasicView,
        Mode.SCIENTIFIC: ScientificView,
        Mode.PROGRAMMER: ProgrammerView,
    }[new_mode]
    self._view = view_cls(self._root)
    self._view.set_callbacks(self._build_callbacks())
    self._view.build_buttons()
    self._view.pack(fill=tk.BOTH, expand=True)

    # 6. Resize and render
    self._mode = new_mode
    self._resize_window(new_mode)
    self._refresh_display()
```

---

## 8. Memory System Design

Memory is a single float value shared across all modes. It is stored as an
instance attribute `_memory` on whichever logic object is currently active.
During mode switches, the Controller transfers it.

### 8.1 Operations

| Operation | Effect | Requirements |
|-----------|--------|-------------|
| MC | `_memory = 0.0` | MF-1 |
| MR | Set display to `_memory` value | MF-2 |
| M+ | `_memory += current_display_value` | MF-3 |
| M- | `_memory -= current_display_value` | MF-4 |
| MS | `_memory = current_display_value` | MF-5 |

### 8.2 Memory Indicator

`DisplayState.memory_indicator` is `True` whenever `_memory != 0.0`. The View
renders this as a small "M" label in the indicator frame. This satisfies MF-6.

### 8.3 Cross-Mode Persistence

Memory persists across mode switches because the Controller explicitly copies
it from the old logic to the new logic during `_switch_mode()`. This satisfies
MF-7.

### 8.4 Memory in Programmer Mode

In Programmer mode, memory still stores a float internally, but `memory_store`
stores `float(self._value)` and `memory_recall` truncates `int(self._memory)`
before displaying. This avoids introducing a second memory slot while
preserving the integer-only constraint of Programmer mode.

---

## 9. Error Handling Strategy

### 9.1 Error Representation

Errors are represented as a boolean flag `_error` on the logic object and the
string `"Error"` in `DisplayState.main_display`. The logic never raises
exceptions to the Controller. Instead:

```python
# Inside a logic method:
def evaluate(self) -> DisplayState:
    try:
        result = self._evaluate_tokens()
        self._current_input = self.format_number(result)
    except (ZeroDivisionError, ValueError, OverflowError):
        self._error = True
        self._current_input = "Error"
    return self.get_display_state()
```

### 9.2 Error Conditions Mapped to Python Exceptions

| Requirement | Condition | Caught Exception |
|-------------|-----------|------------------|
| ER-1 | Division by zero | `ZeroDivisionError` |
| ER-2 | sqrt(-1), log(0), log(-1) | `ValueError` (from `math` module) |
| ER-3 | Word size overflow | Not an exception; handled by `_mask_to_word_size()` |
| ER-4 | Factorial of negative/non-int | `ValueError` (raised explicitly) |
| ER-5 | Mismatched parentheses | `ValueError` (raised explicitly) |
| ER-6 | Malformed expression | `ValueError` (raised explicitly) |
| ER-7 | tan(90 degrees) | `ValueError` (detected by checking near-zero cos) |

### 9.3 Error Recovery

When `_error` is True:

- `input_digit()` clears the error flag, resets input, and starts fresh (RC-1).
- `clear_entry()` and `clear_all()` clear the error flag (RC-2).
- All other operations (operators, functions) are no-ops while in error state.

### 9.4 Crash Prevention

The Controller wraps every event handler in a safety net to satisfy RC-3:

```python
def _safe_call(self, fn: Callable, *args) -> None:
    """Call fn(*args), catching any unexpected exception."""
    try:
        fn(*args)
    except Exception:
        # Last resort: set error state without crashing
        self._logic._error = True
        self._logic._current_input = "Error"
    self._refresh_display()
```

This ensures no Python traceback is ever shown to the user, even for bugs
not anticipated by the logic layer.

---

## 10. Expression Evaluation Strategy

### 10.1 Basic Mode -- Token-Based Evaluation

Expressions are accumulated as a list of tokens rather than as a string
passed to `eval()`. This gives full control over precedence and error
handling without any security risk.

```
User presses: 2 + 3 * 4 =

Tokens accumulated: [2.0, "+", 3.0, "*", 4.0]

Evaluation (two-pass):
  Pass 1 - resolve * and /:
    [2.0, "+", 12.0]
  Pass 2 - resolve + and -:
    [14.0]

Result: 14.0
```

### 10.2 Scientific Mode -- Parenthesized Sub-Expressions

Parentheses are handled by a stack of expression states. When `(` is pressed,
the current token list and pending state are pushed onto the stack. When `)` is
pressed, the sub-expression is evaluated and its result becomes a single token
in the parent expression.

```
User presses: ( 2 + 3 ) * 4 =

Open paren: push current state, start fresh tokens []
Tokens inside parens: [2.0, "+", 3.0]
Close paren: evaluate inner -> 5.0, pop parent state, insert 5.0
Tokens at top level: [5.0, "*", 4.0]
Evaluate: 20.0
```

### 10.3 Programmer Mode -- Immediate Evaluation

Programmer mode uses no precedence. Each binary operator immediately evaluates
the pending operation (left-to-right, like a classic RPN-adjacent calculator):

```
User presses: 12 AND 10 OR 5 =

12 AND -> store 12 as left operand, "AND" as pending op
10 OR  -> evaluate 12 AND 10 = 8, store 8, "OR" as pending op
5 =    -> evaluate 8 OR 5 = 13

Result: 13
```

---

## 11. Display Formatting Rules

Implemented in `BaseLogic.format_number()`:

1. If the value is an integer (no fractional part), display without decimal:
   `5` not `5.0`.
2. For floats, display up to 10 significant digits, stripping trailing zeros.
3. If `abs(value) >= 1e16` or `abs(value) < 1e-10` (and nonzero), switch to
   scientific notation with 10 significant digits.
4. In Programmer mode, `ProgrammerLogic._format_in_base()` overrides this with
   base-specific formatting (uppercase hex, grouped binary, etc.).

---

## 12. Design Decisions and Rationale

| Decision | Rationale |
|----------|-----------|
| Token-based evaluation, not `eval()` | Security, control over error handling, testability |
| ProgrammerLogic inherits BaseLogic, not BasicLogic | Completely different numeric model (int vs float), different operator set, no precedence |
| ScientificLogic inherits BasicLogic | All basic operations carry over; scientific adds to them |
| Single memory float, not per-mode memory | Requirements say memory persists across modes (MF-7) |
| DisplayState dataclass as the View contract | Decouples View from Logic internals; easy to test |
| Keyboard bindings on root, mode-checked in handler | Avoids unbind/rebind churn on mode switch |
| Two's complement via bit masking | Matches hardware behavior; simple and correct |
| Controller wraps all handlers in safety net | Guarantees no traceback reaches the user (RC-3) |
| Views are destroyed and recreated on mode switch | Simpler than hiding/showing; no stale widget state |

---

## 13. Testing Strategy

All logic classes are testable without tkinter:

```python
# Example test
def test_basic_addition():
    logic = BasicLogic()
    logic.input_digit("2")
    logic.input_operator("+")
    logic.input_digit("3")
    state = logic.evaluate()
    assert state.main_display == "5"
    assert state.error is False
```

Test files map to the structure in requirements section 10:

| Test File | Covers |
|-----------|--------|
| `test_basic.py` | BasicLogic: arithmetic, precedence, chaining, percent |
| `test_scientific.py` | ScientificLogic: trig, log, power, root, factorial, parens, constants |
| `test_programmer.py` | ProgrammerLogic: base conversion, bitwise ops, word size, overflow |
| `test_memory.py` | Memory operations via BaseLogic/BasicLogic |
| `test_mode_switch.py` | Value preservation, memory transfer, truncation rules |

Every test instantiates a logic object directly, calls methods, and asserts
on the returned `DisplayState`. No tkinter window is ever created in tests.
