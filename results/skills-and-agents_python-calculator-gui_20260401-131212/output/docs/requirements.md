# Requirements Document: Python Tkinter GUI Calculator

**Version:** 1.0
**Date:** 2026-04-01
**Status:** Draft

---

## 1. Overview

This document defines the requirements for a desktop calculator application built with Python and the Tkinter GUI toolkit. The calculator provides basic arithmetic operations through both mouse-driven button interaction and keyboard input.

---

## 2. Functional Requirements

### FR-1: Arithmetic Operations

| ID    | Requirement | Priority |
|-------|-------------|----------|
| FR-1.1 | The calculator must support addition (+). | Must-have |
| FR-1.2 | The calculator must support subtraction (-). | Must-have |
| FR-1.3 | The calculator must support multiplication (*). | Must-have |
| FR-1.4 | The calculator must support division (/). | Must-have |

**Acceptance Criteria (FR-1):**
- Entering `2 + 3 =` produces `5`.
- Entering `10 - 4 =` produces `6`.
- Entering `3 * 7 =` produces `21`.
- Entering `15 / 4 =` produces `3.75`.
- Operations work correctly with both integer and floating-point operands.

### FR-2: Numeric Input

| ID    | Requirement | Priority |
|-------|-------------|----------|
| FR-2.1 | The calculator must provide buttons for digits 0 through 9. | Must-have |
| FR-2.2 | The calculator must provide a decimal point button. | Must-have |
| FR-2.3 | The calculator must accept integer values (e.g., `42`). | Must-have |
| FR-2.4 | The calculator must accept floating-point values (e.g., `3.14`). | Must-have |
| FR-2.5 | Pressing multiple digits in sequence must build a multi-digit number (e.g., pressing `1`, `2`, `3` produces `123`). | Must-have |

**Acceptance Criteria (FR-2):**
- Each digit button appends the corresponding digit to the current number in the display.
- The decimal point button appends a `.` to the current number.
- Only one decimal point is permitted per number. Additional presses of the decimal button are ignored.
- Leading zeros are handled sensibly (e.g., `007` displays as `7` or is prevented).

### FR-3: Expression Display

| ID    | Requirement | Priority |
|-------|-------------|----------|
| FR-3.1 | The calculator must have a display area showing the current expression being built. | Must-have |
| FR-3.2 | The display must show the computed result after the equals button is pressed. | Must-have |
| FR-3.3 | The display must show error messages when an invalid operation is attempted. | Must-have |

**Acceptance Criteria (FR-3):**
- As the user enters digits and operators, the display reflects the full expression (e.g., `12 + 5`).
- After pressing equals, the display shows the result (e.g., `17`).
- After an error, the display shows a human-readable error message (e.g., `Error`).
- The display is read-only; the user cannot type directly into the display widget to modify it arbitrarily.

### FR-4: Operator Buttons

| ID    | Requirement | Priority |
|-------|-------------|----------|
| FR-4.1 | The calculator must provide a button for each arithmetic operator: `+`, `-`, `*`, `/`. | Must-have |
| FR-4.2 | Pressing an operator after entering a number must append that operator to the expression. | Must-have |
| FR-4.3 | Pressing an operator immediately after another operator must replace the previous operator (not stack them). | Must-have |

**Acceptance Criteria (FR-4):**
- Pressing `+` after `5` shows `5 +` or `5+` in the display.
- Pressing `*` immediately after `+` replaces `+` with `*` in the expression.
- The calculator does not allow two consecutive operators in the expression.

### FR-5: Equals Button

| ID    | Requirement | Priority |
|-------|-------------|----------|
| FR-5.1 | The calculator must provide an equals (`=`) button. | Must-have |
| FR-5.2 | Pressing equals must evaluate the current expression and display the result. | Must-have |
| FR-5.3 | After displaying a result, entering a new digit must start a new expression. | Must-have |
| FR-5.4 | After displaying a result, entering an operator must use the result as the first operand of a new expression. | Must-have |

**Acceptance Criteria (FR-5):**
- `5 + 3 =` displays `8`.
- After seeing `8`, pressing `2` clears the display and starts a new expression with `2`.
- After seeing `8`, pressing `+` begins a new expression: `8 +`.
- Pressing `=` with an incomplete expression (e.g., `5 +`) either evaluates what is possible or shows an error, but does not crash.

### FR-6: Clear Button

