# Advanced Calculator -- Coding Plan

**Version:** 1.0
**Date:** 2026-04-01
**Based on:** requirements.md v1.0, architecture.md v1.0

---

## 1. Implementation Order

The project must be built bottom-up: logic layer first, then GUI layer, then
the controller, and finally the entry point. Tests are written alongside each
logic module. This order ensures that every module can be validated before
anything depends on it.

### Phase 1: Foundation (Logic Layer -- Shared)

| Step | File | Depends On |
|------|------|------------|
| 1.1 | `requirements.txt` | Nothing |
| 1.2 | `calculator/__init__.py` | Nothing |
| 1.3 | `calculator/logic/__init__.py` | Nothing |
| 1.4 | `calculator/logic/base_logic.py` | Nothing |

### Phase 2: Mode-Specific Logic

| Step | File | Depends On |
|------|------|------------|
| 2.1 | `calculator/logic/basic_logic.py` | `base_logic.py` |
| 2.2 | `calculator/logic/scientific_logic.py` | `basic_logic.py` |
| 2.3 | `calculator/logic/programmer_logic.py` | `base_logic.py` |

### Phase 3: Logic Tests

| Step | File | Depends On |
|------|------|------------|
| 3.1 | `tests/__init__.py` | Nothing |
| 3.2 | `tests/test_basic.py` | `basic_logic.py` |
| 3.3 | `tests/test_scientific.py` | `scientific_logic.py` |
| 3.4 | `tests/test_programmer.py` | `programmer_logic.py` |
| 3.5 | `tests/test_memory.py` | `base_logic.py`, `basic_logic.py` |

### Phase 4: GUI Layer

| Step | File | Depends On |
|------|------|------------|
| 4.1 | `calculator/gui/__init__.py` | Nothing |
| 4.2 | `calculator/gui/base_view.py` | Nothing (uses tkinter only) |
| 4.3 | `calculator/gui/basic_view.py` | `base_view.py` |
| 4.4 | `calculator/gui/scientific_view.py` | `base_view.py` |
| 4.5 | `calculator/gui/programmer_view.py` | `base_view.py` |

### Phase 5: Controller and Entry Point

| Step | File | Depends On |
|------|------|------------|
| 5.1 | `calculator/app.py` | All logic modules, all GUI modules |
| 5.2 | `main.py` | `calculator/app.py` |

### Phase 6: Integration Tests

| Step | File | Depends On |
|------|------|------------|
| 6.1 | `tests/test_mode_switch.py` | All logic modules |

---

## 2. File-by-File Breakdown

### 2.1 `requirements.txt`

Contents: a single line specifying `pytest` for testing. No other dependencies.

```
pytest
```

---

### 2.2 `calculator/__init__.py`

Empty file. Marks the directory as a Python package.

---

### 2.3 `calculator/logic/__init__.py`

Empty file. Marks the directory as a Python package.

---

### 2.4 `calculator/logic/base_logic.py`

**Responsibility:** Define all shared data types, the data transfer objects,
and the abstract base class that all three modes inherit from.

**Enums:**

- `Mode` -- values: `BASIC`, `SCIENTIFIC`, `PROGRAMMER`.
- `AngleUnit` -- values: `DEG`, `RAD`.
- `NumberBase` -- values: `DEC` (10), `HEX` (16), `OCT` (8), `BIN` (2).
- `WordSize` -- values: `BITS_8` (8), `BITS_16` (16), `BITS_32` (32), `BITS_64` (64).

**Dataclasses:**

- `DisplayState` -- immutable snapshot of the full calculator state for the
  view to render. Fields: `main_display`, `expression_display`, `error`,
  `memory_indicator`, `angle_unit`, `paren_depth`, `number_base`, `word_size`,
  `hex_value`, `dec_value`, `oct_value`, `bin_value`.
- `ButtonEnabledState` -- which buttons should be enabled or disabled. Fields:
  `digits` (dict mapping digit label to bool), `hex_digits` (dict mapping
  A-F to bool), `decimal_point` (bool).

**Class `BaseLogic(ABC)`:**

Instance attributes:
- `_memory: float` -- stored memory value, initialized to 0.0.
- `_current_input: str` -- the string the user is currently typing, initialized to "0".
- `_expression: str` -- the human-readable expression string for the secondary display.
- `_error: bool` -- True when the display shows "Error".
- `_new_input: bool` -- True when the next digit should replace the display
  rather than append.

Methods:

| Method | Description |
|--------|-------------|
| `memory_clear() -> DisplayState` | Set `_memory` to 0.0, return display state. |
| `memory_recall() -> DisplayState` | Set `_current_input` to formatted `_memory`, set `_new_input = True`. |
| `memory_add() -> DisplayState` | Add current display value to `_memory`. |
| `memory_subtract() -> DisplayState` | Subtract current display value from `_memory`. |
| `memory_store() -> DisplayState` | Set `_memory` to current display value. |
| `has_memory -> bool` (property) | True if `_memory != 0.0`. |
| `input_digit(digit: str) -> DisplayState` | Append digit to `_current_input`. If `_new_input`, replace instead of append. Handle leading zeros (NI-4). Clear error state if set (RC-1). |
| `input_decimal() -> DisplayState` | Append "." if not already present (NI-3). If `_new_input`, start with "0.". |
| `input_sign_toggle() -> DisplayState` | Toggle leading "-" on `_current_input` (NI-5). |
| `input_backspace() -> DisplayState` | Remove last character from `_current_input`. If result is empty or "-", reset to "0". |
| `clear_entry() -> DisplayState` | Reset `_current_input` to "0", clear `_error` flag, preserve expression and pending ops. |
| `clear_all() -> DisplayState` | Reset all state except `_memory`. |
| `evaluate() -> DisplayState` | Abstract. Subclasses implement expression evaluation. |
| `get_current_value() -> float` | Parse `_current_input` to float. Return 0.0 if parsing fails. |
| `set_current_value(value: float) -> DisplayState` | Set `_current_input` to `format_number(value)`, clear expression, set `_new_input = True`. |
| `format_number(value: float) -> str` (static) | Format for display per rules DI-3 through DI-5. |
| `get_display_state() -> DisplayState` | Abstract. Subclasses build the full DisplayState. |

