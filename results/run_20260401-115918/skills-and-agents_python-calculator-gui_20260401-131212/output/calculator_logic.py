"""Business logic module for a Tkinter calculator application.

This module is completely independent of any GUI code and handles
all calculator operations, expression management, and evaluation.
"""

import re


ALLOWED_CHARS_PATTERN = re.compile(r"^[0-9+\-*/.()\s]*$")
OPERATORS = {"+", "-", "*", "/"}


class CalculatorLogic:
    """Core calculator logic handling expression building and evaluation.

    Manages the current expression string and provides methods for
    digit input, operator handling, evaluation, and display formatting.
    """

    def __init__(self) -> None:
        """Initialize calculator state."""
        self._expression: str = ""
        self._result_displayed: bool = False

    def add_digit(self, digit: str) -> None:
        """Append a digit to the current expression.

        Args:
            digit: A single digit character (0-9).
        """
        if self._result_displayed:
            self._expression = ""
            self._result_displayed = False
        self._expression += digit

    def add_operator(self, operator: str) -> None:
        """Append an operator to the current expression.

        If the last character is already an operator, it is replaced.
        A leading minus is allowed to start a negative number.

        Args:
            operator: One of +, -, *, /.
        """
        if self._result_displayed:
            self._result_displayed = False

        if not self._expression:
            if operator == "-":
                self._expression = "-"
            return

        if self._expression[-1] in OPERATORS:
            self._expression = self._expression[:-1] + operator
        else:
            self._expression += operator

    def add_decimal(self) -> None:
        """Add a decimal point, preventing multiple decimals per number."""
        if self._result_displayed:
            self._expression = "0"
            self._result_displayed = False

        current_number = self._get_current_number()
        if "." in current_number:
            return

        if not self._expression or self._expression[-1] in OPERATORS:
            self._expression += "0."
        else:
            self._expression += "."

    def evaluate(self) -> str:
        """Evaluate the current expression and return the result as a string.

        Uses Python's eval with safety checks to compute the result.
        Handles division by zero and other errors gracefully.

        Returns:
            The formatted result string, or "Error" if evaluation fails.
        """
        if not self._expression:
            self._result_displayed = True
            return "0"

        expression = self._expression.rstrip("+-*/")
        if not expression:
            self._result_displayed = True
            return "0"

        if not ALLOWED_CHARS_PATTERN.match(expression):
            self._expression = ""
            self._result_displayed = True
            return "Error"

        try:
            result = eval(expression, {"__builtins__": {}}, {})  # noqa: S307
        except ZeroDivisionError:
            self._expression = ""
            self._result_displayed = True
            return "Error"
        except Exception:
            self._expression = ""
            self._result_displayed = True
            return "Error"

        formatted = self._format_result(result)
        self._expression = formatted
        self._result_displayed = True
        return formatted

    def clear(self) -> None:
        """Reset the expression to an empty string."""
        self._expression = ""
        self._result_displayed = False

    def get_display(self) -> str:
        """Return the current expression for display.

        Returns:
            The current expression, or "0" if empty.
        """
        return self._expression if self._expression else "0"

    def toggle_sign(self) -> None:
        """Toggle the sign of the current number in the expression."""
        if self._result_displayed:
            self._result_displayed = False

        if not self._expression:
            return

        number_start = self._find_current_number_start()
        prefix = self._expression[:number_start]
        current_number = self._expression[number_start:]

        if current_number.startswith("-"):
            self._expression = prefix + current_number[1:]
        else:
            self._expression = prefix + "-" + current_number

    def add_percent(self) -> None:
        """Divide the current number by 100."""
        if self._result_displayed:
            self._result_displayed = False

        if not self._expression:
            return

        number_start = self._find_current_number_start()
        prefix = self._expression[:number_start]
        current_number = self._expression[number_start:]

        if not current_number:
            return

        try:
            value = float(current_number) / 100
            formatted = self._format_result(value)
            self._expression = prefix + formatted
        except ValueError:
            return

    def backspace(self) -> None:
        """Remove the last character from the expression."""
        if self._result_displayed:
            self._expression = ""
            self._result_displayed = False
            return
        self._expression = self._expression[:-1]

    def _get_current_number(self) -> str:
        """Extract the current (rightmost) number from the expression.

        Returns:
            The current number as a string.
        """
        start = self._find_current_number_start()
        return self._expression[start:]

    def _find_current_number_start(self) -> int:
        """Find the starting index of the current number in the expression.

        Returns:
            The index where the current number begins.
        """
        i = len(self._expression) - 1
        while i >= 0:
            char = self._expression[i]
            if char in OPERATORS:
                if i == 0 and char == "-":
                    return 0
                if i > 0 and self._expression[i - 1] in OPERATORS:
                    return i
                if char == "-" and i == 0:
                    return 0
                return i + 1
            i -= 1
        return 0

    @staticmethod
    def _format_result(result: float) -> str:
        """Format a numeric result for display.

        Shows integers without a decimal point, limits float precision
        to 10 significant digits, and strips trailing zeros.

        Args:
            result: The numeric result to format.

        Returns:
            The formatted result string.
        """
        if isinstance(result, float) and result.is_integer():
            return str(int(result))

        if isinstance(result, int):
            return str(result)

        formatted = f"{result:.10g}"
        return formatted
