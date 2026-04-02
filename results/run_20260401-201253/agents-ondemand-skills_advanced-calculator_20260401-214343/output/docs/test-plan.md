# Advanced Calculator -- Test Plan

**Version:** 1.0
**Date:** 2026-04-01
**Based on:** requirements.md v1.0, architecture.md v1.0

---

## 1. Test Strategy

### 1.1 Scope

All tests target the **logic layer only** (`calculator/logic/`). No test
instantiates a Tkinter window, widget, or root object. Each test creates a
logic class instance directly (`BasicLogic`, `ScientificLogic`,
`ProgrammerLogic`), calls its public methods, and asserts on the returned
`DisplayState` dataclass.

### 1.2 Framework and Tooling

- **Framework:** pytest (the only external dependency; listed in
  `requirements.txt`).
- **Runner command:** `python3 -m pytest` from the project root.
- **Parametrized tests:** Operations with multiple input/output pairs use
  `pytest.mark.parametrize` to avoid duplicated test functions. Each
  parametrized combination runs as an independent test.

### 1.3 Test Independence

Every test must be **fully independent**. No shared mutable state between tests.
Each test function creates its own fresh logic instance. No module-level
fixtures mutate state. No test depends on the execution order of any other test.

### 1.4 Assertion Style

Tests assert on fields of the `DisplayState` object returned by logic methods:

```python
def test_example():
    logic = BasicLogic()
    logic.input_digit("2")
    logic.input_operator("+")
    logic.input_digit("3")
    state = logic.evaluate()
    assert state.main_display == "5"
    assert state.error is False
```

For floating-point comparisons where exact equality is inappropriate (e.g.,
trigonometric results), tests use `pytest.approx` or parse `state.main_display`
as a float and compare with a tolerance.

### 1.5 Test File Organization

| Test File               | Logic Class Under Test | Req. Section |
|-------------------------|------------------------|--------------|
| `tests/test_basic.py`       | `BasicLogic`           | 3 (Basic Mode) |
| `tests/test_scientific.py`  | `ScientificLogic`      | 4 (Scientific Mode) |
| `tests/test_programmer.py`  | `ProgrammerLogic`      | 5 (Programmer Mode) |
| `tests/test_memory.py`      | All logic classes      | 3.3 (Memory Functions) |
| `tests/test_mode_switch.py` | All logic classes      | 2.1 (Mode Switching) |

---

## 2. Basic Mode Tests (`tests/test_basic.py`)

All tests in this file instantiate `BasicLogic` directly.

### 2.1 Happy Path -- Arithmetic Operations

These tests verify requirements BA-1 through BA-6.

| Test ID | Description | Input Sequence | Expected `main_display` |
|---------|-------------|----------------|-------------------------|
| BA-HP-01 | Simple addition | `2`, `+`, `3`, `=` | `"5"` |
| BA-HP-02 | Simple subtraction | `1`, `0`, `-`, `3`, `=` | `"7"` |
| BA-HP-03 | Simple multiplication | `4`, `*`, `5`, `=` | `"20"` |
| BA-HP-04 | Simple division | `1`, `0`, `/`, `4`, `=` | `"2.5"` |
| BA-HP-05 | Integer division result | `4`, `/`, `2`, `=` | `"2"` (not `"2.0"`) |
| BA-HP-06 | Operator precedence | `2`, `+`, `3`, `*`, `4`, `=` | `"14"` |
| BA-HP-07 | Chained addition | `1`, `+`, `2`, `+`, `3`, `=` | `"6"` |
| BA-HP-08 | Multi-operand mixed | `1`, `0`, `+`, `2`, `*`, `3`, `-`, `1`, `=` | `"15"` |

**Note:** Use `pytest.mark.parametrize` for BA-HP-01 through BA-HP-05 (simple
two-operand arithmetic with multiple input/output pairs).

### 2.2 Happy Path -- Numeric Input

These tests verify requirements NI-1 through NI-6.

| Test ID | Description | Input Sequence | Expected `main_display` |
|---------|-------------|----------------|-------------------------|
| NI-HP-01 | Single digit | `7` | `"7"` |
| NI-HP-02 | Multi-digit number | `1`, `2`, `3` | `"123"` |
| NI-HP-03 | Decimal number | `3`, `.`, `1`, `4` | `"3.14"` |
| NI-HP-04 | Sign toggle positive to negative | `5`, `+/-` | `"-5"` |
| NI-HP-05 | Sign toggle negative to positive | `5`, `+/-`, `+/-` | `"5"` |
| NI-HP-06 | Percentage | `2`, `0`, `0`, `%` | `"2"` |

