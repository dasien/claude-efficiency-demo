# Coding Plan — Advanced Calculator

## Implementation Order

Files are implemented bottom-up: logic layer first (no dependencies), then views, then controller.

### Phase 1: Project Skeleton

1. **`calculator/__init__.py`** — empty
2. **`calculator/logic/__init__.py`** — empty
3. **`calculator/gui/__init__.py`** — empty
4. **`main.py`** — entry point: `from calculator.app import CalculatorApp; app = CalculatorApp(); app.run()`
5. **`requirements.txt`** — `pytest` only

### Phase 2: Logic Layer

#### 2a. `calculator/logic/base_logic.py`
- `BaseCalculatorLogic` class
- State: display_value, expression tokens, memory, error flag, input_mode
- Digit input, decimal, backspace, clear, all-clear, toggle sign, percent
- Memory operations (MC, MR, M+, M-, MS)
- Number formatting (integer display, precision, scientific notation)
- **Dependencies**: none (stdlib `math` only)

#### 2b. `calculator/logic/basic_logic.py`
- `BasicLogic(BaseCalculatorLogic)` class
- Operator input (+, -, *, /)
- Expression evaluation with operator precedence (two-pass: */÷ first, then +/-)
- Chained operations support
- **Dependencies**: `base_logic.py`

#### 2c. `calculator/logic/scientific_logic.py`
- `ScientificLogic(BasicLogic)` class
- Angle mode (DEG/RAD) with toggle
- Trig functions: sin, cos, tan, asin, acos, atan
- Log functions: log, ln, log2
- Power/root: x², x³, xⁿ, 10^x, e^x, √x, ³√x, 1/x
- Factorial (n!) and absolute value (|x|)
- Constants: π, e
- Parentheses with nesting depth tracking
- **Dependencies**: `basic_logic.py`, stdlib `math`

#### 2d. `calculator/logic/programmer_logic.py`
- `ProgrammerLogic(BaseCalculatorLogic)` class
- Base modes: DEC(10), HEX(16), OCT(8), BIN(2)
- Word sizes: 8, 16, 32, 64 bit with two's complement clamping
- Base conversion and display in all bases simultaneously
- Digit input validation per base
- Bitwise: AND, OR, XOR, NOT, LSH, RSH
- Integer arithmetic: +, -, *, / (truncating), % (modulo)
- **Dependencies**: `base_logic.py`

### Phase 3: GUI Layer

#### 3a. `calculator/gui/base_view.py`
- `BaseView` class
- Display frame: expression label + result label
- Memory indicator label
- Memory button row
- Button factory method with consistent styling
- Callback registration (`on_button` handler)
- **Dependencies**: `tkinter`

#### 3b. `calculator/gui/basic_view.py`
- `BasicView(BaseView)` class
- Button grid: digits 0-9, operators, C, +/-, %, decimal, equals
- 0 button spans two columns
- **Dependencies**: `base_view.py`

#### 3c. `calculator/gui/scientific_view.py`
- `ScientificView(BaseView)` class
- Basic grid + scientific function columns on the left
- Deg/Rad indicator
- Parentheses, trig, log, power/root, constant buttons
- **Dependencies**: `base_view.py`

#### 3d. `calculator/gui/programmer_view.py`
- `ProgrammerView(BaseView)` class
- Base conversion panel (all 4 bases displayed)
- Base selector radio buttons
- Word size selector
- Hex digit buttons (A-F)
- Bitwise operator buttons
- Digit enable/disable based on current base
- **Dependencies**: `base_view.py`

### Phase 4: Controller

#### 4a. `calculator/app.py`
- `CalculatorApp` class
- Root window and menu bar setup
- Mode switching (Basic ↔ Scientific ↔ Programmer)
- Button dispatch: routes view callbacks to logic methods
- Display update after each operation
- Keyboard binding setup (universal + mode-specific)
- Window resizing per mode
- Value and memory preservation across mode switches
- **Dependencies**: all gui and logic modules

### Phase 5: Tests

1. `tests/__init__.py`
2. `tests/test_basic.py` — basic arithmetic, input, clear, display formatting
3. `tests/test_scientific.py` — trig, log, power/root, factorial, parens, constants
4. `tests/test_programmer.py` — base conversion, bitwise, word size, integer arithmetic
5. `tests/test_memory.py` — memory operations across modes
6. `tests/test_mode_switch.py` — value preservation, truncation

## File Dependency Graph

```
base_logic.py
├── basic_logic.py
│   └── scientific_logic.py
└── programmer_logic.py

base_view.py
├── basic_view.py
├── scientific_view.py
└── programmer_view.py

app.py ── depends on all of the above
```

## Key Design Decisions

1. **Expression evaluation**: Use a token list approach rather than string parsing. Tokens are numbers and operator strings. Evaluate with two passes for precedence.
2. **Programmer mode extends BaseCalculatorLogic, not BasicLogic**: Programmer mode has fundamentally different arithmetic (integer-only, bitwise ops, base conversion) and doesn't need expression precedence in the same way.
3. **View callback pattern**: Views call a single `on_button(label: str)` callback. The controller maps labels to logic methods. This keeps views completely decoupled from logic.
4. **Error as state, not exceptions**: Logic sets an error flag rather than raising. The controller checks and updates the view. This simplifies the flow and avoids try/except in the controller.
