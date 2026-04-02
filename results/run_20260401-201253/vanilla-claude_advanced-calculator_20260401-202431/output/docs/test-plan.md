# Test Plan — Advanced Calculator

## Test Strategy

- All tests target the **logic layer only** — no Tkinter instantiation required.
- Tests use `pytest` with `pytest.mark.parametrize` for multi-input operations.
- Each test is independent (no shared mutable state between tests).
- Tests organized by mode, then by category (happy path, edge cases, errors).

## Test Files

### 1. `tests/test_basic.py` — Basic Mode

#### Happy Path - Arithmetic
| Test | Input Sequence | Expected |
|------|---------------|----------|
| Addition | 2 + 3 = | 5 |
| Subtraction | 10 - 3 = | 7 |
| Multiplication | 4 * 5 = | 20 |
| Division | 10 / 4 = | 2.5 |
| Operator precedence | 2 + 3 * 4 = | 14 |
| Chained operations | 1 + 2 + 3 = | 6 |
| Multiple precedence | 2 * 3 + 4 * 5 = | 26 |

#### Happy Path - Numeric Input
| Test | Input Sequence | Expected Display |
|------|---------------|-----------------|
| Single digit | 5 | "5" |
| Multi digit | 1, 2, 3 | "123" |
| Decimal | 3, ., 1, 4 | "3.14" |
| Leading zero prevention | 0, 0, 7 | "7" |
| Decimal leading zero | ., 5 | "0.5" |
| Sign toggle | 5, +/- | "-5" |
| Percent | 200, % | "2" |

#### Happy Path - Display Formatting
| Test | Operation | Expected |
|------|-----------|----------|
| Integer result | 4 / 2 = | "2" (not "2.0") |
| Float result | 1 / 3 = | "0.3333333333" |
| Scientific notation | 9999999999 * 9999999999 = | scientific notation string |

#### Happy Path - Clear/Edit
| Test | Sequence | Expected |
|------|----------|----------|
| Clear entry | 5, +, 3, C, 2, = | 7 |
| All clear | 5, +, 3, AC, 2, = | 2 |
| Backspace | 1, 2, 3, backspace | "12" |

#### Edge Cases
| Test | Input | Expected |
|------|-------|----------|
| Double decimal ignored | 1, ., ., 5 | "1.5" |
| Backspace to empty | 5, backspace | "0" |
| Equals with no op | 5, = | 5 |
| Operator then equals | 5, +, = | 10 (repeat operand) |
| Sign toggle zero | 0, +/- | "0" |

#### Error Cases
| Test | Input | Expected |
|------|-------|----------|
| Division by zero | 5, /, 0, = | Error |
| Error recovery digit | (after error), 5 | "5" (error cleared) |
| Error recovery clear | (after error), C | "0" (error cleared) |

### 2. `tests/test_scientific.py` — Scientific Mode

#### Happy Path - Trigonometry (Degrees)
| Test | Input | Expected |
|------|-------|----------|
| sin(0) | 0, sin | 0 |
| sin(90) | 90, sin | 1 |
| cos(0) | 0, cos | 1 |
| cos(90) | 90, cos | 0 |
| tan(45) | 45, tan | 1 |
| asin(1) | 1, asin | 90 |
| acos(1) | 1, acos | 0 |
| atan(1) | 1, atan | 45 |

#### Happy Path - Trigonometry (Radians)
| Test | Input | Expected |
|------|-------|----------|
| sin(π) | π, sin | ≈0 |
| cos(π) | π, cos | -1 |
| sin(π/2) | (manual 1.5707...), sin | ≈1 |

#### Happy Path - Logarithms
| Test | Input | Expected |
|------|-------|----------|
| log(100) | 100, log | 2 |
| ln(e) | e, ln | 1 |
| log₂(256) | 256, log2 | 8 |

#### Happy Path - Powers and Roots
| Test | Input | Expected |
|------|-------|----------|
| 5² | 5, x² | 25 |
| 2³ | 2, x³ | 8 |
| 2¹⁰ | 2, xⁿ, 10, = | 1024 |
| 10³ | 3, 10ˣ | 1000 |
| e¹ | 1, eˣ | ≈2.71828 |
| √144 | 144, √x | 12 |
| ³√27 | 27, ³√x | 3 |
| 1/4 | 4, 1/x | 0.25 |

#### Happy Path - Factorial and Absolute
| Test | Input | Expected |
|------|-------|----------|
| 5! | 5, n! | 120 |
| 0! | 0, n! | 1 |
| \|-7\| | -7, \|x\| | 7 |
| 170! | 170, n! | valid large number |

#### Happy Path - Constants
| Test | Input | Expected |
|------|-------|----------|
| π | π | ≈3.14159265359 |
| e | e | ≈2.71828182846 |