### 2.3 Happy Path -- Display Formatting

These tests verify requirements DI-1 through DI-5.

| Test ID | Description | Input Sequence | Expected `main_display` |
|---------|-------------|----------------|-------------------------|
| DI-HP-01 | Integer displays without decimal | `4`, `/`, `2`, `=` | `"2"` |
| DI-HP-02 | Repeating decimal precision | `1`, `/`, `3`, `=` | `"0.3333333333"` (10 digits) |
| DI-HP-03 | Large number scientific notation | `9999999999`, `*`, `9999999999`, `=` | Scientific notation string |

### 2.4 Happy Path -- Clear and Edit

These tests verify requirements CE-1 through CE-3.

| Test ID | Description | Input Sequence | Expected `main_display` |
|---------|-------------|----------------|-------------------------|
| CE-HP-01 | Clear entry preserves operation | `5`, `+`, `3`, `C`, `2`, `=` | `"7"` |
| CE-HP-02 | All clear resets everything | `5`, `+`, `3`, `AC`, `2`, `=` | `"2"` |
| CE-HP-03 | Backspace removes last digit | `1`, `2`, `3`, `Backspace` | `"12"` |

### 2.5 Edge Cases

| Test ID | Description | Input Sequence | Expected `main_display` |
|---------|-------------|----------------|-------------------------|
| BA-EC-01 | Leading zeros suppressed | `0`, `0`, `7` | `"7"` |
| BA-EC-02 | Double decimal ignored | `.`, `.`, `5` | `"0.5"` |
| BA-EC-03 | Operator with no second operand then equals | `5`, `+`, `=` | Defined behavior (not crash) |
| BA-EC-04 | Multiple equals presses | `2`, `+`, `3`, `=`, `=` | Defined behavior (not crash) |
| BA-EC-05 | Sign toggle on zero | `0`, `+/-` | `"0"` or `"-0"` (no crash) |
| BA-EC-06 | Backspace to empty | `5`, `Backspace` | `"0"` |
| BA-EC-07 | Backspace on multi-digit | `1`, `0`, `0`, `Backspace`, `Backspace` | `"1"` |
| BA-EC-08 | Percentage of zero | `0`, `%` | `"0"` |
| BA-EC-09 | Very large result | Multiply large numbers | Scientific notation, no crash |
| BA-EC-10 | Very small result | `1`, `/`, very large number, `=` | Near-zero, no crash |

### 2.6 Error Cases

| Test ID | Description | Input Sequence | Expected |
|---------|-------------|----------------|----------|
| BA-ER-01 | Division by zero | `1`, `0`, `0`, `/`, `0`, `=` | `error is True`, `main_display == "Error"` |
| BA-ER-02 | Error recovery with digit | (trigger error), then `5` | `error is False`, `main_display == "5"` |
| BA-ER-03 | Error recovery with clear | (trigger error), then `C` | `error is False`, `main_display == "0"` |
| BA-ER-04 | Error recovery with all clear | (trigger error), then `AC` | `error is False`, `main_display == "0"` |

---

## 3. Scientific Mode Tests (`tests/test_scientific.py`)

All tests in this file instantiate `ScientificLogic` directly. Scientific mode
inherits from `BasicLogic`, so all basic arithmetic works. These tests focus on
the scientific-specific functions.

### 3.1 Happy Path -- Trigonometric Functions

These tests verify requirements TR-1 through TR-6.

**Use `pytest.mark.parametrize` for the following sets.**

#### Degree Mode

| Test ID | Description | Method Call | Expected `main_display` |
|---------|-------------|-------------|-------------------------|
| TR-HP-01 | sin(0) degrees | set 0, `trig_sin()` | `"0"` |
| TR-HP-02 | sin(90) degrees | set 90, `trig_sin()` | `"1"` |
| TR-HP-03 | sin(30) degrees | set 30, `trig_sin()` | `"0.5"` |
| TR-HP-04 | cos(0) degrees | set 0, `trig_cos()` | `"1"` |
| TR-HP-05 | cos(60) degrees | set 60, `trig_cos()` | `"0.5"` |
| TR-HP-06 | tan(45) degrees | set 45, `trig_tan()` | `"1"` |
| TR-HP-07 | asin(1) degrees | set 1, `trig_asin()` | `"90"` |
| TR-HP-08 | acos(0.5) degrees | set 0.5, `trig_acos()` | `"60"` |
| TR-HP-09 | atan(1) degrees | set 1, `trig_atan()` | `"45"` |

