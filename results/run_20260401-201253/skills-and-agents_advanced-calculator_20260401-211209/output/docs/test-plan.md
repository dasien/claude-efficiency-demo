# Advanced Calculator -- Test Plan

**Version:** 1.0
**Date:** 2026-04-01
**Based on:** Requirements Document v1.0, Architecture Document v1.0

---

## 1. Test Strategy

- **Target layer**: All tests target the logic layer only (`calculator/logic/`). No Tkinter imports or GUI instantiation.
- **Framework**: pytest, run via `python3 -m pytest`.
- **Parametrize**: Use `pytest.mark.parametrize` for operations with multiple input/output pairs.
- **Independence**: Each test is fully independent. No shared mutable state between tests. Each test creates its own calculator instance.
- **Fixtures**: Use pytest fixtures to provide fresh calculator instances (`BasicCalculator`, `ScientificCalculator`, `ProgrammerCalculator`).
- **Assertions**: Use `pytest.approx` for floating-point comparisons where needed.

---

## 2. Test Files and Coverage

| File | Covers | Requirement IDs |
|------|--------|-----------------|
| `test_basic.py` | Arithmetic, numeric input, display formatting, clear/edit | BA-1..6, NI-1..6, DI-1..6, CE-1..3, ER-1, ER-6 |
| `test_scientific.py` | Trig, logs, powers/roots, factorial, abs, parentheses, constants | TR-1..8, LG-1..3, PW-1..8, CO-1..2, FA-1..4, PA-1..4, ER-2, ER-4, ER-5, ER-7 |
| `test_programmer.py` | Base conversion, bitwise ops, word size/overflow, integer arithmetic | NB-1..8, HX-1..3, WS-1..4, BW-1..6, PM-1..4, ER-3 |
| `test_memory.py` | MC/MR/M+/M-/MS across all modes | MF-1..7 |
| `test_mode_switch.py` | Value preservation/conversion between modes | MS-1..5 |

---

## 3. test_basic.py

### 3.1 Happy Path -- Arithmetic (BA-1..6)

```python
@pytest.mark.parametrize("steps,expected", [
    # BA-1: addition
    (["2", "+", "3", "="], 5),
    # BA-2: subtraction
    (["10", "-", "3", "="], 7),
    # BA-3: multiplication
    (["4", "*", "5", "="], 20),
    # BA-4: division
    (["10", "/", "4", "="], 2.5),
    # BA-5, BA-6: operator precedence and chaining
    (["2", "+", "3", "*", "4", "="], 14),
])
def test_basic_arithmetic(calc, steps, expected): ...
```

### 3.2 Happy Path -- Numeric Input (NI-1..6)

```python
@pytest.mark.parametrize("digits,expected_display", [
    # NI-4: leading zeros
    (["0", "0", "7"], "7"),
    # NI-3: duplicate decimal point
    ([".", ".", "5"], "0.5"),
])
def test_numeric_input(calc, digits, expected_display): ...
```

- NI-5: Press `5`, `+/-` -- display shows `-5`.
- NI-6: Press `2`, `0`, `0`, `%` -- display shows `2`.

### 3.3 Happy Path -- Display Formatting (DI-1..6)

```python
@pytest.mark.parametrize("steps,expected_display", [
    # DI-3: integer result without decimal
    (["4", "/", "2", "="], "2"),
    # DI-4: float precision (10 significant digits)
    (["1", "/", "3", "="], "0.3333333333"),
])
def test_display_formatting(calc, steps, expected_display): ...
```

- DI-5: `9999999999 * 9999999999 =` displays in scientific notation.

### 3.4 Happy Path -- Clear and Edit (CE-1..3)

- CE-1: Press `5`, `+`, `3`, `C` -- display shows `0`. Then `2`, `=` -- display shows `7` (5+2).
- CE-2: Press `5`, `+`, `3`, `AC` -- display shows `0`. Then `2`, `=` -- display shows `2`.
- CE-3: Press `1`, `2`, `3`, `Backspace` -- display shows `12`.

### 3.5 Edge Cases

