# Advanced Calculator -- Test Plan

**Version:** 1.0
**Date:** 2026-04-01
**Reference:** docs/requirements.md, docs/architecture.md

---

## 1. Test Strategy

### Framework and Conventions

- **Framework:** pytest (the only external dependency).
- **Run command:** `python3 -m pytest -v`
- **Scope:** All tests target the logic layer only. No Tkinter is instantiated in any test. This satisfies NF-5 and NF-7.
- **Parametrize:** Use `@pytest.mark.parametrize` for any operation tested with multiple input/output pairs (TS-11).
- **Independence:** No test depends on another test's state (TS-12). Each test creates its own calculator instance.
- **Assertions:** Use `pytest.approx()` for floating-point comparisons (especially trig functions).
- **Error testing:** Use `pytest.raises(CalculatorError)` for all error condition tests.

### Test File Organization (TS-9, TS-10)

```
tests/
├── __init__.py
├── test_basic.py           # Basic mode: arithmetic, input, display, clear
├── test_scientific.py      # Scientific mode: trig, log, powers, roots, factorial, parens
├── test_programmer.py      # Programmer mode: base conversion, bitwise, word size, int arithmetic
├── test_memory.py          # Memory functions across all modes
└── test_mode_switch.py     # Mode switching with value preservation
```

---

## 2. tests/test_basic.py

### 2.1 Arithmetic Operations -- Happy Path

```
Class: TestBasicArithmetic
```

Use `@pytest.mark.parametrize` with these cases:

| Test ID | Input Sequence | Expected Result | Req |
|---------|---------------|-----------------|-----|
| BA-add-1 | `2 + 3 =` | `5` | BA-1 |
| BA-add-2 | `0 + 0 =` | `0` | BA-1 |
| BA-add-3 | `-5 + 3 =` | `-2` | BA-1 |
| BA-sub-1 | `10 - 3 =` | `7` | BA-2 |
| BA-sub-2 | `3 - 10 =` | `-7` | BA-2 |
| BA-mul-1 | `6 * 7 =` | `42` | BA-3 |
| BA-mul-2 | `0 * 999 =` | `0` | BA-3 |
| BA-div-1 | `10 / 4 =` | `2.5` | BA-4 |
| BA-div-2 | `10 / 5 =` | `2` | BA-4 |

### 2.2 Operator Precedence

| Test ID | Input Sequence | Expected Result | Req |
|---------|---------------|-----------------|-----|
| BA-prec-1 | `2 + 3 * 4 =` | `14` | BA-5 |
| BA-prec-2 | `2 * 3 + 4 =` | `10` | BA-5 |
| BA-prec-3 | `10 - 2 * 3 =` | `4` | BA-5 |
| BA-prec-4 | `10 / 2 + 3 =` | `8` | BA-5 |
| BA-prec-5 | `1 + 2 + 3 + 4 =` | `10` | BA-6 |
| BA-prec-6 | `2 * 3 * 4 =` | `24` | BA-6 |

### 2.3 Arithmetic -- Error Cases

| Test ID | Input Sequence | Expected | Req |
|---------|---------------|----------|-----|
| BA-err-1 | `100 / 0 =` | CalculatorError | ER-1 |
| BA-err-2 | `0 / 0 =` | CalculatorError | ER-1 |

### 2.4 Numeric Input

```
Class: TestNumericInput
```

| Test ID | Input Sequence | Expected Display | Req |
|---------|---------------|-----------------|-----|
| NI-lead-1 | digits `0`, `0`, `7` | `"7"` | NI-4 |
| NI-lead-2 | digits `0`, `0`, `0` | `"0"` | NI-4 |
| NI-dec-1 | digits `.`, `.`, `5` | `"0.5"` | NI-2, NI-3 |
| NI-dec-2 | digits `1`, `.`, `2`, `.`, `3` | `"1.23"` | NI-3 |
| NI-sign-1 | value `5`, toggle_sign | `-5` | NI-5 |
| NI-sign-2 | value `-5`, toggle_sign | `5` | NI-5 |
| NI-sign-3 | value `0`, toggle_sign | `0` | NI-5 |
| NI-pct-1 | value `200`, percentage | `2` | NI-6 |
| NI-pct-2 | value `50`, percentage | `0.5` | NI-6 |

### 2.5 Display Formatting

```
Class: TestDisplayFormatting
```

