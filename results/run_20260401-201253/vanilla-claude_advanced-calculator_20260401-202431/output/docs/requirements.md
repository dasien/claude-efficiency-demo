# Advanced Calculator — Requirements Document

**Version:** 1.0
**Target:** Python 3.8+ with Tkinter (stdlib only, no external dependencies)

---

## 1. Overview

A desktop calculator application with three operating modes: **Basic**, **Scientific**, and **Programmer**. The application is modeled after Apple Calculator and Windows Calculator, providing a professional-grade calculation tool with mode switching, memory functions, and comprehensive keyboard support.

---

## 2. Operating Modes

### 2.1 Mode Switching

| ID | Requirement | Priority |
|----|-------------|----------|
| MS-1 | The application must support three modes: Basic, Scientific, and Programmer. | Must-have |
| MS-2 | The user must be able to switch between modes via a menu bar or tab control. | Must-have |
| MS-3 | The current numeric value must be preserved when switching between Basic and Scientific modes. | Must-have |
| MS-4 | When switching to Programmer mode, the current value must be truncated to an integer. | Must-have |
| MS-5 | When switching from Programmer mode, the current integer value must be preserved. | Must-have |
| MS-6 | The window must resize appropriately when switching modes to accommodate the different button layouts. | Must-have |
| MS-7 | The current mode must be visually indicated (e.g., highlighted tab, menu checkmark). | Must-have |

**Acceptance Criteria (MS):**
- Switching from Basic to Scientific preserves the current display value.
- Switching to Programmer from a display showing `3.14` displays `3`.
- Switching from Programmer showing `FF` (hex) to Basic displays `255`.
- The window grows wider for Scientific mode and taller for Programmer mode.

---

## 3. Basic Mode

### 3.1 Arithmetic Operations

| ID | Requirement | Priority |
|----|-------------|----------|
| BA-1 | Addition (+) of two or more operands. | Must-have |
| BA-2 | Subtraction (-) of two or more operands. | Must-have |
| BA-3 | Multiplication (*) of two or more operands. | Must-have |
| BA-4 | Division (/) of two or more operands. | Must-have |
| BA-5 | Operator precedence must be respected: * and / before + and -. | Must-have |
| BA-6 | Chained operations must work (e.g., `2 + 3 * 4 = 14`). | Must-have |

**Acceptance Criteria (BA):**
- `2 + 3 =` produces `5`.
- `10 / 4 =` produces `2.5`.
- `2 + 3 * 4 =` produces `14` (not `20`).
- `100 / 0 =` displays `Error`.

### 3.2 Numeric Input

| ID | Requirement | Priority |
|----|-------------|----------|
| NI-1 | Digit buttons 0-9 must be provided. | Must-have |
| NI-2 | A decimal point button must be provided. | Must-have |
| NI-3 | Only one decimal point per number is allowed. | Must-have |
| NI-4 | Leading zeros must be prevented (e.g., `007` becomes `7`). | Must-have |
| NI-5 | Negative numbers must be supported via a sign toggle (+/-) button. | Must-have |
| NI-6 | A percentage (%) button must divide the current number by 100. | Must-have |

**Acceptance Criteria (NI):**
- Pressing `0`, `0`, `7` displays `7`.
- Pressing `.`, `.`, `5` displays `0.5`.
- Pressing `5`, `+/-` displays `-5`.
- Pressing `2`, `0`, `0`, `%` displays `2`.

### 3.3 Memory Functions

| ID | Requirement | Priority |
|----|-------------|----------|
| MF-1 | **MC** (Memory Clear): Clear the stored memory value to zero. | Must-have |
| MF-2 | **MR** (Memory Recall): Display the stored memory value. | Must-have |
| MF-3 | **M+** (Memory Add): Add the current display value to the stored memory value. | Must-have |
| MF-4 | **M-** (Memory Subtract): Subtract the current display value from the stored memory value. | Must-have |
| MF-5 | **MS** (Memory Store): Store the current display value in memory, replacing any previous value. | Must-have |
| MF-6 | A visual indicator must show when a value is stored in memory (e.g., "M" indicator). | Must-have |
| MF-7 | Memory must persist across mode switches. | Must-have |