**Implementation notes for `format_number`:**

```
1. If value == int(value) and abs(value) < 1e16:
     return str(int(value))
2. If abs(value) >= 1e16 or (abs(value) < 1e-10 and value != 0):
     return f"{value:.10g}"   (scientific notation via Python's g format)
3. Otherwise:
     return f"{value:.10g}"   (up to 10 significant digits, trailing zeros stripped)
```

The `g` format specifier in Python already handles most of these rules: it
strips trailing zeros, omits the decimal point for integers, and switches to
scientific notation for very large or very small values. The threshold of 10
significant digits satisfies DI-4.

---

### 2.5 `calculator/logic/basic_logic.py`

**Responsibility:** Basic four-function arithmetic with correct operator
precedence. Extends `BaseLogic`.

**Class `BasicLogic(BaseLogic)`:**

Instance attributes (in addition to inherited):
- `_tokens: list` -- accumulated expression tokens, e.g. `[2.0, "+", 3.0, "*", 4.0]`.
- `_pending_op: str` -- the most recently pressed operator, waiting for the
  next operand before being committed to `_tokens`.

Methods:

| Method | Description |
|--------|-------------|
| `input_operator(op: str) -> DisplayState` | Commit the current input as a number token, append the operator token. If there is already a `_pending_op`, commit it first. Update `_expression` string. Set `_new_input = True`. |
| `input_percent() -> DisplayState` | Divide current display value by 100, update `_current_input` (NI-6). |
| `evaluate() -> DisplayState` | Commit any remaining input/operator to `_tokens`, then evaluate the token list using two-pass precedence (see below). On success, set `_current_input` to formatted result and clear `_tokens`. On error, set `_error = True`. |
| `get_display_state() -> DisplayState` | Build a `DisplayState` with `main_display`, `expression_display`, `error`, and `memory_indicator`. |

**Implementation notes for expression evaluation (the tricky part):**

The token list contains alternating numbers and operators:
`[num, op, num, op, num, ...]`

Evaluation uses two passes over the list:

```
Pass 1 -- Multiply and Divide (left to right):
  Create a new list. Walk the tokens:
    - If the token is a number, check if the previous operator was * or /.
      If so, apply it to the accumulated value. Otherwise, append to new list.
    - If the token is + or -, append to new list.
  After this pass, only + and - remain.

Pass 2 -- Add and Subtract (left to right):
  Walk the reduced list and accumulate the result.
```

Concrete algorithm:

```python
def _evaluate_tokens(self, tokens: list) -> float:
    # Pass 1: resolve * and /
    reduced = [tokens[0]]
    i = 1
    while i < len(tokens):
        op = tokens[i]
        right = tokens[i + 1]
        if op == "*":
            reduced[-1] = reduced[-1] * right
        elif op == "/":
            if right == 0:
                raise ZeroDivisionError
            reduced[-1] = reduced[-1] / right
        else:
            reduced.append(op)
            reduced.append(right)
        i += 2

    # Pass 2: resolve + and -
    result = reduced[0]
    i = 1
    while i < len(reduced):
        op = reduced[i]
        right = reduced[i + 1]
        if op == "+":
            result += right
        elif op == "-":
            result -= right
        i += 2

    return result
```

Edge cases to handle:
- Empty token list: return current display value.
- Single number, no operator: return that number.
- Operator pressed with no second operand: use current display value as both operands (e.g., `5 + =` means `5 + 5 = 10`).
- Consecutive operator presses: replace the previous operator (e.g., `5 + - 3` means `5 - 3`).

**Expression string building:**

The `_expression` attribute is a human-readable string shown in the secondary
display. It is built by concatenating formatted numbers and operator symbols as
they are entered. On `evaluate()`, append " =" to the expression. On the next
input after evaluation, clear the expression.

---

### 2.6 `calculator/logic/scientific_logic.py`

**Responsibility:** All scientific functions. Extends `BasicLogic` so that all
basic arithmetic (including precedence) is inherited.

**Class `ScientificLogic(BasicLogic)`:**

Instance attributes (in addition to inherited):
- `_angle_unit: AngleUnit` -- current angle mode, default `DEG`.
- `_paren_depth: int` -- current parenthesis nesting level.
- `_paren_stack: list[dict]` -- stack of saved expression states. Each entry is a dict containing `{"tokens": [...], "pending_op": "...", "expression": "..."}`.

Methods:

| Method | Description |
|--------|-------------|
| `toggle_angle_unit() -> DisplayState` | Toggle between `DEG` and `RAD`. |
| `angle_unit -> AngleUnit` (property) | Return current angle unit. |
| `trig_sin() -> DisplayState` | Apply sin to current value. |
| `trig_cos() -> DisplayState` | Apply cos to current value. |
| `trig_tan() -> DisplayState` | Apply tan to current value. Check for undefined (cos near zero). |
| `trig_asin() -> DisplayState` | Apply arcsin. Error if abs(value) > 1. |
| `trig_acos() -> DisplayState` | Apply arccos. Error if abs(value) > 1. |
| `trig_atan() -> DisplayState` | Apply arctan to current value. |
| `log_base10() -> DisplayState` | Apply log10. Error if value <= 0. |
| `log_natural() -> DisplayState` | Apply ln. Error if value <= 0. |
| `log_base2() -> DisplayState` | Apply log2. Error if value <= 0. |
| `power_square() -> DisplayState` | Replace current value with value**2. |
| `power_cube() -> DisplayState` | Replace current value with value**3. |
| `power_n() -> DisplayState` | Set pending operator to "**" and wait for second operand. |
| `power_10x() -> DisplayState` | Replace current value with 10**value. |
| `power_ex() -> DisplayState` | Replace current value with e**value. |
| `root_square() -> DisplayState` | Replace current value with sqrt(value). Error if value < 0. |
| `root_cube() -> DisplayState` | Replace current value with cbrt(value). Use `math.copysign(abs(v)**(1/3), v)` for negative values. |
| `reciprocal() -> DisplayState` | Replace current value with 1/value. Error if value == 0. |
| `insert_pi() -> DisplayState` | Set current input to `math.pi`. |
| `insert_e() -> DisplayState` | Set current input to `math.e`. |
| `factorial() -> DisplayState` | Compute n!. Error if value < 0 or not an integer. Use `math.factorial`. |
| `absolute_value() -> DisplayState` | Replace current value with abs(value). |
| `open_paren() -> DisplayState` | Push current tokens/pending_op/expression onto `_paren_stack`. Reset tokens to empty. Increment `_paren_depth`. |
| `close_paren() -> DisplayState` | Evaluate current token list to get sub-result. Pop parent state from `_paren_stack`. Insert sub-result as a token in the parent expression. Decrement `_paren_depth`. Error if `_paren_depth` is already 0. |
| `get_display_state() -> DisplayState` | Extend parent to include `angle_unit` and `paren_depth`. |

**Implementation notes for trigonometric functions:**

All trig functions follow the same pattern:

```python
def _apply_unary(self, fn_name: str, fn: Callable) -> DisplayState:
    """Apply a unary function to the current display value."""
    if self._error:
        return self.get_display_state()
    try:
        value = float(self._current_input)
        result = fn(value)
        self._current_input = self.format_number(result)
        self._expression = f"{fn_name}({self.format_number(value)})"
        self._new_input = True
    except (ValueError, OverflowError):
        self._error = True
        self._current_input = "Error"
    return self.get_display_state()
```

For trig functions in degree mode, convert the input from degrees to radians
before calling the `math` function:

```python
def trig_sin(self) -> DisplayState:
    value = float(self._current_input)
    if self._angle_unit == AngleUnit.DEG:
        value = math.radians(value)
    result = math.sin(value)
    # ... (handle near-zero rounding, e.g. sin(180 deg) should be exactly 0)
```

**Handling tan(90 degrees):**

`math.tan(math.radians(90))` does not raise an exception in Python -- it
returns a very large number because `math.radians(90)` is not exactly pi/2.
The implementation must detect this case explicitly:

```python
def trig_tan(self) -> DisplayState:
    value = float(self._current_input)
    if self._angle_unit == AngleUnit.DEG:
        # Check if cos(value) would be zero (value is 90, 270, etc.)
        if value % 180 == 90:
            self._error = True
            self._current_input = "Error"
            return self.get_display_state()
        rad = math.radians(value)
    else:
        rad = value
    result = math.tan(rad)
    ...
```

**Implementation notes for parentheses:**

The parenthesis stack saves and restores the expression evaluation context.
This is the trickiest part of the scientific mode.

```
State before "(":
  _tokens = [2.0, "+"]
  _pending_op = "+"
  _current_input = "2"

User presses "(":
  Push {"tokens": [2.0, "+"], "pending_op": "+", "expression": "2 + "} onto stack.
  Reset: _tokens = [], _pending_op = "", _current_input = "0", _new_input = True.
  _paren_depth = 1.

User enters "3 + 4":
  _tokens = [3.0, "+", 4.0]

User presses ")":
  Evaluate inner tokens: 3.0 + 4.0 = 7.0.
  Pop parent state: _tokens = [2.0, "+"], _pending_op = "+".
  Set _current_input = "7".
  The parent's pending_op "+" will be committed when the next operator or "=" is pressed,
  adding 7.0 to the token list.
  _paren_depth = 0.
```

On `evaluate()`, if `_paren_depth > 0`, raise an error for mismatched
parentheses (PA-3, ER-5).

**Implementation notes for `power_n()` (two-operand):**

`power_n` works like a binary operator. It commits the current value, sets
`_pending_op = "**"`, and waits for the second operand. The `input_operator`
and `evaluate` methods in `BasicLogic` must recognize "**" as a valid operator
in the token list. During evaluation pass 1, "**" should be evaluated at the
same pass as `*` and `/` (it binds tighter than `+` and `-`). Alternatively,
add a pass 0 for exponentiation before pass 1.

Recommended: three-pass evaluation when scientific mode is active:
1. Pass 0: resolve `**` (right to left -- exponentiation is right-associative).
2. Pass 1: resolve `*` and `/` (left to right).
3. Pass 2: resolve `+` and `-` (left to right).

Since `ScientificLogic` inherits from `BasicLogic`, override `_evaluate_tokens`
to add the exponentiation pass. `BasicLogic._evaluate_tokens` only needs two
passes because it does not support `**`.

---

