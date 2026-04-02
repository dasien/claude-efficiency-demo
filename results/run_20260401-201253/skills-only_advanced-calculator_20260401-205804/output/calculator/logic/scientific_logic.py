"""Scientific calculator logic — trig, log, power, factorial, parentheses."""

import math
from typing import List, Optional, Union
from calculator.logic.basic_logic import BasicLogic, Token, OPERATORS


class ScientificLogic(BasicLogic):
    """Scientific mode extending basic with advanced math functions."""

    def __init__(self) -> None:
        super().__init__()
        self.angle_mode: str = "DEG"  # "DEG" or "RAD"
        self.paren_depth: int = 0
        self._paren_stacks: List[dict] = []

    def all_clear(self) -> None:
        """Reset all state."""
        super().all_clear()
        self.paren_depth = 0
        self._paren_stacks = []

    def _clear_error(self) -> None:
        """Clear error state."""
        super()._clear_error()
        self.paren_depth = 0
        self._paren_stacks = []

    def toggle_angle_mode(self) -> None:
        """Toggle between DEG and RAD mode."""
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"

    def _to_radians(self, value: float) -> float:
        """Convert value to radians based on current angle mode."""
        if self.angle_mode == "DEG":
            return math.radians(value)
        return value

    def _from_radians(self, value: float) -> float:
        """Convert radians to current angle unit."""
        if self.angle_mode == "DEG":
            return math.degrees(value)
        return value

    def apply_function(self, name: str) -> None:
        """Apply a unary scientific function to the current value."""
        if self.error:
            return

        value = self.get_current_value()

        try:
            result = self._compute_function(name, value)
        except (ValueError, OverflowError, ZeroDivisionError):
            self._set_error()
            return

        if result is None:
            self._set_error()
            return

        if math.isinf(result) or math.isnan(result):
            self._set_error()
            return

        self.display_value = self.format_number(result)
        self.input_mode = "result"

    def _compute_function(self, name: str, value: float) -> Optional[float]:
        """Compute a scientific function. Returns None on error."""
        if name == "sin":
            rad = self._to_radians(value)
            result = math.sin(rad)
            # Clean up near-zero results
            if abs(result) < 1e-15:
                return 0.0
            return result

        elif name == "cos":
            rad = self._to_radians(value)
            result = math.cos(rad)
            if abs(result) < 1e-15:
                return 0.0
            return result

        elif name == "tan":
            rad = self._to_radians(value)
            cos_val = math.cos(rad)
            if abs(cos_val) < 1e-15:
                return None  # undefined (e.g., tan(90°))
            result = math.tan(rad)
            if abs(result) < 1e-15:
                return 0.0
            return result

        elif name == "asin":
            if value < -1 or value > 1:
                return None
            return self._from_radians(math.asin(value))

        elif name == "acos":
            if value < -1 or value > 1:
                return None
            return self._from_radians(math.acos(value))

        elif name == "atan":
            return self._from_radians(math.atan(value))

        elif name == "log":
            if value <= 0:
                return None
            return math.log10(value)

        elif name == "ln":
            if value <= 0:
                return None
            return math.log(value)

        elif name == "log2":
            if value <= 0:
                return None
            return math.log2(value)

        elif name == "x2":
            return value ** 2

        elif name == "x3":
            return value ** 3

        elif name == "xn":
            # This is handled as a binary operator, not here
            return value

        elif name == "10x":
            return 10.0 ** value

        elif name == "ex":
            return math.exp(value)

        elif name == "sqrt":
            if value < 0:
                return None
            return math.sqrt(value)

        elif name == "cbrt":
            if value < 0:
                return -((-value) ** (1.0 / 3.0))
            return value ** (1.0 / 3.0)

        elif name == "recip":
            if value == 0:
                return None
            return 1.0 / value

        elif name == "fact":
            if value < 0 or value != int(value):
                return None
            n = int(value)
            if n > 170:
                raise OverflowError("Factorial too large")
            return float(math.factorial(n))

        elif name == "abs":
            return abs(value)

        return None

    def insert_constant(self, name: str) -> None:
        """Insert a mathematical constant."""
        if self.error:
            self._clear_error()

        if name == "pi":
            self.display_value = self.format_number(math.pi)
        elif name == "e":
            self.display_value = self.format_number(math.e)
        self.input_mode = "result"

    def open_paren(self) -> None:
        """Handle open parenthesis."""
        if self.error:
            self._clear_error()

        # Save current state
        self._paren_stacks.append({
            "tokens": self._tokens,
            "pending_operator": self._pending_operator,
            "need_operand": self._need_operand,
            "expression_str": self._expression_str,
        })
        self._tokens = []
        self._pending_operator = ""
        self._need_operand = False
        self.paren_depth += 1
        self.input_mode = "ready"
        self.display_value = "0"
        self._update_full_expression()

    def close_paren(self) -> None:
        """Handle close parenthesis."""
        if self.error or self.paren_depth == 0:
            return

        # Evaluate inner expression
        self.evaluate_inner()
        inner_result = self.get_current_value()

        # Restore outer state
        saved = self._paren_stacks.pop()
        self._tokens = saved["tokens"]
        self._pending_operator = saved["pending_operator"]
        self._need_operand = saved["need_operand"]
        self.paren_depth -= 1

        self.display_value = self.format_number(inner_result)
        self.input_mode = "result"
        self._update_full_expression()

    def evaluate_inner(self) -> None:
        """Evaluate the current expression without clearing state."""
        if self.error:
            return

        current = self.get_current_value()
        tokens = list(self._tokens)

        if not tokens:
            self.input_mode = "result"
            return

        if isinstance(tokens[-1], str) and tokens[-1] in OPERATORS:
            tokens.append(current)

        result = self._evaluate_tokens(tokens)
        if result is None:
            self._set_error()
            return

        self.display_value = self.format_number(result)
        self.input_mode = "result"
        self._tokens = []
        self._pending_operator = ""
        self._need_operand = False

    def _update_full_expression(self) -> None:
        """Update expression string including parentheses."""
        parts = []
        for saved in self._paren_stacks:
            for t in saved["tokens"]:
                if isinstance(t, float):
                    parts.append(self.format_number(t))
                else:
                    parts.append(str(t))
            parts.append("(")
        for t in self._tokens:
            if isinstance(t, float):
                parts.append(self.format_number(t))
            else:
                parts.append(str(t))
        self._expression_str = " ".join(parts)

    def evaluate(self) -> None:
        """Evaluate expression, handling unclosed parentheses as error."""
        if self.error:
            return

        if self.paren_depth > 0:
            self._set_error()
            return

        super().evaluate()

    def input_power(self) -> None:
        """Handle xⁿ as a binary operator."""
        self.input_operator("**")

    def _evaluate_tokens(self, tokens: list) -> Optional[float]:
        """Evaluate tokens, supporting ** operator."""
        if not tokens:
            return None

        # First pass: evaluate ** (right-associative but we do left-to-right here)
        intermediate: list = []
        i = 0
        while i < len(tokens):
            if isinstance(tokens[i], str) and tokens[i] == "**":
                i += 1
                if i >= len(tokens):
                    return None
                right = tokens[i]
                if not isinstance(right, (int, float)):
                    return None
                left = intermediate.pop()
                if not isinstance(left, (int, float)):
                    return None
                try:
                    result = float(left) ** float(right)
                    if math.isinf(result) or math.isnan(result):
                        return None
                    intermediate.append(result)
                except (OverflowError, ValueError):
                    return None
            else:
                intermediate.append(tokens[i])
            i += 1

        # Now delegate to parent's logic for *, /, +, -
        # Second pass: evaluate * and /
        second: list = []
        i = 0
        while i < len(intermediate):
            if isinstance(intermediate[i], str) and intermediate[i] in ("*", "/"):
                op = intermediate[i]
                i += 1
                if i >= len(intermediate):
                    return None
                right = intermediate[i]
                if not isinstance(right, (int, float)):
                    return None
                left = second.pop()
                if not isinstance(left, (int, float)):
                    return None
                if op == "*":
                    second.append(float(left) * float(right))
                elif op == "/":
                    if float(right) == 0:
                        return None
                    second.append(float(left) / float(right))
            else:
                second.append(intermediate[i])
            i += 1

        # Third pass: evaluate + and -
        if not second:
            return None

        result = second[0]
        if not isinstance(result, (int, float)):
            return None
        result = float(result)

        i = 1
        while i < len(second):
            if i + 1 >= len(second):
                return None
            op = second[i]
            right = second[i + 1]
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
