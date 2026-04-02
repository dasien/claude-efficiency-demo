"""Basic mode calculator logic with token-based expression evaluation."""

from typing import List, Optional, Union

from calculator.logic.base_logic import BaseLogic, DisplayState


# Type alias for token lists: numbers and operator strings
Token = Union[float, str]


class BasicLogic(BaseLogic):
    """Basic calculator with four-function arithmetic and operator precedence.

    Expressions are stored as a flat token list of alternating numbers
    and operators: [num, op, num, op, num, ...].  Evaluation uses a
    two-pass algorithm (multiply/divide first, then add/subtract) so
    that standard operator precedence is respected.
    """

    OPERATORS = {"+", "-", "*", "/"}

    def __init__(self) -> None:
        super().__init__()
        self._tokens: List[Token] = []
        self._pending_op: Optional[str] = None
        self._last_evaluated: bool = False

    # ── Operator input ──────────────────────────────────────────

    def input_operator(self, op: str) -> DisplayState:
        """Handle an arithmetic operator press (+, -, *, /).

        Commits the current input as a number token, stores the
        pending operator, and updates the expression display string.
        If an operator is pressed immediately after another operator,
        the previous operator is replaced.

        Args:
            op: One of '+', '-', '*', '/'.
        """
        if self._error:
            return self.get_display_state()

        if self._last_evaluated:
            # After evaluation, chain: use result as first operand
            self._last_evaluated = False

        if self._pending_op is not None and self._new_input:
            # Consecutive operator press -- replace previous operator
            self._pending_op = op
            # Update expression string: replace last operator
            expr = self._expression.rstrip()
            if expr and expr[-1] in "+-*/":
                self._expression = expr[:-1] + op + " "
            return self.get_display_state()

        # Commit current value as a token
        value = self.get_current_value()
        if self._pending_op is not None:
            self._tokens.append(self._pending_op)
        self._tokens.append(value)

        self._pending_op = op
        self._expression += self.format_number(value) + " " + op + " "
        self._new_input = True

        return self.get_display_state()

    # ── Percent ─────────────────────────────────────────────────

    def input_percent(self) -> DisplayState:
        """Divide the current display value by 100 (NI-6)."""
        if self._error:
            return self.get_display_state()

        value = self.get_current_value() / 100.0
        self._current_input = self.format_number(value)
        return self.get_display_state()

    # ── Evaluate ────────────────────────────────────────────────

    def evaluate(self) -> DisplayState:
        """Evaluate the full token expression and display the result.

        Edge cases handled:
        - ``5 + =`` evaluates as ``5 + 5 = 10``.
        - Pressing ``=`` with no expression returns the current value.
        - Division by zero sets the error state.
        """
        if self._error:
            return self.get_display_state()

        current_value = self.get_current_value()

        if not self._tokens and self._pending_op is None:
            # No expression at all -- just show current value
            self._expression = (
                self.format_number(current_value) + " ="
            )
            self._last_evaluated = True
            self._new_input = True
            return self.get_display_state()

        # Build final token list for evaluation
        tokens: List[Token] = list(self._tokens)

        if self._pending_op is not None:
            tokens.append(self._pending_op)
            # ``5 + =`` means ``5 + 5``
            tokens.append(current_value)
            self._expression += (
                self.format_number(current_value) + " ="
            )
        else:
            # Tokens already complete -- just append " ="
            self._expression += " ="

        result = self._evaluate_tokens(tokens)

        if result is None:
            # Division by zero or other error
            self._error = True
            self._current_input = "Error"
            self._tokens = []
            self._pending_op = None
            self._last_evaluated = False
            return self.get_display_state()

        self._current_input = self.format_number(result)
        self._tokens = []
        self._pending_op = None
        self._new_input = True
        self._last_evaluated = True

        return self.get_display_state()

    # ── Token evaluation (two-pass) ─────────────────────────────

    def _evaluate_tokens(
        self, tokens: List[Token]
    ) -> Optional[float]:
        """Evaluate a flat token list respecting operator precedence.

        Pass 1: resolve ``*`` and ``/`` left to right.
        Pass 2: resolve ``+`` and ``-`` left to right.

        Args:
            tokens: A list of alternating floats and operator strings,
                e.g. ``[2.0, '+', 3.0, '*', 4.0]``.

        Returns:
            The numeric result, or ``None`` on error (e.g. division
            by zero).
        """
        if not tokens:
            return None

        # --- Pass 1: multiply and divide ---
        intermediate: List[Token] = [tokens[0]]
        i = 1
        while i < len(tokens) - 1:
            op = tokens[i]
            right = tokens[i + 1]
            if op in ("*", "/"):
                left = intermediate.pop()
                if not isinstance(left, (int, float)):
                    return None
                if not isinstance(right, (int, float)):
                    return None
                if op == "*":
                    intermediate.append(float(left) * float(right))
                else:
                    if float(right) == 0.0:
                        return None
                    intermediate.append(float(left) / float(right))
            else:
                intermediate.append(op)
                intermediate.append(right)
            i += 2

        # --- Pass 2: add and subtract ---
        if not intermediate:
            return None

        result = float(intermediate[0])  # type: ignore[arg-type]
        j = 1
        while j < len(intermediate) - 1:
            op = intermediate[j]
            right = intermediate[j + 1]
            if not isinstance(right, (int, float)):
                return None
            if op == "+":
                result += float(right)
            elif op == "-":
                result -= float(right)
            else:
                return None
            j += 2

        return result

    # ── Clear ───────────────────────────────────────────────────

    def clear_all(self) -> DisplayState:
        """Reset all state except memory, including tokens and pending op."""
        self._tokens = []
        self._pending_op = None
        self._last_evaluated = False
        return super().clear_all()

    # ── Digit override for post-evaluation behavior ─────────────

    def input_digit(self, digit: str) -> DisplayState:
        """Append a digit, clearing expression state after an evaluation.

        Args:
            digit: A single character '0'-'9'.
        """
        if self._last_evaluated:
            # After evaluation, next digit starts a completely fresh entry
            self._expression = ""
            self._tokens = []
            self._pending_op = None
            self._last_evaluated = False
            self._new_input = True

        return super().input_digit(digit)

    def input_decimal(self) -> DisplayState:
        """Append a decimal point, clearing expression state after eval."""
        if self._last_evaluated:
            self._expression = ""
            self._tokens = []
            self._pending_op = None
            self._last_evaluated = False
            self._new_input = True

        return super().input_decimal()

    # ── Display state ───────────────────────────────────────────

    def get_display_state(self) -> DisplayState:
        """Build and return the current DisplayState for the View."""
        return DisplayState(
            main_display=self._current_input,
            expression_display=self._expression,
            error=self._error,
            memory_indicator=self.has_memory,
        )