### 2.7 `calculator/logic/programmer_logic.py`

**Responsibility:** Integer-only arithmetic in multiple bases with bitwise
operations and word size constraints. Extends `BaseLogic` directly (not
`BasicLogic`).

**Class `ProgrammerLogic(BaseLogic)`:**

Instance attributes (in addition to inherited):
- `_value: int` -- the current integer value (the authoritative representation).
- `_number_base: NumberBase` -- current display base, default `DEC`.
- `_word_size: WordSize` -- current word size, default `BITS_64`.
- `_pending_op: str` -- pending binary operator ("+", "-", "*", "/", "MOD", "AND", "OR", "XOR", "LSH", "RSH").
- `_operand: int` -- the left operand saved when a binary operator was pressed.

Methods:

| Method | Description |
|--------|-------------|
| `set_base(base: NumberBase) -> DisplayState` | Change `_number_base`. Reformat `_current_input` in the new base. |
| `number_base -> NumberBase` (property) | Return current base. |
| `set_word_size(size: WordSize) -> DisplayState` | Change `_word_size`. Apply `_mask_to_word_size` to `_value`. |
| `word_size -> WordSize` (property) | Return current word size. |
| `_mask_to_word_size(value: int) -> int` | Apply two's complement masking (see implementation notes below). |
| `input_digit(digit: str) -> DisplayState` | Override base class. Parse `_current_input` in the current base, append the digit, re-parse, and mask to word size. Reject invalid digits for the current base. |
| `input_decimal() -> DisplayState` | No-op. Return current display state unchanged (PM-3). |
| `input_operator(op: str) -> DisplayState` | If a `_pending_op` exists, evaluate it immediately (left-to-right, no precedence). Save current value as `_operand`, set `_pending_op = op`. |
| `evaluate() -> DisplayState` | Apply `_pending_op` to `_operand` and `_value`. Mask result to word size. |
| `bitwise_and() -> DisplayState` | Equivalent to `input_operator("AND")`. |
| `bitwise_or() -> DisplayState` | Equivalent to `input_operator("OR")`. |
| `bitwise_xor() -> DisplayState` | Equivalent to `input_operator("XOR")`. |
| `bitwise_not() -> DisplayState` | Immediate unary: `_value = _mask_to_word_size(~_value)`. |
| `bitwise_lshift() -> DisplayState` | Equivalent to `input_operator("LSH")`. |
| `bitwise_rshift() -> DisplayState` | Equivalent to `input_operator("RSH")`. |
| `_format_in_base(value: int, base: NumberBase) -> str` | Format integer for display in given base (see notes below). |
| `get_all_bases() -> dict[str, str]` | Return `{"HEX": ..., "DEC": ..., "OCT": ..., "BIN": ...}` for the conversion panel. |
| `get_button_enabled_state() -> ButtonEnabledState` | Return which digit and hex buttons are enabled for current base. |
| `get_current_value() -> float` | Return `float(self._value)`. |
| `set_current_value(value: float) -> DisplayState` | Set `_value = _mask_to_word_size(int(value))`. |
| `get_display_state() -> DisplayState` | Build DisplayState with all programmer-specific fields populated. |

**Implementation notes for two's complement masking:**

This is the most important function in programmer mode. Python integers have
arbitrary precision, so we must explicitly mask values to simulate fixed-width
two's complement.

```python
def _mask_to_word_size(self, value: int) -> int:
    bits = self._word_size.value  # 8, 16, 32, or 64
    mask = (1 << bits) - 1       # e.g. 0xFF for 8-bit

    # Mask to unsigned range
    unsigned = value & mask

    # Convert to signed: if the high bit is set, subtract 2^bits
    if unsigned >= (1 << (bits - 1)):
        return unsigned - (1 << bits)
    return unsigned
```

Examples:
- 8-bit, value=128: `128 & 0xFF = 128`. `128 >= 128`, so `128 - 256 = -128`.
- 8-bit, value=255: `255 & 0xFF = 255`. `255 >= 128`, so `255 - 256 = -1`.
- 8-bit, value=-1: `-1 & 0xFF = 255`. `255 >= 128`, so `255 - 256 = -1`. (Idempotent.)
- 8-bit, value=300: `300 & 0xFF = 44`. `44 < 128`, so result is `44`.

**Implementation notes for base conversion display:**

```python
def _format_in_base(self, value: int, base: NumberBase) -> str:
    # Get unsigned representation for display
    bits = self._word_size.value
    mask = (1 << bits) - 1
    unsigned = value & mask

    if base == NumberBase.DEC:
        return str(value)  # show signed value
    elif base == NumberBase.HEX:
        return format(unsigned, 'X')  # uppercase hex, no prefix
    elif base == NumberBase.OCT:
        return format(unsigned, 'o')  # no prefix
    elif base == NumberBase.BIN:
        raw = format(unsigned, 'b')
        # Pad to multiple of 4 bits for readability
        padded = raw.zfill((len(raw) + 3) // 4 * 4)
        # Group into nibbles separated by spaces
        return ' '.join(padded[i:i+4] for i in range(0, len(padded), 4))
```

Note that HEX, OCT, and BIN display the unsigned representation (so -1 in
8-bit shows as `FF` in hex), while DEC shows the signed value.

**Implementation notes for digit input in different bases:**

When the user types digits, the input string is in the current base. On each
digit press:

