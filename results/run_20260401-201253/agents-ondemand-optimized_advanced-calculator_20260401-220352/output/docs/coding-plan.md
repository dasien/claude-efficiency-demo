# Advanced Calculator -- Coding Plan

**Version:** 1.0
**Date:** 2026-04-01
**Reference:** docs/requirements.md, docs/architecture.md

---

## Implementation Phases

Work proceeds in three phases: Logic first (testable immediately), then GUI, then Controller glue. Within each phase, implement files in the listed order because later files depend on earlier ones.

---

## Phase 1: Logic Layer

### 1.1 calculator/logic/__init__.py

- Empty file or re-export the main classes for convenience.
- No implementation logic.

### 1.2 calculator/logic/base_logic.py

**Classes:** `CalculatorError`, `ExpressionParser`, `BaseCalculator`

**Implementation order within file:**

1. `CalculatorError(Exception)` -- simple custom exception, no extra fields needed.

2. `ExpressionParser` -- the most critical piece of the entire project.
   - Implement `PRECEDENCE` dict mapping operator strings to integer priority levels.
   - Implement `_to_postfix(tokens)` using the shunting-yard algorithm:
     - Walk tokens left to right.
     - Numbers go directly to output queue.
     - Operators go to operator stack, popping higher/equal precedence operators to output first.
     - `(` pushes to stack, `)` pops until matching `(`.
     - Raise `CalculatorError` on mismatched parentheses.
   - Implement `_evaluate_postfix(postfix)` using a value stack:
     - Numbers push to stack.
     - Operators pop two values, apply, push result.
     - Division by zero raises `CalculatorError`.
     - At end, stack should have exactly one value.
   - Implement `parse(tokens)` as the public entry point that calls both.
   - **Operator set:** `+`, `-`, `*`, `/` for basic/scientific. Add `%` (modulo), `AND`, `OR`, `XOR`, `LSH`, `RSH` for programmer mode. All go through the same parser with appropriate precedence levels:
     - Precedence 1: `+`, `-`
     - Precedence 2: `*`, `/`, `%`
     - Precedence 3: `AND`
     - Precedence 4: `XOR`
     - Precedence 5: `OR`
     - Precedence 3: `LSH`, `RSH`
   - **Testing note:** This class must be thoroughly tested with precedence and parentheses cases before moving on.

3. `BaseCalculator` -- shared state management.
   - `__init__`: Initialize `current_input = ""`, `expression = []`, `memory = 0.0`, `has_memory = False`, `error_state = False`.
   - `format_number(value)`:
     - If `value == int(value)` and not too large, return `str(int(value))`.
     - Otherwise format to 10 significant digits.
     - For very large/small values (abs > 1e10 or abs < 1e-10 and nonzero), use `f"{value:.10g}"`.
   - Memory methods: straightforward get/set on `self.memory` and `self.has_memory`.
   - `append_digit(digit)`: Concatenate to `current_input`. Strip leading zeros (replace `"0"` prefix unless followed by `.`).
   - `append_decimal()`: Add `"."` only if not already present. If `current_input` is empty, set to `"0."`.
   - `toggle_sign(value)`: Return `-value`.
   - `percentage(value)`: Return `value / 100`.
   - `backspace()`: Remove last char from `current_input`. If empty, set to `"0"`.
   - `clear_entry()`: Reset `current_input` to `""`, keep `expression`.
   - `all_clear()`: Reset `current_input`, `expression`, `error_state`.
   - `clear_error()`: Set `error_state = False`, call `all_clear()`.

**Dependencies:** None (stdlib only: `math` module will be used in subclasses).

**Key implementation notes:**
- `current_input` is a string (what the user is typing). It gets parsed to float/int only when finalized (operator pressed or evaluate called).
- `expression` is a list of mixed types: `[2.0, "+", 3.0, "*", 4.0]`. Numbers are always float (or int in programmer mode).

### 1.3 calculator/logic/basic_logic.py

