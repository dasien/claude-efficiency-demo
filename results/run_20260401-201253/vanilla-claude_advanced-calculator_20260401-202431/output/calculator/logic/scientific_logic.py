"""Scientific calculator logic extending basic mode with advanced math functions."""

import math
from typing import List, Optional, Union
from .basic_logic import BasicCalculator, Token


class ScientificCalculator(BasicCalculator):
    """Scientific mode calculator with trig, log, power, and parentheses support."""

    def __init__(self) -> None:
        """Initialize scientific calculator state."""
        super().__init__()
        self._angle_mode: str = "DEG"  # "DEG" or "RAD"
        self._paren_depth: int = 0
        self._paren_stacks: List[dict] = []  # Stack of saved states for parens

    @property
    def angle_mode(self) -> str:
        """Current angle mode (DEG or RAD)."""
        return self._angle_mode

    @property
    def paren_depth(self) -> int:
        """Current parenthesis nesting depth."""
        return self._paren_depth

    def toggle_angle_mode(self) -> None:
        """Toggle between DEG and RAD angle modes."""
        self._angle_mode = "RAD" if self._angle_mode == "DEG" else "DEG"

    def _to_radians(self, value: float) -> float:
        """Convert value to radians based on current angle mode."""
        if self._angle_mode == "DEG":
            return math.radians(value)
        return value

    def _from_radians(self, value: float) -> float:
        """Convert radians to current angle mode."""
        if self._angle_mode == "DEG":
            return math.degrees(value)
        return value

    def _apply_unary(self, func_name: str) -> None:
        """Apply a unary function to the current value and update display."""
        if self._error:
            return
        value = self.get_current_value()
        try:
            result = self._compute_unary(func_name, value)
        except (ValueError, OverflowError, ZeroDivisionError):
            self._set_error("Error")
            return

        if result is None:
            self._set_error("Error")
            return

        if math.isnan(result) or math.isinf(result):
            self._set_error("Error")
            return

        self._computed_value = result
        self._current_input = self.format_number(result)
        self._new_input = True

    def _compute_unary(self, func_name: str, value: float) -> Optional[float]:
        """Compute a unary function. Returns None on domain error."""
        if func_name == "sin":
            rad = self._to_radians(value)
            result = math.sin(rad)
            # Clean up near-zero results
            if abs(result) < 1e-15:
                result = 0.0
            return result

        elif func_name == "cos":
            rad = self._to_radians(value)
            result = math.cos(rad)
            if abs(result) < 1e-15:
                result = 0.0
            return result

        elif func_name == "tan":
            rad = self._to_radians(value)
            # Check for undefined tan (90, 270, etc. in degrees)
            cos_val = math.cos(rad)
            if abs(cos_val) < 1e-15:
                return None
            result = math.tan(rad)
            return result

        elif func_name == "asin":
            if value < -1 or value > 1:
                return None
            return self._from_radians(math.asin(value))

        elif func_name == "acos":
            if value < -1 or value > 1:
                return None
            return self._from_radians(math.acos(value))

        elif func_name == "atan":
            return self._from_radians(math.atan(value))

        elif func_name == "log":
            if value <= 0:
                return None
            return math.log10(value)

        elif func_name == "ln":
            if value <= 0:
                return None
            return math.log(value)

        elif func_name == "log2":
            if value <= 0:
                return None
            return math.log2(value)

        elif func_name == "square":
            return value * value

        elif func_name == "cube":
            return value * value * value

        elif func_name == "ten_power":
            return 10.0 ** value

        elif func_name == "e_power":
            return math.exp(value)

        elif func_name == "sqrt":
            if value < 0:
                return None
            return math.sqrt(value)

        elif func_name == "cbrt":
            if value < 0:
                return -((-value) ** (1.0 / 3.0))
            return value ** (1.0 / 3.0)

        elif func_name == "reciprocal":
            if value == 0:
                return None
            return 1.0 / value

        elif func_name == "factorial":
            if value < 0 or value != int(value):
                return None
            n = int(value)
            if n > 170:
                return None
            return float(math.factorial(n))

        elif func_name == "absolute":
            return abs(value)

        return None

    # Public unary function methods

    def sin(self) -> None:
        """Compute sine of current value."""
        self._apply_unary("sin")

    def cos(self) -> None:
        """Compute cosine of current value."""
        self._apply_unary("cos")

    def tan(self) -> None:
        """Compute tangent of current value."""
        self._apply_unary("tan")

    def asin(self) -> None:
        """Compute inverse sine of current value."""
        self._apply_unary("asin")

    def acos(self) -> None:
        """Compute inverse cosine of current value."""
        self._apply_unary("acos")

    def atan(self) -> None:
        """Compute inverse tangent of current value."""
        self._apply_unary("atan")

    def log(self) -> None:
        """Compute base-10 logarithm."""
        self._apply_unary("log")

    def ln(self) -> None:
        """Compute natural logarithm."""
        self._apply_unary("ln")

    def log2(self) -> None:
        """Compute base-2 logarithm."""
        self._apply_unary("log2")

    def square(self) -> None:
        """Square the current value."""
        self._apply_unary("square")

    def cube(self) -> None:
        """Cube the current value."""
        self._apply_unary("cube")

    def power(self) -> None:
        """Start xⁿ operation (two-operand, uses operator mechanism)."""
        if self._error:
            return
        self.input_operator("**")

    def ten_power(self) -> None:
        """Compute 10 raised to the current value."""
        self._apply_unary("ten_power")

    def e_power(self) -> None:
        """Compute e raised to the current value."""
        self._apply_unary("e_power")

    def sqrt(self) -> None:
        """Compute square root."""
        self._apply_unary("sqrt")

    def cbrt(self) -> None:
        """Compute cube root."""
        self._apply_unary("cbrt")

    def reciprocal(self) -> None:
        """Compute reciprocal (1/x)."""
        self._apply_unary("reciprocal")

    def factorial(self) -> None:
        """Compute factorial."""
        self._apply_unary("factorial")

    def absolute(self) -> None:
        """Compute absolute value."""
        self._apply_unary("absolute")

    def insert_pi(self) -> None:
        """Insert the value of pi."""
        if self._error:
            self._clear_error()
        self._computed_value = math.pi
        self._current_input = self.format_number(math.pi)
        self._new_input = True

    def insert_e(self) -> None:
        """Insert the value of e."""
        if self._error:
            self._clear_error()
        self._computed_value = math.e
        self._current_input = self.format_number(math.e)
        self._new_input = True

    # Parentheses support

    def open_paren(self) -> None:
        """Handle open parenthesis - save current state and start fresh."""
        if self._error:
            self._clear_error()

        # Save current calculator state
        state = {
            "tokens": self._tokens[:],
            "pending_operator": self._pending_operator,
            "expression": self._expression,
        }
        self._paren_stacks.append(state)
        self._paren_depth += 1

        # Reset for sub-expression
        self._tokens = []
        self._pending_operator = None
        self._current_input = "0"
        self._computed_value = None
        self._new_input = True

    def close_paren(self) -> None:
        """Handle close parenthesis - evaluate sub-expression and restore state."""
        if self._error:
            return
        if self._paren_depth <= 0:
            self._set_error("Error")
            return

        # Evaluate the current sub-expression
        current_val = self.get_current_value()
        if self._pending_operator is not None:
            self._tokens.append(current_val)
            result = self._evaluate_tokens(self._tokens)
            if result is None:
                self._set_error("Error")
                return
        elif self._tokens:
            self._tokens.append(current_val)
            result = self._evaluate_tokens(self._tokens)
            if result is None:
                self._set_error("Error")
                return
        else:
            result = current_val

        # Restore parent state
        state = self._paren_stacks.pop()
        self._paren_depth -= 1
        self._tokens = state["tokens"]
        self._pending_operator = state["pending_operator"]

        # Set the result as the current value
        self._computed_value = result
        self._current_input = self.format_number(result)
        self._new_input = True

    def evaluate(self) -> None:
        """Evaluate expression, checking for mismatched parentheses."""
        if self._paren_depth > 0:
            self._set_error("Error")
            self._paren_depth = 0
            self._paren_stacks = []
            return
        super().evaluate()

    @staticmethod
    def _apply_op(left: float, op: str, right: float) -> Optional[float]:
        """Apply a binary operator, including power operator."""
        if op == "**":
            try:
                result = left ** right
                if math.isnan(result) or math.isinf(result):
                    return None
                return result
            except (OverflowError, ValueError):
                return None
        return BasicCalculator._apply_op(left, op, right)
