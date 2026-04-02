# Test Plan — Advanced Calculator

## Strategy

- All tests target the **logic layer only** — no Tkinter instantiation required
- Use `pytest` with `pytest.mark.parametrize` for multi-input operations
- Tests organized by mode, then by category (happy path, edge cases, errors)
- Each test is independent — no shared mutable state between tests
- Run with: `python3 -m pytest -v`

---

## 1. Basic Mode Tests (`tests/test_basic.py`)

### 1.1 Happy Path — Arithmetic
| Test | Input Sequence | Expected |
|------|---------------|----------|
| Addition | 2 + 3 = | 5 |
| Subtraction | 10 - 3 = | 7 |
| Multiplication | 4 * 5 = | 20 |
| Division | 10 / 4 = | 2.5 |
| Chained addition | 1 + 2 + 3 = | 6 |
| Operator precedence | 2 + 3 * 4 = | 14 |
| Complex precedence | 2 * 3 + 4 * 5 = | 26 |

### 1.2 Numeric Input
| Test | Input Sequence | Expected Display |
|------|---------------|-----------------|
| Leading zeros | 0, 0, 7 | "7" |
| Single decimal | ., ., 5 | "0.5" |
| Negate positive | 5, +/- | "-5" |
| Negate negative | 5, +/-, +/- | "5" |
| Percent | 200, % | "2" |
| Decimal number | 3, ., 1, 4 | "3.14" |

### 1.3 Display Formatting
| Test | Operation | Expected Display |
|------|-----------|-----------------|
| Integer result | 4 / 2 = | "2" (not "2.0") |
| Float result | 1 / 3 = | "0.3333333333" |
| Scientific notation | 9999999999 * 9999999999 = | scientific notation |
| Negative display | 0 - 5 = | "-5" |

### 1.4 Clear and Edit
| Test | Input Sequence | Expected |
|------|---------------|----------|
| Clear entry | 5, +, 3, C, 2, = | 7 |
| All clear | 5, +, 3, AC, 2, = | 2 |
| Backspace | 1, 2, 3, ⌫ | "12" |
| Backspace to zero | 5, ⌫ | "0" |

### 1.5 Error Cases
| Test | Input Sequence | Expected |
|------|---------------|----------|
| Division by zero | 100 / 0 = | Error |
| Error recovery digit | (error state), 5 | "5" (no error) |
| Error recovery clear | (error state), C | "0" (no error) |

---

## 2. Scientific Mode Tests (`tests/test_scientific.py`)

### 2.1 Trigonometric — Degree Mode
| Test | Function | Input | Expected |
|------|----------|-------|----------|
| sin 0° | sin | 0 | 0 |
| sin 90° | sin | 90 | 1 |
| cos 0° | cos | 0 | 1 |
| cos 90° | cos | 90 | 0 |
| tan 45° | tan | 45 | 1 |
| asin 1 | asin | 1 | 90 |
| acos 1 | acos | 1 | 0 |
| atan 1 | atan | 1 | 45 |

### 2.2 Trigonometric — Radian Mode
| Test | Function | Input | Expected |
|------|----------|-------|----------|
| sin π | sin | π | ≈0 |
| cos π | cos | π | -1 |
| sin π/2 | sin | π/2 | 1 |

### 2.3 Trigonometric — Error Cases
| Test | Function | Input | Expected |
|------|----------|-------|----------|
| tan 90° | tan | 90 (deg) | Error |
| asin 2 | asin | 2 | Error |
| acos -2 | acos | -2 | Error |

### 2.4 Logarithmic — Happy Path
| Test | Function | Input | Expected |
|------|----------|-------|----------|
| log 100 | log | 100 | 2 |
| log 1 | log | 1 | 0 |
| ln e | ln | e | 1 |
| log₂ 256 | log₂ | 256 | 8 |

### 2.5 Logarithmic — Error Cases
| Test | Function | Input | Expected |
|------|----------|-------|----------|
| log 0 | log | 0 | Error |
| log -1 | log | -1 | Error |
| ln 0 | ln | 0 | Error |

### 2.6 Powers and Roots
| Test | Function | Input | Expected |
|------|----------|-------|----------|
| x² | square | 5 | 25 |
| x³ | cube | 3 | 27 |
| xⁿ | power | 2, 10 | 1024 |
| 10ˣ | ten_power | 3 | 1000 |
| eˣ | e_power | 0 | 1 |
| √x | sqrt | 144 | 12 |
| ³√x | cbrt | 27 | 3 |
| 1/x | reciprocal | 4 | 0.25 |

### 2.7 Powers and Roots — Error Cases
| Test | Function | Input | Expected |
|------|----------|-------|----------|
| √(-1) | sqrt | -1 | Error |
| 1/0 | reciprocal | 0 | Error |

### 2.8 Constants
| Test | Action | Expected |
|------|--------|----------|
| Insert π | pi | 3.14159265359 |
| Insert e | e | 2.71828182846 |

### 2.9 Factorial and Absolute Value
| Test | Function | Input | Expected |
|------|----------|-------|----------|
| 5! | factorial | 5 | 120 |
| 0! | factorial | 0 | 1 |
| 170! | factorial | 170 | valid large number |
| (-3)! | factorial | -3 | Error |
| 3.5! | factorial | 3.5 | Error |
| |-7| | abs | -7 | 7 |

