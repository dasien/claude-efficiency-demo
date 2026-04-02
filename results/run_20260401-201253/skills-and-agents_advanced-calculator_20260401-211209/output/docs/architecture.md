# Advanced Calculator -- Architecture Document

**Version:** 1.0
**Date:** 2026-04-01
**Based on:** Requirements Document v1.0

---

## 1. File Structure

```
project/
├── calculator/
│   ├── __init__.py
│   ├── app.py                  # Controller: coordinates logic and GUI, manages mode switching
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── base_view.py        # Shared display, memory indicator, menu bar, common layout
│   │   ├── basic_view.py       # Basic mode button grid
│   │   ├── scientific_view.py  # Scientific mode button grid (extends basic)
│   │   └── programmer_view.py  # Programmer mode layout with base panel
│   └── logic/
│       ├── __init__.py
│       ├── base_logic.py       # BaseCalculator: memory, display formatting, error state
│       ├── basic_logic.py      # BasicCalculator(BaseCalculator): arithmetic with precedence
│       ├── scientific_logic.py # ScientificCalculator(BasicCalculator): scientific functions
│       └── programmer_logic.py # ProgrammerCalculator(BaseCalculator): integer/bitwise/base ops
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

## 2. MVC Architecture

The application follows Model-View-Controller with a strict dependency rule: the GUI layer depends on the logic layer, never the reverse.

```
+-----------+         +-------------+         +----------+
|   View    | ------> | Controller  | ------> |  Model   |
| (gui/)    |         | (app.py)    |         | (logic/) |
+-----------+         +-------------+         +----------+
      ^                     |
      |                     |
      +---------------------+
        Controller updates View
```

- **Model (logic/)** -- Pure Python classes with no Tkinter imports. All calculator state and computation lives here. Fully unit-testable.
- **View (gui/)** -- Tkinter widgets. Each view knows how to lay out buttons and display results. Views expose methods for the controller to call (e.g., `set_display`, `set_expression`, `enable_buttons`). Views report user actions via callbacks.
- **Controller (app.py)** -- The `App` class inherits from `tk.Tk`. It instantiates the logic objects and view objects, wires button callbacks to logic methods, and pushes results back to the view after each operation.

---

## 3. Module Interfaces

### 3.1 base_logic.py -- BaseCalculator

The abstract base for all calculator modes. Manages memory, display formatting, expression state, and error handling.

```python
class BaseCalculator:
    """Base calculator with memory, display formatting, and error state."""

    # --- State attributes ---
    current_value: float          # The current numeric value
    expression: str               # The expression string being built
    memory: float                 # Stored memory value (0.0 when empty)
    has_memory: bool              # True when memory holds a user-stored value
    error: bool                   # True when in error state
    error_message: str            # e.g., "Error", "Division by zero"
    input_buffer: str             # Raw digit string the user is typing

    # --- Memory functions ---
    def mc(self) -> None: ...              # Memory Clear: reset memory to 0, has_memory = False
    def mr(self) -> float: ...             # Memory Recall: return stored memory value
    def m_plus(self) -> None: ...          # Memory Add: memory += current_value
    def m_minus(self) -> None: ...         # Memory Subtract: memory -= current_value
    def ms(self) -> None: ...              # Memory Store: memory = current_value, has_memory = True

    # --- Display formatting ---
    def format_number(self, value: float) -> str: ...
        # Integer results displayed without decimal (5 not 5.0)
        # Max 10 significant digits for floats
        # Scientific notation for very large/small values

    # --- Input handling ---
    def append_digit(self, digit: str) -> None: ...      # Add digit to input_buffer
    def append_decimal(self) -> None: ...                 # Add decimal point (once only)
    def toggle_sign(self) -> None: ...                    # Negate current value
    def percentage(self) -> None: ...                     # Divide current value by 100
    def backspace(self) -> None: ...                      # Remove last char from input_buffer
    def clear_entry(self) -> None: ...                    # Clear current entry (C)
    def clear_all(self) -> None: ...                      # Reset all state (AC)

    # --- Error state ---
    def set_error(self, message: str = "Error") -> None: ...
    def clear_error(self) -> None: ...

    # --- Value access ---
    def get_display_value(self) -> str: ...               # Formatted string for display
    def get_expression_display(self) -> str: ...          # Expression string for secondary display
