# Coding Plan: Python Tkinter Calculator

## Overview

A desktop calculator application built with Python and Tkinter. The architecture
follows strict separation of concerns: pure business logic lives in one module,
GUI and controller logic in another. Only the Python standard library is required.

---

## Implementation Order

Build modules in this sequence, with rationale:

| Step | File                   | Rationale                                                                 |
|------|------------------------|---------------------------------------------------------------------------|
| 1    | `requirements.txt`     | Establish project dependencies up front (stdlib only, so effectively empty). |
| 2    | `calculator_logic.py`  | Pure logic with no dependencies. Can be built and tested in isolation.     |
| 3    | `test_calculator.py`   | Validate all logic edge cases before wiring up the GUI.                   |
| 4    | `calculator.py`        | GUI layer depends on `calculator_logic.py`. Build last so it consumes a proven API. |

The key principle: build the dependency-free module first, test it, then layer
the dependent module on top. This avoids debugging logic errors through a GUI.

---

## Dependencies Between Modules

```
calculator.py  --->  calculator_logic.py
                         (no external deps, stdlib only)

test_calculator.py  --->  calculator_logic.py
                         (uses pytest as test runner)
```

- `calculator_logic.py` depends on nothing (pure Python, no imports beyond builtins).
- `calculator.py` imports `CalculatorLogic` from `calculator_logic.py` and `tkinter`.
- `test_calculator.py` imports `CalculatorLogic` from `calculator_logic.py` and `pytest`.

---

## File-by-File Breakdown

### 1. `requirements.txt`

Empty file. The application uses only the Python standard library (`tkinter` ships
with CPython). The test suite requires `pytest`, but that is a development
dependency and may be noted in a comment.

**Estimated complexity:** Trivial.

---

### 2. `calculator_logic.py` -- Business Logic

**Class:** `CalculatorLogic`

**Internal state:**
- `_expression: str` -- the raw expression string being built (e.g. `"12+3.5"`)
- `_display: str` -- what the user sees (the expression, a result, or `"Error"`)
- `_error: bool` -- flag set when the last operation produced an error

**Public methods:**

| Method                      | Behavior |
|-----------------------------|----------|
| `append_digit(d: str)`      | Appends a single digit character (`0`-`9`) to the expression. After an evaluation or error, starts a new expression. Returns display string. |
| `append_decimal()`          | Appends `"."` to the expression. Prevents multiple decimals within the same numeric token. Returns display string. |
| `append_operator(op: str)`  | Appends an operator (`+`, `-`, `*`, `/`). Replaces the last operator if one is already trailing. Returns display string. |
| `evaluate()`                | Evaluates the current expression. On success, sets the display to the result. On failure (e.g. division by zero, malformed expression), sets the display to `"Error"` and flags the error state. Returns display string. |
| `clear()`                   | Resets expression, display, and error flag to initial state. Returns display string (should be `"0"`). |
| `get_display() -> str`      | Returns the current display string without mutating state. |
| `has_error() -> bool`       | Returns `True` if the last operation produced an error. |

**Edge cases to handle:**
- Division by zero -> display `"Error"`
- Multiple consecutive decimal points in one number -> ignore second decimal
- Consecutive operators -> replace previous operator with new one
- Leading zeros -> allow `0.` but not `007`
- Evaluating an empty or operator-trailing expression -> handle gracefully
- Very large or very small results -> convert to string cleanly
- After error or evaluation, pressing a digit starts fresh; pressing an operator continues from the result

**Implementation notes:**
- Use Python `eval()` on the sanitized expression string for calculation, wrapped in a `try/except` to catch `ZeroDivisionError` and `SyntaxError`.
- Strip trailing `.0` from integer results so `4+2` displays `6`, not `6.0`.
- The expression is the single source of truth; the display is derived from it.

**Estimated complexity:** Medium. The method bodies are short, but the edge-case
handling (decimal logic, operator replacement, post-eval state transitions)
requires careful conditional logic.

---

### 3. `test_calculator.py` -- Unit Tests

**Test runner:** `pytest`

**Test categories and cases:**

| Category                 | Test Cases |
|--------------------------|------------|
| Basic digit input        | Single digit, multiple digits, display shows concatenated digits. |
| Decimal handling         | One decimal per number, decimal after operator starts new number, reject double decimal. |
| Operator handling        | Append operator after digit, replace consecutive operators, operator after evaluation continues from result. |
| Evaluation               | Simple addition, subtraction, multiplication, division, multi-operator expressions. |
| Division by zero         | `evaluate()` after `"5/0"` -> `"Error"`, `has_error()` returns `True`. |
| Clear                    | Resets display to `"0"`, clears error flag. |
| Post-error behavior      | Digit after error starts fresh, operator after error is ignored or starts fresh. |
| Post-eval behavior       | Digit after eval starts new expression, operator after eval continues from result. |
| Display correctness      | Integer results have no `.0` suffix, decimal results are shown accurately. |
| Edge cases               | Empty expression eval, leading zeros, very large numbers. |

