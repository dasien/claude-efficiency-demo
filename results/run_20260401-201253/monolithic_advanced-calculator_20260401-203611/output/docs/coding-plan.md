# Coding Plan — Advanced Calculator

## Implementation Order

Files are implemented in dependency order: shared logic first, then mode-specific logic, then GUI, then controller.

---

## Phase 1: Project Scaffolding

### 1.1 `requirements.txt`
- Single entry: `pytest`

### 1.2 Directory structure
```
calculator/
├── __init__.py
├── app.py
├── gui/
│   ├── __init__.py
│   ├── base_view.py
│   ├── basic_view.py
│   ├── scientific_view.py
│   └── programmer_view.py
└── logic/
    ├── __init__.py
    ├── base_logic.py
    ├── basic_logic.py
    ├── scientific_logic.py
    └── programmer_logic.py
tests/
├── __init__.py
├── test_basic.py
├── test_scientific.py
├── test_programmer.py
├── test_memory.py
└── test_mode_switch.py
main.py
```

### 1.3 `main.py`
- Entry point: imports and launches `CalculatorApp`
- `if __name__ == "__main__":` guard

---

## Phase 2: Shared Logic (`calculator/logic/base_logic.py`)

**Dependencies:** None

### Implement:
- `Memory` class with `clear`, `recall`, `add`, `subtract`, `store`, `has_value` methods
- `format_number(value: float) -> str` — integer display, precision capping at 10 significant digits, scientific notation for large/small values
- `parse_number(text: str) -> float` — converts display text back to numeric value

---

## Phase 3: Basic Logic (`calculator/logic/basic_logic.py`)

**Dependencies:** `base_logic.py`

### Implement:
- `BasicCalculator` class with full expression evaluation
- Expression builder using shunting-yard algorithm for operator precedence
- Token-based approach: numbers and operators stored as token lists
- Methods:
  - `input_digit(d: str)` — append digit, handle leading zeros
  - `input_decimal()` — add decimal point (max one)
  - `input_operator(op: str)` — +, -, *, / with precedence
  - `input_equals()` — evaluate full expression
  - `input_clear()` — reset current entry
  - `input_all_clear()` — reset everything
  - `input_backspace()` — delete last character
  - `input_percent()` — divide current by 100
  - `input_negate()` — toggle sign
  - `get_display() -> str` — formatted current value
  - `get_expression() -> str` — expression string for display
  - `get_value() -> float` — raw numeric value
  - `set_value(v: float)` — for mode switching
  - `is_error() -> bool` — error state check

---

## Phase 4: Scientific Logic (`calculator/logic/scientific_logic.py`)

**Dependencies:** `basic_logic.py`

### Implement:
- `ScientificCalculator(BasicCalculator)` — inherits expression evaluation
- Angle mode: `set_angle_mode(mode: str)`, `get_angle_mode() -> str`
- Unary scientific functions (applied immediately to current value):
  - `apply_sin()`, `apply_cos()`, `apply_tan()`
  - `apply_asin()`, `apply_acos()`, `apply_atan()`
  - `apply_log()`, `apply_ln()`, `apply_log2()`
  - `apply_square()`, `apply_cube()`, `apply_sqrt()`, `apply_cbrt()`
  - `apply_ten_power()`, `apply_e_power()`
  - `apply_reciprocal()`
  - `apply_factorial()`, `apply_abs()`
- Binary operations: `input_power()` (xⁿ uses operator mechanism)
- Constants: `input_pi()`, `input_e()`
- Parentheses: `input_open_paren()`, `input_close_paren()`, `get_paren_depth() -> int`

---

## Phase 5: Programmer Logic (`calculator/logic/programmer_logic.py`)

**Dependencies:** `base_logic.py`

### Implement:
- `ProgrammerCalculator` class (standalone, not inheriting from BasicCalculator)
- Word size: `set_word_size(bits: int)`, `get_word_size() -> int`, `constrain_value(v: int) -> int`
- Base mode: `set_base(base: str)`, `get_base() -> str`
- Input: `input_digit(d: str)` — validates digit for current base
- Base conversion: `get_all_bases(value: int) -> dict` returning {"DEC": ..., "HEX": ..., "OCT": ..., "BIN": ...}
- Arithmetic: same operator interface as BasicCalculator but integer-only
- Bitwise: `input_and()`, `input_or()`, `input_xor()`, `apply_not()`, `input_lshift()`, `input_rshift()`
- `input_modulo()` — modulo operator
- `get_valid_digits() -> list[str]` — returns which digits are valid for current base
- Value get/set for mode switching: `get_value() -> int`, `set_value(v: int)`

---

## Phase 6: GUI — Base View (`calculator/gui/base_view.py`)

**Dependencies:** None (pure Tkinter)

### Implement:
- `DisplayFrame(ttk.Frame)` — expression label + result entry (read-only)
- `create_button(parent, text, row, col, ...) -> ttk.Button` — factory with consistent sizing
- `MemoryButtonRow(ttk.Frame)` — MC, MR, M+, M-, MS buttons with callback dict
- Memory indicator label

---

## Phase 7: GUI — Mode Views

**Dependencies:** `base_view.py`

### 7.1 `basic_view.py`
- `BasicView(ttk.Frame)` — complete Basic mode panel
- Grid layout per architecture spec
- Exposes `set_display(value, expression)` and button callbacks

### 7.2 `scientific_view.py`
- `ScientificView(ttk.Frame)` — complete Scientific mode panel
- Extended grid with scientific function buttons
- Deg/Rad toggle button and indicator
- Parentheses depth indicator

### 7.3 `programmer_view.py`
- `ProgrammerView(ttk.Frame)` — complete Programmer mode panel
- Base conversion display panel
- Base selector radio buttons
- Hex digit buttons with enable/disable logic
- Word size selector
- Bitwise operation buttons

---

## Phase 8: Controller (`calculator/app.py`)

**Dependencies:** All logic modules, all GUI modules

### Implement:
- `CalculatorApp(tk.Tk)` main class
- Mode switching with view swap and value preservation
- Menu bar with mode options and keyboard shortcuts
- Central `on_button(action)` dispatcher
- Keyboard event binding/unbinding on mode switch
- Display update after every action
- Error state display handling
- Memory instance shared across modes

---

## Phase 9: Tests

**Dependencies:** All logic modules

### Implement in parallel:
- `test_basic.py` — arithmetic, precedence, input handling, clear/backspace, display formatting
- `test_scientific.py` — trig, log, powers, roots, constants, factorial, parentheses
- `test_programmer.py` — base conversion, bitwise, word size, integer arithmetic
- `test_memory.py` — all memory operations, persistence across simulated mode switches
- `test_mode_switch.py` — value preservation, truncation, base conversion on switch

---

## File Dependency Graph

```
base_logic.py          (no deps)
    ├── basic_logic.py
    │       └── scientific_logic.py
    └── programmer_logic.py

base_view.py           (no deps, Tkinter only)
    ├── basic_view.py
    ├── scientific_view.py
    └── programmer_view.py

app.py                 (depends on all logic + all views)
main.py                (depends on app.py)
```