### 2.10 Parentheses
| Test | Expression | Expected |
|------|-----------|----------|
| Simple grouping | (2+3)*4= | 20 |
| Nested | ((2+3)*(4+1))= | 25 |
| Right grouping | 2*(3+4)= | 14 |
| Mismatched | (2+3= | Error |

---

## 3. Programmer Mode Tests (`tests/test_programmer.py`)

### 3.1 Base Conversion
| Test | Input (base) | Target Base | Expected |
|------|-------------|-------------|----------|
| DEC→HEX | 255 (DEC) | HEX | "FF" |
| HEX→DEC | FF (HEX) | DEC | "255" |
| DEC→BIN | 255 (DEC) | BIN | "11111111" |
| DEC→OCT | 255 (DEC) | OCT | "377" |
| HEX→BIN | FF (HEX) | BIN | "11111111" |
| All bases | 255 (DEC) | all | DEC:255, HEX:FF, OCT:377, BIN:11111111 |

### 3.2 Valid Digit Enforcement
| Test | Base | Valid Digits |
|------|------|-------------|
| BIN | BIN | 0, 1 |
| OCT | OCT | 0-7 |
| DEC | DEC | 0-9 |
| HEX | HEX | 0-9, A-F |

### 3.3 Word Size — Ranges
| Test | Word Size | Value | Expected |
|------|----------|-------|----------|
| 8-bit max | 8 | 127 | 127 |
| 8-bit overflow | 8 | 127+1 | -128 |
| 8-bit underflow | 8 | -128-1 | 127 |
| 16-bit max | 16 | 32767 | 32767 |
| 32-bit max | 32 | 2147483647 | 2147483647 |
| Word size change | 64→8 with 300 | 8 | 44 |

### 3.4 Bitwise Operations
| Test | Operation | A | B | Expected |
|------|-----------|---|---|----------|
| AND | AND | 12 | 10 | 8 |
| OR | OR | 12 | 10 | 14 |
| XOR | XOR | 12 | 10 | 6 |
| NOT 0 (8-bit) | NOT | 0 | — | -1 |
| LSH | LSH | 1 | 4 | 16 |
| RSH | RSH | 16 | 2 | 4 |

### 3.5 Integer Arithmetic
| Test | Operation | Expected |
|------|-----------|----------|
| Integer division | 7 / 2 | 3 |
| Modulo | 7 % 2 | 1 |
| Addition | 10 + 20 | 30 |
| Subtraction | 20 - 7 | 13 |
| Multiplication | 6 * 7 | 42 |

### 3.6 Error Cases
| Test | Operation | Expected |
|------|-----------|----------|
| Division by zero | 5 / 0 | Error |
| Modulo by zero | 5 % 0 | Error |

---

## 4. Memory Tests (`tests/test_memory.py`)

### 4.1 Basic Memory Operations
| Test | Sequence | Expected |
|------|----------|----------|
| Store and recall | 5, MS, MR | 5 |
| Memory add | 5, MS, 3, M+, MR | 8 |
| Memory subtract | 10, MS, 3, M-, MR | 7 |
| Memory clear | 5, MS, MC, MR | 0 |
| Has value indicator | MS → has_value=True, MC → has_value=False |

### 4.2 Edge Cases
| Test | Scenario | Expected |
|------|----------|----------|
| Recall empty | MR (no prior store) | 0 |
| Multiple stores | 5 MS, 10 MS, MR | 10 |
| Memory add to empty | 5, M+ (no prior store), MR | 5 |

---

## 5. Mode Switch Tests (`tests/test_mode_switch.py`)

### 5.1 Value Preservation
| Test | From | To | Value | Expected |
|------|------|----|-------|----------|
| Basic→Scientific | Basic | Scientific | 3.14 | 3.14 |
| Scientific→Basic | Scientific | Basic | 2.718 | 2.718 |
| Basic→Programmer | Basic | Programmer | 3.14 | 3 |
| Programmer→Basic | Programmer | Basic | 255 (DEC) | 255 |
| Programmer(HEX)→Basic | Programmer | Basic | FF (HEX) | 255 |

### 5.2 Memory Persistence
| Test | Scenario | Expected |
|------|----------|----------|
| Memory across switch | Store 5 in Basic, switch to Scientific, MR | 5 |
| Memory across all modes | Store in Basic, recall in Programmer | same value (truncated to int) |

---

## 6. Parametrized Test Patterns

Use `@pytest.mark.parametrize` for:
- All arithmetic operations (multiple input pairs)
- All trig functions (multiple angles)
- All base conversions (multiple values)
- All word sizes (boundary values)
- All bitwise operations (multiple operand pairs)

Example:
```python
@pytest.mark.parametrize("a,op,b,expected", [
    (2, "+", 3, 5),
    (10, "-", 3, 7),
    (4, "*", 5, 20),
    (10, "/", 4, 2.5),
])
def test_basic_arithmetic(a, op, b, expected):
    calc = BasicCalculator()
    # ... drive inputs and assert
```