```python
def input_digit(self, digit: str) -> DisplayState:
    if self._error:
        self._error = False
        self._current_input = "0"
        self._new_input = True

    digit = digit.upper()
    # Validate digit for current base
    valid_digits = "01" if self._number_base == NumberBase.BIN else \
                   "01234567" if self._number_base == NumberBase.OCT else \
                   "0123456789" if self._number_base == NumberBase.DEC else \
                   "0123456789ABCDEF"
    if digit not in valid_digits:
        return self.get_display_state()

    if self._new_input:
        self._current_input = digit
        self._new_input = False
    else:
        if self._current_input == "0":
            self._current_input = digit
        else:
            self._current_input += digit

    # Parse the input string in the current base to get the int value
    try:
        self._value = int(self._current_input, self._number_base.value)
        self._value = self._mask_to_word_size(self._value)
        # Re-format in current base (handles overflow/wrap)
        self._current_input = self._format_in_base(self._value, self._number_base)
    except ValueError:
        pass

    return self.get_display_state()
```

**Implementation notes for bitwise operator evaluation:**

```python
def _apply_pending_op(self) -> None:
    left = self._operand
    right = self._value
    op = self._pending_op

    if op == "+":
        result = left + right
    elif op == "-":
        result = left - right
    elif op == "*":
        result = left * right
    elif op == "/":
        if right == 0:
            raise ZeroDivisionError
        # Truncating integer division (toward zero), not floor division
        result = int(left / right)  # NOT left // right (which floors)
    elif op == "MOD":
        if right == 0:
            raise ZeroDivisionError
        result = left % right
    elif op == "AND":
        result = left & right
    elif op == "OR":
        result = left | right
    elif op == "XOR":
        result = left ^ right
    elif op == "LSH":
        result = left << right
    elif op == "RSH":
        result = left >> right
    else:
        result = right

    self._value = self._mask_to_word_size(result)
```

Important: integer division must truncate toward zero (`int(a / b)`), not
floor toward negative infinity (`a // b`). For example, `-7 / 2` must produce
`-3`, not `-4`. This matches requirement PM-2.

---

### 2.8 `calculator/gui/__init__.py`

Empty file.

---

### 2.9 `calculator/gui/base_view.py`

**Responsibility:** Shared GUI skeleton -- the display panel and the abstract
button frame.

**Class `BaseView(tk.Frame)`:**

Widgets created in `__init__`:
- `self._expression_label` -- `tk.Label`, right-aligned, smaller font (e.g. 14pt), for the expression line.
- `self._main_label` -- `tk.Label`, right-aligned, large font (e.g. 32pt), for the current number.
- `self._indicator_frame` -- `tk.Frame` containing the memory indicator and mode-specific indicators.
- `self._memory_label` -- `tk.Label` inside `_indicator_frame`, text="M", hidden when memory is empty.
- `self.button_frame` -- `tk.Frame`, empty placeholder for subclasses to populate.

Methods:

| Method | Description |
|--------|-------------|
| `__init__(parent: tk.Widget)` | Create display panel and empty button frame. |
| `update_display(state: DisplayState)` | Set `_main_label` text to `state.main_display`. Set `_expression_label` text to `state.expression_display`. Show/hide memory indicator based on `state.memory_indicator`. Subclasses extend this for mode-specific indicators. |
| `set_callbacks(callbacks: dict[str, Callable])` | Store callbacks dict as `self._callbacks`. |
| `build_buttons()` | Override in subclasses to populate `self.button_frame` using grid layout. |
| `destroy_buttons()` | Destroy all children of `self.button_frame`. |
| `_make_button(parent, text, callback_key, ...)` | Helper to create a styled `tk.Button` wired to `self._callbacks[callback_key]`. Returns the button widget. Supports `columnspan`, `rowspan`, `width`, `bg` color. |

**Styling constants** (defined at module level or as class attributes):
- `FONT_DISPLAY = ("Helvetica", 32)`
- `FONT_EXPRESSION = ("Helvetica", 14)`
- `FONT_BUTTON = ("Helvetica", 16)`
- `FONT_BUTTON_SMALL = ("Helvetica", 13)`
- `COLOR_BG = "#2D2D2D"` (dark background)
- `COLOR_DISPLAY_BG = "#1C1C1C"`
- `COLOR_BTN_NUMBER = "#505050"`
- `COLOR_BTN_OPERATOR = "#FF9F0A"`
- `COLOR_BTN_FUNCTION = "#3A3A3A"`
- `COLOR_TEXT = "#FFFFFF"`

---

### 2.10 `calculator/gui/basic_view.py`

**Responsibility:** Lay out the basic mode buttons in a 5-column, 6-row grid.

**Class `BasicView(BaseView)`:**

Overrides `build_buttons()` to create:

Row 0 (memory): MC, MR, M+, M-, MS
Row 1: C, +/-, %, /
Row 2: 7, 8, 9, *
Row 3: 4, 5, 6, -
Row 4: 1, 2, 3, +
Row 5: 0 (columnspan=2), ., =

Each button maps to a callback key:
- Digits: `"digit_0"` through `"digit_9"`
- Operators: `"op_add"`, `"op_sub"`, `"op_mul"`, `"op_div"`
- Memory: `"memory_clear"`, `"memory_recall"`, `"memory_add"`, `"memory_sub"`, `"memory_store"`
- Actions: `"clear_entry"`, `"clear_all"`, `"sign_toggle"`, `"percent"`, `"evaluate"`, `"backspace"`, `"decimal"`

---

### 2.11 `calculator/gui/scientific_view.py`

**Responsibility:** Lay out the scientific mode buttons in a 9-column, 7-row grid.

**Class `ScientificView(BaseView)`:**

Extends `update_display()` to also render:
- Deg/Rad indicator label.
- Parenthesis depth indicator.