#### Radian Mode

| Test ID | Description | Method Call | Expected |
|---------|-------------|-------------|----------|
| TR-HP-10 | sin(pi) radians | toggle to RAD, set pi, `trig_sin()` | approximately `"0"` |
| TR-HP-11 | cos(0) radians | toggle to RAD, set 0, `trig_cos()` | `"1"` |

### 3.2 Happy Path -- Logarithmic Functions

These tests verify requirements LG-1 through LG-3.

**Use `pytest.mark.parametrize` for these input/output pairs.**

| Test ID | Description | Method Call | Expected `main_display` |
|---------|-------------|-------------|-------------------------|
| LG-HP-01 | log10(100) | set 100, `log_base10()` | `"2"` |
| LG-HP-02 | log10(1000) | set 1000, `log_base10()` | `"3"` |
| LG-HP-03 | ln(e) | set e (~2.71828), `log_natural()` | `"1"` |
| LG-HP-04 | log2(256) | set 256, `log_base2()` | `"8"` |
| LG-HP-05 | log2(1) | set 1, `log_base2()` | `"0"` |

### 3.3 Happy Path -- Power and Root Functions

These tests verify requirements PW-1 through PW-8.

**Use `pytest.mark.parametrize` for the unary operations.**

| Test ID | Description | Method Call | Expected `main_display` |
|---------|-------------|-------------|-------------------------|
| PW-HP-01 | 5 squared | set 5, `power_square()` | `"25"` |
| PW-HP-02 | 3 cubed | set 3, `power_cube()` | `"27"` |
| PW-HP-03 | 2^10 | set 2, `power_n()`, input 10, `evaluate()` | `"1024"` |
| PW-HP-04 | 10^3 | set 3, `power_10x()` | `"1000"` |
| PW-HP-05 | e^1 | set 1, `power_ex()` | approximately `"2.71828..."` |
| PW-HP-06 | sqrt(144) | set 144, `root_square()` | `"12"` |
| PW-HP-07 | cbrt(27) | set 27, `root_cube()` | `"3"` |
| PW-HP-08 | 1/4 reciprocal | set 4, `reciprocal()` | `"0.25"` |

### 3.4 Happy Path -- Constants

These tests verify requirements CO-1 and CO-2.

| Test ID | Description | Method Call | Expected |
|---------|-------------|-------------|----------|
| CO-HP-01 | Insert pi | `insert_pi()` | `main_display` starts with `"3.14159265"` |
| CO-HP-02 | Insert e | `insert_e()` | `main_display` starts with `"2.71828182"` |
| CO-HP-03 | e^e | `insert_e()`, `power_ex()` | approximately `"15.1542622414"` |

### 3.5 Happy Path -- Factorial and Absolute Value

These tests verify requirements FA-1, FA-2, FA-3, FA-4.

**Use `pytest.mark.parametrize` for factorial happy-path values.**

| Test ID | Description | Method Call | Expected `main_display` |
|---------|-------------|-------------|-------------------------|
| FA-HP-01 | 5! | set 5, `factorial()` | `"120"` |
| FA-HP-02 | 0! | set 0, `factorial()` | `"1"` |
| FA-HP-03 | 1! | set 1, `factorial()` | `"1"` |
| FA-HP-04 | 10! | set 10, `factorial()` | `"3628800"` |
| FA-HP-05 | abs(-7) | set -7, `absolute_value()` | `"7"` |
| FA-HP-06 | abs(7) | set 7, `absolute_value()` | `"7"` |
| FA-HP-07 | abs(0) | set 0, `absolute_value()` | `"0"` |

### 3.6 Happy Path -- Parentheses

These tests verify requirements PA-1 through PA-3.

| Test ID | Description | Input Sequence | Expected `main_display` |
|---------|-------------|----------------|-------------------------|
| PA-HP-01 | (2+3)*4 | `(`, `2`, `+`, `3`, `)`, `*`, `4`, `=` | `"20"` |
| PA-HP-02 | 2*(3+4) | `2`, `*`, `(`, `3`, `+`, `4`, `)`, `=` | `"14"` |
| PA-HP-03 | Nested parens | `(`, `(`, `2`, `+`, `3`, `)`, `*`, `(`, `4`, `+`, `1`, `)`, `)`, `=` | `"25"` |

