"""Business logic for a basic calculator. No GUI dependencies."""


class CalculatorLogic:
    """Pure calculator state machine. All public methods return the display string."""

    def __init__(self) -> None:
        self._reset()

    def _reset(self) -> None:
        """Reset all internal state."""
        self.current_input: str = "0"
        self.first_operand: float | None = None
        self.operator: str | None = None
        self.result_displayed: bool = False
        self.error: bool = False
        self.last_operator: str | None = None
        self.last_operand: float | None = None

    def get_display(self) -> str:
        """Return the current display string."""
        return self.current_input

    def input_digit(self, digit: str) -> str:
        """Append a digit to the current input."""
        if self.error:
            self._reset()
        if self.result_displayed:
            self.current_input = "0"
            self.result_displayed = False
        if self.current_input == "0":
            self.current_input = digit
        else:
            self.current_input += digit
        return self.current_input

    def input_decimal(self) -> str:
        """Append a decimal point if not already present."""
        if self.error:
            self._reset()
        if self.result_displayed:
            self.current_input = "0"
            self.result_displayed = False
        if "." not in self.current_input:
            self.current_input += "."
        return self.current_input

    def input_operator(self, op: str) -> str:
        """Set the pending operator. Evaluates any pending operation first (chaining)."""
        if self.error:
            self._reset()
        if self.operator and not self.result_displayed:
            # Chained operation: evaluate pending, then set new operator
            self._evaluate_pending()
            if self.error:
                return self.current_input
        self.first_operand = float(self.current_input)
        self.operator = op
        self.result_displayed = True
        self.last_operator = None
        self.last_operand = None
        return self.current_input

    def input_equals(self) -> str:
        """Evaluate the pending operation."""
        if self.error:
            self._reset()
            return self.current_input

        if self.operator and self.first_operand is not None:
            b = float(self.current_input)
            self.last_operator = self.operator
            self.last_operand = b
            return self._do_evaluate(self.first_operand, self.operator, b)
        elif self.last_operator and self.last_operand is not None:
            # Repeated equals
            a = float(self.current_input)
            return self._do_evaluate(a, self.last_operator, self.last_operand)

        # No pending operation
        self.result_displayed = True
        return self.current_input

    def input_clear(self) -> str:
        """Reset all state."""
        self._reset()
        return "0"

    def input_backspace(self) -> str:
        """Remove the last character from current input."""
        if self.error:
            self._reset()
            return self.current_input
        if self.result_displayed:
            return self.current_input
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
        return self.current_input

    def _evaluate_pending(self) -> None:
        """Evaluate the pending operation and update state."""
        if self.operator and self.first_operand is not None:
            b = float(self.current_input)
            self._do_evaluate(self.first_operand, self.operator, b)

    def _do_evaluate(self, a: float, op: str, b: float) -> str:
        """Perform arithmetic, update state, return display string."""
        try:
            result = self._evaluate(a, op, b)
        except ZeroDivisionError:
            self.current_input = "Error"
            self.error = True
            self.operator = None
            self.first_operand = None
            return self.current_input

        self.current_input = self._format_result(result)
        self.first_operand = None
        self.operator = None
        self.result_displayed = True
        return self.current_input

    @staticmethod
    def _evaluate(a: float, op: str, b: float) -> float:
        """Perform a single arithmetic operation."""
        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            return a * b
        elif op == "/":
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            return a / b
        raise ValueError(f"Unknown operator: {op}")

    @staticmethod
    def _format_result(value: float) -> str:
        """Format a result: integers show without decimal, floats rounded to 10 digits."""
        # Round to remove floating-point noise (e.g., 0.1 + 0.2 = 0.30000...04)
        rounded = round(value, 10)
        if rounded == int(rounded):
            return str(int(rounded))
        return str(rounded)