**Estimated complexity:** Low-Medium. Straightforward assertion-based tests, but
thorough coverage of edge cases requires many small test functions.

---

### 4. `calculator.py` -- GUI and Controller

**Class:** `CalculatorApp`

**Constructor receives:** `tk.Tk` root window (or creates one internally).

**Components:**
- `CalculatorLogic` instance (composition, not inheritance)
- `tk.Entry` widget for the display (read-only to the user)
- 20 `tk.Button` widgets arranged in a 5x4 grid

#### Widget Layout Plan

The window is a 6-row, 4-column grid. Row 0 spans all 4 columns for the display.

```
Row 0: [ Entry display (columnspan=4)                     ]
Row 1: [  C  ] [  /  ] [  *  ] [  -  ]
Row 2: [  7  ] [  8  ] [  9  ] [  +  ]
Row 3: [  4  ] [  5  ] [  6  ] [  +  ]  (+ spans rows 2-3, see note)
Row 4: [  1  ] [  2  ] [  3  ] [  =  ]
Row 5: [  0 (colspan=2)  ] [  .  ] [  =  ]  (= spans rows 4-5, see note)
```

**Detailed grid positions:**

| Widget   | Row | Column | rowspan | columnspan | Sticky |
|----------|-----|--------|---------|------------|--------|
| Display  | 0   | 0      | 1       | 4          | `nsew` |
| C        | 1   | 0      | 1       | 1          | `nsew` |
| /        | 1   | 1      | 1       | 1          | `nsew` |
| *        | 1   | 2      | 1       | 1          | `nsew` |
| -        | 1   | 3      | 1       | 1          | `nsew` |
| 7        | 2   | 0      | 1       | 1          | `nsew` |
| 8        | 2   | 1      | 1       | 1          | `nsew` |
| 9        | 2   | 2      | 1       | 1          | `nsew` |
| +        | 2   | 3      | 2       | 1          | `nsew` |
| 4        | 3   | 0      | 1       | 1          | `nsew` |
| 5        | 3   | 1      | 1       | 1          | `nsew` |
| 6        | 3   | 2      | 1       | 1          | `nsew` |
| 1        | 4   | 0      | 1       | 1          | `nsew` |
| 2        | 4   | 1      | 1       | 1          | `nsew` |
| 3        | 4   | 2      | 1       | 1          | `nsew` |
| =        | 4   | 3      | 2       | 1          | `nsew` |
| 0        | 5   | 0      | 1       | 2          | `nsew` |
| .        | 5   | 2      | 1       | 1          | `nsew` |

All rows and columns should have `weight=1` so the grid resizes proportionally.

#### Keyboard Bindings

| Key(s)              | Action                          |
|----------------------|---------------------------------|
| `0`-`9`             | `logic.append_digit(key)`       |
| `.`                 | `logic.append_decimal()`        |
| `+`, `-`, `*`, `/`  | `logic.append_operator(key)`    |
| `Return`, `=`       | `logic.evaluate()`              |
| `Escape`, `c`, `C`  | `logic.clear()`                 |

All handlers call the appropriate `CalculatorLogic` method, then update the
`Entry` widget with the return value (or `logic.get_display()`).

#### Display Update Method

A private `_update_display()` method that:
1. Enables the Entry widget (`state='normal'`).
2. Clears its contents (`delete(0, tk.END)`).
3. Inserts the current display string (`insert(0, logic.get_display())`).
4. Disables it again (`state='readonly'`).

**Estimated complexity:** Medium. The grid layout is mechanical but detailed. The
keyboard binding and button wiring is repetitive but straightforward. No complex
logic lives here -- it all delegates to `CalculatorLogic`.

---

## Complexity Summary

| Component            | Estimated Complexity | Lines of Code (approx) |
|----------------------|----------------------|------------------------|
| `requirements.txt`   | Trivial              | 0-2                    |
| `calculator_logic.py`| Medium               | 80-120                 |
| `test_calculator.py` | Low-Medium           | 100-150                |
| `calculator.py`      | Medium               | 80-120                 |
| **Total**            |                      | **260-392**            |

---

## Final Notes

- The `calculator_logic.py` module must have zero dependency on `tkinter`. This
  is the most important architectural constraint -- it enables full test coverage
  without a display server.
- Use `eval()` cautiously. The expression string is constructed entirely by the
  class methods (digit, decimal, operator) so it cannot contain arbitrary code.
  Still, wrap in `try/except` for safety.
- The GUI module (`calculator.py`) should contain a `if __name__ == "__main__"`
  block that instantiates `CalculatorApp` and calls `root.mainloop()`.