**Acceptance Criteria (MF):**
- Press `5`, `MS`. Memory indicator appears. Press `MC`. Memory indicator disappears.
- Press `5`, `MS`, `3`, `M+`, `MR`. Display shows `8`.
- Press `10`, `MS`, `3`, `M-`, `MR`. Display shows `7`.
- Switch to Scientific mode. Press `MR`. Display shows previously stored value.

### 3.4 Display

| ID | Requirement | Priority |
|----|-------------|----------|
| DI-1 | A primary display shows the current number or result. | Must-have |
| DI-2 | A secondary display (expression line) shows the expression being built. | Should-have |
| DI-3 | Integer results must display without a decimal point (e.g., `5` not `5.0`). | Must-have |
| DI-4 | Float results must display with reasonable precision (max 10 significant digits). | Must-have |
| DI-5 | Very large or very small numbers must display in scientific notation. | Must-have |
| DI-6 | The display must handle overflow gracefully (truncation or scrolling). | Must-have |

**Acceptance Criteria (DI):**
- `4 / 2 =` displays `2` (not `2.0`).
- `1 / 3 =` displays `0.3333333333` (10 digits).
- `9999999999 * 9999999999 =` displays in scientific notation.

### 3.5 Clear and Edit

| ID | Requirement | Priority |
|----|-------------|----------|
| CE-1 | **C** (Clear): Reset the current entry to `0` without clearing the pending operation. | Must-have |
| CE-2 | **AC** (All Clear): Reset all state — display, pending operation, expression. | Must-have |
| CE-3 | **Backspace**: Delete the last digit or character from the current entry. | Must-have |

**Acceptance Criteria (CE):**
- Press `5`, `+`, `3`, `C`. Display shows `0`. Press `2`, `=`. Display shows `7` (5+2).
- Press `5`, `+`, `3`, `AC`. Display shows `0`. Press `2`, `=`. Display shows `2`.
- Press `1`, `2`, `3`, `Backspace`. Display shows `12`.

### 3.6 Basic Mode GUI Layout

```
+---------------------------------------+
|  [Expression display]                 |
|  [Result display          ]           |
+---------------------------------------+
| MC  | MR  | M+  | M-  | MS          |
+-----+-----+-----+-----+-------------+
|  C  | +/- |  %  |  /  |             |
+-----+-----+-----+-----+             |
|  7  |  8  |  9  |  *  |             |
+-----+-----+-----+-----+             |
|  4  |  5  |  6  |  -  |             |
+-----+-----+-----+-----+             |
|  1  |  2  |  3  |  +  |             |
+-----+-----+-----+-----+-------------+
|     0     |  .  |  =  |             |
+-----------+-----+-----+-------------+
```

- The `0` button spans two columns.
- Operator buttons are in the rightmost column.
- Memory buttons are in a row above the main grid.

---

## 4. Scientific Mode

Scientific mode extends Basic mode with additional mathematical functions. All Basic mode features remain available.

### 4.1 Trigonometric Functions

| ID | Requirement | Priority |
|----|-------------|----------|
| TR-1 | **sin**: Compute the sine of the current value. | Must-have |
| TR-2 | **cos**: Compute the cosine of the current value. | Must-have |
| TR-3 | **tan**: Compute the tangent of the current value. | Must-have |
| TR-4 | **asin**: Compute the inverse sine (arcsin) of the current value. | Must-have |
| TR-5 | **acos**: Compute the inverse cosine (arccos) of the current value. | Must-have |
| TR-6 | **atan**: Compute the inverse tangent (arctan) of the current value. | Must-have |
| TR-7 | A **Deg/Rad** toggle must switch between degree and radian mode. | Must-have |
| TR-8 | The current angle mode (Deg or Rad) must be visually indicated. | Must-have |

**Acceptance Criteria (TR):**
- In Degree mode: `sin(90)` = `1`.
- In Radian mode: `sin(3.14159265)` ≈ `0` (within floating-point tolerance).
- `asin(1)` in Degree mode = `90`.
- `tan(90)` in Degree mode displays `Error` (undefined).

### 4.2 Logarithmic Functions

| ID | Requirement | Priority |
|----|-------------|----------|
| LG-1 | **log**: Compute the base-10 logarithm. | Must-have |
| LG-2 | **ln**: Compute the natural logarithm (base e). | Must-have |
| LG-3 | **log₂**: Compute the base-2 logarithm. | Must-have |