| ID    | Requirement | Priority |
|-------|-------------|----------|
| FR-6.1 | The calculator must provide a clear (C) button. | Must-have |
| FR-6.2 | Pressing clear must reset the display and internal state to the initial empty state. | Must-have |

**Acceptance Criteria (FR-6):**
- Pressing C at any point resets the display to empty or `0`.
- After pressing C, the calculator is ready for a completely new expression.
- Pressing C after an error clears the error state and returns to normal operation.

### FR-7: Keyboard Input

| ID    | Requirement | Priority |
|-------|-------------|----------|
| FR-7.1 | The calculator must accept digit input (0-9) from the keyboard. | Must-have |
| FR-7.2 | The calculator must accept operator input (`+`, `-`, `*`, `/`) from the keyboard. | Must-have |
| FR-7.3 | The calculator must accept the decimal point (`.`) from the keyboard. | Must-have |
| FR-7.4 | The calculator must accept Enter or Return as equivalent to the equals button. | Must-have |
| FR-7.5 | The calculator must accept Escape or Delete as equivalent to the clear button. | Must-have |

**Acceptance Criteria (FR-7):**
- Typing `1`, `+`, `2`, `Enter` on the keyboard produces `3` in the display.
- Typing `Escape` clears the calculator.
- Keyboard input and button clicks are interchangeable and produce identical behavior.
- Unrecognized key presses are silently ignored (no error, no crash).

---

## 3. Non-Functional Requirements

### NFR-1: Performance

| ID     | Requirement | Priority |
|--------|-------------|----------|
| NFR-1.1 | The calculator must respond to all user input (button click or key press) within 100 milliseconds. | Must-have |
| NFR-1.2 | Expression evaluation must complete within 100 milliseconds for any valid input. | Must-have |
| NFR-1.3 | The application must start and display its window within 2 seconds on standard hardware. | Must-have |

**Acceptance Criteria (NFR-1):**
- No perceptible lag between pressing a button and seeing the display update.
- No freezing of the GUI at any point during normal operation.

### NFR-2: Usability

| ID     | Requirement | Priority |
|--------|-------------|----------|
| NFR-2.1 | The calculator must be usable without reading documentation. Button labels must be self-explanatory. | Must-have |
| NFR-2.2 | Button text must be legible. Use a minimum font size of 14 points for button labels and 18 points for the display. | Must-have |
| NFR-2.3 | The display must have sufficient width to show at least 20 characters. | Must-have |
| NFR-2.4 | The window must have a descriptive title (e.g., "Calculator"). | Must-have |

**Acceptance Criteria (NFR-2):**
- A user familiar with standard calculators can operate this calculator without instruction.
- All button labels are fully visible and not truncated.
- The display can show expressions of reasonable length without clipping.

### NFR-3: Error Handling

| ID     | Requirement | Priority |
|--------|-------------|----------|
| NFR-3.1 | The application must never crash or display an unhandled exception traceback to the user. | Must-have |
| NFR-3.2 | All errors must be displayed as friendly messages within the calculator display (e.g., "Error"). | Must-have |
| NFR-3.3 | After an error, the user must be able to press Clear to reset and continue using the calculator. | Must-have |

**Acceptance Criteria (NFR-3):**
- Division by zero displays "Error" (or similar) in the display, not a Python traceback.
- Malformed expressions display "Error" in the display, not a Python traceback.
- After any error, pressing C resets the calculator to a usable state.

### NFR-4: Compatibility

| ID     | Requirement | Priority |
|--------|-------------|----------|
| NFR-4.1 | The application must run on Python 3.8 or later. | Must-have |
| NFR-4.2 | The application must use only the Python standard library (Tkinter is included). No external dependencies are required. | Must-have |
| NFR-4.3 | The application must run on Windows, macOS, and Linux where Python and Tkinter are available. | Must-have |

**Acceptance Criteria (NFR-4):**
- The application launches and functions correctly on Python 3.8+.
- No `pip install` is needed to run the application.

### NFR-5: Code Quality

| ID     | Requirement | Priority |
|--------|-------------|----------|
| NFR-5.1 | Business logic (expression parsing and evaluation) must be separated from GUI code. | Must-have |
| NFR-5.2 | The business logic must be independently testable without instantiating a Tkinter window. | Must-have |
| NFR-5.3 | The code must follow PEP 8 style guidelines. | Must-have |