| Test ID | Input Value | Expected Format | Req |
|---------|------------|-----------------|-----|
| DI-int-1 | `4 / 2` result | `"2"` (not `"2.0"`) | DI-3 |
| DI-int-2 | `5.0` | `"5"` | DI-3 |
| DI-float-1 | `1 / 3` result | 10 significant digits | DI-4 |
| DI-sci-1 | `9999999999 * 9999999999` | scientific notation string | DI-5 |

### 2.6 Clear and Edit

```
Class: TestClearAndEdit
```

| Test ID | Sequence | Expected | Req |
|---------|----------|----------|-----|
| CE-clear-1 | `5 + 3`, clear_entry, `2 =` | `7` (5+2) | CE-1 |
| CE-ac-1 | `5 + 3`, all_clear, `2 =` | `2` | CE-2 |
| CE-back-1 | digits `1`, `2`, `3`, backspace | `"12"` | CE-3 |
| CE-back-2 | digit `5`, backspace | `"0"` or `""` | CE-3 |

### 2.7 Error Recovery

```
Class: TestErrorRecovery
```

| Test ID | Sequence | Expected | Req |
|---------|----------|----------|-----|
| RC-digit-1 | Trigger error (div/0), then digit `5` | Error cleared, input is `"5"` | RC-1 |
| RC-clear-1 | Trigger error (div/0), then clear | Error cleared, display `"0"` | RC-2 |
| RC-ac-1 | Trigger error (div/0), then all_clear | Error cleared, display `"0"` | RC-2 |

---

## 3. tests/test_scientific.py

### 3.1 Trigonometric Functions -- Happy Path

```
Class: TestTrigFunctions
```

Use `@pytest.mark.parametrize` with `pytest.approx`:

| Test ID | Function | Input | Angle Mode | Expected | Req |
|---------|----------|-------|------------|----------|-----|
| TR-sin-deg-1 | sin | 90 | DEG | 1.0 | TR-1 |
| TR-sin-deg-2 | sin | 0 | DEG | 0.0 | TR-1 |
| TR-sin-deg-3 | sin | 30 | DEG | 0.5 | TR-1 |
| TR-sin-rad-1 | sin | 3.14159265 | RAD | approx 0.0 | TR-1 |
| TR-cos-deg-1 | cos | 0 | DEG | 1.0 | TR-2 |
| TR-cos-deg-2 | cos | 90 | DEG | approx 0.0 | TR-2 |
| TR-tan-deg-1 | tan | 45 | DEG | approx 1.0 | TR-3 |
| TR-asin-1 | asin | 1 | DEG | 90.0 | TR-4 |
| TR-acos-1 | acos | 1 | DEG | 0.0 | TR-5 |
| TR-atan-1 | atan | 1 | DEG | 45.0 | TR-6 |

### 3.2 Trigonometric Functions -- Error Cases

| Test ID | Function | Input | Expected | Req |
|---------|----------|-------|----------|-----|
| TR-err-1 | tan | 90 (DEG) | CalculatorError | ER-7 |
| TR-err-2 | asin | 2 | CalculatorError | TR-4 |
| TR-err-3 | asin | -2 | CalculatorError | TR-4 |
| TR-err-4 | acos | 1.5 | CalculatorError | TR-5 |

### 3.3 Angle Mode Toggle

| Test ID | Sequence | Expected | Req |
|---------|----------|----------|-----|
| TR-mode-1 | Default mode | "DEG" | TR-7 |
| TR-mode-2 | Toggle once | "RAD" | TR-7 |
| TR-mode-3 | Toggle twice | "DEG" | TR-7 |

### 3.4 Logarithmic Functions -- Happy Path

```
Class: TestLogFunctions
```

| Test ID | Function | Input | Expected | Req |
|---------|----------|-------|----------|-----|
| LG-log-1 | log10 | 100 | 2.0 | LG-1 |
| LG-log-2 | log10 | 1 | 0.0 | LG-1 |
| LG-ln-1 | ln | math.e | 1.0 | LG-2 |
| LG-ln-2 | ln | 1 | 0.0 | LG-2 |
| LG-log2-1 | log2 | 256 | 8.0 | LG-3 |
| LG-log2-2 | log2 | 1 | 0.0 | LG-3 |

### 3.5 Logarithmic Functions -- Error Cases

