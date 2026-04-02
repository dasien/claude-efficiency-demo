"""Scientific calculator logic extending basic arithmetic.

Provides trigonometric functions (with degree/radian toggle), logarithms,
powers, roots, reciprocal, factorial, absolute value, parentheses with
nesting, and mathematical constants (pi, e).
"""

from __future__ import annotations

import math

from calculator.logic.base_logic import CalculatorError
from calculator.logic.basic_logic import BasicCalculator


class ScientificCalculator(BasicCalculator):
    """Scientific mode: extends Basic with advanced math functions.

    Adds trig, log, power, root, factorial, constants, and
    parenthesized expressions to the basic four-function calculator.
    """

    def __init__(self) -> None:
        super().__init__()
        self.angle_mode: str = "DEG"
        self.paren_depth: int = 0

    # --- Angle mode ---

    def toggle_angle_mode(self) -> str:
        """Toggle between degree and radian mode.

        Returns:
            The new angle mode string ('DEG' or 'RAD').
        """
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        return self.angle_mode

    def _to_radians(self, value: float) -> float:
        """Convert value to radians based on current angle mode.

        Args:
            value: Angle value in current mode's units.

        Returns:
            Value in radians.
        """
        if self.angle_mode == "DEG":
            return math.radians(value)
        return value

    def _from_radians(self, value: float) -> float:
        """Convert radians to current angle mode's units.

        Args:
            value: Angle value in radians.

        Returns:
            Value in current mode's units.
        """
        if self.angle_mode == "DEG":
            return math.degrees(value)
        return value

    # --- Trigonometric functions ---

    def sin(self, value: float) -> float:
        """Compute the sine of the value.

        Args:
            value: Angle in current angle mode units.

        Returns:
            The sine of the angle.
        """
        rad = self._to_radians(value)
        result = math.sin(rad)
        if abs(result) < 1e-15:
            result = 0.0
        return result

    def cos(self, value: float) -> float:
        """Compute the cosine of the value.

        Args:
            value: Angle in current angle mode units.

        Returns:
            The cosine of the angle.
        """
        rad = self._to_radians(value)
        result = math.cos(rad)
        if abs(result) < 1e-15:
            result = 0.0
        return result

    def tan(self, value: float) -> float:
        """Compute the tangent of the value.

        Args:
            value: Angle in current angle mode units.

        Returns:
            The tangent of the angle.

        Raises:
            CalculatorError: If tangent is undefined (cos near zero).
        """
        rad = self._to_radians(value)
        cos_val = math.cos(rad)
        if abs(cos_val) < 1e-15:
            raise CalculatorError("Undefined: tan at 90/270 degrees")
        result = math.tan(rad)
        if abs(result) < 1e-15:
            result = 0.0
        return result

    def asin(self, value: float) -> float:
        """Compute the inverse sine (arcsin) of the value.

        Args:
            value: A value in [-1, 1].

        Returns:
            The arcsin in current angle mode units.

        Raises:
            CalculatorError: If value is outside [-1, 1].
        """
        if value < -1 or value > 1:
            raise CalculatorError("Domain error: asin requires -1 <= x <= 1")
        result = math.asin(value)
        return self._from_radians(result)

    def acos(self, value: float) -> float:
        """Compute the inverse cosine (arccos) of the value.

        Args:
            value: A value in [-1, 1].

        Returns:
            The arccos in current angle mode units.

        Raises:
            CalculatorError: If value is outside [-1, 1].
        """
        if value < -1 or value > 1:
            raise CalculatorError("Domain error: acos requires -1 <= x <= 1")
        result = math.acos(value)
        return self._from_radians(result)

    def atan(self, value: float) -> float:
        """Compute the inverse tangent (arctan) of the value.

        Args:
            value: Any real number.

        Returns:
            The arctan in current angle mode units.
        """
        result = math.atan(value)
        return self._from_radians(result)

    # --- Logarithmic functions ---

    def log10(self, value: float) -> float:
        """Compute the base-10 logarithm.

        Args:
            value: Must be positive.

        Returns:
            log10(value).

        Raises:
            CalculatorError: If value <= 0.
        """
        if value <= 0:
            raise CalculatorError("Domain error: log requires x > 0")
        return math.log10(value)

    def ln(self, value: float) -> float:
        """Compute the natural logarithm (base e).

        Args:
            value: Must be positive.

        Returns:
            ln(value).

        Raises:
            CalculatorError: If value <= 0.
        """
        if value <= 0:
            raise CalculatorError("Domain error: ln requires x > 0")
        return math.log(value)

    def log2(self, value: float) -> float:
        """Compute the base-2 logarithm.

        Args:
            value: Must be positive.

        Returns:
            log2(value).

        Raises:
            CalculatorError: If value <= 0.
        """
        if value <= 0:
            raise CalculatorError("Domain error: log2 requires x > 0")
        return math.log2(value)

    # --- Power and root functions ---

    def square(self, value: float) -> float:
        """Compute x squared.

        Args:
            value: The value to square.

        Returns:
            value ** 2.
        """
        return value ** 2

    def cube(self, value: float) -> float:
        """Compute x cubed.

        Args:
            value: The value to cube.

        Returns:
            value ** 3.
        """
        return value ** 3

    def power(self, base: float, exponent: float) -> float:
        """Raise base to the power of exponent.

        Args:
            base: The base value.
            exponent: The exponent.

        Returns:
            base ** exponent.

        Raises:
            CalculatorError: On domain errors.
        """
        try:
            result = base ** exponent
            if isinstance(result, complex):
                raise CalculatorError("Domain error: complex result")
            return float(result)
        except (OverflowError, ValueError) as e:
            raise CalculatorError(f"Math error: {e}") from e

    def ten_to_x(self, value: float) -> float:
        """Compute 10 raised to the given power.

        Args:
            value: The exponent.

        Returns:
            10 ** value.
        """
        try:
            return 10.0 ** value
        except OverflowError as e:
            raise CalculatorError(f"Overflow: {e}") from e

    def e_to_x(self, value: float) -> float:
        """Compute e raised to the given power.

        Args:
            value: The exponent.

        Returns:
            e ** value.
        """
        try:
            return math.exp(value)
        except OverflowError as e:
            raise CalculatorError(f"Overflow: {e}") from e

    def sqrt(self, value: float) -> float:
        """Compute the square root.

        Args:
            value: Must be non-negative.

        Returns:
            The square root of value.

        Raises:
            CalculatorError: If value is negative.
        """
        if value < 0:
            raise CalculatorError("Domain error: sqrt requires x >= 0")
        return math.sqrt(value)

    def cbrt(self, value: float) -> float:
        """Compute the cube root.

        Handles negative values correctly.

        Args:
            value: Any real number.

        Returns:
            The cube root of value.
        """
        if value < 0:
            return -(abs(value) ** (1.0 / 3.0))
        return value ** (1.0 / 3.0)

    def reciprocal(self, value: float) -> float:
        """Compute the reciprocal (1/x).

        Args:
            value: Must be non-zero.

        Returns:
            1 / value.

        Raises:
            CalculatorError: If value is zero.
        """
        if value == 0:
            raise CalculatorError("Division by zero: 1/0")
        return 1.0 / value

    # --- Constants ---

    def get_pi(self) -> float:
        """Return the value of pi.

        Returns:
            math.pi (3.14159265358979...)
        """
        return math.pi

    def get_e(self) -> float:
        """Return the value of Euler's number e.

        Returns:
            math.e (2.71828182845905...)
        """
        return math.e

    # --- Factorial and absolute value ---

    def factorial(self, value: float) -> float:
        """Compute the factorial of a non-negative integer.

        Args:
            value: Must be a non-negative integer.

        Returns:
            n! as a float.

        Raises:
            CalculatorError: If value is negative or non-integer.
        """
        if value < 0:
            raise CalculatorError("Error: factorial of negative number")
        if value != int(value):
            raise CalculatorError("Error: factorial of non-integer")
        n = int(value)
        try:
            result = math.factorial(n)
            return float(result)
        except (OverflowError, ValueError) as e:
            raise CalculatorError(f"Overflow: {e}") from e

    def absolute_value(self, value: float) -> float:
        """Compute the absolute value.

        Args:
            value: Any real number.

        Returns:
            |value|.
        """
        return abs(value)

    # --- Parentheses ---

    def open_paren(self) -> None:
        """Insert an open parenthesis into the expression.

        Increments the parenthesis depth counter.
        """
        if self.error_state:
            return

        if self.current_input:
            # Implicit multiplication: e.g., 5( => 5 * (
            value = float(self.current_input)
            self.expression.append(value)
            self.expression.append("*")
            self.current_input = ""
        elif (
            self.expression
            and isinstance(self.expression[-1], (int, float))
        ):
            self.expression.append("*")

        self.expression.append("(")
        self.paren_depth += 1

    def close_paren(self) -> None:
        """Insert a close parenthesis into the expression.

        Finalizes any current input first. Decrements the depth counter.

        Raises:
            CalculatorError: If no matching open parenthesis.
        """
        if self.error_state:
            return

        if self.paren_depth <= 0:
            raise CalculatorError("Mismatched parentheses")

        if self.current_input:
            value = float(self.current_input)
            self.expression.append(value)
            self.current_input = ""

        self.expression.append(")")
        self.paren_depth -= 1

    def get_paren_depth(self) -> int:
        """Return the current parenthesis nesting depth.

        Returns:
            Number of unmatched open parentheses.
        """
        return self.paren_depth

    def all_clear(self) -> None:
        """Reset all state including parenthesis depth."""
        super().all_clear()
        self.paren_depth = 0

    def evaluate(self) -> float:
        """Evaluate the expression, checking for mismatched parentheses.

        Returns:
            The computed result.

        Raises:
            CalculatorError: On mismatched parentheses or other errors.
        """
        if self.paren_depth != 0:
            self.paren_depth = 0
            raise CalculatorError("Mismatched parentheses")
        return super().evaluate()
