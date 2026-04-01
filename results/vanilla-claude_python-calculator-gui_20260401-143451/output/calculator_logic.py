"""Calculator business logic — no GUI dependencies."""


class CalculatorLogic:
    """Pure business logic for a calculator application."""

    OPERATORS = {"+", "-", "*", "/"}

    def __init__(self) -> None:
        self._expression: str = ""
        self._result: str = "0"
        self._evaluated: bool = False
        self._error: bool = False

    def get_expression(self) -> str:
        return self._expression

    def get_result(self) -> str:
        return self._result

    def append_digit(self, digit: str) -> None:
        if self._evaluated or self._error:
            self._expression = ""
            self._result = "0"
            self._evaluated = False
            self._error = False
        self._expression += digit

    def append_decimal(self) -> None:
        if self._evaluated or self._error:
            self._expression = "0"
            self._result = "0"
            self._evaluated = False
            self._error = False

        current_number = self._get_current_number()
        if "." not in current_number:
            if current_number == "":
                self._expression += "0"
            self._expression += "."

    def append_operator(self, operator: str) -> None:
        if operator not in self.OPERATORS:
            return

        if self._error:
            self._error = False
            self._expression = ""
            self._result = "0"
            return

        if self._evaluated:
            self._expression = self._result
            self._evaluated = False

        if self._expression == "":
            return

        # Replace consecutive operator
        if self._expression and self._expression[-1] in self.OPERATORS:
            self._expression = self._expression[:-1]

        self._expression += operator

    def evaluate(self) -> None:
        if self._expression == "" or self._evaluated:
            return

        # Don't evaluate if expression ends with an operator
        expr = self._expression
        if expr and expr[-1] in self.OPERATORS:
            expr = expr[:-1]

        if not expr:
            return

        try:
            # Validate: only allow digits, operators, and decimal points
            allowed = set("0123456789.+-*/")
            if not all(c in allowed for c in expr):
                raise ValueError("Invalid characters in expression")

            result = eval(expr)  # noqa: S307
            self._result = self._format_result(result)
            self._expression = self._expression + "="
            self._evaluated = True
        except ZeroDivisionError:
            self._result = "Error"
            self._expression = self._expression + "="
            self._evaluated = False
            self._error = True
        except Exception:
            self._result = "Error"
            self._expression = self._expression + "="
            self._evaluated = False
            self._error = True

    def clear(self) -> None:
        self._expression = ""
        self._result = "0"
        self._evaluated = False
        self._error = False

    def _format_result(self, value: float) -> str:
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)

    def _get_current_number(self) -> str:
        """Extract the last number token from the expression."""
        result = ""
        for char in reversed(self._expression):
            if char in self.OPERATORS:
                break
            result = char + result
        return result