**Acceptance Criteria (NFR-5):**
- Unit tests can exercise the calculation engine without importing Tkinter.
- The code passes a PEP 8 linter with no errors.

---

## 4. GUI Specification

### 4.1 Window Properties

- **Title:** "Calculator"
- **Default size:** Approximately 300 pixels wide by 400 pixels tall.
- **Resizable:** Optional. If resizable, buttons and display must scale proportionally.
- **Minimum size:** The window must not be shrinkable below a size where buttons become illegible.

### 4.2 Layout

The window is organized into two sections arranged vertically:

```
+-------------------------------+
|          DISPLAY              |  Row 0 (spans all columns)
+-------------------------------+
|   7   |   8   |   9   |   /  |  Row 1
+-------+-------+-------+------+
|   4   |   5   |   6   |   *  |  Row 2
+-------+-------+-------+------+
|   1   |   2   |   3   |   -  |  Row 3
+-------+-------+-------+------+
|   0   |   .   |   =   |   +  |  Row 4
+-------+-------+-------+------+
|            C (Clear)          |  Row 5 (spans all columns)
+-------------------------------+
```

### 4.3 Display Behavior

- The display is a single-line text area spanning the full width of the window.
- Text in the display is right-aligned.
- The display uses a larger font than the buttons (minimum 18pt).
- The display is read-only to direct text editing but updates in response to button presses and key events.

### 4.4 Button Specifications

| Button | Label | Grid Position | Behavior |
|--------|-------|---------------|----------|
| Digit 7 | `7` | Row 1, Col 0 | Appends `7` to expression |
| Digit 8 | `8` | Row 1, Col 1 | Appends `8` to expression |
| Digit 9 | `9` | Row 1, Col 2 | Appends `9` to expression |
| Divide  | `/` | Row 1, Col 3 | Appends `/` operator |
| Digit 4 | `4` | Row 2, Col 0 | Appends `4` to expression |
| Digit 5 | `5` | Row 2, Col 1 | Appends `5` to expression |
| Digit 6 | `6` | Row 2, Col 2 | Appends `6` to expression |
| Multiply | `*` | Row 2, Col 3 | Appends `*` operator |
| Digit 1 | `1` | Row 3, Col 0 | Appends `1` to expression |
| Digit 2 | `2` | Row 3, Col 1 | Appends `2` to expression |
| Digit 3 | `3` | Row 3, Col 2 | Appends `3` to expression |
| Subtract | `-` | Row 3, Col 3 | Appends `-` operator |
| Digit 0 | `0` | Row 4, Col 0 | Appends `0` to expression |
| Decimal | `.` | Row 4, Col 1 | Appends `.` to current number |
| Equals  | `=` | Row 4, Col 2 | Evaluates expression |
| Add     | `+` | Row 4, Col 3 | Appends `+` operator |
| Clear   | `C` | Row 5, Col 0-3 | Resets calculator state |

### 4.5 Keyboard Bindings

| Key(s) | Action |
|--------|--------|
| `0`-`9` | Append digit to expression |
| `.` | Append decimal point |
| `+`, `-`, `*`, `/` | Append operator |
| `Enter` or `Return` | Evaluate expression (same as `=` button) |
| `Escape` | Clear calculator (same as `C` button) |
| `Backspace` or `Delete` | Clear calculator (same as `C` button) |

---

## 5. Edge Cases and Boundary Conditions

### 5.1 Division by Zero

- **Condition:** User enters an expression that divides by zero (e.g., `5 / 0`).
- **Expected behavior:** Display shows "Error". Calculator remains operational after pressing Clear.
- **Acceptance Criteria:** `5 / 0 =` displays "Error". Pressing C returns to normal state.

### 5.2 Multiple Decimal Points

- **Condition:** User presses the decimal button more than once within a single number (e.g., `3..5` or `3.1.4`).
- **Expected behavior:** The second decimal point press is ignored.
- **Acceptance Criteria:** Pressing `3`, `.`, `.`, `5` produces `3.5` in the display.

### 5.3 Leading Decimal Point

- **Condition:** User starts a number with a decimal point (e.g., `.5`).
- **Expected behavior:** The number is treated as `0.5`. The display may show `.5` or `0.5`.
- **Acceptance Criteria:** `.5 + .5 =` produces `1` or `1.0`.

### 5.4 Consecutive Operators