**Class:** `BasicCalculator(BaseCalculator)`

**Implementation:**

1. `add_operator(op)`:
   - If `current_input` is not empty, parse it to float and append to `expression`.
   - Append `op` string to `expression`.
   - Clear `current_input`.
   - If `current_input` is empty and expression ends with an operator, replace the last operator (allows changing mind).

2. `evaluate()`:
   - If `current_input` is not empty, parse and append to `expression`.
   - Call `ExpressionParser().parse(self.expression)`.
   - Store result, clear expression, set `current_input` to formatted result.
   - Return the result.

3. `get_expression_display()`:
   - Join expression tokens with spaces, appending current_input if present.

**Dependencies:** `base_logic.py`

### 1.4 calculator/logic/scientific_logic.py

**Class:** `ScientificCalculator(BasicCalculator)`

**Implementation:**

1. `__init__`: Call super, add `self.angle_mode = "DEG"`, `self.paren_depth = 0`.

2. Angle helpers:
   - `toggle_angle_mode()`: Flip between "DEG" and "RAD", return new mode string.
   - `_to_radians(value)`: If DEG mode, convert `value * math.pi / 180`. If RAD, return as-is.
   - `_from_radians(value)`: Inverse of above.

3. Trig functions (sin, cos, tan, asin, acos, atan):
   - Each takes a float value, converts to radians if needed, calls `math.sin()` etc.
   - `tan`: Check if cos is approximately zero (angle near 90 or 270 deg); raise `CalculatorError`.
   - `asin`/`acos`: Check domain [-1, 1]; raise `CalculatorError` if outside.
   - Return result, converting from radians if inverse trig in degree mode.

4. Log functions (log10, ln, log2):
   - Check `value > 0`; raise `CalculatorError` otherwise.
   - Call `math.log10()`, `math.log()`, `math.log2()`.

5. Power/root functions:
   - `square(v)`: `v ** 2`
   - `cube(v)`: `v ** 3`
   - `power(base, exp)`: `base ** exp` -- this is a binary op; the Controller manages the two-operand flow using the expression system (add `"**"` operator or handle specially).
   - `ten_to_x(v)`: `10 ** v`
   - `e_to_x(v)`: `math.e ** v`
   - `sqrt(v)`: Check `v >= 0`, then `math.sqrt(v)`.
   - `cbrt(v)`: `v ** (1/3)`, handle negative values correctly: `-(abs(v) ** (1/3))`.
   - `reciprocal(v)`: Check `v != 0`, then `1 / v`.

6. Constants: `get_pi()` returns `math.pi`, `get_e()` returns `math.e`.

7. Factorial:
   - Check `value >= 0` and `value == int(value)`; raise `CalculatorError` otherwise.
   - Use `math.factorial(int(value))`. This handles up to 170 via float conversion.
   - For n > 170, the result overflows float; return `math.factorial` result and let `format_number` handle the display.

8. `absolute_value(v)`: Return `abs(v)`.

9. Parentheses:
   - `open_paren()`: Append `"("` to expression, increment `paren_depth`.
   - `close_paren()`: Check `paren_depth > 0` (else raise error), finalize current input, append `")"`, decrement `paren_depth`.

**Dependencies:** `basic_logic.py`, `math` stdlib module.

**Key implementation note on x^n:** The `power` operation is binary. When the user presses `x^n`, the Controller should call `add_operator("**")` on the model. The ExpressionParser needs to handle `**` with high precedence (add precedence level 4 for `**`, right-associative).

### 1.5 calculator/logic/programmer_logic.py

**Class:** `ProgrammerCalculator(BaseCalculator)`

**Implementation:**

1. `__init__`: Call super, add `self.base = 10`, `self.word_size = 64`, `self.value = 0`.

