# Calculator Application — Coding Plan

## 1. Implementation Order

| Step | File | Rationale |
|------|------|-----------|
| 1 | `calculator_logic.py` | Core business logic with no dependencies. Must exist before GUI or tests. |
| 2 | `test_calculator.py` | Validate logic before building the GUI. Catches bugs early. |
| 3 | `calculator.py` | GUI layer that delegates to the already-tested logic. |
| 4 | `requirements.txt` | Document dependencies (only pytest for testing). |

## 2. File-by-File Breakdown

### `calculator_logic.py`
- **`CalculatorLogic` class** (~100 lines)
  - `__init__`: Initialize state (`current_input="0"`, `first_operand=None`, `operator=None`, `result_displayed=False`, `last_operator=None`, `last_operand=None`, `error=False`).
  - `get_display() -> str`: Return `current_input`.
  - `input_digit(digit: str) -> str`: If result just displayed or error, reset input. Replace leading `"0"` unless decimal. Append digit.
  - `input_decimal() -> str`: Add `"."` if not already present. Handle fresh input after result.
  - `input_operator(op: str) -> str`: If pending operation exists, evaluate first (chaining). Store current input as `first_operand`, store operator, mark ready for new input.
  - `input_equals() -> str`: Evaluate `first_operand <op> current`. Handle repeated `=`. Catch errors. Format result (strip trailing `.0`).
  - `input_clear() -> str`: Reset all state, return `"0"`.
  - `input_backspace() -> str`: Remove last char from `current_input`. If empty, reset to `"0"`.
  - `_evaluate(a: float, op: str, b: float) -> float`: Perform the arithmetic. Raise `ZeroDivisionError` for `/ 0`.
  - `_format_result(value: float) -> str`: Return `str(int(value))` if whole number, else `str(value)`.

### `calculator.py`
- **`CalculatorApp` class** (~100 lines)
  - `__init__(root)`: Store root, create `CalculatorLogic`, call setup methods.
  - `_create_display()`: `tk.Entry` widget, row 0, columnspan 4, right-aligned, font size 24.
  - `_create_buttons()`: Iterate over button layout definition (list of rows), create `tk.Button` for each, place in grid. Apply colors by category.
  - `_on_button_click(value)`: Route to appropriate `CalculatorLogic` method, call `_update_display`.
  - `_update_display(text)`: Clear entry, insert new text.
  - `_bind_keyboard()`: Bind `<Key>` event on root, map keysym/char to button values.
- **`main()` function**: Create `Tk` root, instantiate `CalculatorApp`, call `mainloop()`.
- **`if __name__ == "__main__"` guard**.

### `test_calculator.py`
- Import `CalculatorLogic` from `calculator_logic`.
- Fixture: fresh `CalculatorLogic` instance.
- Test classes/groups: digits, decimals, operators, equals, clear, backspace, chaining, edge cases, error handling.
- Uses `pytest.mark.parametrize` for arithmetic operation coverage.

### `requirements.txt`
```
pytest>=7.0
```

## 3. Dependencies Between Modules

```
calculator.py ──imports──► calculator_logic.py
test_calculator.py ──imports──► calculator_logic.py
```

No circular dependencies. `calculator_logic.py` is standalone.

## 4. Widget Layout Plan

### Grid Positions (row, col, colspan)
```
Display:  row=0, col=0, colspan=4
C:        row=1, col=0    (:        row=1, col=1    ):        row=1, col=2    /:  row=1, col=3
7:        row=2, col=0    8:        row=2, col=1    9:        row=2, col=2    *:  row=2, col=3
4:        row=3, col=0    5:        row=3, col=1    6:        row=3, col=2    -:  row=3, col=3
1:        row=4, col=0    2:        row=4, col=1    3:        row=4, col=2    +:  row=4, col=3
0:        row=5, col=0, colspan=2   .:  row=5, col=2                          =:  row=5, col=3
```

### Column/Row Weights
- All 4 columns: weight=1, uniform="btn" (equal width).
- All button rows: weight=1, uniform="btn" (equal height).
- Row 0 (display): weight=0 (fixed height).

## 5. Estimated Complexity Per Component

| Component | Complexity | Notes |
|-----------|-----------|-------|
| `CalculatorLogic.__init__` | Low | Just set initial values |
| `input_digit` | Low | String append with a few guards |
| `input_decimal` | Low | One conditional check |
| `input_operator` | Medium | Must handle chaining (evaluate pending op) |
| `input_equals` | Medium | Evaluation + error handling + repeated equals |
| `input_clear` | Low | Reset all fields |
| `input_backspace` | Low | String slice |
| `_evaluate` | Low | Four arithmetic operations |
| `_format_result` | Low | int/float formatting |
| GUI setup | Medium | Grid layout, styling, keyboard bindings |
| Tests | Medium | Many cases but straightforward assertions |