### 3.7 Happy Path -- Angle Unit Toggle

| Test ID | Description | Expected |
|---------|-------------|----------|
| TR-HP-20 | Default is DEG | `state.angle_unit == AngleUnit.DEG` |
| TR-HP-21 | Toggle to RAD | After `toggle_angle_unit()`, `state.angle_unit == AngleUnit.RAD` |
| TR-HP-22 | Toggle back to DEG | After two toggles, `state.angle_unit == AngleUnit.DEG` |
| TR-HP-23 | Toggle does not change display value | Set 45, toggle, display still shows `"45"` |

### 3.8 Edge Cases

| Test ID | Description | Input | Expected |
|---------|-------------|-------|----------|
| SC-EC-01 | sin(360) degrees | set 360, `trig_sin()` | approximately `"0"` |
| SC-EC-02 | cos(360) degrees | set 360, `trig_cos()` | approximately `"1"` |
| SC-EC-03 | Large factorial (170!) | set 170, `factorial()` | Valid result (no crash), potentially scientific notation |
| SC-EC-04 | Factorial at float boundary | set 170, `factorial()` | No overflow crash |
| SC-EC-05 | Nested parentheses depth | Three levels of nesting | Correct result |
| SC-EC-06 | Empty parentheses | `(`, `)` | Defined behavior (not crash) |
| SC-EC-07 | Square of negative | set -5, `power_square()` | `"25"` |
| SC-EC-08 | Cube of negative | set -3, `power_cube()` | `"-27"` |
| SC-EC-09 | Reciprocal of 1 | set 1, `reciprocal()` | `"1"` |
| SC-EC-10 | Reciprocal of -1 | set -1, `reciprocal()` | `"-1"` |
| SC-EC-11 | log10(1) | set 1, `log_base10()` | `"0"` |
| SC-EC-12 | cbrt(-8) | set -8, `root_cube()` | `"-2"` |

### 3.9 Error Cases

| Test ID | Description | Input | Expected |
|---------|-------------|-------|----------|
| SC-ER-01 | sqrt(-1) | set -1, `root_square()` | `error is True`, `main_display == "Error"` |
| SC-ER-02 | log(0) | set 0, `log_base10()` | `error is True`, `main_display == "Error"` |
| SC-ER-03 | log(-1) | set -1, `log_base10()` | `error is True`, `main_display == "Error"` |
| SC-ER-04 | ln(0) | set 0, `log_natural()` | `error is True`, `main_display == "Error"` |
| SC-ER-05 | ln(-1) | set -1, `log_natural()` | `error is True`, `main_display == "Error"` |
| SC-ER-06 | log2(0) | set 0, `log_base2()` | `error is True`, `main_display == "Error"` |
| SC-ER-07 | log2(-1) | set -1, `log_base2()` | `error is True`, `main_display == "Error"` |
| SC-ER-08 | tan(90) degrees | set 90, `trig_tan()` | `error is True`, `main_display == "Error"` |
| SC-ER-09 | asin(2) out of domain | set 2, `trig_asin()` | `error is True`, `main_display == "Error"` |
| SC-ER-10 | acos(2) out of domain | set 2, `trig_acos()` | `error is True`, `main_display == "Error"` |
| SC-ER-11 | Factorial of negative | set -3, `factorial()` | `error is True`, `main_display == "Error"` |
| SC-ER-12 | Factorial of non-integer | set 3.5, `factorial()` | `error is True`, `main_display == "Error"` |
| SC-ER-13 | Reciprocal of zero | set 0, `reciprocal()` | `error is True`, `main_display == "Error"` |
| SC-ER-14 | Mismatched parentheses | `(`, `2`, `+`, `3`, `=` | `error is True`, `main_display == "Error"` |

**Note:** Use `pytest.mark.parametrize` for SC-ER-01 through SC-ER-07 (log/root
error cases share the same assertion pattern).

---

## 4. Programmer Mode Tests (`tests/test_programmer.py`)

All tests in this file instantiate `ProgrammerLogic` directly.

### 4.1 Happy Path -- Number Base Conversion

These tests verify requirements NB-1 through NB-7.