- Pressing `=` with no expression returns `0`.
- Very long digit strings are handled without crash.
- Multiple operators in sequence are handled gracefully (ER-6).
- Percentage of zero: `0`, `%` -- display shows `0`.
- Sign toggle on zero: `0`, `+/-` -- display shows `0`.
- Backspace on single digit returns to `0`.
- Backspace on empty input is a no-op.

### 3.6 Error Cases

```python
@pytest.mark.parametrize("steps", [
    # ER-1: division by zero
    ["100", "/", "0", "="],
])
def test_division_by_zero(calc, steps): ...
```

- ER-1: `100 / 0 =` -- display shows `Error`.
- RC-1: After error, pressing a digit clears the error and starts a new number.
- RC-2: After error, pressing `C` or `AC` clears the error.

---

## 4. test_scientific.py

### 4.1 Happy Path -- Trigonometric Functions (TR-1..8)

```python
@pytest.mark.parametrize("func,input_val,angle_mode,expected", [
    # TR-1: sin in degree mode
    ("sin", 90, "DEG", 1),
    # TR-2: cos
    ("cos", 0, "DEG", 1),
    # TR-4: asin in degree mode
    ("asin", 1, "DEG", 90),
    # TR-6: atan
    ("atan", 1, "DEG", 45),
])
def test_trig_happy_path(sci_calc, func, input_val, angle_mode, expected): ...
```

- TR-7: Toggle between DEG and RAD mode.
- TR-1 (RAD): `sin(3.14159265)` is approximately `0`.

### 4.2 Happy Path -- Logarithmic Functions (LG-1..3)

```python
@pytest.mark.parametrize("func,input_val,expected", [
    ("log", 100, 2),       # LG-1
    ("ln", math.e, 1),     # LG-2
    ("log2", 256, 8),      # LG-3
])
def test_log_happy_path(sci_calc, func, input_val, expected): ...
```

### 4.3 Happy Path -- Powers and Roots (PW-1..8)

```python
@pytest.mark.parametrize("func,input_val,expected", [
    ("square", 5, 25),          # PW-1
    ("cube", 3, 27),            # PW-2
    ("ten_power", 3, 1000),     # PW-4
    ("square_root", 144, 12),   # PW-6
    ("cube_root", 27, 3),       # PW-7
    ("reciprocal", 4, 0.25),    # PW-8
])
def test_powers_roots(sci_calc, func, input_val, expected): ...
```

- PW-3: `2`, `xⁿ`, `10`, `=` produces `1024` (two-operand power).
- PW-5: `e^x` with value `1` produces `math.e`.

### 4.4 Happy Path -- Constants (CO-1..2)

- CO-1: `insert_pi()` sets value to `math.pi`, displays `3.14159265359` (or similar).
- CO-2: Press `e` then `e^x` produces approximately `15.1542622414`.

### 4.5 Happy Path -- Factorial and Absolute Value (FA-1..4)

```python
@pytest.mark.parametrize("input_val,expected", [
    (5, 120),     # FA-1
    (0, 1),       # FA-1 (zero case)
])
def test_factorial_happy(sci_calc, input_val, expected): ...
```

- FA-4: `|-7|` produces `7`.

### 4.6 Happy Path -- Parentheses (PA-1..3)

```python
@pytest.mark.parametrize("expression,expected", [
    ("(2 + 3) * 4", 20),         # PA-2
    ("2 * (3 + 4)", 14),         # PA-2
    ("((2 + 3) * (4 + 1))", 25), # PA-2
])
def test_parentheses(sci_calc, expression, expected): ...
```

### 4.7 Edge Cases

- `sin(0)` in both DEG and RAD mode returns `0`.
- `cos(360)` in DEG mode returns `1`.
- `factorial(170)` succeeds (NF-4: limit of float).
- `cube_root(-8)` returns `-2`.
- Nested parentheses at depth 5+.
- `e_power(0)` returns `1`.
- `log(1)` returns `0`.

### 4.8 Error Cases

```python
@pytest.mark.parametrize("func,input_val", [
    ("square_root", -1),    # PW-6, ER-2
    ("reciprocal", 0),      # PW-8, ER-2
    ("log", 0),             # LG-1, ER-2
    ("log", -1),            # LG-1, ER-2
    ("ln", 0),              # LG-2, ER-2
    ("log2", -5),           # LG-3, ER-2
])
def test_scientific_errors(sci_calc, func, input_val): ...
```