**Acceptance Criteria (LG):**
- `log(100)` = `2`.
- `ln(e)` = `1` (where e ≈ 2.71828).
- `log₂(256)` = `8`.
- `log(0)` displays `Error`.
- `log(-1)` displays `Error`.

### 4.3 Power and Root Functions

| ID | Requirement | Priority |
|----|-------------|----------|
| PW-1 | **x²**: Square the current value. | Must-have |
| PW-2 | **x³**: Cube the current value. | Must-have |
| PW-3 | **xⁿ**: Raise x to the power of n (two-operand). | Must-have |
| PW-4 | **10ˣ**: Compute 10 raised to the current value. | Must-have |
| PW-5 | **eˣ**: Compute e raised to the current value. | Must-have |
| PW-6 | **√x**: Compute the square root. | Must-have |
| PW-7 | **³√x**: Compute the cube root. | Must-have |
| PW-8 | **1/x**: Compute the reciprocal. | Must-have |

**Acceptance Criteria (PW):**
- `5`, `x²` = `25`.
- `2`, `xⁿ`, `10`, `=` = `1024`.
- `10ˣ` with value `3` = `1000`.
- `√x` with value `144` = `12`.
- `√x` with value `-1` displays `Error`.
- `1/x` with value `0` displays `Error`.

### 4.4 Constants and Special Values

| ID | Requirement | Priority |
|----|-------------|----------|
| CO-1 | **π**: Insert the value of pi (3.14159265358979...). | Must-have |
| CO-2 | **e**: Insert the value of Euler's number (2.71828182845905...). | Must-have |

**Acceptance Criteria (CO):**
- Pressing `π` displays `3.14159265359` (or similar precision).
- Pressing `e` then `eˣ` displays `15.1542622414` (e^e).

### 4.5 Factorial and Absolute Value

| ID | Requirement | Priority |
|----|-------------|----------|
| FA-1 | **n!**: Compute the factorial of the current integer value. | Must-have |
| FA-2 | Factorial of negative numbers must display `Error`. | Must-have |
| FA-3 | Factorial of non-integer values must display `Error`. | Must-have |
| FA-4 | **|x|**: Compute the absolute value of the current value. | Must-have |

**Acceptance Criteria (FA):**
- `5`, `n!` = `120`.
- `0`, `n!` = `1`.
- `-3`, `n!` displays `Error`.
- `3.5`, `n!` displays `Error`.
- `-7`, `|x|` = `7`.

### 4.6 Parentheses

| ID | Requirement | Priority |
|----|-------------|----------|
| PA-1 | Open `(` and close `)` parenthesis buttons must be provided. | Must-have |
| PA-2 | Parentheses must correctly group sub-expressions. | Must-have |
| PA-3 | Mismatched parentheses must display `Error`. | Must-have |
| PA-4 | A counter or indicator should show the current nesting depth. | Should-have |

**Acceptance Criteria (PA):**
- `(2 + 3) * 4 =` produces `20`.
- `2 * (3 + 4) =` produces `14`.
- `((2 + 3) * (4 + 1)) =` produces `25`.
- `(2 + 3 =` displays `Error` (mismatched parentheses).

### 4.7 Scientific Mode GUI Layout

The Scientific mode extends the Basic layout with additional button columns on the left:

```
+-----------------------------------------------------------+
|  [Expression display]                                     |
|  [Result display                            ] [Deg/Rad]   |
+-----------------------------------------------------------+
| MC  | MR  | M+  | M-  | MS                               |
+-----+-----+-----+-----+-----+-----+-----+-----+----------+
|  (  |  )  | x²  | x³  | xⁿ  |  C  | +/- |  %  |  /     |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+---+
| sin | cos | tan  | √x  | ³√x |  7  |  8  |  9  |  *     |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+---+
| asin| acos| atan | 10ˣ | eˣ  |  4  |  5  |  6  |  -     |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+---+
| n!  | |x| | log  | ln  | log₂|  1  |  2  |  3  |  +     |
+-----+-----+-----+-----+-----+-----+-----+-----+-----+---+
|  π  |  e  | 1/x  |     |     |     0     |  .  |  =     |
+-----+-----+-----+-----+-----+-----------+-----+---------+
```

---

## 5. Programmer Mode