- **Condition:** User presses two operators in a row (e.g., `5 + *`).
- **Expected behavior:** The second operator replaces the first. The expression becomes `5 *`.
- **Acceptance Criteria:** Pressing `5`, `+`, `*`, `3`, `=` produces `15` (evaluates `5 * 3`).

### 5.5 Equals on Empty or Incomplete Expression

- **Condition:** User presses equals with no input, or with an incomplete expression (e.g., `5 +`).
- **Expected behavior:** Either ignores the press, re-displays the current value, or shows "Error". Must not crash.
- **Acceptance Criteria:** Pressing `=` on an empty display does not crash. Pressing `5`, `+`, `=` does not crash.

### 5.6 Very Large Numbers

- **Condition:** User enters or produces a very large result (e.g., `99999999999999 * 99999999999999`).
- **Expected behavior:** The result is displayed, potentially in scientific notation. The display does not overflow the window or crash.
- **Acceptance Criteria:** Large results are shown without crashing. The display handles long numbers gracefully.

### 5.7 Very Small Floating-Point Results

- **Condition:** A calculation produces a very small floating-point result (e.g., `1 / 3`).
- **Expected behavior:** The result is displayed with reasonable precision (not an excessively long decimal).
- **Acceptance Criteria:** `1 / 3 =` displays a number like `0.3333333333` (reasonable precision, not infinite digits).

### 5.8 Negative Numbers as Results

- **Condition:** A calculation produces a negative result (e.g., `3 - 5`).
- **Expected behavior:** The negative sign is displayed correctly.
- **Acceptance Criteria:** `3 - 5 =` displays `-2`.

### 5.9 Chained Operations

- **Condition:** User enters a long chain of operations (e.g., `1 + 2 + 3 + 4 =`).
- **Expected behavior:** The full expression is evaluated correctly following standard operator precedence (multiplication and division before addition and subtraction).
- **Acceptance Criteria:** `2 + 3 * 4 =` displays `14` (not `20`), respecting operator precedence.

### 5.10 Using a Result in the Next Calculation

- **Condition:** After obtaining a result, the user presses an operator to continue calculating.
- **Expected behavior:** The previous result becomes the first operand of the new expression.
- **Acceptance Criteria:** `5 + 3 =` displays `8`. Then pressing `+ 2 =` displays `10`.

### 5.11 Clear After Error

- **Condition:** An error is displayed and the user presses Clear.
- **Expected behavior:** The error is cleared. The calculator returns to its initial state, ready for new input.
- **Acceptance Criteria:** After seeing "Error", pressing C returns the display to its initial state. New calculations work normally.

### 5.12 Floating-Point Display Formatting

- **Condition:** A result is a whole number but was computed via floating-point arithmetic (e.g., `2.5 + 2.5`).
- **Expected behavior:** The result is displayed as an integer when possible (e.g., `5` instead of `5.0`).
- **Acceptance Criteria:** `2.5 + 2.5 =` displays `5` (not `5.0`).

---

## 6. Project Structure

The application must follow this structure to maintain separation of concerns:

```
project/
    calculator_engine.py    # Pure business logic: expression parsing, evaluation
    calculator_gui.py       # Tkinter GUI: window, widgets, event bindings
    main.py                 # Entry point: instantiates GUI and starts main loop
    test_calculator.py      # Unit tests for calculator_engine (no Tkinter dependency)
```

- `calculator_engine.py` contains all arithmetic and expression evaluation logic as pure functions or a class with no GUI imports.
- `calculator_gui.py` contains the Tkinter application class. It delegates all computation to `calculator_engine`.
- `main.py` is the entry point that creates and runs the application.
- `test_calculator.py` contains unit tests that validate the engine logic independently.

---

## 7. Summary of Acceptance Criteria

All of the following must pass for the application to be considered complete:

1. All four arithmetic operations produce correct results for integer and floating-point inputs.
2. The GUI matches the specified layout with display, digit buttons, operator buttons, equals, and clear.
3. Keyboard input works identically to button clicks for all supported keys.
4. Division by zero displays "Error" in the display, not a crash.
5. Multiple decimal points in one number are prevented.
6. Consecutive operators replace rather than stack.
7. Clear resets the calculator from any state, including error states.
8. Operator precedence is respected (multiplication/division before addition/subtraction).
9. Results that are whole numbers display without a trailing `.0`.
10. The application runs on Python 3.8+ with no external dependencies.
11. Business logic is testable independently of the GUI.
12. The application never shows a Python traceback or crashes during normal or erroneous use.