- ER-4, FA-2: `factorial(-3)` displays `Error`.
- ER-4, FA-3: `factorial(3.5)` displays `Error`.
- ER-7, TR-3: `tan(90)` in DEG mode displays `Error`.
- ER-5, PA-3: `(2 + 3 =` with mismatched parentheses displays `Error`.

---

## 5. test_programmer.py

### 5.1 Happy Path -- Base Conversion (NB-1..8)

```python
@pytest.mark.parametrize("input_base,input_val,target_base,expected", [
    ("DEC", 255, "HEX", "FF"),           # NB-2, NB-6
    ("HEX", "FF", "DEC", "255"),         # NB-1, NB-6
    ("HEX", "FF", "BIN", "11111111"),    # NB-4, NB-6
    ("DEC", 255, "OCT", "377"),          # NB-3, NB-6
])
def test_base_conversion(prog_calc, input_base, input_val, target_base, expected): ...
```

- NB-7: `get_all_bases()` returns `{"DEC": "255", "HEX": "FF", "OCT": "377", "BIN": "11111111"}`.
- NB-8: `get_valid_digits()` in BIN mode returns `{"0", "1"}`.
- HX-3: Hex digits display uppercase.

### 5.2 Happy Path -- Bitwise Operations (BW-1..6)

```python
@pytest.mark.parametrize("op,a,b,expected", [
    ("AND", 12, 10, 8),   # BW-1
    ("OR", 12, 10, 14),   # BW-2
    ("XOR", 12, 10, 6),   # BW-3
    ("LSH", 1, 4, 16),    # BW-5
    ("RSH", 16, 2, 4),    # BW-6
])
def test_bitwise_ops(prog_calc, op, a, b, expected): ...
```

- BW-4: `NOT 0` in 8-bit mode produces `-1`.

### 5.3 Happy Path -- Word Size (WS-1..4)

```python
@pytest.mark.parametrize("word_size,value,expected", [
    (8, 128, -128),       # WS-3: overflow wraps
    (8, 256, 0),          # WS-2: wraps to 0
])
def test_word_size_wrapping(prog_calc, word_size, value, expected): ...
```

- WS-1: Setting word size to 8, 16, 32, 64 is accepted.
- WS: `127 + 1` in 8-bit produces `-128`.

### 5.4 Happy Path -- Integer Arithmetic (PM-1..4)

```python
@pytest.mark.parametrize("steps,expected", [
    (["7", "/", "2", "="], 3),     # PM-2: integer division
    (["7", "%", "2", "="], 1),     # PM-4: modulo
    (["3", "+", "4", "="], 7),     # PM-1: addition
    (["10", "-", "3", "="], 7),    # PM-1: subtraction
    (["3", "*", "4", "="], 12),    # PM-1: multiplication
])
def test_programmer_arithmetic(prog_calc, steps, expected): ...
```

- PM-3: `append_decimal()` is a no-op in programmer mode.

### 5.5 Edge Cases

- Switching from 64-bit to 8-bit with value `300` truncates to `44` (WS).
- `NOT` of max positive value for each word size.
- Left shift that exceeds word size wraps correctly.
- Zero in all bases displays as `0`.
- Negative value displayed in HEX uses two's complement representation.
- `get_valid_digits()` for each base returns correct set:
  - BIN: `{"0", "1"}`
  - OCT: `{"0".."7"}`
  - DEC: `{"0".."9"}`
  - HEX: `{"0".."9", "A".."F"}`

### 5.6 Error Cases

- ER-1: Integer division by zero displays `Error`.
- ER-3: Overflow wraps via two's complement (not an error, but tested for correctness).
- Modulo by zero displays `Error`.

---

## 6. test_memory.py

### 6.1 Happy Path (MF-1..6)

Tests use `BasicCalculator` as the primary instance but also verify with `ScientificCalculator` and `ProgrammerCalculator`.

