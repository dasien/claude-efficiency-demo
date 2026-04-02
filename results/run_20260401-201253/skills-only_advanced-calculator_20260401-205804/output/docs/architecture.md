# Architecture Document — Advanced Calculator

## 1. High-Level Design

The application follows the **MVC (Model-View-Controller)** pattern:

- **Model (logic/)**: Pure Python classes encapsulating all calculation logic. No GUI imports. Independently testable.
- **View (gui/)**: Tkinter widgets for display and input. No calculation logic. Receives display updates from the controller.
- **Controller (app.py)**: Mediates between Model and View. Handles events, delegates to logic, updates the view.

```
┌─────────────┐     events      ┌──────────────┐    method calls   ┌─────────────┐
│   View      │ ──────────────> │  Controller  │ ────────────────> │   Model     │
│  (gui/)     │ <────────────── │  (app.py)    │ <──────────────── │  (logic/)   │
│             │  display updates│              │   return values   │             │
└─────────────┘                 └──────────────┘                   └─────────────┘
```

## 2. Module Structure

```
calculator/
├── __init__.py
├── app.py                  # CalculatorApp controller — owns root window, manages modes
├── gui/
│   ├── __init__.py
│   ├── base_view.py        # BaseView — display area, memory row, shared button helpers
│   ├── basic_view.py       # BasicView(BaseView) — basic mode button grid
│   ├── scientific_view.py  # ScientificView(BaseView) — scientific functions + basic grid
│   └── programmer_view.py  # ProgrammerView(BaseView) — base selector, hex digits, bitwise
└── logic/
    ├── __init__.py
    ├── base_logic.py       # BaseCalculatorLogic — memory, display formatting, expression state
    ├── basic_logic.py      # BasicLogic(BaseCalculatorLogic) — arithmetic with precedence
    ├── scientific_logic.py # ScientificLogic(BasicLogic) — trig, log, power, factorial, parens
    └── programmer_logic.py # ProgrammerLogic(BaseCalculatorLogic) — base conversion, bitwise, word size
```

## 3. Model Layer Design

### 3.1 BaseCalculatorLogic

Shared state and operations for all modes:

- **State**: `display_value: str`, `expression: list`, `memory: float`, `has_memory: bool`, `error: bool`, `input_mode: str` (typing vs result)
- **Memory**: `memory_clear()`, `memory_recall()`, `memory_add()`, `memory_subtract()`, `memory_store()`
- **Input**: `input_digit(d: str)`, `input_decimal()`, `clear_entry()`, `all_clear()`, `backspace()`, `toggle_sign()`, `percent()`
- **Display formatting**: `format_number(value: float) -> str` — handles integer display, precision, scientific notation

### 3.2 BasicLogic

Extends BaseCalculatorLogic:

- **Expression evaluation**: Builds an expression list of numbers and operators, evaluates with correct precedence using a two-pass approach (first multiply/divide, then add/subtract).
- **Methods**: `input_operator(op: str)`, `evaluate() -> float`
- Operators: `+`, `-`, `*`, `/`

### 3.3 ScientificLogic

Extends BasicLogic (all basic operations available):

- **Angle mode**: `angle_mode: str` ("DEG" or "RAD"), `toggle_angle_mode()`
- **Unary functions**: `apply_function(name: str) -> float` — dispatches to sin, cos, tan, asin, acos, atan, log, ln, log2, x², x³, 10^x, e^x, √x, ³√x, 1/x, n!, |x|
- **Parentheses**: `open_paren()`, `close_paren()`, tracked via `paren_depth: int`
- **Constants**: `insert_constant(name: str)` — π, e

### 3.4 ProgrammerLogic

Extends BaseCalculatorLogic (not BasicLogic — different arithmetic):

- **Base**: `current_base: int` (2, 8, 10, 16), `set_base(base: int)`
- **Word size**: `word_size: int` (8, 16, 32, 64), `set_word_size(bits: int)`
- **Value clamping**: `clamp(value: int) -> int` — two's complement wrap
- **Base conversion**: `to_base(value: int, base: int) -> str`, `get_all_bases() -> dict`
- **Bitwise**: `bitwise_not()`, and binary ops via `input_operator()`: AND, OR, XOR, LSH, RSH
- **Arithmetic**: Integer +, -, *, / (truncating), % (modulo)
- **Input**: Override `input_digit()` to validate against current base; disable decimal point

## 4. View Layer Design

### 4.1 BaseView

Common GUI elements shared by all modes:

- **Display frame**: Expression label (secondary) + result label (primary)
- **Memory row**: MC, MR, M+, M-, MS buttons
- **Button helper**: `create_button(parent, text, command, ...)` with consistent styling
- **Callback interface**: All buttons call `self.on_button(label)` which the controller binds

### 4.2 BasicView

- 6×4 grid: C, +/-, %, / | 7,8,9,* | 4,5,6,- | 1,2,3,+ | 0(span 2),.,=
- 0 button uses `columnspan=2`

### 4.3 ScientificView

- Extends basic grid with 5 additional columns on the left for scientific functions
- Deg/Rad indicator in the display area
- Parentheses buttons, trig functions, log functions, power/root functions, constants

### 4.4 ProgrammerView

- Base conversion panel showing HEX/DEC/OCT/BIN values simultaneously
- Base selector radio buttons (DEC, HEX, OCT, BIN)
- Word size selector (8, 16, 32, 64)
- Hex digit buttons (A-F), enabled/disabled based on current base
- Bitwise operator buttons (AND, OR, XOR, NOT, LSH, RSH)
- No decimal point button

## 5. Controller Design (app.py)

### CalculatorApp

- Owns the `tk.Tk()` root window and menu bar
- Manages mode switching: creates/destroys view and logic instances
- Routes button callbacks from view to logic methods
- Updates view display after each operation
- Handles keyboard bindings (universal + mode-specific)

### Event Flow

1. User clicks button or presses key
2. View calls `controller.on_button(label)` or keyboard binding fires
3. Controller dispatches to appropriate logic method
4. Logic updates internal state and returns
5. Controller reads logic state and updates view display

### Mode Switching

1. Controller stores current numeric value from logic
2. Destroys current view frame
3. Creates new logic instance, transferring: value (truncated to int for Programmer), memory state
4. Creates new view instance
5. Resizes window appropriately

## 6. Window Sizing

| Mode | Approximate Size |
|------|-----------------|
| Basic | 320 × 480 |
| Scientific | 560 × 520 |
| Programmer | 560 × 560 |

## 7. Error Handling Strategy

- Logic methods raise no exceptions to the controller. Instead, they set `self.error = True` and `self.display_value = "Error"`.
- The controller checks `logic.error` after each operation and updates the view accordingly.
- On error, the next digit input or clear operation resets the error state.
- All math operations are wrapped in try/except within the logic layer to catch unexpected errors (ZeroDivisionError, ValueError, OverflowError).

## 8. Display Formatting Rules

- Integer results: no decimal point (`5` not `5.0`)
- Float results: up to 10 significant digits, trailing zeros stripped
- Very large/small: scientific notation (e.g., `1.23456e+15`)
- Programmer mode: value displayed in current base, uppercase hex digits