Overrides `build_buttons()` to create the full scientific layout. The left 5
columns hold scientific functions, the right 4 columns hold the basic number
pad and operators, matching the layout in the architecture document.

Additional callback keys:
- Trig: `"trig_sin"`, `"trig_cos"`, `"trig_tan"`, `"trig_asin"`, `"trig_acos"`, `"trig_atan"`
- Log: `"log_base10"`, `"log_natural"`, `"log_base2"`
- Power: `"power_square"`, `"power_cube"`, `"power_n"`, `"power_10x"`, `"power_ex"`
- Root: `"root_square"`, `"root_cube"`
- Other: `"reciprocal"`, `"insert_pi"`, `"insert_e"`, `"factorial"`, `"absolute_value"`, `"toggle_angle"`, `"open_paren"`, `"close_paren"`

---

### 2.12 `calculator/gui/programmer_view.py`

**Responsibility:** Lay out the programmer mode buttons, base conversion panel,
base selector radio buttons, and word size selector.

**Class `ProgrammerView(BaseView)`:**

Overrides `__init__()` to add:
- Conversion panel: a `tk.Frame` with four `tk.Label` widgets showing HEX, DEC, OCT, BIN values.
- Base selector: four `tk.Radiobutton` widgets sharing a `tk.StringVar`.
- Word size selector: an `tk.OptionMenu` or four `tk.Radiobutton` widgets for 8/16/32/64-bit.

Extends `update_display()` to also update:
- Conversion panel labels from `state.hex_value`, `state.dec_value`, `state.oct_value`, `state.bin_value`.
- Base selector highlight from `state.number_base`.
- Word size indicator from `state.word_size`.
- Button enabled/disabled states (hex digits A-F, digit buttons 2-9 based on base).

Overrides `build_buttons()` for the programmer layout. The left 5 columns hold
hex digits and bitwise operators, the right 4 columns hold the number pad and
arithmetic operators.

Additional callback keys:
- Hex digits: `"digit_A"` through `"digit_F"`
- Bitwise: `"bitwise_and"`, `"bitwise_or"`, `"bitwise_xor"`, `"bitwise_not"`, `"bitwise_lsh"`, `"bitwise_rsh"`
- Base: `"set_base_dec"`, `"set_base_hex"`, `"set_base_oct"`, `"set_base_bin"`
- Word size: `"set_word_8"`, `"set_word_16"`, `"set_word_32"`, `"set_word_64"`
- `"modulo"` for the MOD/% operation.

Provides a `set_button_states(state: ButtonEnabledState)` method that the
controller calls after `update_display()` to enable/disable buttons per base.

---

### 2.13 `calculator/app.py`

**Responsibility:** The Controller. Orchestrates mode switching, event routing,
keyboard bindings, and the menu bar.

**Class `CalculatorApp`:**

Instance attributes:
- `_root: tk.Tk` -- the main window.
- `_mode: Mode` -- current calculator mode.
- `_logic: BaseLogic` -- current logic instance (BasicLogic, ScientificLogic, or ProgrammerLogic).
- `_view: BaseView` -- current view instance.
- `_memory: float` -- temporarily held during mode switch (otherwise lives in logic).

Methods:

| Method | Description |
|--------|-------------|
| `__init__(root: tk.Tk)` | Configure root window (title, background). Build menu. Switch to BASIC mode. Bind keyboard. |
| `_build_menu()` | Create a `tk.Menu` bar with a "Mode" menu containing Basic, Scientific, Programmer as radio items. |
| `_switch_mode(new_mode: Mode)` | Full mode switch sequence: save state, destroy old view, create new logic, transfer state, create new view, wire callbacks, resize, refresh. |
| `_resize_window(mode: Mode)` | Set root geometry: Basic=320x480, Scientific=560x520, Programmer=560x580. |
| `_build_callbacks() -> dict` | Build and return the complete callback dictionary for the current mode. Uses lambdas and bound methods. Includes mode-specific callbacks only when in the appropriate mode. |
| `_refresh_display()` | Get DisplayState from logic, push to view. For programmer mode, also update button enabled states. |
| `_safe_call(fn, *args)` | Try/except wrapper. On any exception, set error state. Always refresh display afterward. |
| `_on_digit(digit: str)` | Call `_safe_call(self._logic.input_digit, digit)`. |
| `_on_operator(op: str)` | Call `_safe_call(self._logic.input_operator, op)`. |
| `_on_evaluate()` | Call `_safe_call(self._logic.evaluate)`. |
| `_on_clear_entry()` | Call `_safe_call(self._logic.clear_entry)`. |
| `_on_clear_all()` | Call `_safe_call(self._logic.clear_all)`. |
| `_on_backspace()` | Call `_safe_call(self._logic.input_backspace)`. |
| `_on_decimal()` | Call `_safe_call(self._logic.input_decimal)`. |
| `_on_sign_toggle()` | Call `_safe_call(self._logic.input_sign_toggle)`. |
| `_on_percent()` | Check mode is not PROGRAMMER, then call `_safe_call(self._logic.input_percent)`. |
| `_on_memory_*()`  | Six methods: clear, recall, add, subtract, store. Each delegates to logic. |
| `_on_trig(fn_name)` | Check mode is SCIENTIFIC, dispatch to the matching logic method. |
| `_on_bitwise(op)` | Check mode is PROGRAMMER, dispatch to the matching logic method. |
| `_on_open_paren()` | Check mode is SCIENTIFIC, call `self._logic.open_paren()`. |
| `_on_close_paren()` | Check mode is SCIENTIFIC, call `self._logic.close_paren()`. |
| `_bind_keyboard()` | Bind all keys as described in architecture section 6.2. All bindings are on `self._root`. |

