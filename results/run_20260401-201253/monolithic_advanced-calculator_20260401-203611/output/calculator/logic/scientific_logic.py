"""Scientific calculator logic extending BasicCalculator.

Adds trigonometric, logarithmic, power/root functions,
constants, factorial, absolute value, and parentheses.
"""

from __future__ import annotations

import math

from calculator.logic.base_logic import format_number
from calculator.logic.basic_logic import BasicCalculator, PRECEDENCE


class ScientificCalculator(BasicCalculator):
    """Scientific mode calculator with trig, log, powers, and parentheses."""

    def __init__(self) -> None:
        super().__init__()
        self._angle_mode: str = "DEG"
        self._paren_depth: int = 0

    # --- Angle mode ---

    def set_angle_mode(self, mode: str) -> None:
        """Set angle mode to 'DEG' or 'RAD'."""
        self._angle_mode = mode.upper()

    def get_angle_mode(self) -> str:
        """Return the current angle mode ('DEG' or 'RAD')."""
        return self._angle_mode

    def toggle_angle_mode(self) -> None:
        """Toggle between DEG and RAD."""
        if self._angle_mode == "DEG":
            self._angle_mode = "RAD"
        else:
            self._angle_mode = "DEG"

    # --- Angle conversion helpers ---

    def _to_radians(self, value: float) -> float:
        """Convert value to radians if in degree mode."""
        if self._angle_mode == "DEG":
            return math.radians(value)
        return value

    def _from_radians(self, value: float) -> float:
        """Convert radians to current angle unit."""
        if self._angle_mode == "DEG":
            return math.degrees(value)
        return value

    # --- Trig functions ---

    def apply_sin(self) -> None:
        """Compute sine of the current value."""
        self._apply_unary(
            lambda v: math.sin(self._to_radians(v))
        )

    def apply_cos(self) -> None:
        """Compute cosine of the current value."""
        self._apply_unary(
            lambda v: math.cos(self._to_radians(v))
        )

    def apply_tan(self) -> None:
        """Compute tangent of the current value."""
        def _tan(v: float) -> float | None:
            rad = self._to_radians(v)
            cos_val = math.cos(rad)
            if abs(cos_val) < 1e-15:
                return None
            return math.sin(rad) / cos_val
        self._apply_unary_checked(_tan)

    def apply_asin(self) -> None:
        """Compute inverse sine of the current value."""
        def _asin(v: float) -> float | None:
            if v < -1 or v > 1:
                return None
            return self._from_radians(math.asin(v))
        self._apply_unary_checked(_asin)

    def apply_acos(self) -> None:
        """Compute inverse cosine of the current value."""
        def _acos(v: float) -> float | None:
            if v < -1 or v > 1:
                return None
            return self._from_radians(math.acos(v))
        self._apply_unary_checked(_acos)

    def apply_atan(self) -> None:
        """Compute inverse tangent of the current value."""
        self._apply_unary(
            lambda v: self._from_radians(math.atan(v))
        )

    # --- Logarithmic functions ---

    def apply_log(self) -> None:
        """Compute base-10 logarithm."""
        def _log(v: float) -> float | None:
            if v <= 0:
                return None
            return math.log10(v)
        self._apply_unary_checked(_log)

    def apply_ln(self) -> None:
        """Compute natural logarithm."""
        def _ln(v: float) -> float | None:
            if v <= 0:
                return None
            return math.log(v)
        self._apply_unary_checked(_ln)

    def apply_log2(self) -> None:
        """Compute base-2 logarithm."""
        def _log2(v: float) -> float | None:
            if v <= 0:
                return None
            return math.log2(v)
        self._apply_unary_checked(_log2)

    # --- Power and root functions ---

    def apply_square(self) -> None:
        """Square the current value."""
        self._apply_unary(lambda v: v * v)

    def apply_cube(self) -> None:
        """Cube the current value."""
        self._apply_unary(lambda v: v * v * v)

    def input_power(self) -> None:
        """Start a power operation (xⁿ). Uses operator mechanism."""
        self.input_operator("**")

    def apply_ten_power(self) -> None:
        """Compute 10 raised to the current value."""
        self._apply_unary(lambda v: 10.0 ** v)

    def apply_e_power(self) -> None:
        """Compute e raised to the current value."""
        self._apply_unary(lambda v: math.exp(v))

    def apply_sqrt(self) -> None:
        """Compute the square root."""
        def _sqrt(v: float) -> float | None:
            if v < 0:
                return None
            return math.sqrt(v)
        self._apply_unary_checked(_sqrt)

    def apply_cbrt(self) -> None:
        """Compute the cube root."""
        self._apply_unary(lambda v: math.copysign(
            abs(v) ** (1.0 / 3.0), v
        ))

    def apply_reciprocal(self) -> None:
        """Compute 1/x."""
        def _recip(v: float) -> float | None:
            if v == 0:
                return None
            return 1.0 / v
        self._apply_unary_checked(_recip)

    # --- Constants ---

    def input_pi(self) -> None:
        """Insert the value of pi."""
        if self._error:
            self._clear_error()
        self._current_input = format_number(math.pi)
        self._new_input = False
        self._just_evaluated = False

    def input_e(self) -> None:
        """Insert the value of Euler's number e."""
        if self._error:
            self._clear_error()
        self._current_input = format_number(math.e)
        self._new_input = False
        self._just_evaluated = False

    # --- Factorial and absolute value ---

    def apply_factorial(self) -> None:
        """Compute n! for the current value."""
        def _factorial(v: float) -> float | None:
            if v < 0:
                return None
            if v != int(v):
                return None
            n = int(v)
            if n > 170:
                return float("inf")
            return float(math.factorial(n))
        self._apply_unary_checked(_factorial)

    def apply_abs(self) -> None:
        """Compute the absolute value."""
        self._apply_unary(lambda v: abs(v))

    # --- Parentheses ---

    def input_open_paren(self) -> None:
        """Handle opening parenthesis."""
        if self._error:
            return
        if self._just_evaluated:
            self.input_all_clear()
        self._operators.append("(")
        self._paren_depth += 1
        self._expression_display += "("
        self._new_input = True

    def input_close_paren(self) -> None:
        """Handle closing parenthesis."""
        if self._error:
            return
        if self._paren_depth <= 0:
            self._error = True
            return
        self._push_current_number()
        self._expression_display += ")"
        while self._operators and self._operators[-1] != "(":
            self._apply_top_operator()
            if self._error:
                return
        if not self._operators or self._operators[-1] != "(":
            self._error = True
            return
        self._operators.pop()  # Remove the "("
        self._paren_depth -= 1
        if self._tokens:
            self._current_input = format_number(
                float(self._tokens[-1])
            )
        self._new_input = True

    def get_paren_depth(self) -> int:
        """Return the current parenthesis nesting depth."""
        return self._paren_depth

    # --- Override binary evaluation for ** ---

    def _evaluate_binary(
        self, a: float, op: str, b: float
    ) -> float | None:
        """Evaluate a binary operation including power."""
        if op == "**":
            try:
                result = a ** b
                if isinstance(result, complex):
                    return None
                return result
            except (OverflowError, ValueError):
                return None
        return super()._evaluate_binary(a, op, b)

    def input_operator(self, op: str) -> None:
        """Handle operators, adding ** to precedence."""
        if op == "**" and "**" not in PRECEDENCE:
            pass  # We handle precedence inline below
        if self._error:
            return
        self._push_current_number()
        self._expression_display += f" {op} "
        op_prec = PRECEDENCE.get(op, 3)  # ** gets precedence 3
        while (
            self._operators
            and self._operators[-1] != "("
            and self._operators[-1] in {
                "+", "-", "*", "/", "**"
            }
            and PRECEDENCE.get(self._operators[-1], 3)
            >= op_prec
        ):
            self._apply_top_operator()
        self._operators.append(op)
        self._new_input = True
        self._just_evaluated = False

    def input_all_clear(self) -> None:
        """Reset all state including paren depth."""
        super().input_all_clear()
        self._paren_depth = 0

    # --- Internal helpers ---

    def _apply_unary(self, func: object) -> None:
        """Apply a unary function that always succeeds."""
        if self._error:
            return
        value = self._get_current_value()
        result = func(value)  # type: ignore[operator]
        self._current_input = format_number(result)
        self._new_input = True
        self._just_evaluated = False

    def _apply_unary_checked(self, func: object) -> None:
        """Apply a unary function that may return None on error."""
        if self._error:
            return
        value = self._get_current_value()
        result = func(value)  # type: ignore[operator]
        if result is None:
            self._error = True
            return
        self._current_input = format_number(result)
        self._new_input = True
        self._just_evaluated = False
