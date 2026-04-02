# Architecture Document — Advanced Calculator

## 1. High-Level Design

The application follows the **MVC (Model-View-Controller)** pattern:

- **Model (logic/)**: Pure Python classes containing all calculation logic, state management, and data transformation. Zero GUI dependencies.
- **View (gui/)**: Tkinter widgets responsible only for rendering and capturing user input. No calculation logic.
- **Controller (app.py)**: Mediates between views and logic. Routes user actions to the appropriate logic module and updates the view with results.

```
┌─────────────┐     events      ┌─────────────┐     calls      ┌─────────────┐
│   GUI Views │ ──────────────> │  Controller  │ ──────────────>│    Logic    │
│  (Tkinter)  │ <────────────── │   (app.py)   │ <──────────────│  (Models)   │
└─────────────┘   update display└─────────────┘   return results└─────────────┘
```

## 2. Module Architecture

### 2.1 Logic Layer (`calculator/logic/`)

#### `base_logic.py` — Shared Base
- `CalculatorState` dataclass: holds display value, expression, memory, error state, pending operations
- `Memory` class: MC, MR, M+, M-, MS operations
- `format_number(value) -> str`: formats numbers for display (integer cleanup, scientific notation, precision)
- `parse_number(text) -> float`: parses display text back to a number

#### `basic_logic.py` — Basic Mode Engine
- `BasicCalculator` class
  - Manages expression building with operator precedence
  - Uses Python's `ast.literal_eval` or a safe expression evaluator (shunting-yard algorithm) for precedence
  - Methods: `input_digit`, `input_operator`, `input_decimal`, `input_equals`, `input_clear`, `input_all_clear`, `input_backspace`, `input_percent`, `input_negate`
  - Returns `CalculatorState` after each operation

#### `scientific_logic.py` — Scientific Mode Engine
- `ScientificCalculator(BasicCalculator)` — extends basic with:
  - Trigonometric: `sin`, `cos`, `tan`, `asin`, `acos`, `atan` (with deg/rad mode)
  - Logarithmic: `log`, `ln`, `log2`
  - Powers/roots: `square`, `cube`, `power`, `ten_power`, `e_power`, `sqrt`, `cbrt`, `reciprocal`
  - Constants: `pi`, `e`
  - `factorial`, `abs_value`
  - Parentheses support integrated into expression builder

#### `programmer_logic.py` — Programmer Mode Engine
- `ProgrammerCalculator` class (separate from BasicCalculator, integer-only)
  - Base conversion: `to_hex`, `to_oct`, `to_bin`, `to_dec`, `convert_base`
  - Word size management: 8, 16, 32, 64-bit with two's complement wrapping
  - Bitwise operations: `and_op`, `or_op`, `xor_op`, `not_op`, `lshift`, `rshift`
  - Integer arithmetic: `add`, `subtract`, `multiply`, `int_divide`, `modulo`
  - `get_all_bases(value) -> dict`: returns value in all four bases simultaneously

### 2.2 GUI Layer (`calculator/gui/`)

#### `base_view.py` — Shared GUI Components
- `DisplayFrame`: expression line + result display
- `MemoryButtonRow`: MC, MR, M+, M-, MS buttons
- Common button factory with consistent sizing and styling
- Memory indicator label

#### `basic_view.py` — Basic Mode Layout
- Grid layout: 6 rows x 4 columns
- Memory row on top, then C/+/-/%/÷, digit grid, operators on right
- `0` button spans two columns
- Callbacks dict maps button text to controller methods

#### `scientific_view.py` — Scientific Mode Layout
- Extended grid: 6 rows x 9 columns
- Left 5 columns: scientific functions (trig, log, powers, constants)
- Right 4 columns: basic digit/operator grid
- Deg/Rad toggle indicator
- Parentheses buttons with nesting depth indicator

#### `programmer_view.py` — Programmer Mode Layout
- Base conversion panel at top showing all 4 bases
- Base selector radio buttons (DEC/HEX/OCT/BIN)
- Hex digit buttons (A-F) with enable/disable based on base
- Bitwise operation buttons (AND, OR, XOR, NOT, LSH, RSH)
- Word size selector (8/16/32/64-bit)
- Standard digit grid with context-sensitive enabling