```

### 3.2 basic_logic.py -- BasicCalculator

Inherits from `BaseCalculator`. Adds arithmetic with correct operator precedence via expression parsing.

```python
class BasicCalculator(BaseCalculator):
    """Basic arithmetic calculator with operator precedence."""

    def add_operator(self, operator: str) -> None: ...
        # operator is one of: '+', '-', '*', '/'
        # Finalizes the current input_buffer into the expression
        # Appends the operator to the expression

    def evaluate(self) -> float: ...
        # Parses and evaluates the full expression string
        # Respects operator precedence (* and / before + and -)
        # Sets error state on division by zero or malformed expression
        # Returns the result

    def _parse_expression(self, expr: str) -> float: ...
        # Internal: tokenizes and evaluates with precedence
        # Uses a simple recursive descent or shunting-yard approach
```

### 3.3 scientific_logic.py -- ScientificCalculator

Inherits from `BasicCalculator`. Adds scientific functions, parentheses, constants, and degree/radian toggle.

```python
class ScientificCalculator(BasicCalculator):
    """Scientific calculator with trig, logs, powers, roots, and parentheses."""

    angle_mode: str               # "DEG" or "RAD"
    paren_depth: int              # Current parenthesis nesting depth

    # --- Angle mode ---
    def toggle_angle_mode(self) -> str: ...   # Toggle DEG/RAD, return new mode

    # --- Trigonometric (operate on current_value, respect angle_mode) ---
    def sin(self) -> float: ...
    def cos(self) -> float: ...
    def tan(self) -> float: ...               # Error if undefined (e.g., 90 deg)
    def asin(self) -> float: ...              # Error if |value| > 1
    def acos(self) -> float: ...              # Error if |value| > 1
    def atan(self) -> float: ...

    # --- Logarithmic (operate on current_value) ---
    def log(self) -> float: ...               # Base-10; Error if value <= 0
    def ln(self) -> float: ...                # Natural log; Error if value <= 0
    def log2(self) -> float: ...              # Base-2; Error if value <= 0

    # --- Powers and roots ---
    def square(self) -> float: ...            # x^2
    def cube(self) -> float: ...              # x^3
    def power(self) -> None: ...              # xⁿ -- sets pending two-operand op
    def ten_power(self) -> float: ...         # 10^x
    def e_power(self) -> float: ...           # e^x
    def square_root(self) -> float: ...       # Error if value < 0
    def cube_root(self) -> float: ...
    def reciprocal(self) -> float: ...        # 1/x; Error if value == 0

    # --- Factorial and absolute value ---
    def factorial(self) -> float: ...         # Error if value < 0 or non-integer
    def absolute(self) -> float: ...          # |x|

    # --- Parentheses ---
    def open_paren(self) -> None: ...         # Push '(' onto expression, increment depth
    def close_paren(self) -> None: ...        # Push ')' onto expression, decrement depth

    # --- Constants ---
    def insert_pi(self) -> None: ...          # Set current_value to math.pi
    def insert_e(self) -> None: ...           # Set current_value to math.e
```

### 3.4 programmer_logic.py -- ProgrammerCalculator

Inherits from `BaseCalculator` (not BasicCalculator, since it operates on integers only with different rules).

```python
class ProgrammerCalculator(BaseCalculator):
    """Integer-only calculator with base conversion, bitwise ops, word size."""

    base: str                     # "DEC", "HEX", "OCT", or "BIN"
    word_size: int                # 8, 16, 32, or 64

    # --- Base conversion ---
    def set_base(self, base: str) -> None: ...
        # Convert current value display to new base
        # Enable/disable digit buttons via returned info

    def get_value_in_base(self, base: str) -> str: ...
        # Return current integer value formatted in the given base
        # Used by the base conversion panel to show all four bases

    def get_all_bases(self) -> dict[str, str]: ...
        # Return {"DEC": "255", "HEX": "FF", "OCT": "377", "BIN": "11111111"}

    def get_valid_digits(self) -> set[str]: ...
        # Return set of valid digit characters for current base

    # --- Word size ---
    def set_word_size(self, bits: int) -> None: ...
        # Constrain current value to new word size via mask_value
        # bits is one of: 8, 16, 32, 64

    def mask_value(self, value: int) -> int: ...
        # Apply two's complement wrapping for current word_size
        # e.g., 8-bit: value & 0xFF, then sign-extend if bit 7 is set

    # --- Arithmetic (integer only) ---
    def add_operator(self, operator: str) -> None: ...
        # operator: '+', '-', '*', '/', '%'

    def evaluate(self) -> int: ...
        # Integer arithmetic; division truncates toward zero
        # Result is masked to word_size

    # --- Bitwise operations ---
    def bitwise_and(self) -> None: ...        # Two-operand: pending AND
    def bitwise_or(self) -> None: ...         # Two-operand: pending OR
    def bitwise_xor(self) -> None: ...        # Two-operand: pending XOR
    def bitwise_not(self) -> int: ...         # Unary: flip all bits within word_size
    def left_shift(self) -> None: ...         # Two-operand: pending LSH
    def right_shift(self) -> None: ...        # Two-operand: pending RSH

    # --- Hex digit input ---
    def append_hex_digit(self, digit: str) -> None: ...
        # digit is one of: 'A'-'F'
        # Only valid when base == "HEX"

    # --- Overrides ---
    def append_decimal(self) -> None: ...     # No-op; decimal point disabled
    def format_number(self, value: float) -> str: ...
        # Override: always format as integer in current base