| Test ID | Function | Input | Expected | Req |
|---------|----------|-------|----------|-----|
| LG-err-1 | log10 | 0 | CalculatorError | LG-1 |
| LG-err-2 | log10 | -1 | CalculatorError | LG-1 |
| LG-err-3 | ln | 0 | CalculatorError | LG-2 |
| LG-err-4 | ln | -5 | CalculatorError | LG-2 |
| LG-err-5 | log2 | 0 | CalculatorError | LG-3 |

### 3.6 Power and Root Functions -- Happy Path

```
Class: TestPowerAndRoot
```

| Test ID | Function | Input | Expected | Req |
|---------|----------|-------|----------|-----|
| PW-sq-1 | square | 5 | 25 | PW-1 |
| PW-sq-2 | square | -3 | 9 | PW-1 |
| PW-cube-1 | cube | 3 | 27 | PW-2 |
| PW-cube-2 | cube | -2 | -8 | PW-2 |
| PW-pow-1 | power | 2, 10 | 1024 | PW-3 |
| PW-pow-2 | power | 5, 0 | 1 | PW-3 |
| PW-10x-1 | ten_to_x | 3 | 1000 | PW-4 |
| PW-ex-1 | e_to_x | 0 | 1.0 | PW-5 |
| PW-ex-2 | e_to_x | 1 | approx 2.71828 | PW-5 |
| PW-sqrt-1 | sqrt | 144 | 12 | PW-6 |
| PW-sqrt-2 | sqrt | 0 | 0 | PW-6 |
| PW-cbrt-1 | cbrt | 27 | 3 | PW-7 |
| PW-cbrt-2 | cbrt | -8 | -2 | PW-7 |
| PW-recip-1 | reciprocal | 4 | 0.25 | PW-8 |
| PW-recip-2 | reciprocal | -2 | -0.5 | PW-8 |

### 3.7 Power and Root Functions -- Error Cases

| Test ID | Function | Input | Expected | Req |
|---------|----------|-------|----------|-----|
| PW-err-1 | sqrt | -1 | CalculatorError | PW-6 |
| PW-err-2 | reciprocal | 0 | CalculatorError | PW-8 |

### 3.8 Constants

```
Class: TestConstants
```

| Test ID | Function | Expected | Req |
|---------|----------|----------|-----|
| CO-pi-1 | get_pi | math.pi | CO-1 |
| CO-e-1 | get_e | math.e | CO-2 |

### 3.9 Factorial and Absolute Value

```
Class: TestFactorialAndAbsolute
```

| Test ID | Function | Input | Expected | Req |
|---------|----------|-------|----------|-----|
| FA-fact-1 | factorial | 5 | 120 | FA-1 |
| FA-fact-2 | factorial | 0 | 1 | FA-1 |
| FA-fact-3 | factorial | 1 | 1 | FA-1 |
| FA-fact-4 | factorial | 10 | 3628800 | FA-1 |
| FA-fact-5 | factorial | 170 | large number (no error) | NF-4 |
| FA-abs-1 | absolute_value | -7 | 7 | FA-4 |
| FA-abs-2 | absolute_value | 7 | 7 | FA-4 |
| FA-abs-3 | absolute_value | 0 | 0 | FA-4 |

### 3.10 Factorial -- Error Cases

| Test ID | Function | Input | Expected | Req |
|---------|----------|-------|----------|-----|
| FA-err-1 | factorial | -3 | CalculatorError | FA-2 |
| FA-err-2 | factorial | 3.5 | CalculatorError | FA-3 |
| FA-err-3 | factorial | -1.5 | CalculatorError | FA-2, FA-3 |

### 3.11 Parentheses

```
Class: TestParentheses
```

| Test ID | Expression Tokens | Expected | Req |
|---------|------------------|----------|-----|
| PA-group-1 | `(2 + 3) * 4 =` | 20 | PA-2 |
| PA-group-2 | `2 * (3 + 4) =` | 14 | PA-2 |
| PA-group-3 | `((2 + 3) * (4 + 1)) =` | 25 | PA-2 |
| PA-nested-1 | `((1 + 2) * (3 + 4)) =` | 21 | PA-2 |

### 3.12 Parentheses -- Error Cases

