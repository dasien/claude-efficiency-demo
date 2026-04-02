# Architecture Document — Advanced Calculator

## 1. High-Level Design

The application follows the **MVC (Model-View-Controller)** pattern:

- **Model (Logic Layer):** Pure Python classes in `calculator/logic/` that perform all calculations, state management, memory operations, and expression evaluation. No Tkinter dependency.
- **View (GUI Layer):** Tkinter widgets in `calculator/gui/` that render buttons, displays, and mode-specific layouts. Views emit events but contain no business logic.
- **Controller (App Layer):** `calculator/app.py` coordinates between views and logic, handles mode switching, and routes user input to the appropriate logic module.

```
┌─────────────────────────────────────────────┐
│                  app.py                      │
│            (Controller Layer)                │
│  - Mode switching                            │
│  - Routes input → logic                      │
│  - Updates view from logic state             │
├──────────────────┬──────────────────────────┤
│   gui/ (View)    │    logic/ (Model)         │
│                  │                           │
│  base_view.py    │  base_logic.py            │
│  basic_view.py   │  basic_logic.py           │
│  scientific_view │  scientific_logic.py       │
│  programmer_view │  programmer_logic.py       │
└──────────────────┴──────────────────────────┘
```

## 2. Module Interfaces

### 2.1 Logic Layer

#### `base_logic.py` — BaseCalculator
Shared base class for all calculator modes.

```python
class BaseCalculator:
    # State
    current_value: float        # Current displayed value
    expression: str             # Expression string being built
    memory: float               # Memory register
    has_memory: bool            # Whether memory contains a value
    error: bool                 # Error state flag

    # Core methods
    def input_digit(self, digit: str) -> None
    def input_decimal(self) -> None
    def input_operator(self, op: str) -> None
    def evaluate(self) -> None
    def clear_entry(self) -> None
    def all_clear(self) -> None
    def backspace(self) -> None
    def toggle_sign(self) -> None
    def percent(self) -> None

    # Memory
    def memory_clear(self) -> None
    def memory_recall(self) -> None
    def memory_add(self) -> None
    def memory_subtract(self) -> None
    def memory_store(self) -> None

    # Display
    def get_display_value(self) -> str
    def get_expression(self) -> str
    def format_number(self, value: float) -> str
```

#### `basic_logic.py` — BasicCalculator(BaseCalculator)
Handles expression building and evaluation with operator precedence.

Uses a token-based expression evaluator that respects `* /` before `+ -`.

#### `scientific_logic.py` — ScientificCalculator(BasicCalculator)
Extends BasicCalculator with:

```python
class ScientificCalculator(BasicCalculator):
    angle_mode: str  # "DEG" or "RAD"

    # Trig
    def sin(self) -> None
    def cos(self) -> None
    def tan(self) -> None
    def asin(self) -> None
    def acos(self) -> None
    def atan(self) -> None
    def toggle_angle_mode(self) -> None

    # Log
    def log(self) -> None
    def ln(self) -> None
    def log2(self) -> None

    # Powers/Roots
    def square(self) -> None
    def cube(self) -> None
    def power(self) -> None        # Two-operand: xⁿ
    def ten_power(self) -> None
    def e_power(self) -> None
    def sqrt(self) -> None
    def cbrt(self) -> None
    def reciprocal(self) -> None

    # Other
    def factorial(self) -> None
    def absolute(self) -> None
    def insert_pi(self) -> None
    def insert_e(self) -> None

    # Parentheses
    def open_paren(self) -> None
    def close_paren(self) -> None
```

#### `programmer_logic.py` — ProgrammerCalculator
Separate class (not extending BasicCalculator) for integer-only math.