- MF-5, MF-6: `ms()` stores value, `has_memory` becomes `True`.
- MF-1: `mc()` clears memory, `has_memory` becomes `False`.
- MF-2: `mr()` returns stored value.
- MF-3: Store `5`, then `m_plus()` with value `3`, `mr()` returns `8`.
- MF-4: Store `10`, then `m_minus()` with value `3`, `mr()` returns `7`.

```python
@pytest.mark.parametrize("operations,expected_recall", [
    # MF-3: M+ accumulates
    ([("ms", 5), ("m_plus", 3)], 8),
    # MF-4: M- subtracts
    ([("ms", 10), ("m_minus", 3)], 7),
])
def test_memory_operations(calc, operations, expected_recall): ...
```

### 6.2 Memory Across Modes (MF-7)

- Store a value in Basic mode. Switch to Scientific mode (simulated by copying memory to a new ScientificCalculator). `mr()` returns the same value.
- Store a value in Basic mode. Switch to Programmer mode. `mr()` returns the integer-truncated value or the same memory value (memory is float, display adapts).

### 6.3 Edge Cases

- `mr()` when no value stored returns `0`.
- `m_plus()` and `m_minus()` when no value stored treat memory as `0`.
- `mc()` when memory is already clear is a no-op.
- Multiple `ms()` calls overwrite previous value.

---

## 7. test_mode_switch.py

### 7.1 Happy Path (MS-1..5)

```python
@pytest.mark.parametrize("from_mode,to_mode,input_value,expected_value", [
    # MS-3: Basic to Scientific preserves float
    ("basic", "scientific", 3.14, 3.14),
    # MS-4: Scientific to Programmer truncates to int
    ("scientific", "programmer", 3.14, 3),
    # MS-5: Programmer (hex FF = 255) to Basic
    ("programmer", "basic", 255, 255.0),
])
def test_mode_switch_value_preservation(from_mode, to_mode, input_value, expected_value): ...
```

### 7.2 Edge Cases

- Switching to the same mode is a no-op.
- Switching with value `0` preserves `0`.
- Switching from Programmer with negative value to Basic preserves the negative sign.
- Switching from 8-bit Programmer (value `-128`) to Basic produces `-128.0`.
- Switching from Basic with a very large float to Programmer truncates and masks to word size.

### 7.3 Memory Preservation During Switch

- Store a value in Basic, switch to Scientific, recall returns the same value (MS-3 combined with MF-7).
- Store a value in Scientific, switch to Programmer, recall returns the same value.

---

## 8. Requirement Traceability

Every requirement ID maps to at least one test case:

| Req ID | Test File | Section |
|--------|-----------|---------|
| MS-1..5 | test_mode_switch.py | 7.1 |
| BA-1..6 | test_basic.py | 3.1 |
| NI-1..6 | test_basic.py | 3.2 |
| MF-1..7 | test_memory.py | 6.1, 6.2 |
| DI-1..6 | test_basic.py | 3.3 |
| CE-1..3 | test_basic.py | 3.4 |
| TR-1..8 | test_scientific.py | 4.1 |
| LG-1..3 | test_scientific.py | 4.2 |
| PW-1..8 | test_scientific.py | 4.3 |
| CO-1..2 | test_scientific.py | 4.4 |
| FA-1..4 | test_scientific.py | 4.5 |
| PA-1..4 | test_scientific.py | 4.6 |
| NB-1..8 | test_programmer.py | 5.1 |
| HX-1..3 | test_programmer.py | 5.1 |
| WS-1..4 | test_programmer.py | 5.3 |
| BW-1..6 | test_programmer.py | 5.2 |
| PM-1..4 | test_programmer.py | 5.4 |
| ER-1 | test_basic.py | 3.6 |
| ER-2 | test_scientific.py | 4.8 |
| ER-3 | test_programmer.py | 5.6 |
| ER-4 | test_scientific.py | 4.8 |
| ER-5 | test_scientific.py | 4.8 |
| ER-6 | test_basic.py | 3.5 |
| ER-7 | test_scientific.py | 4.8 |
| RC-1..2 | test_basic.py | 3.6 |
| NF-4 | test_scientific.py | 4.7 |
