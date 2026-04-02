"""Basic calculator logic with four-function arithmetic and expression parsing.

Supports +, -, *, / with proper operator precedence via the shunting-yard
algorithm. Handles digit input, decimal points, sign toggle, percentage,
clear, all-clear, and backspace.
"""

from __future__ import annotations

from calculator.logic.base_logic import (
    BaseCalculator,
    CalculatorError,
    ExpressionParser,
)


class BasicCalculator(BaseCalculator):
    """Basic mode: four-function arithmetic with expression parsing.

    Builds an expression token list as the user enters digits and
    operators, then evaluates using the shunting-yard parser when
    equals is pressed.
    """

    def __init__(self) -> None:
        super().__init__()
        self._parser = ExpressionParser()

    def add_operator(self, op: str) -> None:
        """Append an operator to the expression.

        Finalizes the current input as a number token, then appends
        the operator. If no current input and expression ends with
        an operator, replaces the last operator.

        Args:
            op: The operator string ('+', '-', '*', '/').
        """
        if self.error_state:
            return

        if self.current_input:
            value = float(self.current_input)
            self.expression.append(value)
            self.current_input = ""
            self.last_result = None
        elif self.last_result is not None and not self.expression:
            self.expression.append(self.last_result)
            self.last_result = None
        elif (
            not self.current_input
            and self.expression
            and isinstance(self.expression[-1], str)
            and self.expression[-1] in self._parser.PRECEDENCE
        ):
            self.expression[-1] = op
            return
        elif not self.current_input and not self.expression:
            self.expression.append(0.0)

        self.expression.append(op)

    def evaluate(self) -> float:
        """Evaluate the full expression and return the result.

        Finalizes any current input, runs the parser, stores the
        result, and resets the expression.

        Returns:
            The computed result.

        Raises:
            CalculatorError: On division by zero or malformed expression.
        """
        if self.error_state:
            raise CalculatorError("Error state active")

        if self.current_input:
            value = float(self.current_input)
            self.expression.append(value)
            self.current_input = ""
        elif self.last_result is not None and not self.expression:
            return self.last_result
        elif (
            self.expression
            and isinstance(self.expression[-1], str)
            and self.expression[-1] in self._parser.PRECEDENCE
        ):
            if self.last_result is not None:
                self.expression.append(self.last_result)
            else:
                self.expression.pop()

        if not self.expression:
            return 0.0

        # Remove trailing operators
        while (
            self.expression
            and isinstance(self.expression[-1], str)
            and self.expression[-1] in self._parser.PRECEDENCE
        ):
            self.expression.pop()

        if not self.expression:
            return 0.0

        result = self._parser.parse(self.expression)
        self.last_result = result
        self.expression = []
        self.current_input = ""
        return result

    def get_expression_display(self) -> str:
        """Return the current expression as a display string.

        Includes the current input at the end if present.

        Returns:
            The expression formatted for the secondary display.
        """
        display = super().get_expression_display()
        if self.current_input:
            if display:
                display += f" {self.current_input}"
            else:
                display = self.current_input
        return display