```python
class ProgrammerCalculator:
    value: int
    base: str          # "DEC", "HEX", "OCT", "BIN"
    word_size: int     # 8, 16, 32, 64
    memory: float      # Shared memory reference
    has_memory: bool

    # Input
    def input_digit(self, digit: str) -> None
    def input_operator(self, op: str) -> None  # +, -, *, /, %, AND, OR, XOR, LSH, RSH
    def evaluate(self) -> None

    # Bitwise unary
    def bitwise_not(self) -> None
    def toggle_sign(self) -> None

    # Base/Word
    def set_base(self, base: str) -> None
    def set_word_size(self, bits: int) -> None
    def get_base_conversions(self) -> dict  # Returns {DEC: str, HEX: str, OCT: str, BIN: str}

    # Word size enforcement
    def truncate_to_word_size(self, value: int) -> int
```

### 2.2 GUI Layer

#### `base_view.py` — BaseView
Shared GUI components:
- Expression display label (secondary)
- Result display label (primary)
- Memory indicator
- Common styling constants

#### `basic_view.py` — BasicView(BaseView)
- Memory row: MC, MR, M+, M-, MS
- Grid: C, +/-, %, /, 7-9, *, 4-6, -, 1-3, +, 0 (double-width), ., =

#### `scientific_view.py` — ScientificView(BaseView)
- Extends basic layout with left-side scientific function columns
- Deg/Rad toggle indicator
- Parenthesis buttons

#### `programmer_view.py` — ProgrammerView(BaseView)
- Base conversion panel (all 4 bases displayed)
- Base selector radio buttons (DEC/HEX/OCT/BIN)
- Word size selector
- Hex digit buttons A-F
- Bitwise operation buttons (AND, OR, XOR, NOT, LSH, RSH)

### 2.3 Controller — `app.py`

```python
class CalculatorApp:
    def __init__(self, root: tk.Tk):
        # Initialize all logic engines
        # Initialize views
        # Set up mode switching
        # Bind keyboard shortcuts

    def switch_mode(self, mode: str) -> None
    def handle_input(self, action: str) -> None
    def update_display(self) -> None
```

## 3. GUI Layout Per Mode

### Basic Mode (approx 320×480)
- 2-line display at top (expression + result)
- Memory button row
- 5×5 button grid (0 spans 2 cols)

### Scientific Mode (approx 560×520)
- 2-line display at top with Deg/Rad indicator
- Memory button row
- 9×6 button grid (scientific functions on left, basic on right)

### Programmer Mode (approx 560×580)
- 2-line display with word size indicator
- Base conversion panel showing all 4 bases
- Base selector radio buttons
- 9×7 button grid (hex digits + bitwise on left, digits + operators on right)

## 4. Event Handling Design

### Button Clicks
Each button widget calls `app.handle_input(action_string)` where `action_string` identifies the operation (e.g., "digit_5", "op_+", "sin", "base_HEX").

### Keyboard Bindings
Keyboard events are bound at the root window level. The controller maps key events to the same `handle_input()` actions. Mode-specific keys (hex digits, bitwise operators) are only active when the corresponding mode is selected.

### Display Updates
After every input action, the controller:
1. Calls the appropriate logic method
2. Reads back the display state from the logic object
3. Updates the view's display labels

### Error Flow
Logic methods set an `error` flag and an error message. The controller checks this flag after each operation and displays "Error" in the result display. On next valid input, the error flag is cleared.

## 5. Data Flow Example

```
User clicks "5" → View calls app.handle_input("digit_5")
  → Controller calls logic.input_digit("5")
  → Controller calls logic.get_display_value() → "5"
  → Controller calls view.update_display("5", expression)
```

## 6. Key Design Decisions

1. **Expression evaluation:** Use Python's tokenizer/parser approach with a safe expression evaluator (NOT `eval()`). Build an AST or use shunting-yard algorithm for operator precedence.

2. **Shared memory:** Memory register is stored in the controller and passed to each logic engine on mode switch.

3. **Two's complement:** Programmer mode uses Python's arbitrary-precision integers but masks/truncates to the selected word size using bitwise operations.

4. **Number formatting:** The `format_number()` method handles integer display (no `.0`), precision limits (10 significant digits), and scientific notation for very large/small numbers.