| Test ID | Expression Tokens | Expected | Req |
|---------|------------------|----------|-----|
| PA-err-1 | `(2 + 3 =` (unmatched open) | CalculatorError | PA-3 |
| PA-err-2 | `2 + 3) =` (unmatched close) | CalculatorError | PA-3 |

---

## 4. tests/test_programmer.py

### 4.1 Base Conversion -- Happy Path

```
Class: TestBaseConversion
```

| Test ID | Value (DEC) | Target Base | Expected String | Req |
|---------|------------|-------------|-----------------|-----|
| NB-dec-hex-1 | 255 | HEX | "FF" | NB-2, NB-6 |
| NB-hex-dec-1 | 255 (entered as FF in HEX) | DEC | "255" | NB-1, NB-6 |
| NB-dec-bin-1 | 255 | BIN | "11111111" | NB-4, NB-6 |
| NB-dec-oct-1 | 255 | OCT | "377" | NB-3, NB-6 |
| NB-zero-1 | 0 | HEX | "0" | NB-2 |
| NB-zero-2 | 0 | BIN | "0" | NB-4 |
| NB-neg-1 | -1 (8-bit) | HEX | "FF" | NB-2 |
| NB-neg-2 | -1 (8-bit) | BIN | "11111111" | NB-4 |

### 4.2 All-Bases Display

| Test ID | Value (DEC) | Expected Dict | Req |
|---------|------------|---------------|-----|
| NB-all-1 | 255 | {"DEC":"255", "HEX":"FF", "OCT":"377", "BIN":"11111111"} | NB-7 |
| NB-all-2 | 0 | {"DEC":"0", "HEX":"0", "OCT":"0", "BIN":"0"} | NB-7 |

### 4.3 Valid Digits Per Base

```
Class: TestValidDigits
```

| Test ID | Base | Expected Valid Set | Req |
|---------|------|-------------------|-----|
| NB-valid-1 | BIN (2) | {"0", "1"} | NB-8 |
| NB-valid-2 | OCT (8) | {"0"-"7"} | NB-8 |
| NB-valid-3 | DEC (10) | {"0"-"9"} | NB-8 |
| NB-valid-4 | HEX (16) | {"0"-"9", "A"-"F"} | NB-8, HX-1 |

### 4.4 Word Size -- Happy Path

```
Class: TestWordSize
```

| Test ID | Word Size | Operation | Expected | Req |
|---------|-----------|-----------|----------|-----|
| WS-overflow-1 | 8 | 127 + 1 | -128 | WS-3 |
| WS-overflow-2 | 8 | -128 - 1 | 127 | WS-3 |
| WS-overflow-3 | 16 | 32767 + 1 | -32768 | WS-3 |
| WS-truncate-1 | 8 (from 64-bit with 300) | 44 | WS-2 |
| WS-truncate-2 | 8 (from 64-bit with 256) | 0 | WS-2 |
| WS-range-1 | 8 | _apply_word_size(255) | -1 | WS-2 |
| WS-range-2 | 8 | _apply_word_size(128) | -128 | WS-2 |

### 4.5 Bitwise Operations -- Happy Path

```
Class: TestBitwiseOps
```

Use `@pytest.mark.parametrize`:

| Test ID | Operation | A | B | Word Size | Expected | Req |
|---------|-----------|---|---|-----------|----------|-----|
| BW-and-1 | AND | 12 | 10 | 64 | 8 | BW-1 |
| BW-and-2 | AND | 0xFF | 0x0F | 64 | 15 | BW-1 |
| BW-or-1 | OR | 12 | 10 | 64 | 14 | BW-2 |
| BW-xor-1 | XOR | 12 | 10 | 64 | 6 | BW-3 |
| BW-not-1 | NOT | 0 | -- | 8 | -1 | BW-4 |
| BW-not-2 | NOT | -1 | -- | 8 | 0 | BW-4 |
| BW-lsh-1 | LSH | 1 | 4 | 64 | 16 | BW-5 |
| BW-lsh-2 | LSH | 1 | 7 | 8 | -128 | BW-5 |
| BW-rsh-1 | RSH | 16 | 2 | 64 | 4 | BW-6 |
| BW-rsh-2 | RSH | -128 | 7 | 8 | -1 | BW-6 |

### 4.6 Integer Arithmetic

```
Class: TestIntegerArithmetic
```

