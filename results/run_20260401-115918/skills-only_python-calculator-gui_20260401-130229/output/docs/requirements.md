# Calculator Application — Requirements Document

## 1. Functional Requirements

### FR-1: Numeric Input
- The calculator must accept digits 0-9 via GUI buttons and keyboard input.
- The calculator must accept a decimal point (`.`) to support floating-point numbers.
- Multiple digits can be entered sequentially to form multi-digit numbers (e.g., `123`).
- Only one decimal point is allowed per number (pressing `.` again is ignored if the current number already contains one).

**Acceptance criteria:** User can enter any valid integer or floating-point number via buttons or keyboard.

### FR-2: Arithmetic Operations
- The calculator must support four operations:
  - Addition (`+`)
  - Subtraction (`-`)
  - Multiplication (`*`)
  - Division (`/`)
- Pressing an operator stores the current number and the chosen operation, then prepares the display for the next operand.
- Pressing an operator after another operator (without entering a new number) replaces the previous operator.

**Acceptance criteria:** Each operator correctly computes the result when combined with two operands.

### FR-3: Expression Evaluation
- Pressing the equals button (`=`) or the Enter key evaluates the current expression and displays the result.
- After evaluation, the result becomes the starting point for a new expression (chaining).
- Pressing `=` with no pending operation does nothing beyond re-displaying the current value.

**Acceptance criteria:** `5 + 3 =` displays `8`; the user can then press `+ 2 =` to get `10`.

### FR-4: Display
- A text display at the top of the calculator shows the current input and results.
- The display updates in real time as the user types digits or selects operators.
- Results are shown as integers when there is no fractional part (e.g., `8` not `8.0`).
- Results with fractional parts display as floats (e.g., `7.5`).

**Acceptance criteria:** Display always reflects the current state — current number being entered or most recent result.

### FR-5: Clear
- A `C` button resets the calculator to its initial state (display shows `0`, all pending operations are cleared).
- The Escape key also triggers a clear.

**Acceptance criteria:** After pressing `C`, the display shows `0` and no prior state affects the next calculation.

### FR-6: Keyboard Input
- Number keys (`0`-`9`) enter digits.
- `.` enters a decimal point.
- `+`, `-`, `*`, `/` select operators.
- `Enter` or `=` evaluates the expression.
- `Escape` clears the calculator.
- `Backspace` deletes the last entered digit.

**Acceptance criteria:** Every keyboard shortcut produces the same result as pressing the equivalent GUI button.

### FR-7: Chained Operations
- The user can chain operations without pressing `=`: entering `5 + 3 * 2` evaluates `5 + 3` when `*` is pressed (yielding `8`), then applies `* 2` when `=` is pressed (yielding `16`).
- This is left-to-right evaluation (no operator precedence), which is standard for basic calculators.

**Acceptance criteria:** Chained operations evaluate left-to-right, displaying intermediate results.

## 2. Non-Functional Requirements

### NFR-1: Usability
- The GUI must be intuitive with clearly labeled buttons.
- Button layout follows the standard calculator convention (7-8-9 on top row, 0 spanning bottom).
- Responsive button clicks with no perceptible delay.

### NFR-2: Performance
- All calculations complete in under 10ms.
- The GUI remains responsive at all times.

### NFR-3: Error Handling
- Errors are displayed in the calculator display (e.g., "Error") — the application never crashes.
- After an error, the user can press `C` to reset and continue.

### NFR-4: Compatibility
- Runs on Python 3.8+ with only the standard library (Tkinter).
- Works on macOS, Linux, and Windows.

## 3. GUI Specification

### Window Layout
- Fixed-size window with a title "Calculator".
- A single-line display/entry at the top spanning the full width.
- A 5-row by 4-column grid of buttons below the display.

### Button Grid Layout
```
[ C ][ ( ][ ) ][ / ]
[ 7 ][ 8 ][ 9 ][ * ]
[ 4 ][ 5 ][ 6 ][ - ]
[ 1 ][ 2 ][ 3 ][ + ]
[   0   ][ . ][ = ]
```

- `0` spans two columns.
- All buttons have equal height.
- Operator buttons are visually distinct (different color).

### Display Behavior
- Right-aligned text.
- Font size large enough for easy reading.
- Shows `0` on startup.
- Shows "Error" on invalid operations (e.g., division by zero).

## 4. Edge Cases and Boundary Conditions

| Case | Input | Expected Behavior |
|------|-------|-------------------|
| Division by zero | `5 / 0 =` | Display shows "Error" |
| Multiple decimal points | `3..5` | Second `.` is ignored; number is `3.5` |
| Leading operator | `+ 5 =` | Treats as `0 + 5 = 5` |
| Multiple operators | `5 + - 3 =` | Last operator wins: `5 - 3 = 2` |
| Equals with no operation | `5 =` | Display remains `5` |
| Very large numbers | `99999999 * 99999999` | Display shows the result (Python handles big ints) |
| Very small decimals | `0.0001 + 0.0002` | Display shows `0.0003` |
| Negative results | `3 - 5 =` | Display shows `-2` |
| Clear after error | Error state then `C` | Resets to `0`, calculator functional |
| Repeated equals | `5 + 3 = = =` | Each `=` repeats the last operation: `8`, `11`, `14` |
| Backspace on empty | Backspace when display is `0` | No change, display stays `0` |
| Decimal only | `. 5` | Treated as `0.5` |
| Operator after equals | `5 + 3 = + 2 =` | Chains: `8 + 2 = 10` |

## 5. Acceptance Criteria Summary

1. All four arithmetic operations produce correct results for integer and float inputs.
2. The display updates correctly at every step of input.
3. Keyboard and button inputs are equivalent.
4. Division by zero shows "Error" without crashing.
5. Clear resets all state.
6. Chained operations evaluate left-to-right.
7. The application launches without errors on Python 3.8+.