| Test ID | Description | Setup | Expected |
|---------|-------------|-------|----------|
| NB-HP-01 | DEC 255 to HEX | Input `255` in DEC, `set_base(HEX)` | `main_display == "FF"` |
| NB-HP-02 | HEX FF to DEC | Set base HEX, input `F`, `F`, `set_base(DEC)` | `main_display == "255"` |
| NB-HP-03 | HEX FF to BIN | Set base HEX, input `F`, `F`, `set_base(BIN)` | `main_display == "11111111"` |
| NB-HP-04 | DEC 255 to OCT | Input `255` in DEC, `set_base(OCT)` | `main_display == "377"` |
| NB-HP-05 | BIN 1010 to DEC | Set base BIN, input `1`,`0`,`1`,`0`, `set_base(DEC)` | `main_display == "10"` |
| NB-HP-06 | All bases panel | Input `255` in DEC, `get_all_bases()` | `{"HEX": "FF", "DEC": "255", "OCT": "377", "BIN": "11111111"}` |

**Use `pytest.mark.parametrize` for base conversion pairs.**

### 4.2 Happy Path -- Integer Arithmetic

These tests verify requirements PM-1 through PM-4.

| Test ID | Description | Input Sequence | Expected `main_display` |
|---------|-------------|----------------|-------------------------|
| PM-HP-01 | Integer addition | `5`, `+`, `3`, `=` | `"8"` |
| PM-HP-02 | Integer subtraction | `1`, `0`, `-`, `3`, `=` | `"7"` |
| PM-HP-03 | Integer multiplication | `4`, `*`, `5`, `=` | `"20"` |
| PM-HP-04 | Integer division (truncating) | `7`, `/`, `2`, `=` | `"3"` |
| PM-HP-05 | Modulo | `7`, `MOD`, `2`, `=` | `"1"` |
| PM-HP-06 | Decimal point is no-op | `input_decimal()` | No change (PM-3) |

### 4.3 Happy Path -- Bitwise Operations

These tests verify requirements BW-1 through BW-6.

**Use `pytest.mark.parametrize` for the binary bitwise operations.**

| Test ID | Description | Input Sequence | Expected `main_display` |
|---------|-------------|----------------|-------------------------|
| BW-HP-01 | 12 AND 10 | `12`, `AND`, `10`, `=` | `"8"` |
| BW-HP-02 | 12 OR 10 | `12`, `OR`, `10`, `=` | `"14"` |
| BW-HP-03 | 12 XOR 10 | `12`, `XOR`, `10`, `=` | `"6"` |
| BW-HP-04 | NOT 0 (8-bit) | Set 8-bit word, `0`, `NOT` | `"-1"` |
| BW-HP-05 | 1 LSH 4 | `1`, `LSH`, `4`, `=` | `"16"` |
| BW-HP-06 | 16 RSH 2 | `16`, `RSH`, `2`, `=` | `"4"` |

### 4.4 Happy Path -- Word Size

These tests verify requirements WS-1 through WS-3.

| Test ID | Description | Setup | Expected |
|---------|-------------|-------|----------|
| WS-HP-01 | Default word size is 64-bit | Fresh instance | `word_size == WordSize.BITS_64` |
| WS-HP-02 | Set 8-bit word size | `set_word_size(BITS_8)` | `word_size == WordSize.BITS_8` |
| WS-HP-03 | 8-bit overflow wraps | 8-bit, set 127, `+`, `1`, `=` | `main_display == "-128"` |
| WS-HP-04 | 8-bit negative overflow wraps | 8-bit, set -128, `-`, `1`, `=` | `main_display == "127"` |
| WS-HP-05 | Truncate on word size reduction | 64-bit value 300, `set_word_size(BITS_8)` | `main_display == "44"` |

### 4.5 Happy Path -- Button Enabled State

These tests verify requirement NB-8.

| Test ID | Description | Base | Expected |
|---------|-------------|------|----------|
| BN-HP-01 | BIN mode buttons | BIN | Only `0`, `1` enabled |
| BN-HP-02 | OCT mode buttons | OCT | Only `0`-`7` enabled |
| BN-HP-03 | DEC mode buttons | DEC | Only `0`-`9` enabled |
| BN-HP-04 | HEX mode buttons | HEX | `0`-`9` and `A`-`F` enabled |
| BN-HP-05 | Decimal point disabled | Any | `decimal_point is False` |

**Use `pytest.mark.parametrize` across the four base modes.**

### 4.6 Edge Cases