```

---

## 4. GUI Layout Per Mode

Each view class extends a shared `BaseView` that provides the display area (expression line and result line) and the memory indicator.

### 4.1 base_view.py -- BaseView

```python
class BaseView(ttk.Frame):
    """Shared display components for all calculator modes."""

    # Components:
    #   - expression_label: secondary display showing the expression being built
    #   - result_display: primary display showing the current number or result
    #   - memory_indicator: small "M" label, visible when memory is stored
    #   - mode_menu: menu bar or tab strip for mode switching

    def set_display(self, text: str) -> None: ...
    def set_expression(self, text: str) -> None: ...
    def show_memory_indicator(self, visible: bool) -> None: ...
    def set_button_callback(self, button_id: str, callback: Callable) -> None: ...
```

### 4.2 basic_view.py -- BasicView(BaseView)

Lays out the Basic mode grid as specified in requirements section 3.6. Memory row on top, then the 5x4 button grid with operators on the right and `0` spanning two columns.

### 4.3 scientific_view.py -- ScientificView(BaseView)

Extends the layout with five additional columns on the left for scientific functions, plus a Deg/Rad indicator near the display. Layout per requirements section 4.7.

### 4.4 programmer_view.py -- ProgrammerView(BaseView)

Distinct layout with base conversion panel, base selector radio buttons, hex digit row, bitwise operation buttons, and word size selector. Layout per requirements section 5.6. Adds:

```python
class ProgrammerView(BaseView):
    def set_base_panel(self, values: dict[str, str]) -> None: ...
        # Update the HEX/DEC/OCT/BIN simultaneous display

    def set_active_base(self, base: str) -> None: ...
        # Highlight the active base selector

    def enable_digits(self, valid_digits: set[str]) -> None: ...
        # Enable/disable digit buttons based on current base

    def set_word_size_display(self, bits: int) -> None: ...
```

---

## 5. Event Handling Design

### 5.1 Callback Registration

The controller (`app.py`) registers callbacks on each view's buttons during initialization. Views do not call logic directly.

```
Button press -> View fires callback -> Controller method -> Logic method -> Controller updates View
```

### 5.2 Keyboard Shortcuts

The controller binds keyboard events on the root `tk.Tk` window using `bind()` and `bind_all()`. A single dispatcher method routes key events to the appropriate logic method based on the current mode.

```python
# In App.__init__:
self.bind('<Key>', self._on_key_press)
self.bind('<Control-Key-1>', lambda e: self.switch_mode("basic"))
self.bind('<Control-Key-2>', lambda e: self.switch_mode("scientific"))
self.bind('<Control-Key-3>', lambda e: self.switch_mode("programmer"))
```

### 5.3 Controller Dispatch Pattern

Every user action follows the same pattern in the controller:

```python
def _on_digit(self, digit: str) -> None:
    self.logic.append_digit(digit)
    self._update_display()

def _on_operator(self, op: str) -> None:
    self.logic.add_operator(op)
    self._update_display()

def _on_equals(self) -> None:
    self.logic.evaluate()
    self._update_display()

def _update_display(self) -> None:
    if self.logic.error:
        self.view.set_display(self.logic.error_message)
    else:
        self.view.set_display(self.logic.get_display_value())
    self.view.set_expression(self.logic.get_expression_display())
    self.view.show_memory_indicator(self.logic.has_memory)
    # Programmer mode: also update base conversion panel
```

---

## 6. Mode Switching

The controller owns the mode-switching logic. Each mode has its own logic instance and view instance.

### 6.1 State During Mode Switch

```python
class App(tk.Tk):
    def __init__(self):
        self.logic_instances = {
            "basic": BasicCalculator(),
            "scientific": ScientificCalculator(),
            "programmer": ProgrammerCalculator(),
        }
        self.views = {
            "basic": BasicView(self),
            "scientific": ScientificView(self),
            "programmer": ProgrammerView(self),
        }
        self.current_mode: str = "basic"