---

### 2.14 `main.py`

**Responsibility:** Entry point for the application.

```python
import tkinter as tk
from calculator.app import CalculatorApp


def main() -> None:
    root = tk.Tk()
    root.title("Calculator")
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
```

---

### 2.15 `tests/__init__.py`

Empty file.

---

### 2.16 `tests/test_basic.py`

**Covers:** `BasicLogic` -- arithmetic, operator precedence, chaining, percent,
display formatting, clear/backspace, numeric input edge cases.

**Test categories:**

1. Simple arithmetic: `2+3=5`, `10-3=7`, `4*5=20`, `10/4=2.5`.
2. Operator precedence: `2+3*4=14`, `10-2*3=4`, `2*3+4*5=26`.
3. Division by zero: `5/0=Error`.
4. Chained operations: `1+2+3=6`, `10-3-2=5`.
5. Percent: `200%=2`, `50%=0.5`.
6. Sign toggle: `5 -> -5 -> 5`.
7. Decimal input: `0.5`, double-dot prevention, leading zero removal.
8. Clear entry vs all clear behavior.
9. Backspace behavior.
10. Display formatting: integers without ".0", scientific notation for large values.
11. Edge case: pressing `=` with no expression.
12. Edge case: pressing operator with no first operand.
13. Consecutive operator replacement: `5 + - 3 = 2`.

Use `pytest.mark.parametrize` for operations with multiple input/output pairs
(requirement TS-11).

---

### 2.17 `tests/test_scientific.py`

**Covers:** `ScientificLogic` -- trig, log, power, root, factorial, constants,
parentheses, absolute value.

**Test categories:**

1. Trig in degree mode: `sin(0)=0`, `sin(90)=1`, `cos(0)=1`, `cos(90)=0`, `tan(45)=1`.
2. Trig in radian mode: `sin(pi)~0`, `cos(pi)=-1`.
3. Trig errors: `tan(90)=Error`, `asin(2)=Error`, `acos(2)=Error`.
4. Inverse trig: `asin(1)=90` (deg), `atan(1)=45` (deg).
5. Logarithms: `log(100)=2`, `ln(e)=1`, `log2(256)=8`.
6. Log errors: `log(0)=Error`, `log(-1)=Error`, `ln(0)=Error`.
7. Powers: `5 x^2=25`, `2 x^3=8`, `2 x^n 10=1024`, `10^x(3)=1000`, `e^x(1)~2.71828`.
8. Roots: `sqrt(144)=12`, `cbrt(27)=3`, `sqrt(-1)=Error`.
9. Reciprocal: `1/x(4)=0.25`, `1/x(0)=Error`.
10. Factorial: `5!=120`, `0!=1`, `(-3)!=Error`, `3.5!=Error`.
11. Absolute value: `abs(-7)=7`, `abs(5)=5`.
12. Constants: pi inserts 3.14159..., e inserts 2.71828....
13. Parentheses: `(2+3)*4=20`, `2*(3+4)=14`, nested parens, mismatched paren error.
14. Angle mode toggle: verify DEG/RAD switching.

---

### 2.18 `tests/test_programmer.py`

**Covers:** `ProgrammerLogic` -- base conversion, bitwise operations, word size,
integer arithmetic.

**Test categories:**

1. Base conversion: 255 in DEC = FF in HEX = 377 in OCT = 11111111 in BIN.
2. Base switching preserves value.
3. Digit input in each base (valid and invalid digits rejected).
4. Integer arithmetic: `7/2=3`, `7%2=1`, `10+5=15`, `10-3=7`, `3*4=12`.
5. Bitwise AND: `12 AND 10=8`.
6. Bitwise OR: `12 OR 10=14`.
7. Bitwise XOR: `12 XOR 10=6`.
8. Bitwise NOT: `NOT 0` in 8-bit = `-1`.
9. Left shift: `1 LSH 4=16`.
10. Right shift: `16 RSH 2=4`.
11. Word size 8-bit overflow: `127+1=-128`.
12. Word size switching truncation: 64-bit value 300, switch to 8-bit, get 44.
13. Two's complement: negative values display correctly in all bases.
14. Decimal point disabled (returns unchanged state).
15. Button enabled states per base.
16. `get_all_bases()` returns all four representations.
17. Division by zero: `5/0=Error`.

---

### 2.19 `tests/test_memory.py`

**Covers:** Memory operations on `BasicLogic` (which inherits memory from
`BaseLogic`).

**Test categories:**

1. MS stores value, MR recalls it.
2. MC clears memory, indicator disappears.
3. M+ adds to memory: store 5, add 3, recall = 8.
4. M- subtracts from memory: store 10, subtract 3, recall = 7.
5. Memory indicator true when nonzero, false when zero.
6. Memory recall sets `_new_input` so next digit replaces.
7. Memory operations work on `ScientificLogic` (inherited).
8. Memory operations work on `ProgrammerLogic` (stores as float, recalls as int).

---

### 2.20 `tests/test_mode_switch.py`

**Covers:** Mode switching logic at the logic-layer level (no GUI). Tests
simulate what the Controller does: read value from old logic, create new logic,
transfer state.

**Test categories:**

1. Basic to Scientific: float value preserved.
2. Scientific to Basic: float value preserved.
3. Basic (3.14) to Programmer: truncated to 3.
4. Programmer (FF hex = 255) to Basic: displays 255.
5. Memory preserved across all mode switches.
6. Expression and pending ops are discarded on switch.
7. Programmer to Programmer (same mode): value unchanged.

