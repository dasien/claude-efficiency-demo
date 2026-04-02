# Advanced Calculator -- Coding Plan

**Version:** 1.0
**Date:** 2026-04-01
**Based on:** Requirements v1.0, Architecture v1.0

---

## 1. Implementation Order

### Phase 1: Logic Layer (no Tkinter imports)

1. `calculator/logic/base_logic.py`
2. `calculator/logic/basic_logic.py`
3. `calculator/logic/scientific_logic.py`
4. `calculator/logic/programmer_logic.py`
5. `calculator/logic/__init__.py`

### Phase 2: GUI Layer

6. `calculator/gui/base_view.py`
7. `calculator/gui/basic_view.py`
8. `calculator/gui/scientific_view.py`
9. `calculator/gui/programmer_view.py`
10. `calculator/gui/__init__.py`

### Phase 3: Controller and Entry Point

11. `calculator/app.py`
12. `calculator/__init__.py`
13. `main.py`
14. `requirements.txt`

### Phase 4: Tests

15. `tests/test_basic.py`
16. `tests/test_scientific.py`
17. `tests/test_programmer.py`
18. `tests/test_memory.py`
19. `tests/test_mode_switch.py`
20. `tests/__init__.py`

---

## 2. Dependency Graph

```
main.py
  -> calculator/app.py
       -> calculator/logic/basic_logic.py
       -> calculator/logic/scientific_logic.py
       -> calculator/logic/programmer_logic.py
       -> calculator/gui/basic_view.py
       -> calculator/gui/scientific_view.py
       -> calculator/gui/programmer_view.py

calculator/logic/basic_logic.py -> base_logic.py
calculator/logic/scientific_logic.py -> basic_logic.py -> base_logic.py
calculator/logic/programmer_logic.py -> base_logic.py

calculator/gui/basic_view.py -> base_view.py
calculator/gui/scientific_view.py -> base_view.py
calculator/gui/programmer_view.py -> base_view.py

tests/* -> calculator/logic/* (no GUI imports in tests)
```

---

## 3. File-by-File Breakdown

### 3.1 `calculator/logic/base_logic.py`

**Class:** `BaseCalculator`
**Dependencies:** None (stdlib `math` only)

**State attributes:**
- `current_value: float` -- current numeric value
- `expression: str` -- expression string being built
- `memory: float` -- stored memory value (default 0.0)
- `has_memory: bool` -- whether memory holds a user-stored value
- `error: bool` -- error state flag
- `error_message: str` -- error text for display
- `input_buffer: str` -- raw digit string user is typing

**Methods to implement:**

| Method | Details |
|--------|---------|
| `__init__()` | Initialize all state to defaults |
| `mc()` | Set `memory = 0.0`, `has_memory = False` |
| `mr() -> float` | Return `memory`; set `current_value = memory` |
| `m_plus()` | `memory += current_value` |
| `m_minus()` | `memory -= current_value` |
| `ms()` | `memory = current_value`, `has_memory = True` |
| `format_number(value: float) -> str` | See formatting rules below |
| `append_digit(digit: str)` | Append to `input_buffer`; strip leading zeros; update `current_value` |
| `append_decimal()` | Append `"."` to `input_buffer` only if not already present |
| `toggle_sign()` | Negate `current_value`; update `input_buffer` accordingly |
| `percentage()` | `current_value /= 100`; update `input_buffer` |
| `backspace()` | Remove last char from `input_buffer`; update `current_value` |
| `clear_entry()` | Reset `input_buffer` to `"0"`, `current_value` to 0; preserve expression and pending ops |
| `clear_all()` | Reset all state except memory |
| `set_error(message)` | Set `error = True`, `error_message = message` |
| `clear_error()` | Set `error = False`, `error_message = ""` |
| `get_display_value() -> str` | If `input_buffer` is active, return it; else return `format_number(current_value)` |
| `get_expression_display() -> str` | Return `expression` |

**Display formatting rules (`format_number`):**
- If value is an integer (e.g., `5.0`), display as `"5"` using `int(value)` check
- For floats, use up to 10 significant digits: `f"{value:.10g}"`
- For very large numbers (abs > 1e10) or very small (abs < 1e-4 and != 0), use scientific notation via `g` format
- Return `"0"` for zero

