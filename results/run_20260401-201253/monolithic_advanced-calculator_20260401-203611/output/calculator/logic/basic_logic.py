"""Basic calculator logic with operator precedence via shunting-yard."""

from __future__ import annotations

from calculator.logic.base_logic import format_number

# Operator precedence levels
PRECEDENCE = {"+": 1, "-": 1, "*": 2, "/": 2}


class BasicCalculator:
    """Basic mode calculator with full expression evaluation.

    Supports +, -, *, / with correct operator precedence using
    a token-based shunting-yard approach.
    """

    def __init__(self) -> None:
        self._current_input: str = "0"
        self._tokens: list[str] = []
        self._operators: list[str] = []
        self._new_input: bool = True
        self._error: bool = False
        self._expression_display: str = ""
        self._last_result: float | None = None
        self._just_evaluated: bool = False

    def input_digit(self, digit: str) -> None:
        """Append a digit to the current input."""
        if self._error:
            self._clear_error()
        if self._just_evaluated:
            self.input_all_clear()
        if self._new_input:
            self._current_input = digit
            self._new_input = False
        else:
            if self._current_input == "0" and digit != "0":
                self._current_input = digit
            elif self._current_input == "0" and digit == "0":
                pass
            else:
                self._current_input += digit

    def input_decimal(self) -> None:
        """Add a decimal point to the current input."""
        if self._error:
            self._clear_error()
        if self._just_evaluated:
            self.input_all_clear()
        if self._new_input:
            self._current_input = "0."
            self._new_input = False
        elif "." not in self._current_input:
            self._current_input += "."

    def input_operator(self, op: str) -> None:
        """Handle an arithmetic operator (+, -, *, /).

        Pushes the current number onto the token stack and
        manages operator precedence.
        """
        if self._error:
            return
        self._push_current_number()
        self._expression_display += f" {op} "
        while (
            self._operators
            and self._operators[-1] != "("
            and self._operators[-1] in PRECEDENCE
            and PRECEDENCE.get(self._operators[-1], 0)
            >= PRECEDENCE.get(op, 0)
        ):
            self._apply_top_operator()
        self._operators.append(op)
        self._new_input = True
        self._just_evaluated = False

    def input_equals(self) -> None:
        """Evaluate the full expression and display the result."""
        if self._error:
            return
        self._push_current_number()
        while self._operators:
            if self._operators[-1] == "(":
                self._error = True
                return
            self._apply_top_operator()
            if self._error:
                return
        if self._tokens:
            try:
                result = float(self._tokens[-1])
            except (ValueError, IndexError):
                self._error = True
                return
            self._last_result = result
            self._current_input = format_number(result)
            self._expression_display = ""
            self._tokens = []
            self._operators = []
            self._new_input = True
            self._just_evaluated = True

    def input_clear(self) -> None:
        """Clear current entry without clearing the pending operation."""
        self._current_input = "0"
        self._new_input = True
        self._error = False

    def input_all_clear(self) -> None:
        """Reset all state."""
        self._current_input = "0"
        self._tokens = []
        self._operators = []
        self._new_input = True
        self._error = False
        self._expression_display = ""
        self._last_result = None
        self._just_evaluated = False

    def input_backspace(self) -> None:
        """Delete the last character from current input."""
        if self._error:
            self._clear_error()
            return
        if self._new_input:
            return
        if len(self._current_input) <= 1 or (
            len(self._current_input) == 2
            and self._current_input[0] == "-"
        ):
            self._current_input = "0"
            self._new_input = True
        else:
            self._current_input = self._current_input[:-1]

    def input_percent(self) -> None:
        """Divide the current value by 100."""
        if self._error:
            return
        value = self._get_current_value()
        result = value / 100.0
        self._current_input = format_number(result)
        self._just_evaluated = False

    def input_negate(self) -> None:
        """Toggle the sign of the current value."""
        if self._error:
            return
        value = self._get_current_value()
        result = -value
        self._current_input = format_number(result)
        self._just_evaluated = False

    def get_display(self) -> str:
        """Return the formatted current value for display."""
        if self._error:
            return "Error"
        return self._current_input

    def get_expression(self) -> str:
        """Return the expression string for the secondary display."""
        return self._expression_display

    def get_value(self) -> float:
        """Return the raw numeric value of the current display."""
        if self._error:
            return 0.0
        try:
            return float(self._current_input)
        except ValueError:
            return 0.0

    def set_value(self, value: float) -> None:
        """Set the current display value (for mode switching)."""
        self._current_input = format_number(value)
        self._new_input = True
        self._just_evaluated = False

    def is_error(self) -> bool:
        """Return whether the calculator is in an error state."""
        return self._error

    def _get_current_value(self) -> float:
        """Parse the current input string to a float."""
        try:
            return float(self._current_input)
        except ValueError:
            return 0.0

    def _push_current_number(self) -> None:
        """Push the current input number onto the token stack."""
        value = self._current_input
        if not self._new_input or not self._tokens:
            self._tokens.append(value)
            if not self._expression_display or self._new_input:
                self._expression_display += value
        self._new_input = True

    def _apply_top_operator(self) -> None:
        """Pop the top operator and apply it to the top two tokens."""
        if len(self._tokens) < 2 or not self._operators:
            self._error = True
            return
        op = self._operators.pop()
        try:
            b = float(self._tokens.pop())
            a = float(self._tokens.pop())
        except (ValueError, IndexError):
            self._error = True
            return
        result = self._evaluate_binary(a, op, b)
        if result is None:
            self._error = True
            return
        self._tokens.append(str(result))

    def _evaluate_binary(
        self, a: float, op: str, b: float
    ) -> float | None:
        """Evaluate a binary operation, returning None on error."""
        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            return a * b
        elif op == "/":
            if b == 0:
                return None
            return a / b
        return None

    def _clear_error(self) -> None:
        """Clear error state and reset for new input."""
        self._error = False
        self._current_input = "0"
        self._tokens = []
        self._operators = []
        self._expression_display = ""
        self._new_input = True
        self._just_evaluated = False