Programmer mode replaces the Basic/Scientific layout with integer arithmetic in multiple number bases.

### 5.1 Number Base Modes

| ID | Requirement | Priority |
|----|-------------|----------|
| NB-1 | **DEC** (Decimal): Standard base-10 input and display. | Must-have |
| NB-2 | **HEX** (Hexadecimal): Base-16 input and display (0-9, A-F). | Must-have |
| NB-3 | **OCT** (Octal): Base-8 input and display (0-7). | Must-have |
| NB-4 | **BIN** (Binary): Base-2 input and display (0-1). | Must-have |
| NB-5 | The current base mode must be visually indicated (e.g., radio buttons or highlighted label). | Must-have |
| NB-6 | Switching bases must convert and display the current value in the new base. | Must-have |
| NB-7 | A base conversion panel must show the current value in ALL four bases simultaneously. | Must-have |
| NB-8 | Only valid digits for the current base must be enabled (e.g., in BIN mode, only 0 and 1). | Must-have |

**Acceptance Criteria (NB):**
- Enter `255` in DEC. Switch to HEX. Display shows `FF`.
- Enter `FF` in HEX. Switch to DEC. Display shows `255`.
- Enter `FF` in HEX. Switch to BIN. Display shows `11111111`.
- In BIN mode, digit buttons 2-9 and A-F are disabled.
- In OCT mode, digit buttons 8-9 and A-F are disabled.
- The base conversion panel shows `DEC: 255 | HEX: FF | OCT: 377 | BIN: 11111111` simultaneously.

### 5.2 Hex Digit Buttons

| ID | Requirement | Priority |
|----|-------------|----------|
| HX-1 | Buttons for hex digits A, B, C, D, E, F must be provided. | Must-have |
| HX-2 | Hex digit buttons must only be enabled in HEX mode. | Must-have |
| HX-3 | Hex digits must display as uppercase. | Must-have |

### 5.3 Word Size

