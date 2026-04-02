"""Pure calculator business logic with no GUI dependencies."""

import re


class CalculatorLogic:
    """Pure calculator logic: expression building, evaluation, and error handling.

    Attributes:
        expression: The current expression string being built.
        result: The last evaluation result string.
    """

    OPERATORS = set("+-*/")
    ALLOWED_CHARS = re.compile(r"^[0-9+\-*/.()\s]*$")

    def __init__(self) -> None:
        """Initialize with an empty expression."""
        self._expression: str = ""
        self._result: str = ""
        self._evaluated: bool = False

    @property
    def expression(self) -> str:
        """Return the current expression string."""
        return self._expression

    @property
    def result(self) -> str:
        """Return the last evaluation result."""
        return self._result

    def append_number(self, number: str) -> str:
        """Append a digit or decimal point to the expression.

        Args:
            number: A single character ('0'-'9' or '.').

        Returns:
            The updated expression string for display.
        """
        if self._evaluated:
            if self._result == "Error":
                self._expression = ""
            else:
                self._expression = ""
            self._evaluated = False
            self._result = ""

        if number == ".":
            current_number = self._get_current_number()
            if "." in current_number:
                return self._expression
        self._expression += number
        return self._expression

    def append_operator(self, operator: str) -> str:
        """Append an operator (+, -, *, /) to the expression.

        Args:
            operator: One of '+', '-', '*', '/'.

        Returns:
            The updated expression string for display.
        """
        if self._evaluated:
            if self._result != "Error":
                self._expression = self._result
            else:
                self._expression = ""
            self._evaluated = False
            self._result = ""

        if not self._expression:
            return self._expression

        if self._expression[-1] in self.OPERATORS:
            self._expression = self._expression[:-1] + operator
        else:
            self._expression += operator

        return self._expression

    def evaluate(self) -> str:
        """Evaluate the current expression and return the result as a string.

        Returns:
            The result as a string. Returns "Error" if evaluation fails
            (e.g., division by zero, syntax error). If the result is a
            whole number, returns it without a decimal point.
        """
        if not self._expression:
            self._result = "Error"
            self._evaluated = True
            return self._result

        if not self.ALLOWED_CHARS.match(self._expression):
            self._result = "Error"
            self._evaluated = True
            return self._result

        try:
            value = eval(self._expression)  # noqa: S307
            if isinstance(value, float) and value == int(value):
                self._result = str(int(value))
            else:
                self._result = str(value)
        except (SyntaxError, ZeroDivisionError, TypeError,
                NameError, OverflowError, ValueError):
            self._result = "Error"

        self._evaluated = True
        return self._result

    def clear(self) -> str:
        """Clear the current expression and reset to initial state.

        Returns:
            An empty string for display.
        """
        self._expression = ""
        self._result = ""
        self._evaluated = False
        return ""

    def get_display_text(self) -> str:
        """Return what should be shown in the display.

        Returns:
            The result if just evaluated, otherwise the current expression.
        """
        if self._evaluated and self._result:
            return self._result
        return self._expression

    def get_expression(self) -> str:
        """Return the current expression string.

        Returns:
            The current expression.
        """
        return self._expression

    def append_to_expression(self, value: str) -> str:
        """Append a character (digit, operator, or decimal point) to the expression.

        This is a convenience method that routes to append_number or
        append_operator based on the value.

        Args:
            value: A single character to append.

        Returns:
            The updated expression string for display.
        """
        if value in self.OPERATORS:
            return self.append_operator(value)
        return self.append_number(value)

    def _get_current_number(self) -> str:
        """Extract the current (rightmost) number being typed.

        Returns:
            The current number segment as a string.
        """
        current = ""
        for char in reversed(self._expression):
            if char in self.OPERATORS:
                break
            current = char + current
        return current
