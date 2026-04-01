"""Pure Python calculator logic module with no GUI dependencies."""

import re


class CalculatorLogic:
    """Core calculator logic handling expression building and evaluation.

    Manages an expression string and provides methods for appending
    digits, operators, decimals, and evaluating the result. Designed
    to be independently testable with no UI dependencies.
    """

    _OPERATORS = {"+", "-", "*", "/"}
    _VALID_EXPR_PATTERN = re.compile(r"^[0-9+\-*/.]+$")

    def __init__(self) -> None:
        self._expression: str = ""
        self._error: bool = False
        self._just_evaluated: bool = False

    def append_digit(self, digit: str) -> str:
        """Append a digit ('0'-'9') to the expression.

        Args:
            digit: A single character '0' through '9'.

        Returns:
            The updated display string.
        """
        if self._error:
            self._error = False
            self._expression = digit
            self._just_evaluated = False
            return self.get_display()

        if self._just_evaluated:
            self._expression = digit
            self._just_evaluated = False
            return self.get_display()

        if self._expression == "0" and digit == "0":
            return self.get_display()

        if self._expression == "0" and digit != "0":
            self._expression = digit
            return self.get_display()

        current_number = self._get_current_number()
        if (
            current_number == "0"
            and digit == "0"
            and "." not in current_number
        ):
            return self.get_display()

        if (
            current_number == "0"
            and digit != "0"
            and "." not in current_number
        ):
            self._expression = self._expression[:-1] + digit
            return self.get_display()

        self._expression += digit
        return self.get_display()

    def append_decimal(self) -> str:
        """Append a decimal point to the expression.

        If the current number already contains a decimal, the call
        is ignored. If the expression is empty or ends with an
        operator, '0.' is appended.

        Returns:
            The updated display string.
        """
        if self._error:
            return self.get_display()

        if self._just_evaluated:
            self._expression = "0."
            self._just_evaluated = False
            return self.get_display()

        current_number = self._get_current_number()

        if "." in current_number:
            return self.get_display()

        if (
            self._expression == ""
            or self._expression[-1] in self._OPERATORS
        ):
            self._expression += "0."
        else:
            self._expression += "."

        return self.get_display()

    def append_operator(self, op: str) -> str:
        """Append an operator (+, -, *, /) to the expression.

        If the expression ends with an operator, replaces it with
        the new one. If the expression is empty, only '-' is allowed
        (for negative numbers). Ignored during error state.

        Args:
            op: One of '+', '-', '*', '/'.

        Returns:
            The updated display string.
        """
        if self._error:
            return self.get_display()

        if self._just_evaluated:
            self._just_evaluated = False

        if self._expression == "":
            if op == "-":
                self._expression = "-"
            return self.get_display()

        if self._expression[-1] in self._OPERATORS:
            self._expression = self._expression[:-1] + op
        else:
            self._expression += op

        return self.get_display()

    def evaluate(self) -> str:
        """Evaluate the current expression.

        Uses eval() on a validated expression string containing only
        digits, decimal points, and arithmetic operators. Handles
        division by zero and other errors gracefully.

        Returns:
            The result as a display string, or 'Error' on failure.
        """
        if self._expression == "" or self._expression == "-":
            self._just_evaluated = True
            return self.get_display()

        expr = self._expression.rstrip("+-*/")

        if not expr:
            self._expression = ""
            self._just_evaluated = True
            return self.get_display()

        if not self._VALID_EXPR_PATTERN.match(expr):
            self._error = True
            self._expression = "Error"
            return self.get_display()

        try:
            result = eval(expr)  # noqa: S307
        except ZeroDivisionError:
            self._error = True
            self._expression = "Error"
            return self.get_display()
        except Exception:
            self._error = True
            self._expression = "Error"
            return self.get_display()

        if isinstance(result, float) and result == int(result):
            result_str = str(int(result))
        else:
            result_str = str(result)

        self._expression = result_str
        self._just_evaluated = True
        return self.get_display()

    def clear(self) -> str:
        """Reset all internal state.

        Returns:
            The display string '0'.
        """
        self._expression = ""
        self._error = False
        self._just_evaluated = False
        return self.get_display()

    def get_display(self) -> str:
        """Return the current display string.

        Returns:
            The expression if non-empty, 'Error' if in error state,
            or '0' if the expression is empty.
        """
        if self._error:
            return self._expression

        if self._expression == "":
            return "0"

        return self._expression

    def has_error(self) -> bool:
        """Return whether the calculator is in an error state.

        Returns:
            True if the last operation produced an error.
        """
        return self._error

    def _get_current_number(self) -> str:
        """Extract the current (rightmost) number from the expression.

        Returns:
            The current number token being built, or empty string.
        """
        if not self._expression:
            return ""

        current = ""
        for char in reversed(self._expression):
            if char in self._OPERATORS and current:
                break
            if char in self._OPERATORS and not current:
                break
            current = char + current

        return current