**Input buffer rules (`append_digit`):**
- If `input_buffer` is `"0"`, replace with the new digit (unless digit is `"0"`)
- If error state, call `clear_error()` and `clear_all()` first, then append
- After appending, update `current_value = float(input_buffer)`

---

### 3.2 `calculator/logic/basic_logic.py`

**Class:** `BasicCalculator(BaseCalculator)`
**Dependencies:** `base_logic.py`

**Additional state:**
- `pending_tokens: list` -- list of tokens (numbers and operator strings) for expression evaluation

**Methods to implement:**

| Method | Details |
|--------|---------|
| `__init__()` | Call `super().__init__()`; init `pending_tokens = []` |
| `add_operator(op: str)` | Finalize `input_buffer` into `pending_tokens` as a float; append operator string; clear `input_buffer`; update `expression` display string |
| `evaluate() -> float` | Finalize `input_buffer`; evaluate `pending_tokens` with precedence; set `current_value`; reset tokens; update `expression` with ` =` suffix |
| `_evaluate_tokens(tokens: list) -> float` | Shunting-yard or two-pass evaluation (see algorithm below) |

**Expression evaluation algorithm (two-pass on token list):**
1. `pending_tokens` is a flat list like `[7.0, '+', 3.0, '*', 4.0]`
2. **Pass 1 -- high precedence:** Scan left-to-right. When encountering `*` or `/`, compute the result with adjacent operands, replace the three elements with the result. On division by zero, call `set_error("Error")` and return.
3. **Pass 2 -- low precedence:** Scan left-to-right. When encountering `+` or `-`, compute similarly.
4. Result is the single remaining number.
5. Wrap all evaluation in try/except; any error calls `set_error("Error")`.

---

### 3.3 `calculator/logic/scientific_logic.py`

**Class:** `ScientificCalculator(BasicCalculator)`
**Dependencies:** `basic_logic.py`, stdlib `math`

**Additional state:**
- `angle_mode: str` -- `"DEG"` or `"RAD"` (default `"DEG"`)
- `paren_depth: int` -- current nesting depth (default 0)

**Methods to implement:**

| Method | Category | Details |
|--------|----------|---------|
| `toggle_angle_mode() -> str` | Angle | Toggle between `"DEG"` and `"RAD"`; return new mode |
| `_to_radians(value: float) -> float` | Internal | If DEG mode, return `math.radians(value)`; else return value |
| `_from_radians(value: float) -> float` | Internal | If DEG mode, return `math.degrees(value)`; else return value |
| `sin() -> float` | Trig | `math.sin(_to_radians(current_value))`; update current_value |
| `cos() -> float` | Trig | `math.cos(_to_radians(current_value))` |
| `tan() -> float` | Trig | Check if cos is ~0 (i.e., 90 or 270 deg); if so, `set_error("Error")`; else `math.tan(...)` |
| `asin() -> float` | Trig | Error if abs(value) > 1; `_from_radians(math.asin(value))` |
| `acos() -> float` | Trig | Error if abs(value) > 1; `_from_radians(math.acos(value))` |
| `atan() -> float` | Trig | `_from_radians(math.atan(value))` |
| `log() -> float` | Log | Error if value <= 0; `math.log10(value)` |
| `ln() -> float` | Log | Error if value <= 0; `math.log(value)` |
| `log2() -> float` | Log | Error if value <= 0; `math.log2(value)` |
| `square() -> float` | Power | `value ** 2` |
| `cube() -> float` | Power | `value ** 3` |
| `power()` | Power | Two-operand: call `add_operator('**')` to set pending power op |
| `ten_power() -> float` | Power | `10 ** value` |
| `e_power() -> float` | Power | `math.exp(value)` |
| `square_root() -> float` | Root | Error if value < 0; `math.sqrt(value)` |
| `cube_root() -> float` | Root | `value ** (1/3)` with sign handling for negatives |
| `reciprocal() -> float` | Other | Error if value == 0; `1 / value` |
| `factorial() -> float` | Other | Error if value < 0 or not integer; `math.factorial(int(value))` |
| `absolute() -> float` | Other | `abs(value)` |
| `open_paren()` | Paren | Append `"("` to `pending_tokens`; increment `paren_depth` |
| `close_paren()` | Paren | Append current value and `")"` to tokens; decrement `paren_depth`; error if depth < 0 |
| `insert_pi()` | Const | `current_value = math.pi`; clear `input_buffer` |
| `insert_e()` | Const | `current_value = math.e`; clear `input_buffer` |

