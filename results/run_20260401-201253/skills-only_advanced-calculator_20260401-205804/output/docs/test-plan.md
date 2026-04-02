# Test Plan — Advanced Calculator

## Strategy

- All tests target the **logic layer only** — no Tkinter instantiation required.
- Tests instantiate logic classes directly and call their methods.
- Use `pytest.mark.parametrize` for operations with multiple input/output pairs.
- Tests are independent — no shared mutable state between tests.
- Run with: `python3 -m pytest`

## Test Organization

```
tests/
├── __init__.py
├── test_basic.py           # Basic mode logic
├── test_scientific.py      # Scientific mode logic
├── test_programmer.py      # Programmer mode logic
├── test_memory.py          # Memory functions (all modes)
└── test_mode_switch.py     # Mode switching value preservation
```

---

## test_basic.py — Basic Mode

### Happy Path
- **Arithmetic**: 2+3=5, 10-3=7, 4*5=20, 10/4=2.5
- **Operator precedence**: 2+3*4=14, 10-2*3=4, 2*3+4*5=26
- **Chained operations**: 1+2+3=6, 10/2*3=15
- **Decimal input**: 0.5+0.5=1, 3.14*2=6.28
- **Percentage**: 200%=2, 50+50%=0.5 (50% of current)
- **Sign toggle**: 5→-5→5

### Input Handling
- **Leading zeros**: 007→7
- **Single decimal**: 1..5→1.5 (second dot ignored)
- **Backspace**: 123→12→1→0
- **Clear entry (C)**: 5+3,C,2,=→7 (preserves pending op)
- **All clear (AC)**: 5+3,AC,2,=→2 (resets everything)

### Display Formatting
- **Integer display**: 4/2=2 (not 2.0)
- **Precision**: 1/3=0.3333333333 (10 significant digits)
- **Scientific notation**: 9999999999*9999999999 → scientific notation

### Error Cases
- **Division by zero**: 100/0=Error
- **Error recovery digit**: Error→press 5→displays 5
- **Error recovery clear**: Error→press C→displays 0

---

## test_scientific.py — Scientific Mode

### Trigonometric Functions (parametrized by angle mode)

#### Degree Mode
- sin(0)=0, sin(90)=1, sin(180)=0, sin(270)=-1
- cos(0)=1, cos(90)=0, cos(180)=-1
- tan(0)=0, tan(45)=1
- asin(1)=90, acos(1)=0, atan(1)=45

#### Radian Mode
- sin(0)=0, sin(π/2)=1, sin(π)≈0
- cos(0)=1, cos(π)=-1
- tan(0)=0

### Logarithmic Functions
- log(100)=2, log(1000)=3
- ln(e)=1, ln(1)=0
- log₂(256)=8, log₂(1)=0

### Power and Root Functions
- 5²=25, 3³=27
- 2^10=1024
- 10^3=1000, e^1≈2.71828
- √144=12, √0=0
- ³√27=3, ³√-8=-2
- 1/4=0.25, 1/0.5=2

### Constants
- π≈3.14159265359
- e≈2.71828182846

### Factorial and Absolute Value
- 0!=1, 1!=1, 5!=120, 10!=3628800, 170!=large number
- |-7|=7, |0|=0, |5|=5

### Parentheses
- (2+3)*4=20
- 2*(3+4)=14
- ((2+3)*(4+1))=25
- Nested: ((1+2)*(3+4))=21

### Error Cases
- tan(90°)=Error
- √(-1)=Error
- log(0)=Error, log(-1)=Error, ln(0)=Error
- (-3)!=Error, 3.5!=Error
- 1/0=Error
- Mismatched parens: (2+3=Error

---

## test_programmer.py — Programmer Mode

### Base Conversion (parametrized)
- DEC 255 → HEX FF, OCT 377, BIN 11111111
- DEC 0 → HEX 0, OCT 0, BIN 0
- DEC -1 (8-bit) → display as two's complement
- HEX FF → DEC 255
- BIN 1010 → DEC 10, HEX A

### Digit Validation
- BIN mode: only 0,1 accepted; 2-9,A-F rejected
- OCT mode: only 0-7 accepted; 8-9,A-F rejected
- DEC mode: only 0-9 accepted; A-F rejected
- HEX mode: 0-9,A-F all accepted

### Word Size
- 8-bit range: -128 to 127
- 16-bit range: -32768 to 32767
- 32-bit range: -2147483648 to 2147483647
- 64-bit range: full signed 64-bit range

### Two's Complement Overflow
- 8-bit: 127+1=-128
- 8-bit: -128-1=127
- 16-bit: 32767+1=-32768
- Word size change: 64-bit 300 → 8-bit 44

### Bitwise Operations
- 12 AND 10 = 8
- 12 OR 10 = 14
- 12 XOR 10 = 6
- NOT 0 (8-bit) = -1
- NOT 1 (8-bit) = -2
- 1 LSH 4 = 16
- 16 RSH 2 = 4

### Integer Arithmetic
- 7/2=3 (truncating division)
- 7%2=1 (modulo)
- -7/2=-3 (truncating, not floor)
- 10+20=30, 20-30=-10
- 3*4=12

### Error Cases
- Division by zero: 5/0=Error
- Modulo by zero: 5%0=Error

---

## test_memory.py — Memory Functions

### Basic Memory Operations
- MS stores, MR recalls: store 5, recall→5
- MC clears: store 5, MC, recall→0
- M+ adds: store 5, enter 3, M+, recall→8
- M- subtracts: store 10, enter 3, M-, recall→7
- has_memory flag: false initially, true after MS, false after MC

### Memory Across Modes
- Store in Basic, recall in Scientific → same value
- Store in Scientific, recall in Basic → same value
- Store float, switch to Programmer, recall → integer truncation of memory value
- Memory persists through mode switches

---

## test_mode_switch.py — Mode Switching

### Value Preservation
- Basic 3.14 → Scientific: displays 3.14
- Scientific 2.5 → Basic: displays 2.5
- Basic 3.14 → Programmer: displays 3 (truncated)
- Programmer 255 (DEC) → Basic: displays 255
- Programmer FF (HEX) → Basic: displays 255

### State Reset
- Expression state is cleared on mode switch
- Error state is cleared on mode switch
- Memory is preserved on mode switch

---

## Floating Point Comparison

For floating-point results, tests use `pytest.approx()` with appropriate tolerance (default rel=1e-9).