| Test ID | Operation | A | B | Expected | Req |
|---------|-----------|---|---|----------|-----|
| PM-add-1 | + | 5 | 3 | 8 | PM-1 |
| PM-sub-1 | - | 5 | 3 | 2 | PM-1 |
| PM-mul-1 | * | 6 | 7 | 42 | PM-1 |
| PM-idiv-1 | / | 7 | 2 | 3 | PM-2 |
| PM-idiv-2 | / | -7 | 2 | -3 (truncating) | PM-2 |
| PM-idiv-3 | / | 7 | -2 | -3 (truncating) | PM-2 |
| PM-mod-1 | % | 7 | 2 | 1 | PM-4 |
| PM-mod-2 | % | 10 | 3 | 1 | PM-4 |

### 4.7 Integer Arithmetic -- Error Cases

| Test ID | Operation | A | B | Expected | Req |
|---------|-----------|---|---|----------|-----|
| PM-err-1 | / | 5 | 0 | CalculatorError | ER-1 |
| PM-err-2 | % | 5 | 0 | CalculatorError | PM-4 |

### 4.8 No Decimal Point

| Test ID | Sequence | Expected | Req |
|---------|----------|----------|-----|
| PM-nodec-1 | append_decimal on ProgrammerCalculator | no-op or error | PM-3 |

---

## 5. tests/test_memory.py

```
Class: TestMemoryFunctions
```

### 5.1 Memory -- Happy Path

| Test ID | Sequence | Expected | Req |
|---------|----------|----------|-----|
| MF-store-1 | memory_store(5), memory_recall | 5 | MF-5, MF-2 |
| MF-add-1 | memory_store(5), memory_add(3), memory_recall | 8 | MF-3 |
| MF-sub-1 | memory_store(10), memory_subtract(3), memory_recall | 7 | MF-4 |
| MF-clear-1 | memory_store(5), memory_clear, memory_recall | 0 | MF-1 |
| MF-indicator-1 | memory_store(5) | has_memory == True | MF-6 |
| MF-indicator-2 | memory_store(5), memory_clear | has_memory == False | MF-6 |

### 5.2 Memory -- Edge Cases

| Test ID | Sequence | Expected | Req |
|---------|----------|----------|-----|
| MF-empty-1 | memory_recall (no store) | 0 | MF-2 |
| MF-overwrite-1 | memory_store(5), memory_store(10), memory_recall | 10 | MF-5 |
| MF-neg-1 | memory_store(-5), memory_recall | -5 | MF-5 |
| MF-add-neg-1 | memory_store(10), memory_add(-3), memory_recall | 7 | MF-3 |

---

## 6. tests/test_mode_switch.py

```
Class: TestModeSwitching
```

These tests verify value transfer logic between calculator instances. Since mode switching is a Controller responsibility, these tests simulate what the Controller does: read value from one model, transfer to another.

### 6.1 Value Preservation

| Test ID | From Mode | Value | To Mode | Expected | Req |
|---------|-----------|-------|---------|----------|-----|
| MS-basic-sci-1 | Basic | 3.14 | Scientific | 3.14 | MS-3 |
| MS-sci-basic-1 | Scientific | 2.718 | Basic | 2.718 | MS-3 |
| MS-basic-prog-1 | Basic | 3.14 | Programmer | 3 (truncated) | MS-4 |
| MS-sci-prog-1 | Scientific | -7.9 | Programmer | -7 (truncated) | MS-4 |
| MS-prog-basic-1 | Programmer | 255 (DEC) | Basic | 255.0 | MS-5 |
| MS-prog-basic-2 | Programmer | 255 (showing as FF in HEX) | Basic | 255.0 | MS-5 |

### 6.2 Memory Persistence Across Mode Switches

| Test ID | Sequence | Expected | Req |
|---------|----------|----------|-----|
| MF-persist-1 | Store 42 in Basic, switch to Scientific, recall | 42 | MF-7 |
| MF-persist-2 | Store 42 in Basic, switch to Programmer, recall | 42 | MF-7 |
| MF-persist-3 | has_memory True in Basic, switch to Scientific | has_memory still True | MF-7 |

---

## 7. Expression Parser Tests (in test_basic.py or separate section)

These test the `ExpressionParser` class directly, since it is the highest-risk component.

```
Class: TestExpressionParser
```

### 7.1 Parser -- Happy Path