2. Base conversion:
   - `set_base(base)`: Set `self.base`, return formatted current value.
   - `format_in_base(value, base)`: Use `bin()`, `oct()`, `hex()` builtins, strip prefixes, uppercase. For DEC, just `str()`.
   - `get_all_bases(value)`: Return dict with all four formatted representations.
   - `parse_input(digit)`: Validate `digit` is legal for `self.base`. Append to current input, reparse full input string in current base using `int(input_str, base)`.
   - `get_valid_digits()`: Return `{"0","1"}` for BIN, `{"0"-"7"}` for OCT, `{"0"-"9"}` for DEC, `{"0"-"9","A"-"F"}` for HEX.

3. Word size:
   - `set_word_size(bits)`: Set `self.word_size`, apply to current value (may truncate).
   - `_apply_word_size(value)`: Bitmask and two's complement as described in architecture doc.

4. Bitwise operations:
   - `bitwise_and(a, b)`: `_apply_word_size(a & b)`
   - `bitwise_or(a, b)`: `_apply_word_size(a | b)`
   - `bitwise_xor(a, b)`: `_apply_word_size(a ^ b)`
   - `bitwise_not(value)`: `_apply_word_size(~value)`
   - `left_shift(value, n)`: `_apply_word_size(value << n)`
   - `right_shift(value, n)`: `_apply_word_size(value >> n)`

5. Integer arithmetic:
   - `integer_divide(a, b)`: Check `b != 0`, return `_apply_word_size(int(a / b))`. Use `int(a/b)` for truncating division (not `//` which is floor division).
   - `modulo(a, b)`: Check `b != 0`, return `_apply_word_size(a % b)`.

6. `evaluate()`: Use ExpressionParser, cast result to int, apply word size.

7. Override `append_decimal()` to be a no-op (PM-3).

8. Override `append_digit(digit)`: Validate against current base, build number in current base.

**Dependencies:** `base_logic.py`

**Key implementation notes:**
- Internally, always store and compute with Python arbitrary-precision `int`. Apply word size constraint only at the boundary (before display and after each operation result).
- For truncating division: `int(a / b)` truncates toward zero. Python's `//` floors toward negative infinity, which is different for negative numbers. Use `int(a / b)`.
- Bitwise NOT: Python's `~x` gives `-(x+1)` which is correct for two's complement, but apply word size mask afterward.

---

## Phase 2: GUI Layer

### 2.1 calculator/gui/__init__.py

- Empty or re-exports.

### 2.2 calculator/gui/base_view.py

**Class:** `BaseView(ttk.Frame)`

**Implementation:**
1. `__init__(parent, controller)`: Store controller ref, call `_create_display()`.
2. `_create_display()`:
   - Create expression label (secondary display): `tk.Label`, small font, left-aligned, `anchor="e"`.
   - Create result label (primary display): `tk.Label`, large font (e.g., 24pt), right-aligned.
   - Grid both at top spanning all columns.
3. `_create_button(parent, text, row, col, command, colspan, style)`:
   - Create `tk.Button` with specified text and command.
   - Grid it at (row, col) with columnspan.
   - Apply style (digit buttons: light gray, operator buttons: orange, equals: blue, function buttons: dark gray).
   - Return the button reference (so subclasses can store refs for enable/disable).
4. `update_display(value, expression)`: Set result label text, expression label text.
5. `show_error(message)`: Set result label to message (default "Error").
6. `show_memory_indicator(visible)`: Show/hide "M" label.
7. `_create_memory_row(parent, row)`: Create MC, MR, M+, M-, MS buttons in a row.

### 2.3 calculator/gui/basic_view.py

**Class:** `BasicView(BaseView)`

**Implementation:**
1. `__init__`: Call super, then `_create_buttons()`.
2. `_create_buttons()`:
   - Create memory row (row 0).
   - Create main grid (rows 1-6): C, +/-, %, /, 7, 8, 9, *, 4, 5, 6, -, 1, 2, 3, +, 0 (colspan=2), ., =.
   - Each button's command calls the appropriate controller method.