**Trig edge cases:**
- `tan(90)` in DEG: Check `cos(rad_value)` proximity to zero using `abs(math.cos(rad)) < 1e-10`
- Unary functions (sin, cos, etc.) operate on `current_value` immediately and update it; they do NOT go into the expression token list

**Parentheses handling:**
- Override `_evaluate_tokens` to handle `(` and `)` tokens. Use recursive evaluation: when a `(` is encountered, find the matching `)`, evaluate the sub-list, and replace.
- Alternatively, convert to shunting-yard algorithm that supports parentheses.
- On `evaluate()`, if `paren_depth != 0`, call `set_error("Error")`.

**Power operator (`**`) in token evaluation:**
- Add `**` as highest precedence in the evaluation passes (Pass 0 before `*`/`/`).

---

### 3.4 `calculator/logic/programmer_logic.py`

**Class:** `ProgrammerCalculator(BaseCalculator)`
**Dependencies:** `base_logic.py`

**Additional state:**
- `base: str` -- `"DEC"`, `"HEX"`, `"OCT"`, or `"BIN"` (default `"DEC"`)
- `word_size: int` -- 8, 16, 32, or 64 (default 64)
- `current_value: int` -- override as int, not float
- `pending_tokens: list` -- same pattern as BasicCalculator

**Methods to implement:**

| Method | Details |
|--------|---------|
| `set_base(base: str)` | Set `self.base`; does not change `current_value` (internal is always int) |
| `get_value_in_base(base: str) -> str` | Format `current_value` for display in given base |
| `get_all_bases() -> dict` | Return `{"DEC": ..., "HEX": ..., "OCT": ..., "BIN": ...}` |
| `get_valid_digits() -> set` | BIN: `{"0","1"}`; OCT: `{"0"-"7"}`; DEC: `{"0"-"9"}`; HEX: `{"0"-"9","A"-"F"}` |
| `set_word_size(bits: int)` | Set `self.word_size`; apply `mask_value` to `current_value` |
| `mask_value(value: int) -> int` | Two's complement mask (see algorithm below) |
| `add_operator(op: str)` | Supports `+`, `-`, `*`, `/`, `%`, `AND`, `OR`, `XOR`, `LSH`, `RSH` |
| `evaluate() -> int` | Evaluate `pending_tokens`; apply `mask_value` to result |
| `bitwise_and/or/xor()` | Call `add_operator("AND"/"OR"/"XOR")` |
| `bitwise_not() -> int` | `current_value = mask_value(~current_value)` |
| `left_shift/right_shift()` | Call `add_operator("LSH"/"RSH")` |
| `append_hex_digit(digit: str)` | Only if `base == "HEX"`; append to `input_buffer`; parse with `int(input_buffer, 16)` |
| `append_digit(digit: str)` | Override: parse `input_buffer` with `int(input_buffer, current_base_int)` |
| `append_decimal()` | No-op (disabled in programmer mode) |
| `format_number(value) -> str` | Format as integer in current base; uppercase for hex |

**Two's complement masking algorithm (`mask_value`):**
```python
def mask_value(self, value: int) -> int:
    bits = self.word_size
    mask = (1 << bits) - 1          # e.g., 0xFF for 8-bit
    value = value & mask             # Truncate to word size
    if value & (1 << (bits - 1)):   # Check sign bit
        value -= (1 << bits)         # Sign-extend
    return value
```

**Base conversion (`get_value_in_base`):**
- DEC: `str(value)`
- HEX: `format(value & mask, 'X')` -- use unsigned representation for display
- OCT: `format(value & mask, 'o')`
- BIN: `format(value & mask, 'b')`
- For negative values in non-DEC bases, display the two's complement unsigned representation.

**Token evaluation:**
- Same two-pass approach as BasicCalculator but with additional operators.
- Pass 0: `LSH`, `RSH` (lowest precedence in programmer context, or adjust as needed)
- Pass 1: `*`, `/`, `%`
- Pass 2: `+`, `-`
- Pass 3: `AND`, `XOR`, `OR` (bitwise ops are low precedence)
- Division uses `int(a / b)` (truncation toward zero) -- use `int()` not `//` to match C-style truncation for negative numbers.