---

## 3. Module Dependency Graph

```
calculator/logic/base_logic.py        (no dependencies, pure Python + stdlib)
    |
    +---> calculator/logic/basic_logic.py      (imports base_logic)
    |         |
    |         +---> calculator/logic/scientific_logic.py  (imports basic_logic, base_logic)
    |
    +---> calculator/logic/programmer_logic.py  (imports base_logic)

calculator/gui/base_view.py           (imports tkinter only)
    |
    +---> calculator/gui/basic_view.py         (imports base_view)
    +---> calculator/gui/scientific_view.py    (imports base_view)
    +---> calculator/gui/programmer_view.py    (imports base_view)

calculator/app.py                     (imports all logic modules, all gui modules)

main.py                               (imports calculator.app)
```

Key points:
- Logic modules never import GUI modules.
- GUI modules never import logic modules (they receive `DisplayState` objects via the controller).
- `app.py` is the only module that bridges both layers.
- `scientific_logic.py` imports `basic_logic.py` (inheritance).
- `programmer_logic.py` imports `base_logic.py` only (no inheritance from `BasicLogic`).

---

## 4. Implementation Notes for Tricky Parts

### 4.1 Expression Evaluation with Precedence (BasicLogic)

The two-pass token evaluation algorithm is the core of the basic calculator.
Pitfalls to watch for:

- **Token list must alternate number-operator-number.** If the user presses
  `+ + 3`, the second `+` should replace the first, not create a malformed
  list.
- **Empty token list.** Pressing `=` with no expression should display the
  current value unchanged.
- **Single operand with operator.** Pressing `5 + =` should compute `5 + 5 = 10`
  (repeating the first operand as the second).
- **Chained equals.** Pressing `= = =` after `2 + 3 =` should repeat the last
  operation: `5 + 3 = 8`, `8 + 3 = 11`, etc. Store the last operator and
  operand for repeat evaluation.

### 4.2 Two's Complement and Word Size (ProgrammerLogic)

- Python integers are arbitrary precision, so all masking must be explicit.
- The `_mask_to_word_size` method must be called after every arithmetic or
  bitwise operation, and after every digit input.
- When switching word size from larger to smaller, the value must be masked to
  the new size. This can change the sign.
- When displaying negative numbers in HEX/OCT/BIN, display the unsigned
  bit pattern (e.g., -1 in 8-bit = FF in hex). When displaying in DEC, show
  the signed value (-1).
- Arithmetic right shift (`>>` in Python) already performs sign extension for
  negative numbers, which is correct for two's complement.

### 4.3 Base Conversion Input Parsing (ProgrammerLogic)

- The `_current_input` string is always in the current base's representation.
- When the base changes, `_current_input` must be reformatted from the
  internal `_value` in the new base.
- Parsing input: use `int(self._current_input, base)` where base is 2, 8, 10,
  or 16.
- When building the input string digit-by-digit, always re-parse and re-mask
  after each digit to catch overflow immediately.

### 4.4 Parenthesized Expressions (ScientificLogic)

- The parenthesis stack must save the complete evaluation context: the token
  list, the pending operator, and the expression string.
- Nested parentheses work recursively: `((2+3)*(4+1))` pushes twice, pops twice.
- If the user presses `=` while parentheses are still open (`_paren_depth > 0`),
  display an error for mismatched parentheses.
- The close-paren operation evaluates the inner expression and injects the
  result as a single number token into the parent context.

### 4.5 Trigonometric Edge Cases (ScientificLogic)

- `sin(180)` in degree mode should return exactly 0, but `math.sin(math.radians(180))`
  returns a tiny nonzero value (~1.2e-16). Round results that are very close
  to 0 or 1 to those exact values when the input is a "clean" degree value.
  A simple approach: if `abs(result) < 1e-15`, treat as 0.
- `tan(90)` in degree mode: detect by checking if the input modulo 180 equals 90.
  Do not rely on the math library to produce an error; it produces a large float
  instead.
- Inverse trig functions in degree mode: compute in radians, then convert the
  result to degrees with `math.degrees()`.

### 4.6 Factorial Limits (ScientificLogic)

- `math.factorial(n)` returns an exact integer, but converting to float overflows
  past n=170 (since `float` maxes out around 1.8e308).
- For n > 170, either catch the `OverflowError` when converting to float, or
  check the limit before computing.
- For n=0, the result is 1. This is a common edge case to test.

### 4.7 Display Formatting (BaseLogic)

- Use Python's `g` format specifier with 10 significant digits: `f"{value:.10g}"`.
- This automatically strips trailing zeros and switches to scientific notation
  for extreme values.
- Special case: if `value == int(value)` and the value fits in a reasonable
  range, display as `str(int(value))` to avoid any decimal point.
- Watch for `-0.0`: format as `"0"`, not `"-0"`.

### 4.8 Integer Division Toward Zero (ProgrammerLogic)

Python's `//` operator floors toward negative infinity, which is wrong for this
application. Use `int(a / b)` which truncates toward zero.

- `-7 // 2` in Python = `-4` (floor division). Wrong.
- `int(-7 / 2)` in Python = `-3` (truncation toward zero). Correct.

### 4.9 Mode Switch Value Transfer (app.py)

When switching from Scientific to Programmer, the current value might be in the
middle of an expression (e.g., `2 + 3 *` with display showing `3`). The value
to transfer is the current display value (`3`), not the pending expression
result. The expression is discarded. This means `get_current_value()` returns
the current display/input value, not an evaluated result.