#### Happy Path - Parentheses
| Test | Expression | Expected |
|------|-----------|----------|
| (2+3)*4 | (, 2, +, 3, ), *, 4, = | 20 |
| 2*(3+4) | 2, *, (, 3, +, 4, ), = | 14 |
| Nested | (, (, 2, +, 3, ), *, (, 4, +, 1, ), ), = | 25 |

#### Edge Cases
| Test | Input | Expected |
|------|-------|----------|
| sin(0) radians | toggle to RAD, 0, sin | 0 |
| Very small trig result | sin(π) in rad | ≈0 (within tolerance) |
| Large factorial | 170, n! | no error |

#### Error Cases
| Test | Input | Expected |
|------|-------|----------|
| √(-1) | -1, √x | Error |
| log(0) | 0, log | Error |
| log(-1) | -1, log | Error |
| ln(0) | 0, ln | Error |
| tan(90°) | 90, tan (deg mode) | Error |
| (-3)! | -3, n! | Error |
| 3.5! | 3.5, n! | Error |
| 1/0 | 0, 1/x | Error |
| Mismatched parens | (, 2, +, 3, = | Error |

### 3. `tests/test_programmer.py` — Programmer Mode

#### Happy Path - Base Conversion
| Test | Value (DEC) | HEX | OCT | BIN |
|------|------------|-----|-----|-----|
| 255 | 255 | FF | 377 | 11111111 |
| 0 | 0 | 0 | 0 | 0 |
| 16 | 16 | 10 | 20 | 10000 |
| -1 (8-bit) | -1 | FF | 377 | 11111111 |

#### Happy Path - Arithmetic
| Test | Operation | Expected |
|------|-----------|----------|
| 7 / 2 | integer division | 3 |
| 7 % 2 | modulo | 1 |
| 10 + 5 | addition | 15 |
| 10 - 5 | subtraction | 5 |
| 3 * 4 | multiplication | 12 |

#### Happy Path - Bitwise Operations
| Test | Operation | Expected |
|------|-----------|----------|
| 12 AND 10 | bitwise AND | 8 |
| 12 OR 10 | bitwise OR | 14 |
| 12 XOR 10 | bitwise XOR | 6 |
| NOT 0 (8-bit) | bitwise NOT | -1 |
| 1 LSH 4 | left shift | 16 |
| 16 RSH 2 | right shift | 4 |

#### Happy Path - Hex Input
| Test | Input (HEX mode) | DEC equivalent |
|------|------------------|----------------|
| FF | F, F | 255 |
| A0 | A, 0 | 160 |

#### Happy Path - Word Size
| Test | Word Size | Value | Expected |
|------|-----------|-------|----------|
| 8-bit max | 8 | 127 | 127 |
| 8-bit overflow | 8 | 127 + 1 | -128 |
| Truncation 64→8 | change to 8-bit | 300 | 44 |

#### Edge Cases
| Test | Input | Expected |
|------|-------|----------|
| Base switch preserves value | 255 DEC → HEX | "FF" |
| HEX → BIN | FF HEX → BIN | "11111111" |
| Word size boundary | 8-bit, -128 - 1 | 127 (wraps) |
| NOT NOT x | NOT(NOT(5)) 8-bit | 5 |
| Shift by 0 | 5 LSH 0 | 5 |

#### Error Cases
| Test | Input | Expected |
|------|-------|----------|
| Division by zero | 5, /, 0, = | Error |

### 4. `tests/test_memory.py` — Memory Functions

#### Happy Path
| Test | Sequence | Expected |
|------|----------|----------|
| Store and recall | 5, MS, MR | 5 |
| Memory add | 5, MS, 3, M+, MR | 8 |
| Memory subtract | 10, MS, 3, M-, MR | 7 |
| Memory clear | 5, MS, MC, has_memory | False |
| Memory indicator | 5, MS | has_memory = True |

#### Cross-Mode Memory
| Test | Sequence | Expected |
|------|----------|----------|
| Basic → Scientific | Store 5 in basic, recall in scientific | 5 |
| Basic → Programmer | Store 5 in basic, recall in programmer | 5 |

### 5. `tests/test_mode_switch.py` — Mode Switching

#### Value Preservation
| Test | From | To | Input Value | Expected |
|------|------|----|------------|----------|
| Basic → Scientific | Basic | Scientific | 3.14 | 3.14 |
| Scientific → Basic | Scientific | Basic | 2.5 | 2.5 |
| Basic → Programmer | Basic | Programmer | 3.14 | 3 (truncated) |
| Programmer → Basic | Programmer | Basic | 255 | 255 |
| Programmer HEX → Basic | Programmer (HEX, FF) | Basic | FF | 255 |

## Running Tests

```bash
python3 -m pytest tests/ -v
```

All tests must pass with zero failures.
