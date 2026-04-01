# Calculator Application — Coding Plan

## 1. Implementation Order

| Order | File | Reason |
|-------|------|--------|
| 1 | `calculator_logic.py` | Core logic with no dependencies. Must be complete and testable before GUI work begins. |
| 2 | `test_calculator.py` | Write tests against the logic module to verify correctness before building the GUI. |
| 3 | `calculator.py` | GUI layer that imports and uses `calculator_logic.py`. Built last because it depends on the logic layer. |
| 4 | `requirements.txt` | Document dependencies (minimal — only pytest for testing). |

## 2. File-by-File Breakdown

### `calculator_logic.py`
- **`CalculatorLogic` class**
  - `__init__()`: Initialize `_expression = ""` and `_last_was_eval = False`.
  - `display_text` property: Return `_expression` or `"0"` if empty.
  - `add_character(char: str) -> str`: Core input handling.
    - If `_last_was_eval` and char is a digit/decimal: reset expression.
    - If `_last_was_eval` and char is an operator: continue from result.
    - Prevent consecutive operators (replace last).
    - Prevent multiple decimals in the same number token.
    - Handle leading negative numbers.
  - `evaluate() -> str`: Parse and compute.
    - Use a safe evaluation approach (no raw `eval`).
    - Catch `ZeroDivisionError`, `SyntaxError`, `ValueError`.
    - Format result: strip trailing zeros from floats.
    - Set `_last_was_eval = True`.
  - `clear() -> str`: Reset all state, return `"0"`.
  - `backspace() -> str`: Remove last character, return updated display.
- **`safe_eval(expression: str) -> float`** (module-level function)
  - Validate that expression contains only digits, operators, decimals, parentheses, and spaces.
  - Use `ast.parse` + custom node visitor to ensure only numeric/arithmetic AST nodes.
  - Compile and evaluate the validated AST.

### `calculator.py`
- **`CalculatorApp(tk.Tk)` class**
  - `__init__()`: Configure window (title, size, resizable=False). Create `CalculatorLogic` instance. Call `_create_widgets()` and `_bind_events()`.
  - `_create_widgets()`:
    - Create main frame with padding.
    - Create display entry (row 0, columnspan 4).
    - Create buttons in a loop from a layout definition list.
  - `_bind_events()`: Bind `<Key>` to `_on_key_press`.
  - `_update_display(text: str)`: Set `display_var` to `text`.
  - `_on_button_click(value: str)`: Route to logic methods based on value.
  - `_on_key_press(event)`: Map `event.char` and `event.keysym` to button values.
- **`if __name__ == "__main__":` block**: Instantiate and run `mainloop()`.

### `test_calculator.py`
- Tests for `CalculatorLogic` (no Tkinter needed).
- Tests for `safe_eval` function directly.
- Organized into categories: basic operations, edge cases, error cases, chained operations.

### `requirements.txt`
- `pytest` (only dev/test dependency; Tkinter is stdlib).

## 3. Module Dependencies

```
calculator.py ──imports──> calculator_logic.py
test_calculator.py ──imports──> calculator_logic.py
```

No circular dependencies. `calculator_logic.py` imports only from the standard library (`ast`).

## 4. Widget Layout Plan

### Button Definition (used in loop)
```python
BUTTONS = [
    ("C", 1, 0, 1), ("(", 1, 1, 1), (")", 1, 2, 1), ("/", 1, 3, 1),
    ("7", 2, 0, 1), ("8", 2, 1, 1), ("9", 2, 2, 1), ("*", 2, 3, 1),
    ("4", 3, 0, 1), ("5", 3, 1, 1), ("6", 3, 2, 1), ("-", 3, 3, 1),
    ("1", 4, 0, 1), ("2", 4, 1, 1), ("3", 4, 2, 1), ("+", 4, 3, 1),
    ("0", 5, 0, 2), (".", 5, 2, 1), ("=", 5, 3, 1),
]
# Tuple: (label, row, col, columnspan)
```

### Grid Configuration
- 4 columns, all weight=1 for equal sizing.
- 6 rows: row 0 is display, rows 1-5 are buttons.
- Row 0 has higher weight for a taller display area.

## 5. Estimated Complexity

| Component | Complexity | Notes |
|-----------|-----------|-------|
| `safe_eval()` | Medium | AST validation requires careful node whitelisting. |
| `CalculatorLogic.add_character()` | Medium | Multiple input validation rules to handle correctly. |
| `CalculatorLogic.evaluate()` | Low | Delegates to `safe_eval`, wraps in try/except. |
| `CalculatorLogic.clear/backspace` | Low | Simple state resets. |
| `CalculatorApp` GUI setup | Low-Medium | Straightforward grid layout with button loop. |
| Keyboard binding | Low | Simple key-to-value mapping. |
| Test suite | Medium | Many edge cases to cover thoroughly. |