| ID | Requirement | Priority |
|----|-------------|----------|
| WS-1 | The user must be able to select word size: 8-bit, 16-bit, 32-bit, or 64-bit. | Must-have |
| WS-2 | Values must be constrained to the selected word size range. | Must-have |
| WS-3 | Overflow must wrap around (two's complement behavior). | Must-have |
| WS-4 | The current word size must be visually indicated. | Must-have |

**Word size ranges (signed, two's complement):**

| Word Size | Min | Max |
|-----------|-----|-----|
| 8-bit | -128 | 127 |
| 16-bit | -32,768 | 32,767 |
| 32-bit | -2,147,483,648 | 2,147,483,647 |
| 64-bit | -9,223,372,036,854,775,808 | 9,223,372,036,854,775,807 |

**Acceptance Criteria (WS):**
- In 8-bit mode: `127 + 1 =` produces `-128` (overflow wraps).
- In 8-bit mode: entering `256` is not possible or wraps to `0`.
- Switching from 64-bit to 8-bit with value `300` truncates to 8-bit representation (`44`).

### 5.4 Bitwise Operations

| ID | Requirement | Priority |
|----|-------------|----------|
| BW-1 | **AND**: Bitwise AND of two operands. | Must-have |
| BW-2 | **OR**: Bitwise OR of two operands. | Must-have |
| BW-3 | **XOR**: Bitwise exclusive OR of two operands. | Must-have |
| BW-4 | **NOT**: Bitwise complement of the current value. | Must-have |
| BW-5 | **LSH** (Left Shift): Shift bits left by n positions. | Must-have |
| BW-6 | **RSH** (Right Shift): Arithmetic right shift by n positions. | Must-have |

**Acceptance Criteria (BW):**
- `12 AND 10 =` produces `8` (binary: `1100 AND 1010 = 1000`).
- `12 OR 10 =` produces `14` (binary: `1100 OR 1010 = 1110`).
- `12 XOR 10 =` produces `6` (binary: `1100 XOR 1010 = 0110`).
- `NOT 0` in 8-bit = `-1` (all bits set, two's complement).
- `1 LSH 4 =` produces `16`.
- `16 RSH 2 =` produces `4`.

### 5.5 Programmer Mode Arithmetic

| ID | Requirement | Priority |
|----|-------------|----------|
| PM-1 | Integer addition, subtraction, multiplication, and division must be supported. | Must-have |
| PM-2 | Division must be integer division (truncating, not floor). | Must-have |
| PM-3 | No decimal point is allowed in Programmer mode. | Must-have |
| PM-4 | Modulo (%) operation must be supported. | Must-have |

**Acceptance Criteria (PM):**
- `7 / 2 =` produces `3` (integer division).
- `7 % 2 =` produces `1`.
- The decimal point button is disabled in Programmer mode.

### 5.6 Programmer Mode GUI Layout

```
+-----------------------------------------------------------+
|  [Expression display]                                     |
|  [Result display                            ] [Word: 64]  |
+-----------------------------------------------------------+
|  HEX: FF        DEC: 255       OCT: 377     BIN: 11111111|
+-----------------------------------------------------------+
| (DEC) (HEX) (OCT) (BIN)     <-- base selector            |
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
|  A  |  B  |  C  |  D  |  E  |  F  | AND | OR  |  AC     |
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
| NOT | XOR | LSH | RSH |  %  |  C  | +/- | MOD |  /      |
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
|     |     |     |     |     |  7  |  8  |  9  |  *      |
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
|     |     |     |     |     |  4  |  5  |  6  |  -      |
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
|     |     |     |     |     |  1  |  2  |  3  |  +      |
+-----+-----+-----+-----+-----+-----+-----+-----+---------+
|                               |     0     |  = |  ⌫     |
+-------------------------------+-----------+----+---------+
```

---

## 6. Keyboard Support

### 6.1 Universal Keyboard Shortcuts

| Key(s) | Action | All Modes |
|--------|--------|-----------|
| `0`-`9` | Enter digit | Yes |
| `.` | Enter decimal point | Basic/Scientific only |
| `+` | Addition | Yes |
| `-` | Subtraction | Yes |
| `*` | Multiplication | Yes |
| `/` | Division | Yes |
| `Enter` or `Return` | Evaluate (equals) | Yes |
| `Escape` | All Clear | Yes |
| `Backspace` or `Delete` | Delete last character | Yes |
| `(` | Open parenthesis | Scientific only |
| `)` | Close parenthesis | Scientific only |

### 6.2 Programmer Mode Keyboard Shortcuts

| Key(s) | Action |
|--------|--------|
| `a`-`f` or `A`-`F` | Enter hex digit (HEX mode only) |
| `&` | AND |
| `\|` | OR |
| `^` | XOR |
| `~` | NOT |
| `<` | Left Shift |
| `>` | Right Shift |
| `%` | Modulo |

### 6.3 Mode Switching Keyboard Shortcuts

| Key(s) | Action |
|--------|--------|
| `Ctrl+1` | Switch to Basic mode |
| `Ctrl+2` | Switch to Scientific mode |
| `Ctrl+3` | Switch to Programmer mode |

---

## 7. Error Handling

### 7.1 Error Conditions

| ID | Condition | Expected Behavior |
|----|-----------|-------------------|
| ER-1 | Division by zero | Display `Error`. Return to normal on next input or Clear. |
| ER-2 | Invalid mathematical operation (e.g., `√(-1)`, `log(0)`) | Display `Error`. |
| ER-3 | Overflow beyond word size (Programmer mode) | Wrap using two's complement. |
| ER-4 | Factorial of negative or non-integer | Display `Error`. |
| ER-5 | Mismatched parentheses | Display `Error`. |
| ER-6 | Malformed expression (e.g., consecutive operators) | Display `Error` or handle gracefully. |
| ER-7 | `tan(90°)` (undefined) | Display `Error`. |

### 7.2 Error Recovery

| ID | Requirement | Priority |
|----|-------------|----------|
| RC-1 | After an error, pressing any digit must clear the error and start a new number. | Must-have |
| RC-2 | After an error, pressing `C` or `AC` must clear the error. | Must-have |
| RC-3 | The application must never crash or show a Python traceback. | Must-have |

---

## 8. Non-Functional Requirements

### 8.1 Performance

| ID | Requirement |
|----|-------------|
| NF-1 | All button presses and display updates must respond within 100ms. |
| NF-2 | Expression evaluation must complete within 500ms for any valid input. |
| NF-3 | Application startup must complete within 3 seconds. |
| NF-4 | Factorial must handle values up to at least `n=170` (limit of float). |

### 8.2 Code Quality

| ID | Requirement |
|----|-------------|
| NF-5 | Business logic must be completely separated from GUI code. |
| NF-6 | Each calculator mode's logic must be in its own module. |
| NF-7 | All business logic must be unit-testable without instantiating Tkinter. |
| NF-8 | Code must follow PEP 8 style guidelines. |
| NF-9 | All public functions must have type hints. |
| NF-10 | All public functions must have docstrings. |

### 8.3 Architecture

| ID | Requirement |
|----|-------------|
| NF-11 | The application must follow an MVC or MVP pattern. |
| NF-12 | The GUI layer must depend on the logic layer, never the reverse. |
| NF-13 | Mode-specific logic must be encapsulated in separate classes or modules. |
| NF-14 | A shared base class or interface should define common calculator operations. |

### 8.4 Compatibility

| ID | Requirement |
|----|-------------|
| NF-15 | Must run on Python 3.8+. |
| NF-16 | Must use only the Python standard library (tkinter is included). |
| NF-17 | No external dependencies for the application (pytest is allowed for testing only). |
| NF-18 | Must run on macOS, Windows, and Linux where Python and Tkinter are available. |

---

## 9. Testing Requirements

### 9.1 Test Coverage

| ID | Requirement |
|----|-------------|
| TS-1 | Unit tests must cover all arithmetic operations in all modes. |
| TS-2 | Unit tests must cover all scientific functions (trig, log, powers, roots). |
| TS-3 | Unit tests must cover all programmer operations (bitwise, base conversion, word size). |
| TS-4 | Unit tests must cover memory functions. |
| TS-5 | Unit tests must cover error conditions (division by zero, overflow, invalid operations). |
| TS-6 | Unit tests must cover mode switching with value preservation. |
| TS-7 | Unit tests must cover edge cases (boundary values, extreme inputs). |
| TS-8 | All tests must pass using `python3 -m pytest`. |

### 9.2 Test Organization

| ID | Requirement |
|----|-------------|
| TS-9 | Tests must be organized by mode (basic, scientific, programmer). |
| TS-10 | Tests must be organized by category within each mode (happy path, edge cases, errors). |
| TS-11 | Tests must use `pytest.mark.parametrize` for operations with multiple input/output pairs. |
| TS-12 | No test may depend on another test's state. |

---

## 10. Suggested File Structure

```
project/
├── calculator/
│   ├── __init__.py
│   ├── app.py              # Main application entry point, mode switching
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── base_view.py    # Shared GUI components (display, common buttons)
│   │   ├── basic_view.py   # Basic mode button layout
│   │   ├── scientific_view.py  # Scientific mode button layout
│   │   └── programmer_view.py  # Programmer mode button layout
│   └── logic/
│       ├── __init__.py
│       ├── base_logic.py   # Shared logic (memory, display formatting)
│       ├── basic_logic.py  # Basic arithmetic, expression evaluation
│       ├── scientific_logic.py  # Scientific functions
│       └── programmer_logic.py  # Base conversion, bitwise operations, word size
├── tests/
│   ├── __init__.py
│   ├── test_basic.py       # Basic mode tests
│   ├── test_scientific.py  # Scientific mode tests
│   ├── test_programmer.py  # Programmer mode tests
│   ├── test_memory.py      # Memory function tests
│   └── test_mode_switch.py # Mode switching tests
├── main.py                 # Entry point: `python3 main.py`
└── requirements.txt        # pytest (for testing only)
```

This structure is a suggestion. The implementation may adjust it based on architectural decisions, but the separation between `gui/` and `logic/` is mandatory per NF-5, NF-12.

---

## 11. Acceptance Summary

The implementation is complete when:

1. All three modes (Basic, Scientific, Programmer) are functional with their specified buttons and operations.
2. Mode switching preserves values appropriately.
3. Memory functions work across all modes.
4. All keyboard shortcuts function as specified.
5. All error conditions are handled gracefully (no crashes, no tracebacks).
6. The base conversion panel in Programmer mode shows all four bases simultaneously.
7. Word size selection correctly constrains values with two's complement overflow.
8. Business logic is fully separated from GUI and independently testable.
9. All unit tests pass with `python3 -m pytest`.
10. The application runs on Python 3.8+ with no external dependencies.
