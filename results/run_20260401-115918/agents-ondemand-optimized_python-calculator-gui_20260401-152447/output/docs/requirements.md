# Requirements Document: Python Tkinter GUI Calculator

**Date:** 2026-04-01
**Version:** 1.0

---

## 1. Overview

This document specifies the requirements for a desktop calculator application built with Python and Tkinter. The calculator provides a graphical interface for performing basic arithmetic operations on integer and floating-point numbers.

---

## 2. Functional Requirements

### FR-01: Number Input

**Description:** The user must be able to input digits 0 through 9 and a decimal point to form numbers.

**Details:**
- Buttons labeled 0-9 and "." are available in the GUI.
- Clicking a number button appends that digit to the current expression in the display.
- Clicking the decimal point button appends "." to the current expression.
- The display updates immediately to reflect the input.

**Acceptance Criteria:**
- Clicking buttons 0-9 appends the corresponding digit to the display.
- Clicking "." appends a decimal point to the display.
- Multiple digits can be entered sequentially to form multi-digit numbers (e.g., "123").
- The display shows the full expression as it is built.

---

### FR-02: Arithmetic Operations

**Description:** The calculator must support addition, subtraction, multiplication, and division.

**Details:**
- Operator buttons: `+`, `-`, `*`, `/`
- Clicking an operator button appends that operator to the current expression.
- Operations follow standard mathematical precedence (multiplication and division before addition and subtraction).

**Acceptance Criteria:**
- Each operator button appends the correct operator symbol to the display.
- Expressions like "2+3*4" evaluate to 14 (not 20), respecting standard precedence.
- Operators can be chained: "1+2+3" evaluates to 6.

---

### FR-03: Expression Evaluation

**Description:** The user must be able to evaluate the current expression by pressing the equals button.

**Details:**
- An "=" button triggers evaluation of the expression shown in the display.
- The result replaces the expression in the display.
- The result can be used as the starting value for a new expression.

**Acceptance Criteria:**
- Pressing "=" evaluates "2+3" and displays "5".
- Pressing "=" evaluates "10/3" and displays the floating-point result.
- After evaluation, entering a new number starts a fresh expression.
- After evaluation, entering an operator appends to the result (chaining).

---

### FR-04: Clear Functionality

**Description:** The user must be able to reset the calculator to its initial state.

**Details:**
- A "C" (Clear) button resets the display to an empty or default state.
- All pending expressions and state are discarded.

**Acceptance Criteria:**
- Pressing "C" clears the display completely.
- After clearing, the calculator behaves as if freshly launched.
- Pressing "C" during mid-expression discards the entire expression.

---

### FR-05: Display

**Description:** A text display area shows the current expression being built and the result after evaluation.

**Details:**
- The display is a read-only text field at the top of the calculator window.
- It shows the expression as the user types it (e.g., "12+34").
- After pressing "=", it shows the result (e.g., "46").
- Error messages are shown in the display when operations fail.

**Acceptance Criteria:**
- The display is visible and positioned at the top of the window.
- The display updates in real time as buttons are pressed.
- The display shows error messages (e.g., "Error") for invalid operations.
- The display text is right-aligned or left-aligned consistently.

---

### FR-06: Keyboard Input Support

**Description:** The user must be able to type numbers and operators using the keyboard in addition to clicking buttons.

**Details:**
- Keys 0-9 input the corresponding digits.
- Keys `+`, `-`, `*`, `/` input the corresponding operators.
- The `.` key inputs a decimal point.
- The Enter/Return key triggers evaluation (same as "=").
- The Escape key or Delete/Backspace key triggers clear (same as "C").

**Acceptance Criteria:**
- Typing "1", "+", "2", Enter on the keyboard produces "3" in the display.
- Keyboard input and button clicks can be mixed freely.
- All keyboard bindings work regardless of focus state within the application window.

---

### FR-07: Integer and Floating-Point Support

**Description:** The calculator must handle both integer and floating-point numbers correctly.

**Details:**
- Whole number results are displayed without a trailing decimal point or zero (e.g., "5" not "5.0").
- Floating-point results are displayed with appropriate precision.
- Input can include decimal points to form floating-point numbers.

**Acceptance Criteria:**
- "2+3" evaluates to "5" (integer display).
- "1.5+2.5" evaluates to "4" (integer display when result is whole).
- "10/3" evaluates to a floating-point result (e.g., "3.3333333333333335" or a reasonably precise representation).
- "0.1+0.2" produces a result (floating-point behavior is acceptable).

---

## 3. Non-Functional Requirements

### NFR-01: Performance

- The calculator must respond to button clicks and keyboard input within 100ms.
- Expression evaluation must complete within 100ms for any supported expression.
- The GUI must remain responsive at all times (no freezing or hanging).