| Test ID | Description | Setup | Expected |
|---------|-------------|-------|----------|
| PM-EC-01 | HEX digits uppercase | HEX mode, input `a` (lowercase) | Stored/displayed as uppercase `"A"` |
| PM-EC-02 | Zero in all bases | Set 0 | HEX `"0"`, DEC `"0"`, OCT `"0"`, BIN `"0"` |
| PM-EC-03 | NOT NOT cancels | 8-bit, `5`, `NOT`, `NOT` | `main_display == "5"` |
| PM-EC-04 | Max positive 8-bit | 8-bit, input `127` | `main_display == "127"` |
| PM-EC-05 | Max negative 8-bit | 8-bit, input `-128` | `main_display == "-128"` |
| PM-EC-06 | Left shift to overflow | 8-bit, `1`, `LSH`, `8`, `=` | Wraps to `"0"` (or defined behavior) |
| PM-EC-07 | Right shift negative | 8-bit, `-1`, `RSH`, `1`, `=` | `"-1"` (arithmetic shift preserves sign) |
| PM-EC-08 | Word size increase | 8-bit value -1, switch to 16-bit | Value preserved as -1 or extended (defined behavior) |
| PM-EC-09 | Division truncates toward zero | `-7`, `/`, `2`, `=` | `"-3"` (truncating, not floor) |
| PM-EC-10 | Base conversion of negative | 8-bit, -1 in DEC, switch to HEX | `"FF"` |

### 4.7 Error Cases

| Test ID | Description | Input Sequence | Expected |
|---------|-------------|----------------|----------|
| PM-ER-01 | Integer division by zero | `1`, `0`, `/`, `0`, `=` | `error is True`, `main_display == "Error"` |
| PM-ER-02 | Modulo by zero | `1`, `0`, `MOD`, `0`, `=` | `error is True`, `main_display == "Error"` |
| PM-ER-03 | Error recovery with digit | (trigger error), then `5` | `error is False` |

---

## 5. Memory Function Tests (`tests/test_memory.py`)

Memory tests verify requirements MF-1 through MF-7. These tests use
`BasicLogic` as the primary test class (since memory is defined in `BaseLogic`
and inherited by all modes). Cross-mode memory persistence is tested in
section 6.

### 5.1 Happy Path

| Test ID | Description | Input Sequence | Expected |
|---------|-------------|----------------|----------|
| MF-HP-01 | Memory store and recall | `5`, `MS`, `MR` | `main_display == "5"`, `memory_indicator is True` |
| MF-HP-02 | Memory add | `5`, `MS`, `3`, `M+`, `MR` | `main_display == "8"` |
| MF-HP-03 | Memory subtract | `1`, `0`, `MS`, `3`, `M-`, `MR` | `main_display == "7"` |
| MF-HP-04 | Memory clear | `5`, `MS`, `MC` | `memory_indicator is False` |
| MF-HP-05 | Memory recall after clear | `5`, `MS`, `MC`, `MR` | `main_display == "0"` |
| MF-HP-06 | Memory indicator appears | `5`, `MS` | `memory_indicator is True` |
| MF-HP-07 | Memory indicator absent initially | Fresh instance | `memory_indicator is False` |
| MF-HP-08 | Memory store replaces | `5`, `MS`, `9`, `MS`, `MR` | `main_display == "9"` |

### 5.2 Edge Cases

| Test ID | Description | Input Sequence | Expected |
|---------|-------------|----------------|----------|
| MF-EC-01 | Memory recall with no stored value | `MR` (fresh instance) | `main_display == "0"` |
| MF-EC-02 | Memory add to empty | `5`, `M+`, `MR` | `main_display == "5"` |
| MF-EC-03 | Memory subtract from empty | `5`, `M-`, `MR` | `main_display == "-5"` |
| MF-EC-04 | Memory clear when already empty | `MC` (fresh instance) | No crash, `memory_indicator is False` |
| MF-EC-05 | Store zero clears indicator | `0`, `MS` | `memory_indicator is False` |
| MF-EC-06 | Multiple M+ accumulates | `3`, `M+`, `3`, `M+`, `3`, `M+`, `MR` | `main_display == "9"` |

### 5.3 Cross-Mode Memory

| Test ID | Description | Procedure | Expected |
|---------|-------------|-----------|----------|
| MF-CM-01 | Memory in Scientific mode | Create `ScientificLogic`, `5`, `MS`, `MR` | `main_display == "5"` |
| MF-CM-02 | Memory in Programmer mode | Create `ProgrammerLogic`, `5`, `MS`, `MR` | `main_display == "5"` |

---

## 6. Mode Switching Tests (`tests/test_mode_switch.py`)