| Test ID | Tokens | Expected |
|---------|--------|----------|
| EP-simple-1 | [2, "+", 3] | 5 |
| EP-simple-2 | [10, "-", 3] | 7 |
| EP-simple-3 | [6, "*", 7] | 42 |
| EP-simple-4 | [10, "/", 4] | 2.5 |
| EP-prec-1 | [2, "+", 3, "*", 4] | 14 |
| EP-prec-2 | [2, "*", 3, "+", 4] | 10 |
| EP-prec-3 | [10, "-", 2, "*", 3] | 4 |
| EP-paren-1 | ["(", 2, "+", 3, ")", "*", 4] | 20 |
| EP-paren-2 | [2, "*", "(", 3, "+", 4, ")"] | 14 |
| EP-nested-1 | ["(", "(", 2, "+", 3, ")", "*", "(", 4, "+", 1, ")", ")"] | 25 |
| EP-single-1 | [42] | 42 |

### 7.2 Parser -- Error Cases

| Test ID | Tokens | Expected |
|---------|--------|----------|
| EP-err-1 | [10, "/", 0] | CalculatorError (div by zero) |
| EP-err-2 | ["(", 2, "+", 3] | CalculatorError (unmatched paren) |
| EP-err-3 | [2, "+", 3, ")"] | CalculatorError (unmatched paren) |
| EP-err-4 | [] | CalculatorError (empty expression) |
| EP-err-5 | ["+", 3] | CalculatorError or handled gracefully |

### 7.3 Parser -- Programmer Mode Operators

| Test ID | Tokens | Expected |
|---------|--------|----------|
| EP-prog-1 | [12, "AND", 10] | 8 |
| EP-prog-2 | [12, "OR", 10] | 14 |
| EP-prog-3 | [12, "XOR", 10] | 6 |
| EP-prog-4 | [1, "LSH", 4] | 16 |
| EP-prog-5 | [16, "RSH", 2] | 4 |
| EP-prog-6 | [7, "%", 2] | 1 |

---

## 8. Performance Edge Cases

These are not strict performance tests but verify the system handles extreme inputs without crashing (RC-3, NF-4).

| Test ID | Scenario | Expected |
|---------|----------|----------|
| PERF-1 | factorial(170) | Valid large number, no crash |
| PERF-2 | factorial(171) | May overflow float; should return result or Error, no crash |
| PERF-3 | Very long chained expression (20+ operators) | Correct result, no crash |
| PERF-4 | Deeply nested parens (10 levels) | Correct result, no crash |

---

## 9. Test Implementation Notes

### Fixture Pattern

```python
import pytest
from calculator.logic.basic_logic import BasicCalculator
from calculator.logic.base_logic import CalculatorError

@pytest.fixture
def calc():
    return BasicCalculator()

class TestBasicArithmetic:
    @pytest.mark.parametrize("a, op, b, expected", [
        (2, "+", 3, 5),
        (10, "/", 4, 2.5),
        (2, "+", 3, 5),  # ... more cases
    ])
    def test_binary_operation(self, calc, a, op, b, expected):
        calc.append_digit(str(a))
        calc.add_operator(op)
        calc.append_digit(str(b))
        result = calc.evaluate()
        assert result == pytest.approx(expected)

    def test_division_by_zero(self, calc):
        calc.append_digit("10")
        calc.add_operator("/")
        calc.append_digit("0")
        with pytest.raises(CalculatorError):
            calc.evaluate()
```

### Testing Strategy for Multi-Digit Numbers

For multi-digit inputs, call `append_digit()` once per character:

```python
def enter_number(calc, number_str):
    for ch in number_str:
        if ch == ".":
            calc.append_decimal()
        elif ch == "-":
            pass  # handle via toggle_sign after entry
        else:
            calc.append_digit(ch)
```

### Testing Strategy for Programmer Mode

Create a `ProgrammerCalculator` instance, set the desired word size and base, then operate:

```python
@pytest.fixture
def prog_calc():
    calc = ProgrammerCalculator()
    calc.set_word_size(8)
    return calc

def test_8bit_overflow(prog_calc):
    result = prog_calc._apply_word_size(128)
    assert result == -128
```

### Floating-Point Tolerance

Use `pytest.approx` for all float comparisons. Default tolerance (1e-6 relative) is fine for most cases. For trig near-zero results, use absolute tolerance:

```python
assert result == pytest.approx(0.0, abs=1e-10)
```