### 2.3 Controller (`app.py`)

- `CalculatorApp(tk.Tk)`: main window
  - Manages mode switching (Basic/Scientific/Programmer)
  - Holds references to all three logic engines and views
  - Routes button presses and keyboard events to active logic engine
  - Updates display after each operation
  - Preserves value on mode switch (truncating to int for Programmer)
  - Memory shared across modes via `Memory` instance
  - Menu bar with mode selection + keyboard shortcuts (Ctrl+1/2/3)

## 3. GUI Layout Per Mode

### 3.1 Basic Mode (300x400)
```
Row 0: Expression display (colspan=4)
Row 1: Result display (colspan=4)
Row 2: MC | MR | M+ | M- | MS
Row 3: C  | +/-| %  | /
Row 4: 7  | 8  | 9  | *
Row 5: 4  | 5  | 6  | -
Row 6: 1  | 2  | 3  | +
Row 7: 0 (colspan=2) | . | =
```

### 3.2 Scientific Mode (550x450)
```
Row 0: Expression display (colspan=9)
Row 1: Result display (colspan=8) + Deg/Rad label
Row 2: MC | MR | M+ | M- | MS (colspan=9)
Row 3: (  | )  | x² | x³ | xⁿ | C  | +/-| %  | /
Row 4: sin|cos |tan | √x |³√x | 7  | 8  | 9  | *
Row 5: asin|acos|atan|10ˣ| eˣ | 4  | 5  | 6  | -
Row 6: n! ||x| |log | ln |log₂| 1  | 2  | 3  | +
Row 7: π  | e  |1/x |    |    | 0(span2) | . | =
```

### 3.3 Programmer Mode (600x500)
```
Row 0: Expression display (colspan=9)
Row 1: Result display (colspan=8) + Word size label
Row 2: Base conversion panel (HEX/DEC/OCT/BIN values)
Row 3: Base selector radio buttons
Row 4: A  | B  | C  | D  | E  | F  | AND| OR | AC
Row 5: NOT|XOR |LSH |RSH | %  | C  |+/- |MOD | /
Row 6:    |    |    |    |    | 7  | 8  | 9  | *
Row 7:    |    |    |    |    | 4  | 5  | 6  | -
Row 8:    |    |    |    |    | 1  | 2  | 3  | +
Row 9:                        | 0(span2)  | = | ⌫
```

## 4. Event Handling Design

### 4.1 Button Events
- Each button widget has a `command=` callback pointing to the controller
- Controller method signature: `on_button(action: str)`
- Controller dispatches to active logic engine based on action type

### 4.2 Keyboard Events
- `bind_all` on the root window for universal shortcuts (digits, operators, Enter, Escape, Backspace)
- Mode-specific bindings added/removed on mode switch
- Ctrl+1/2/3 bound at root level for mode switching
- Hex digits (a-f) bound only in Programmer mode + HEX base

### 4.3 Event Flow
```
User Press → Tkinter Event → Controller.on_button(action)
  → Logic Engine processes action
  → Returns updated CalculatorState
  → Controller updates View displays
```

### 4.4 Error Handling Flow
- Logic layer raises no exceptions to controller; instead returns state with `error=True`
- Controller checks `state.error` and displays "Error" in result display
- Next digit input or Clear action clears error state automatically

## 5. State Management

### 5.1 Calculator State (per-mode)
- `current_value: float | int` — the number being displayed
- `expression: str` — the expression being built (for display line)
- `pending_operator: str | None` — operator waiting for second operand
- `operand_stack: list` — for operator precedence handling
- `new_input: bool` — whether next digit starts a new number
- `error: bool` — whether an error is currently displayed

### 5.2 Shared State
- `Memory` instance — persists across mode switches
- `current_mode: str` — "basic", "scientific", "programmer"

### 5.3 Mode Switch Logic
- Basic → Scientific: preserve float value as-is
- Scientific → Basic: preserve float value as-is
- Any → Programmer: `int(value)`, apply word size constraint
- Programmer → Any: `float(int_value)`, preserve as decimal