Mode switching tests verify requirements MS-1 through MS-7. These tests
simulate the Controller's mode-switch logic: they create one logic instance,
extract its value and memory, create a second logic instance, and transfer the
state.

### 6.1 Happy Path -- Value Preservation

| Test ID | Description | Procedure | Expected |
|---------|-------------|-----------|----------|
| MS-HP-01 | Basic to Scientific preserves float | BasicLogic with 3.14, transfer to ScientificLogic | `main_display == "3.14"` |
| MS-HP-02 | Scientific to Basic preserves float | ScientificLogic with 2.5, transfer to BasicLogic | `main_display == "2.5"` |
| MS-HP-03 | Basic to Programmer truncates | BasicLogic with 3.14, transfer to ProgrammerLogic | `main_display == "3"` |
| MS-HP-04 | Scientific to Programmer truncates | ScientificLogic with 3.14, transfer to ProgrammerLogic | `main_display == "3"` |
| MS-HP-05 | Programmer to Basic preserves int | ProgrammerLogic with 255, transfer to BasicLogic | `main_display == "255"` |
| MS-HP-06 | Programmer HEX to Basic | ProgrammerLogic with FF (hex, = 255), transfer to BasicLogic | `main_display == "255"` |

### 6.2 Happy Path -- Memory Preservation

| Test ID | Description | Procedure | Expected |
|---------|-------------|-----------|----------|
| MS-HP-07 | Memory survives Basic to Scientific | BasicLogic store 42, transfer memory to ScientificLogic, `MR` | `main_display == "42"` |
| MS-HP-08 | Memory survives Scientific to Programmer | ScientificLogic store 10, transfer memory to ProgrammerLogic, `MR` | `main_display == "10"` |
| MS-HP-09 | Memory survives Programmer to Basic | ProgrammerLogic store 7, transfer memory to BasicLogic, `MR` | `main_display == "7"` |
| MS-HP-10 | Memory indicator survives switch | Store nonzero, transfer to new mode | `memory_indicator is True` |

### 6.3 Edge Cases

| Test ID | Description | Procedure | Expected |
|---------|-------------|-----------|----------|
| MS-EC-01 | Negative float to Programmer | BasicLogic with -3.7, transfer to ProgrammerLogic | `main_display == "-3"` (truncate toward zero) |
| MS-EC-02 | Zero preserved across modes | BasicLogic with 0, transfer to ProgrammerLogic | `main_display == "0"` |
| MS-EC-03 | Large int from Programmer | ProgrammerLogic with 2^32, transfer to BasicLogic | Value preserved as float |
| MS-EC-04 | Expression discarded on switch | BasicLogic with pending `5 + `, transfer to ScientificLogic | Expression is empty, value is 5 |

---

## 7. Parametrize Summary

The following test groups must use `pytest.mark.parametrize` to avoid
duplicating test function bodies. Each parametrized test receives input values
and expected output as parameters.

| Test Group | File | Parameters |
|------------|------|------------|
| Basic two-operand arithmetic | `test_basic.py` | `(digit_a, op, digit_b, expected)` |
| Trig functions in degree mode | `test_scientific.py` | `(value, method_name, expected)` |
| Log error cases (0 and negative) | `test_scientific.py` | `(value, method_name)` |
| Factorial happy path | `test_scientific.py` | `(value, expected)` |
| Base conversions | `test_programmer.py` | `(input_value, from_base, to_base, expected)` |
| Bitwise binary operations | `test_programmer.py` | `(a, op_method, b, expected)` |
| Button enabled state per base | `test_programmer.py` | `(base, enabled_digits)` |
| Word size overflow | `test_programmer.py` | `(word_size, a, op, b, expected)` |

---

## 8. Requirements Traceability

Every acceptance criterion from `requirements.md` is covered by at least one
test case. The mapping is as follows:

| Acceptance Criterion | Test ID(s) |
|----------------------|------------|
| `2 + 3 = 5` (BA) | BA-HP-01 |
| `10 / 4 = 2.5` (BA) | BA-HP-04 |
| `2 + 3 * 4 = 14` (BA) | BA-HP-06 |
| `100 / 0 = Error` (BA) | BA-ER-01 |
| Leading zeros `007 -> 7` (NI) | BA-EC-01 |
| Double decimal `..5 -> 0.5` (NI) | BA-EC-02 |
| Sign toggle `5 -> -5` (NI) | NI-HP-04 |
| Percentage `200 -> 2` (NI) | NI-HP-06 |
| `4 / 2 = 2` not `2.0` (DI) | DI-HP-01 |
| `1 / 3` precision (DI) | DI-HP-02 |
| Scientific notation for large numbers (DI) | DI-HP-03 |
| Clear entry preserves op (CE) | CE-HP-01 |
| All clear resets state (CE) | CE-HP-02 |
| Backspace deletes last digit (CE) | CE-HP-03 |
| `MS` shows indicator, `MC` hides it (MF) | MF-HP-06, MF-HP-04 |
| `5 MS, 3 M+, MR = 8` (MF) | MF-HP-02 |
| `10 MS, 3 M-, MR = 7` (MF) | MF-HP-03 |
| Memory persists across modes (MF) | MS-HP-07, MS-HP-08, MS-HP-09 |
| `sin(90) = 1` in DEG (TR) | TR-HP-02 |
| `sin(pi) ~ 0` in RAD (TR) | TR-HP-10 |
| `asin(1) = 90` in DEG (TR) | TR-HP-07 |
| `tan(90) = Error` in DEG (TR) | SC-ER-08 |
| `log(100) = 2` (LG) | LG-HP-01 |
| `ln(e) = 1` (LG) | LG-HP-03 |
| `log2(256) = 8` (LG) | LG-HP-04 |
| `log(0) = Error` (LG) | SC-ER-02 |
| `log(-1) = Error` (LG) | SC-ER-03 |
| `5 x^2 = 25` (PW) | PW-HP-01 |
| `2^10 = 1024` (PW) | PW-HP-03 |
| `10^3 = 1000` (PW) | PW-HP-04 |
| `sqrt(144) = 12` (PW) | PW-HP-06 |
| `sqrt(-1) = Error` (PW) | SC-ER-01 |
| `1/0 = Error` (PW) | SC-ER-13 |
| `pi` value (CO) | CO-HP-01 |
| `e^e` (CO) | CO-HP-03 |
| `5! = 120` (FA) | FA-HP-01 |
| `0! = 1` (FA) | FA-HP-02 |
| `-3! = Error` (FA) | SC-ER-11 |
| `3.5! = Error` (FA) | SC-ER-12 |
| `abs(-7) = 7` (FA) | FA-HP-05 |
| `(2+3)*4 = 20` (PA) | PA-HP-01 |
| `2*(3+4) = 14` (PA) | PA-HP-02 |
| `((2+3)*(4+1)) = 25` (PA) | PA-HP-03 |
| Mismatched parens = Error (PA) | SC-ER-14 |
| DEC 255 -> HEX FF (NB) | NB-HP-01 |
| HEX FF -> DEC 255 (NB) | NB-HP-02 |
| HEX FF -> BIN 11111111 (NB) | NB-HP-03 |
| BIN digits only 0,1 (NB) | BN-HP-01 |
| OCT digits only 0-7 (NB) | BN-HP-02 |
| All-bases panel (NB) | NB-HP-06 |
| 8-bit 127+1 = -128 (WS) | WS-HP-03 |
| 64-bit to 8-bit truncation (WS) | WS-HP-05 |
| `12 AND 10 = 8` (BW) | BW-HP-01 |
| `12 OR 10 = 14` (BW) | BW-HP-02 |
| `12 XOR 10 = 6` (BW) | BW-HP-03 |
| `NOT 0 = -1` 8-bit (BW) | BW-HP-04 |
| `1 LSH 4 = 16` (BW) | BW-HP-05 |
| `16 RSH 2 = 4` (BW) | BW-HP-06 |
| `7 / 2 = 3` integer div (PM) | PM-HP-04 |
| `7 % 2 = 1` modulo (PM) | PM-HP-05 |
| Decimal point disabled (PM) | PM-HP-06, BN-HP-05 |
| Basic to Scientific preserves value (MS) | MS-HP-01 |
| 3.14 to Programmer shows 3 (MS) | MS-HP-03 |
| Programmer FF (hex) to Basic shows 255 (MS) | MS-HP-06 |

---

## 9. Test Execution

Run all tests:

```
python3 -m pytest tests/ -v
```

Run a single test file:

```
python3 -m pytest tests/test_basic.py -v
```

Run tests matching a keyword:

```
python3 -m pytest tests/ -v -k "factorial"
```

Run with coverage (if `pytest-cov` is added to `requirements.txt`):

```
python3 -m pytest tests/ --cov=calculator.logic --cov-report=term-missing
```