---

### 3.5 `calculator/gui/base_view.py`

**Class:** `BaseView(ttk.Frame)`
**Dependencies:** `tkinter`, `tkinter.ttk`

**Components to create:**
- `expression_label` -- `ttk.Label` for secondary display (top line, right-aligned, smaller font)
- `result_display` -- `ttk.Label` for primary display (large font, right-aligned, bold)
- `memory_indicator` -- small `ttk.Label` showing "M", hidden by default
- Internal `_callbacks: dict` mapping button IDs to callables

**Methods:**
- `set_display(text: str)` -- update `result_display` text
- `set_expression(text: str)` -- update `expression_label` text
- `show_memory_indicator(visible: bool)` -- show/hide the "M" label
- `set_button_callback(button_id: str, callback: Callable)` -- store callback
- `_create_display()` -- internal: build display widgets using `grid()`
- `_make_button(parent, text, button_id, row, col, ...)` -- helper to create a button wired to callback dict

**Layout:** Use `grid()` throughout. Display area at row 0-1, buttons below.

---

### 3.6 `calculator/gui/basic_view.py`

**Class:** `BasicView(BaseView)`
**Dependencies:** `base_view.py`

**Layout (matching requirements section 3.6):**
- Row 0-1: Display (inherited)
- Row 2: Memory buttons: MC, MR, M+, M-, MS
- Row 3: C, +/-, %, /
- Row 4: 7, 8, 9, *
- Row 5: 4, 5, 6, -
- Row 6: 1, 2, 3, +
- Row 7: 0 (colspan=2), ., =

**Button IDs:** `"digit_0"` through `"digit_9"`, `"op_add"`, `"op_sub"`, `"op_mul"`, `"op_div"`, `"equals"`, `"clear"`, `"all_clear"`, `"backspace"`, `"decimal"`, `"toggle_sign"`, `"percent"`, `"mc"`, `"mr"`, `"m_plus"`, `"m_minus"`, `"ms"`

---

### 3.7 `calculator/gui/scientific_view.py`

**Class:** `ScientificView(BaseView)`
**Dependencies:** `base_view.py`

**Additional elements beyond BasicView:**
- Deg/Rad indicator label near display
- 5 additional columns on the left for scientific buttons
- Parentheses buttons, trig buttons, log buttons, power/root buttons, constants

**Additional button IDs:** `"sin"`, `"cos"`, `"tan"`, `"asin"`, `"acos"`, `"atan"`, `"log"`, `"ln"`, `"log2"`, `"square"`, `"cube"`, `"power"`, `"ten_power"`, `"e_power"`, `"sqrt"`, `"cbrt"`, `"reciprocal"`, `"factorial"`, `"absolute"`, `"open_paren"`, `"close_paren"`, `"pi"`, `"euler"`, `"toggle_angle"`

**Additional methods:**
- `set_angle_mode(mode: str)` -- update the Deg/Rad indicator
- `set_paren_depth(depth: int)` -- optionally show nesting count

---

### 3.8 `calculator/gui/programmer_view.py`

**Class:** `ProgrammerView(BaseView)`
**Dependencies:** `base_view.py`

**Additional elements:**
- Base conversion panel: 4 labels showing HEX, DEC, OCT, BIN values simultaneously
- Base selector: 4 radio buttons (DEC, HEX, OCT, BIN)
- Word size selector: dropdown or buttons for 8, 16, 32, 64
- Hex digit buttons: A-F
- Bitwise operation buttons: AND, OR, XOR, NOT, LSH, RSH
- MOD button for modulo

**Additional methods:**
- `set_base_panel(values: dict)` -- update the 4-base display panel
- `set_active_base(base: str)` -- select the radio button
- `enable_digits(valid_digits: set)` -- enable/disable digit and hex buttons
- `set_word_size_display(bits: int)` -- update word size indicator

**Additional button IDs:** `"hex_a"` through `"hex_f"`, `"base_dec"`, `"base_hex"`, `"base_oct"`, `"base_bin"`, `"word_8"`, `"word_16"`, `"word_32"`, `"word_64"`, `"op_and"`, `"op_or"`, `"op_xor"`, `"op_not"`, `"op_lsh"`, `"op_rsh"`, `"op_mod"`