### 2.4 calculator/gui/scientific_view.py

**Class:** `ScientificView(BaseView)`

**Implementation:**
1. Same display as BasicView but wider.
2. Left panel (5 columns) with scientific function buttons.
3. Right panel replicates basic buttons.
4. Deg/Rad indicator label in header area.
5. Paren depth counter near ( ) buttons.

### 2.5 calculator/gui/programmer_view.py

**Class:** `ProgrammerView(BaseView)`

**Implementation:**
1. Base conversion panel: 4 labels showing DEC, HEX, OCT, BIN values simultaneously. Updated via `update_base_panel(values_dict)` method.
2. Base selector: 4 radio buttons (DEC, HEX, OCT, BIN).
3. Word size selector: dropdown or radio buttons (8, 16, 32, 64).
4. Hex digit buttons A-F: store references for enable/disable.
5. Bitwise operation buttons: AND, OR, XOR, NOT, LSH, RSH.
6. Standard digit buttons 0-9 (store refs for enable/disable).
7. No decimal point button.
8. `update_button_states(valid_digits)`: Enable/disable buttons based on the set of valid digits for the current base.

---

## Phase 3: Controller and Entry Point

### 3.1 calculator/__init__.py

- Empty or version string.

### 3.2 calculator/app.py

**Class:** `App(tk.Tk)`

**Implementation:**
1. `__init__`: Create all three model instances, create menu bar, create all three view instances (pack_forget the inactive ones), bind keyboard, switch to basic mode.
2. `_create_menu()`: Menu bar with Mode menu (Basic, Scientific, Programmer) with Ctrl+1/2/3 accelerators. Checkmark on active mode.
3. `_switch_mode(mode)`: Full implementation per architecture doc section 5.
4. Event handler methods: Each delegates to the active model, wraps in try/except for CalculatorError, calls `_update_display()`.
5. `_bind_keyboard()`: Bind all keys from requirements section 6. Use `bind_all` for universal keys, check active mode for mode-specific keys.
6. `_update_display()`: Pull state from active model, push to active view. For programmer mode, also update the base conversion panel.

### 3.3 main.py

```python
from calculator.app import App

def main() -> None:
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
```

### 3.4 requirements.txt

```
pytest
```

---

## Module Dependency Summary

```
Phase 1 (no GUI dependency):
  base_logic.py          <- no deps
  basic_logic.py         <- base_logic
  scientific_logic.py    <- basic_logic
  programmer_logic.py    <- base_logic

Phase 2 (depends on Phase 3 controller interface, but can be built in parallel):
  base_view.py           <- tkinter only
  basic_view.py          <- base_view
  scientific_view.py     <- base_view
  programmer_view.py     <- base_view

Phase 3 (depends on both Phase 1 and Phase 2):
  app.py                 <- all logic modules + all view modules
  main.py                <- app.py
```

---

## Implementation Checklist

| # | File | Phase | Est. Lines | Key Risk |
|---|------|-------|-----------|----------|
| 1 | logic/base_logic.py | 1 | 200-250 | Expression parser correctness |
| 2 | logic/basic_logic.py | 1 | 80-100 | Operator chaining edge cases |
| 3 | logic/scientific_logic.py | 1 | 180-220 | Trig domain errors, angle mode |
| 4 | logic/programmer_logic.py | 1 | 200-250 | Two's complement, base conversion |
| 5 | gui/base_view.py | 2 | 100-130 | Layout consistency |
| 6 | gui/basic_view.py | 2 | 80-100 | Button grid alignment |
| 7 | gui/scientific_view.py | 2 | 120-150 | Wide layout, many buttons |
| 8 | gui/programmer_view.py | 2 | 150-180 | Dynamic button enable/disable |
| 9 | app.py | 3 | 250-300 | Mode switch state transfer |
| 10 | main.py | 3 | 10 | None |

**Total estimated:** 1,370-1,690 lines of application code, plus tests.
