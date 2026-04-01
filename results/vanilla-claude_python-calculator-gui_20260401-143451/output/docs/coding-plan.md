# Calculator Coding Plan

## 1. Implementation Order

### Step 1: `calculator_logic.py` (Model)
Build the business logic first since it has no dependencies and can be tested immediately.

### Step 2: `test_calculator.py` (Tests for logic)
Write tests for the logic before building the GUI to validate correctness early.

### Step 3: `calculator.py` (View + Controller)
Build the GUI last — it depends on the logic module being complete.

### Step 4: `requirements.txt`
Document dependencies (pytest for testing; no runtime dependencies beyond stdlib).

## 2. File-by-File Breakdown

### `calculator_logic.py`
- `CalculatorLogic` class with:
  - `__init__`: Initialize `_expression = ""`, `_result = "0"`, `_evaluated = False`.
  - `get_expression() -> str`: Return `_expression`.
  - `get_result() -> str`: Return `_result`.
  - `append_digit(digit: str) -> None`: Handle digit input, reset state if post-evaluation.
  - `append_decimal() -> None`: Add `.` if current number lacks one.
  - `append_operator(op: str) -> None`: Add operator, handle consecutive operators and post-eval continuation.
  - `evaluate() -> None`: Parse and compute expression, handle errors.
  - `clear() -> None`: Reset all state.
  - `_format_result(value: float) -> str`: Format number — strip `.0` from whole numbers.
  - `_get_current_number() -> str`: Extract the last number token from the expression (for decimal point checking).

### `calculator.py`
- `CalculatorApp` class with:
  - `__init__(root)`: Configure window, create logic instance, build UI, bind keys.
  - `_create_display()`: Build expression label and result label in a display frame.
  - `_create_buttons()`: Build button grid using a layout definition list.
  - `_update_display()`: Read from logic, update both labels.
  - `_on_button_click(value)`: Route button value to appropriate logic method.
  - `_on_key_press(event)`: Map `event.char` / `event.keysym` to button values.
- `main()` function: Create `Tk` root, instantiate `CalculatorApp`, run `mainloop`.
- `if __name__ == "__main__": main()`

### `test_calculator.py`
- Import `CalculatorLogic` from `calculator_logic`.
- Test classes/functions organized by category (see test plan).

### `requirements.txt`
- `pytest` (for running tests).

## 3. Dependencies Between Modules

```
calculator.py ──depends on──> calculator_logic.py
test_calculator.py ──depends on──> calculator_logic.py
```

No circular dependencies. `calculator_logic.py` is standalone.

## 4. Widget Layout Plan

### Display Frame (pack layout, top of window)
| Widget | Type | Position | Config |
|--------|------|----------|--------|
| expression_label | Label | top | anchor=E, small font, gray text |
| result_label | Label | below expression | anchor=E, large font, black text |

### Button Frame (grid layout, below display)
| Row | Col 0 | Col 1 | Col 2 | Col 3 |
|-----|-------|-------|-------|-------|
| 0 | C (colspan=3) | | | / |
| 1 | 7 | 8 | 9 | * |
| 2 | 4 | 5 | 6 | - |
| 3 | 1 | 2 | 3 | + |
| 4 | 0 (colspan=2) | | . | = |

## 5. Estimated Complexity per Component

| Component | Complexity | Notes |
|-----------|-----------|-------|
| `CalculatorLogic.__init__` | Low | Simple state init |
| `append_digit` | Low | Append + post-eval reset |
| `append_decimal` | Medium | Must parse current number to check for existing `.` |
| `append_operator` | Medium | Consecutive operator replacement, post-eval continuation |
| `evaluate` | Medium | `eval()` with error handling, result formatting |
| `clear` | Low | Reset state |
| `CalculatorApp.__init__` | Low | Window setup |
| `_create_display` | Low | Two labels |
| `_create_buttons` | Medium | Grid layout with spans |
| `_on_button_click` | Low | Routing logic |
| `_on_key_press` | Low | Key mapping |
| Test suite | Medium | Many edge cases to cover |