---

### 3.9 `calculator/app.py`

**Class:** `App(tk.Tk)`
**Dependencies:** All logic modules, all GUI modules

**Responsibilities:**
- Create all 3 logic instances and all 3 view instances at startup
- Register callbacks from each view to the appropriate logic methods
- Handle mode switching with value/memory transfer
- Bind keyboard shortcuts on the root window
- Implement the `_update_display()` pattern from the architecture doc

**Key methods:**

| Method | Details |
|--------|---------|
| `__init__()` | Set title, create logic/view dicts, set initial mode to basic, register callbacks, bind keys |
| `switch_mode(new_mode: str)` | Transfer value and memory per architecture section 6.2; swap views; resize |
| `_register_callbacks(mode: str)` | Wire each button ID in the view to the corresponding logic call + `_update_display()` |
| `_on_key_press(event)` | Route key to appropriate handler based on `current_mode` |
| `_on_digit(digit: str)` | Logic.append_digit; update display |
| `_on_operator(op: str)` | Logic.add_operator; update display |
| `_on_equals()` | Logic.evaluate; update display |
| `_on_scientific_func(func_name: str)` | Call the named method on ScientificCalculator; update display |
| `_on_base_change(base: str)` | ProgrammerCalculator.set_base; update display + base panel |
| `_on_word_size_change(bits: int)` | ProgrammerCalculator.set_word_size; update display |
| `_update_display()` | Read logic state; push to view; handle error state; update base panel if programmer |
| `_resize_for_mode(mode: str)` | Set geometry: basic ~300x400, scientific ~500x400, programmer ~550x500 |

**Keyboard binding map:**
```python
DIGIT_KEYS = {str(i): str(i) for i in range(10)}
OPERATOR_KEYS = {'+': '+', '-': '-', '*': '*', '/': '/'}
SPECIAL_KEYS = {'Return': 'equals', 'Escape': 'all_clear', 'BackSpace': 'backspace'}
PAREN_KEYS = {'(': 'open_paren', ')': 'close_paren'}  # scientific only
HEX_KEYS = {c: c for c in 'abcdefABCDEF'}             # programmer HEX only
BITWISE_KEYS = {'&': 'AND', '|': 'OR', '^': 'XOR', '~': 'NOT', '<': 'LSH', '>': 'RSH'}
```

---

### 3.10 `main.py`

**Dependencies:** `calculator.app`

```python
from calculator.app import App

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
```

---

### 3.11 `requirements.txt`

```
pytest
```

---

## 4. Key Implementation Notes

### Expression Evaluation Strategy
Use a token-list-based approach (not string parsing). Operators and operands are stored in `pending_tokens` as a flat list. Evaluation uses multi-pass scanning by precedence level. This avoids the complexity of a full parser while correctly handling precedence. For parentheses in scientific mode, use recursive sub-list evaluation.

### Base Conversion in Programmer Mode
- Internal storage is always a Python `int` in base 10.
- Display conversion uses `format()` for HEX/OCT/BIN output.
- Input parsing uses `int(input_buffer, base)` where base is 2/8/10/16.

### Two's Complement
```python
mask = (1 << bits) - 1
value = value & mask
if value & (1 << (bits - 1)):
    value -= (1 << bits)
```
This handles overflow wrapping, sign extension, and word size truncation in a single operation.

### Trigonometric Functions
- Use `math.sin`, `math.cos`, `math.tan` which expect radians.
- Convert degrees to radians with `math.radians()` when `angle_mode == "DEG"`.
- Detect `tan(90)` by checking if `abs(math.cos(radians)) < 1e-10`.
- Inverse trig functions return radians; convert back to degrees if needed.

### Display Formatting
- Integer check: `value == int(value)` and value is finite.
- Use `f"{value:.10g}"` for up to 10 significant digits.
- Python's `g` format automatically switches to scientific notation for large/small values.
- Cap display length; truncate if needed for GUI fit.

### Error Handling
- All logic methods that can fail should catch exceptions internally and call `set_error()`.
- The controller checks `logic.error` after every operation in `_update_display()`.
- After an error, the next digit input triggers `clear_error()` + `clear_all()` + `append_digit()`.
- No Python tracebacks may reach the user. Wrap evaluate calls in try/except as a safety net.
