# Calculator Application — Requirements Document

## 1. Functional Requirements

### FR-1: Numeric Input
- The calculator must accept digits 0-9 via GUI buttons and keyboard input.
- The calculator must accept a decimal point (`.`) to form floating-point numbers.
- Multiple leading zeros must be prevented (e.g., `007` becomes `7`).
- Only one decimal point per number is allowed.

### FR-2: Arithmetic Operations
- **Addition (+)**: Sum two operands.
- **Subtraction (-)**: Subtract the right operand from the left.
- **Multiplication (*)**: Multiply two operands.
- **Division (/)**: Divide the left operand by the right.
- Operations follow standard left-to-right evaluation with operator precedence
  (multiplication and division before addition and subtraction).

### FR-3: Expression Display
- A read-only display shows the current expression as the user builds it.
- After pressing equals, the display shows the result.
- The expression display updates in real time as buttons are pressed.

### FR-4: Evaluation (Equals)
- Pressing `=` (button or Enter key) evaluates the current expression.
- The result replaces the expression in the display.
- After evaluation, typing a digit starts a new expression.
- After evaluation, typing an operator uses the result as the left operand.

### FR-5: Clear
- A "C" button resets the calculator to its initial empty state.
- The display is cleared to show "0" or empty.

### FR-6: Keyboard Input
- Number keys (0-9) enter digits.
- `.` enters a decimal point.
- `+`, `-`, `*`, `/` enter operators.
- `Enter` or `=` evaluates the expression.
- `Escape` or `c`/`C` clears the calculator.
- `Backspace` deletes the last character.

### FR-7: Error Handling
- Division by zero displays "Error" in the display (no crash).
- Invalid expressions (e.g., `++`, `3*/2`) display "Error".
- Errors are cleared when the user starts a new expression.

## 2. Non-Functional Requirements

### NFR-1: Performance
- Button presses and display updates must feel instantaneous (<50ms).
- Expression evaluation must complete in under 100ms for any valid input.

### NFR-2: Usability
- Button layout follows standard calculator conventions (numbers in grid, operators on the right).
- The display is large and readable.
- The window has a reasonable default size and is not resizable (fixed layout).

### NFR-3: Reliability
- The application must never crash due to user input.
- All error conditions result in a user-visible message, not an exception.

### NFR-4: Portability
- Runs on any system with Python 3.8+ and Tkinter (included in standard library).
- No external dependencies beyond the standard library.

## 3. GUI Specification

### Window
- Title: "Calculator"
- Fixed size: approximately 300x400 pixels.
- Non-resizable.

### Display
- Spans the full width of the window at the top.
- Read-only text entry or label showing the current expression/result.
- Right-aligned text, large font (e.g., 18-20pt).

### Button Grid (4 columns x 5 rows below the display)

| Row | Col 0 | Col 1 | Col 2 | Col 3 |
|-----|-------|-------|-------|-------|
| 1   | C     | (     | )     | /     |
| 2   | 7     | 8     | 9     | *     |
| 3   | 4     | 5     | 6     | -     |
| 4   | 1     | 2     | 3     | +     |
| 5   | 0 (colspan 2) | .  | =     |

### Button Behavior
- Number and decimal buttons append to the current expression.
- Operator buttons append the operator to the expression.
- `=` evaluates and displays the result.
- `C` clears the expression and resets to initial state.

## 4. Edge Cases and Boundary Conditions

| ID   | Case                              | Expected Behavior                    |
|------|-----------------------------------|--------------------------------------|
| EC-1 | Division by zero (`5/0`)          | Display "Error"                      |
| EC-2 | Multiple decimal points (`3.2.1`) | Ignore second decimal point          |
| EC-3 | Leading operator (`+5`)           | Treat as positive 5                  |
| EC-4 | Trailing operator (`5+`)          | Evaluate as if operator not present, or show Error |
| EC-5 | Empty expression, press `=`       | Display "0" or remain empty          |
| EC-6 | Very large numbers                | Display result (Python handles big ints) |
| EC-7 | Very small decimals               | Display result with reasonable precision |
| EC-8 | Consecutive operators (`5++3`)    | Replace previous operator with new one |
| EC-9 | Result used in next calc          | After `=`, operator starts new expr with result |
| EC-10| Floating-point display            | Remove unnecessary trailing zeros    |

## 5. Acceptance Criteria

| Requirement | Acceptance Criteria |
|-------------|-------------------|
| FR-1 | All digits 0-9 and decimal appear in display when clicked or typed. |
| FR-2 | `2+3` = `5`, `10-4` = `6`, `3*7` = `21`, `8/2` = `4` all correct. |
| FR-3 | Display updates after every button press, shows result after `=`. |
| FR-4 | Pressing `=` evaluates expression; result can be used in next operation. |
| FR-5 | Pressing `C` resets display to "0" and clears all state. |
| FR-6 | All listed keyboard shortcuts produce the same result as button clicks. |
| FR-7 | `5/0` shows "Error"; no unhandled exceptions for any input sequence. |