```

### 6.2 Value Transfer Rules

| From | To | Conversion |
|------|----|------------|
| Basic | Scientific | Preserve float value as-is |
| Scientific | Basic | Preserve float value as-is |
| Basic/Scientific | Programmer | Truncate to int via `int()`, mask to current word size |
| Programmer | Basic/Scientific | Convert current integer to float |

### 6.3 Switch Procedure

```python
def switch_mode(self, new_mode: str) -> None:
    if new_mode == self.current_mode:
        return

    old_logic = self.logic_instances[self.current_mode]
    new_logic = self.logic_instances[new_mode]

    # Transfer value
    value = old_logic.current_value
    if new_mode == "programmer":
        value = int(value)
        new_logic.current_value = new_logic.mask_value(value)
    else:
        if self.current_mode == "programmer":
            value = float(old_logic.current_value)
        new_logic.current_value = value

    # Transfer memory (shared across all modes)
    new_logic.memory = old_logic.memory
    new_logic.has_memory = old_logic.has_memory

    # Swap views: hide current, show new
    self.views[self.current_mode].pack_forget()
    self.views[new_mode].pack(fill="both", expand=True)

    # Resize window
    self._resize_for_mode(new_mode)

    self.current_mode = new_mode
    self._update_display()
```

Memory persists across mode switches because it is explicitly copied between logic instances.

---

## 7. Data Flow

### 7.1 Standard Calculation Flow

```
User clicks "7"
  -> BasicView fires digit_callback("7")
  -> App._on_digit("7")
  -> BasicCalculator.append_digit("7")
     (input_buffer becomes "7", current_value becomes 7.0)
  -> App._update_display()
  -> BasicView.set_display("7")

User clicks "+"
  -> App._on_operator("+")
  -> BasicCalculator.add_operator("+")
     (expression becomes "7 +", input_buffer cleared)
  -> App._update_display()
  -> BasicView.set_expression("7 +")

User clicks "3", then "="
  -> BasicCalculator.append_digit("3")
  -> BasicCalculator.evaluate()
     (_parse_expression("7 + 3") returns 10.0)
  -> App._update_display()
  -> BasicView.set_display("10")
  -> BasicView.set_expression("7 + 3 =")
```

### 7.2 Error Flow

```
User enters "1 / 0 ="
  -> BasicCalculator.evaluate()
     (division by zero detected)
  -> BasicCalculator.set_error("Error")
     (error = True, error_message = "Error")
  -> App._update_display()
  -> BasicView.set_display("Error")

User presses "5"
  -> App._on_digit("5")
  -> BasicCalculator.clear_error() is called first
  -> BasicCalculator.clear_all()
  -> BasicCalculator.append_digit("5")
  -> App._update_display()
  -> BasicView.set_display("5")
```

### 7.3 Programmer Mode Base Conversion Flow

```
User is in DEC mode, display shows "255"
User clicks "HEX" radio button
  -> App._on_base_change("HEX")
  -> ProgrammerCalculator.set_base("HEX")
     (internal value stays 255, display format changes)
  -> App._update_display()
  -> ProgrammerView.set_display("FF")
  -> ProgrammerView.set_base_panel({"DEC": "255", "HEX": "FF", "OCT": "377", "BIN": "11111111"})
  -> ProgrammerView.enable_digits({"0"-"9", "A"-"F"})
```

---

## 8. Key Design Decisions

1. **Expression-based evaluation**: Both `BasicCalculator` and `ScientificCalculator` build an expression string and parse it on `evaluate()`. This naturally handles operator precedence and parentheses without complex state machines.

2. **ProgrammerCalculator inherits from BaseCalculator, not BasicCalculator**: Programmer mode has fundamentally different rules (integer-only, no decimals, different operator set, base conversion). Sharing the base memory and display infrastructure is sufficient; arithmetic behavior diverges too much to share with BasicCalculator.

3. **Separate logic instances per mode**: Each mode maintains its own logic instance. This avoids state contamination and simplifies mode-specific behavior. Values and memory are explicitly transferred during mode switches.

4. **Views are swapped, not rebuilt**: All three views are created at startup and shown/hidden during mode switches. This avoids widget creation overhead and preserves any internal widget state.

5. **No external dependencies**: The application uses only the Python standard library. `math` module provides all scientific functions. Expression parsing uses a simple recursive descent parser or Python's `ast` module for safe evaluation.

6. **Two's complement via bit masking**: `ProgrammerCalculator.mask_value()` applies a bitmask for the current word size and then sign-extends, giving correct two's complement behavior without needing a special integer type.
