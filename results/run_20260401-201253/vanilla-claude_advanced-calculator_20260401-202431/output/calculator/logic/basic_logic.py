"""Basic calculator logic with expression evaluation and operator precedence."""

from typing import List, Optional, Tuple, Union
from .base_logic import BaseCalculator


Token = Union[float, str]


class BasicCalculator(BaseCalculator):
    """Basic mode calculator with arithmetic and operator precedence."""

    def __init__(self) -> None:
        """Initialize basic calculator state."""
        super().__init__()
        self._tokens: List[Token] = []
        self._pending_operator: Optional[str] = None
        self._last_operator: Optional[str] = None
        self._last_operand: Optional[float] = None

    def all_clear(self) -> None:
        """Reset all state including expression tokens."""
        super().all_clear()
        self._tokens = []
        self._pending_operator = None
        self._last_operator = None
        self._last_operand = None

    def input_digit(self, digit: str) -> None:
        """Handle digit input, committing pending operator if needed."""
        if self._error:
            self.all_clear()

        if self._new_input and self._pending_operator is not None:
            # Commit the current value and operator to tokens
            pass

        super().input_digit(digit)

    def input_operator(self, op: str) -> None:
        """Handle an operator (+, -, *, /) input."""
        if self._error:
            return

        current_val = self.get_current_value()

        if self._pending_operator is not None and self._new_input:
            # User pressed operator again without entering a number - replace pending op
            if self._tokens and isinstance(self._tokens[-1], str):
                self._tokens[-1] = op
                self._pending_operator = op
                self._update_expression()
                return
        elif self._pending_operator is not None and not self._new_input:
            # Chained operation: append the current value, then the new operator
            self._tokens.append(current_val)
        elif not self._tokens:
            # First operand
            self._tokens.append(current_val)
        else:
            self._tokens.append(current_val)

        self._pending_operator = op
        self._tokens.append(op)
        self._new_input = True
        self._update_expression()

    def evaluate(self) -> None:
        """Evaluate the full expression and display the result."""
        if self._error:
            return

        current_val = self.get_current_value()

        if self._pending_operator is not None and not self._new_input:
            # Complete the expression with the current input
            self._tokens.append(current_val)
            self._last_operator = self._pending_operator
            self._last_operand = current_val
        elif self._pending_operator is not None and self._new_input:
            # Operator pressed but no second operand - use current value as both
            self._tokens.append(current_val)
            self._last_operator = self._pending_operator
            self._last_operand = current_val
        elif self._last_operator is not None and self._last_operand is not None:
            # Repeated equals - apply last operation again
            self._tokens = [current_val, self._last_operator, self._last_operand]
        else:
            # Just a number, no operation
            self._computed_value = current_val
            self._current_input = self.format_number(current_val)
            self._new_input = True
            self._expression = ""
            return

        # Build expression string for display
        self._update_expression_with_equals()

        # Evaluate the token list
        result = self._evaluate_tokens(self._tokens)
        if result is None:
            self._set_error("Error")
        else:
            self._computed_value = result
            self._current_input = self.format_number(result)

        self._tokens = []
        self._pending_operator = None
        self._new_input = True

    def _evaluate_tokens(self, tokens: List[Token]) -> Optional[float]:
        """Evaluate a list of tokens respecting operator precedence.

        Uses two-pass approach:
        1. First pass: evaluate * and /
        2. Second pass: evaluate + and -
        """
        if not tokens:
            return None

        # Separate into numbers and operators
        # tokens should be: [num, op, num, op, num, ...]
        values: List[float] = []
        ops: List[str] = []

        for i, token in enumerate(tokens):
            if i % 2 == 0:
                if isinstance(token, (int, float)):
                    values.append(float(token))
                else:
                    return None
            else:
                if isinstance(token, str):
                    ops.append(token)
                else:
                    return None

        if len(values) != len(ops) + 1:
            return None

        # First pass: * and /
        new_values: List[float] = [values[0]]
        new_ops: List[str] = []

        for i, op in enumerate(ops):
            if op in ("*", "/"):
                left = new_values.pop()
                right = values[i + 1]
                result = self._apply_op(left, op, right)
                if result is None:
                    return None
                new_values.append(result)
            else:
                new_values.append(values[i + 1])
                new_ops.append(op)

        # Second pass: + and -
        result = new_values[0]
        for i, op in enumerate(new_ops):
            right = new_values[i + 1]
            r = self._apply_op(result, op, right)
            if r is None:
                return None
            result = r

        return result

    @staticmethod
    def _apply_op(left: float, op: str, right: float) -> Optional[float]:
        """Apply a binary operator. Returns None on error (e.g., division by zero)."""
        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            if right == 0:
                return None
            return left / right
        return None

    def _update_expression(self) -> None:
        """Update the expression display string from current tokens."""
        parts = []
        for token in self._tokens:
            if isinstance(token, float):
                parts.append(self.format_number(token))
            elif isinstance(token, str):
                parts.append(f" {token} ")
            else:
                parts.append(str(token))
        self._expression = "".join(parts)

    def _update_expression_with_equals(self) -> None:
        """Update expression with = sign for display."""
        parts = []
        for token in self._tokens:
            if isinstance(token, float):
                parts.append(self.format_number(token))
            elif isinstance(token, str):
                parts.append(f" {token} ")
            else:
                parts.append(str(token))
        self._expression = "".join(parts) + " ="
