# Coding Plan — Advanced Calculator

## Implementation Order

Files are implemented bottom-up: logic layer first, then GUI, then controller.

### Phase 1: Project Structure
1. **`calculator/__init__.py`** — Empty package init
2. **`calculator/logic/__init__.py`** — Empty package init
3. **`calculator/gui/__init__.py`** — Empty package init
4. **`tests/__init__.py`** — Empty package init
5. **`main.py`** — Entry point (stub, completed in Phase 5)
6. **`requirements.txt`** — pytest dependency

### Phase 2: Logic Layer (no GUI dependency)

#### 2a. `calculator/logic/base_logic.py`
- `BaseCalculator` class with:
  - Display state management (current input string, computed value)
  - Number formatting (integers without `.0`, 10 sig digits, scientific notation)
  - Memory operations (MC, MR, M+, M-, MS)
  - Clear/AC/Backspace
  - Sign toggle, percent
- **Dependencies:** None (stdlib `math` only)

#### 2b. `calculator/logic/basic_logic.py`
- `BasicCalculator(BaseCalculator)` class with:
  - Expression tokenizer and builder
  - Operator input (queues operator, stores pending operand)
  - Expression evaluator with operator precedence (shunting-yard)
  - Chained operation support
- **Dependencies:** `base_logic.py`

#### 2c. `calculator/logic/scientific_logic.py`
- `ScientificCalculator(BasicCalculator)` class with:
  - Trig functions (sin, cos, tan, asin, acos, atan) with deg/rad toggle
  - Log functions (log, ln, log2)
  - Power/root functions (x², x³, xⁿ, 10ˣ, eˣ, √x, ³√x, 1/x)
  - Factorial, absolute value
  - Constants (π, e)
  - Parentheses support in expression builder
- **Dependencies:** `basic_logic.py`, stdlib `math`

#### 2d. `calculator/logic/programmer_logic.py`
- `ProgrammerCalculator` class (standalone, not inheriting BasicCalculator) with:
  - Integer-only input and arithmetic
  - Base conversion (DEC, HEX, OCT, BIN)
  - Word size management (8, 16, 32, 64-bit)
  - Two's complement truncation and overflow wrapping
  - Bitwise operations (AND, OR, XOR, NOT, LSH, RSH)
  - Modulo operation
  - Memory operations (shared interface)
  - Base conversion panel data (all 4 bases simultaneously)
- **Dependencies:** `base_logic.py` (for memory interface)

### Phase 3: GUI Layer

#### 3a. `calculator/gui/base_view.py`
- `BaseView` class with:
  - Main frame container
  - Expression display label
  - Result display label
  - Memory indicator label
  - Button creation helper methods
  - Color/style constants
- **Dependencies:** `tkinter`

#### 3b. `calculator/gui/basic_view.py`
- `BasicView(BaseView)` with:
  - Memory button row
  - Numeric grid (0-9, decimal, operators)
  - Button layout per spec (0 spans 2 cols)
  - Callback binding for all buttons
- **Dependencies:** `base_view.py`

#### 3c. `calculator/gui/scientific_view.py`
- `ScientificView(BaseView)` with:
  - All basic view buttons
  - Scientific function buttons (trig, log, power, etc.)
  - Parenthesis buttons
  - Deg/Rad toggle button and indicator
  - Constants buttons (π, e)
- **Dependencies:** `base_view.py`

#### 3d. `calculator/gui/programmer_view.py`
- `ProgrammerView(BaseView)` with:
  - Base conversion display panel
  - Base selector (DEC/HEX/OCT/BIN radio buttons)
  - Word size selector
  - Hex digit buttons (A-F) with enable/disable logic
  - Bitwise operation buttons
  - Digit enable/disable based on current base
- **Dependencies:** `base_view.py`

### Phase 4: Controller

#### 4a. `calculator/app.py`
- `CalculatorApp` class with:
  - Tkinter root window setup
  - All three logic engines instantiated
  - All three views instantiated (only active one shown)
  - Mode switching (menu/tabs + Ctrl+1/2/3)
  - Value preservation on mode switch
  - Memory sharing across modes
  - Keyboard binding (universal + mode-specific)
  - Input routing to active logic engine
  - Display update after every action

### Phase 5: Entry Point

#### 5a. `main.py`
- Create Tk root, instantiate `CalculatorApp`, run mainloop

### Phase 6: Tests (see test-plan.md)

## File Dependency Graph

```
main.py
  └── calculator/app.py
        ├── calculator/logic/basic_logic.py
        │     └── calculator/logic/base_logic.py
        ├── calculator/logic/scientific_logic.py
        │     └── calculator/logic/basic_logic.py
        ├── calculator/logic/programmer_logic.py
        ├── calculator/gui/basic_view.py
        │     └── calculator/gui/base_view.py
        ├── calculator/gui/scientific_view.py
        │     └── calculator/gui/base_view.py
        └── calculator/gui/programmer_view.py
              └── calculator/gui/base_view.py
```

## Key Implementation Notes

- **Expression evaluator:** Implement a safe shunting-yard algorithm. Never use `eval()`.
- **Number formatting:** Handle edge cases: `-0` → `0`, trailing zeros, scientific notation threshold.
- **Programmer mode:** Use bitmask `value & ((1 << bits) - 1)` for unsigned, then convert back to signed for two's complement.
- **Error handling:** Every operation that can fail wraps in try/except, sets error state. No exceptions propagate to GUI.
