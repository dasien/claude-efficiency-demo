"""Basic calculator logic — arithmetic with operator precedence."""

from typing import List, Union
from calculator.logic.base_logic import BaseCalculatorLogic


Token = Union[float, str]

OPERATORS = {"+", "-", "*", "/", "**"}


class BasicLogic(BaseCalculatorLogic):
    """Basic mode calculator with four operations and operator precedence."""

    def __init__(self) -> None:
        super().__init__()
        self._pending_operator: str = ""
        self._tokens: List[Token] = []
        self._need_operand: bool = False

    def all_clear(self) -> None:
        """Reset all state."""
        super().all_clear()
        self._pending_operator = ""
        self._tokens = []
        self._need_operand = False

    def _clear_error(self) -> None:
        """Clear error state."""
        super()._clear_error()
        self._pending_operator = ""
        self._tokens = []
        self._need_operand = False

    def input_operator(self, op: str) -> None:
        """Handle operator input (+, -, *, /)."""
        if self.error:
            return

        current = self.get_current_value()

        if self._need_operand or self.input_mode == "typing" or self.input_mode == "result":
            self._tokens.append(current)
            self._need_operand = False

        # If the last token is an operator, replace it
        if self._tokens and isinstance(self._tokens[-1], str) and self._tokens[-1] in OPERATORS:
            self._tokens[-1] = op
        else:
            self._tokens.append(op)

        self._pending_operator = op
        self.input_mode = "ready"
        self._update_expression_str()

    def _update_expression_str(self) -> None:
        """Update the expression display string."""
        parts = []
        for t in self._tokens:
            if isinstance(t, float):
                parts.append(self.format_number(t))
            else:
                parts.append(str(t))
        self._expression_str = " ".join(parts)

    def evaluate(self) -> None:
        """Evaluate the full expression with operator precedence."""
        if self.error:
            return

        current = self.get_current_value()

        # Build complete token list
        tokens = list(self._tokens)
        if not tokens:
            # No pending expression, just keep current value
            self.input_mode = "result"
            return

        # If last token is an operator, add current value
        if isinstance(tokens[-1], str) and tokens[-1] in OPERATORS:
            tokens.append(current)

        # Update expression display
        parts = []
        for t in tokens:
            if isinstance(t, float):
                parts.append(self.format_number(t))
            else:
                parts.append(str(t))
        self._expression_str = " ".join(parts) + " ="

        # Evaluate with precedence
        result = self._evaluate_tokens(tokens)
        if result is None:
            self._set_error()
            return

        self.display_value = self.format_number(result)
        self.input_mode = "result"
        self._tokens = []
        self._pending_operator = ""
        self._need_operand = False

    def _evaluate_tokens(self, tokens: List[Token]) -> Union[float, None]:
        """Evaluate token list with operator precedence (*, / before +, -)."""
        if not tokens:
            return None

        # First pass: evaluate * and /
        intermediate: List[Token] = []
        i = 0
        while i < len(tokens):
            if isinstance(tokens[i], str) and tokens[i] in ("*", "/"):
                op = tokens[i]
                i += 1
                if i >= len(tokens):
                    return None
                right = tokens[i]
                if not isinstance(right, (int, float)):
                    return None
                left = intermediate.pop()
                if not isinstance(left, (int, float)):
                    return None
                if op == "*":
                    intermediate.append(float(left) * float(right))
                elif op == "/":
                    if float(right) == 0:
                        return None
                    intermediate.append(float(left) / float(right))
            else:
                intermediate.append(tokens[i])
            i += 1

        # Second pass: evaluate + and -
        if not intermediate:
            return None

        result = intermediate[0]
        if not isinstance(result, (int, float)):
            return None
        result = float(result)

        i = 1
        while i < len(intermediate):
            if i + 1 >= len(intermediate):
                return None
            op = intermediate[i]
            right = intermediate[i + 1]
            if not isinstance(right, (int, float)):
                return None
            if op == "+":
                result += float(right)
            elif op == "-":
                result -= float(right)
            else:
                return None
            i += 2

        return result
