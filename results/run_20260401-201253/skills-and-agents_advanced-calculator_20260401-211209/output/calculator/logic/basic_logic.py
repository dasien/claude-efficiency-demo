"""Basic calculator with operator chaining and expression evaluation."""

from calculator.logic.base_logic import BaseCalculator


class BasicCalculator(BaseCalculator):
    """Calculator supporting basic arithmetic with proper operator precedence.

    Extends BaseCalculator with operator handling and two-pass expression
    evaluation for correct order of operations.
    """

    def __init__(self) -> None:
        """Initialize the basic calculator."""
        super().__init__()
        self.pending_tokens: list = []

    def add_operator(self, op: str) -> None:
        """Finalize current input and add an operator.

        Converts the current input buffer to a float token, appends
        the operator, and prepares for new input.

        Args:
            op: The operator string ('+', '-', '*', '/', '**').
        """
        if not self._new_input:
            self.pending_tokens.append(float(self.input_buffer))
        elif self.pending_tokens or self.current_value != 0.0:
            if not self.pending_tokens or not isinstance(
                self.pending_tokens[-1], str
            ):
                self.pending_tokens.append(self.current_value)

        self.pending_tokens.append(op)
        self.input_buffer = "0"
        self._new_input = True
        self.expression += f" {self.format_number(self.current_value)} {op}"

    def evaluate(self) -> float:
        """Evaluate the pending expression and return the result.

        Finalizes current input, evaluates all tokens respecting
        operator precedence, and resets for new input.

        Returns:
            The computed result.
        """
        try:
            if not self._new_input:
                self.pending_tokens.append(float(self.input_buffer))
            elif not self.pending_tokens:
                return self.current_value
            else:
                self.pending_tokens.append(self.current_value)

            result = self._evaluate_tokens(self.pending_tokens)
            self.current_value = result
            self.pending_tokens = []
            self.expression += (
                f" {self.format_number(self.current_value)} ="
                if "=" not in self.expression
                else ""
            )
            self._new_input = True
            self.input_buffer = "0"
            return result
        except (ValueError, ZeroDivisionError, OverflowError):
            self.set_error("Error")
            self.pending_tokens = []
            self._new_input = True
            return 0.0

    def clear_all(self) -> None:
        """Reset all state except memory, including pending tokens."""
        super().clear_all()
        self.pending_tokens = []

    def _evaluate_tokens(self, tokens: list) -> float:
        """Evaluate a flat list of tokens with correct operator precedence.

        Uses two-pass evaluation:
        - Pass 1: Process *, /, ** (high precedence)
        - Pass 2: Process +, - (low precedence)

        Args:
            tokens: A list of alternating float values and operator strings.

        Returns:
            The computed result as a float.

        Raises:
            ValueError: If division by zero is attempted or tokens are
                malformed.
        """
        tokens = list(tokens)

        # Pass 1: high precedence (**, *, /)
        high_ops = {"*", "/", "**"}
        i = 1
        while i < len(tokens):
            if isinstance(tokens[i], str) and tokens[i] in high_ops:
                left = tokens[i - 1]
                op = tokens[i]
                right = tokens[i + 1]
                if op == "*":
                    result = left * right
                elif op == "/":
                    if right == 0:
                        raise ValueError("Division by zero")
                    result = left / right
                elif op == "**":
                    result = left ** right
                else:
                    result = 0.0
                tokens[i - 1:i + 2] = [result]
            else:
                i += 1

        # Pass 2: low precedence (+, -)
        low_ops = {"+", "-"}
        i = 1
        while i < len(tokens):
            if isinstance(tokens[i], str) and tokens[i] in low_ops:
                left = tokens[i - 1]
                op = tokens[i]
                right = tokens[i + 1]
                if op == "+":
                    result = left + right
                elif op == "-":
                    result = left - right
                else:
                    result = 0.0
                tokens[i - 1:i + 2] = [result]
            else:
                i += 1

        return float(tokens[0])