### NFR-02: Usability

- The calculator window must have a clear, intuitive layout resembling a standard calculator.
- Buttons must be large enough to click easily.
- The display must use a readable font size.
- The window title must identify the application as a calculator.

### NFR-03: Reliability

- The application must not crash under any user input combination.
- All errors must be caught and displayed gracefully in the calculator display.
- The application must handle rapid repeated input without losing or duplicating characters.

### NFR-04: Portability

- The application must run on any system with Python 3.7+ and Tkinter (included in standard library).
- No third-party dependencies are required for the application itself.

### NFR-05: Maintainability

- Business logic must be fully separated from the GUI layer.
- The codebase must follow PEP 8 style guidelines.
- All public methods and classes must have docstrings.
- Type hints must be used on all function signatures.

---

## 4. GUI Specification

### Window Properties

| Property       | Value               |
|----------------|---------------------|
| Title          | "Calculator"        |
| Default Size   | ~300x400 pixels     |
| Resizable      | Yes (with min size) |
| Layout Manager | grid                |

### Widget Hierarchy

```
CalculatorApp (Tk root window)
+-- Display (Entry widget, row 0, spans 4 columns)
+-- Button Grid (rows 1-5, 4 columns)
    +-- Row 1: 7, 8, 9, /
    +-- Row 2: 4, 5, 6, *
    +-- Row 3: 1, 2, 3, -
    +-- Row 4: 0, ., =, +
    +-- Row 5: C (spans 4 columns)
```

### Display Behavior

- The display widget is an Entry or Label at the top of the window.
- It spans all 4 columns of the button grid.
- It shows the current expression or the result after evaluation.
- When an error occurs, it shows the text "Error".

### Button Behavior

- Number buttons (0-9): Append the digit to the current expression.
- Decimal button (.): Append "." to the current expression.
- Operator buttons (+, -, *, /): Append the operator to the current expression.
- Equals button (=): Evaluate the expression and display the result.
- Clear button (C): Reset the expression and display.

---

## 5. Edge Cases and Boundary Conditions

### EC-01: Division by Zero

- **Input:** "5/0" then "="
- **Expected:** Display shows "Error"
- **Requirement:** No crash; error message in display.

### EC-02: Empty Expression Evaluation

- **Input:** Press "=" with nothing in the display.
- **Expected:** No crash; display remains empty or shows "0" or "Error".
- **Requirement:** Graceful handling.

### EC-03: Multiple Decimal Points in One Number

- **Input:** "1.2.3"
- **Expected:** Either prevent the second decimal point or show "Error" on evaluation.
- **Requirement:** No crash.

### EC-04: Leading Operator

- **Input:** Press "+" before entering any number.
- **Expected:** Either ignore the operator, treat it as "+0", or handle gracefully.
- **Requirement:** No crash.

### EC-05: Consecutive Operators

- **Input:** "5++3"
- **Expected:** Either prevent the second operator, replace the first, or show "Error" on evaluation.
- **Requirement:** No crash.

### EC-06: Trailing Operator

- **Input:** "5+" then "="
- **Expected:** Show "Error" or ignore the trailing operator.
- **Requirement:** No crash.

### EC-07: Very Large Numbers

- **Input:** Extremely large multiplication results.
- **Expected:** Display the result or show "Error" if it exceeds limits.
- **Requirement:** No crash.

### EC-08: Very Small Floating-Point Numbers

- **Input:** "0.0000001+0.0000002"
- **Expected:** Correct floating-point result displayed.
- **Requirement:** No crash.

### EC-09: Clearing After Error

- **Input:** Cause an error, then press "C".
- **Expected:** Calculator resets to initial state, fully functional.
- **Requirement:** Error state does not persist.

### EC-10: Chaining After Result

- **Input:** "2+3", "=", then "+4", "="
- **Expected:** First "=" shows "5", then "+4=" shows "9".
- **Requirement:** Result is reusable as input.

---

## 6. Requirements Traceability

| Requirement | Priority  | Tested By         |
|-------------|-----------|-------------------|
| FR-01       | Must-have | Unit + Manual     |
| FR-02       | Must-have | Unit + Manual     |
| FR-03       | Must-have | Unit + Manual     |
| FR-04       | Must-have | Unit + Manual     |
| FR-05       | Must-have | Manual            |
| FR-06       | Must-have | Manual            |
| FR-07       | Must-have | Unit + Manual     |
| NFR-01      | Must-have | Manual            |
| NFR-02      | Must-have | Manual            |
| NFR-03      | Must-have | Unit + Manual     |
| NFR-04      | Must-have | Environment check |
| NFR-05      | Must-have | Code review       |
