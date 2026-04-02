"""Scientific calculator with trig, logarithmic, and advanced functions."""

import math

from calculator.logic.basic_logic import BasicCalculator


class ScientificCalculator(BasicCalculator):
    """Calculator supporting scientific operations.

    Extends BasicCalculator with trigonometric, logarithmic, power,
    root, factorial, and parenthesized expression support.
    """

    def __init__(self) -> None:
        """Initialize the scientific calculator."""
        super().__init__()
        self.angle_mode: str = "DEG"
        self.paren_depth: int = 0

    def toggle_angle_mode(self) -> str:
        """Toggle between degrees and radians angle mode.

        Returns:
            The new angle mode ('DEG' or 'RAD').
        """
        self.angle_mode = "RAD" if self.angle_mode == "DEG" else "DEG"
        return self.angle_mode

    def _to_radians(self, value: float) -> float:
        """Convert a value to radians based on the current angle mode.

        Args:
            value: The angle value.

        Returns:
            The value in radians.
        """
        if self.angle_mode == "DEG":
            return math.radians(value)
        return value

    def _from_radians(self, value: float) -> float:
        """Convert a radian value based on the current angle mode.

        Args:
            value: The angle in radians.

        Returns:
            The value in the current angle mode units.
        """
        if self.angle_mode == "DEG":
            return math.degrees(value)
        return value

    def _finalize_input(self) -> float:
        """Finalize current input and return the current value.

        Returns:
            The current value after finalizing input.
        """
        if not self._new_input:
            self.current_value = float(self.input_buffer)
        return self.current_value

    def _set_result(self, result: float) -> float:
        """Set the result as current value and prepare for new input.

        Args:
            result: The computed result.

        Returns:
            The result value.
        """
        self.current_value = result
        self.input_buffer = ""
        self._new_input = True
        return result

    # Trigonometric functions

    def sin(self) -> float:
        """Compute the sine of the current value.

        Returns:
            The sine result.
        """
        self._finalize_input()
        rad = self._to_radians(self.current_value)
        result = math.sin(rad)
        if abs(result) < 1e-10:
            result = 0.0
        return self._set_result(result)

    def cos(self) -> float:
        """Compute the cosine of the current value.

        Returns:
            The cosine result.
        """
        self._finalize_input()
        rad = self._to_radians(self.current_value)
        result = math.cos(rad)
        if abs(result) < 1e-10:
            result = 0.0
        return self._set_result(result)

    def tan(self) -> float:
        """Compute the tangent of the current value.

        Sets error if cosine is near zero (undefined tangent).

        Returns:
            The tangent result, or 0.0 on error.
        """
        self._finalize_input()
        rad = self._to_radians(self.current_value)
        if abs(math.cos(rad)) < 1e-10:
            self.set_error("Error")
            return 0.0
        result = math.tan(rad)
        return self._set_result(result)

    def asin(self) -> float:
        """Compute the arcsine of the current value.

        Sets error if value is outside [-1, 1].

        Returns:
            The arcsine result in the current angle mode.
        """
        self._finalize_input()
        val = self.current_value
        if abs(val) > 1:
            self.set_error("Error")
            return 0.0
        result = self._from_radians(math.asin(val))
        return self._set_result(result)

    def acos(self) -> float:
        """Compute the arccosine of the current value.

        Sets error if value is outside [-1, 1].

        Returns:
            The arccosine result in the current angle mode.
        """
        self._finalize_input()
        val = self.current_value
        if abs(val) > 1:
            self.set_error("Error")
            return 0.0
        result = self._from_radians(math.acos(val))
        return self._set_result(result)

    def atan(self) -> float:
        """Compute the arctangent of the current value.

        Returns:
            The arctangent result in the current angle mode.
        """
        self._finalize_input()
        val = self.current_value
        result = self._from_radians(math.atan(val))
        return self._set_result(result)

    # Logarithmic functions

    def log(self) -> float:
        """Compute the base-10 logarithm of the current value.

        Sets error if value is not positive.

        Returns:
            The log10 result.
        """
        self._finalize_input()
        val = self.current_value
        if val <= 0:
            self.set_error("Error")
            return 0.0
        result = math.log10(val)
        return self._set_result(result)

    def ln(self) -> float:
        """Compute the natural logarithm of the current value.

        Sets error if value is not positive.

        Returns:
            The natural log result.
        """
        self._finalize_input()
        val = self.current_value
        if val <= 0:
            self.set_error("Error")
            return 0.0
        result = math.log(val)
        return self._set_result(result)

    def log2(self) -> float:
        """Compute the base-2 logarithm of the current value.

        Sets error if value is not positive.

        Returns:
            The log2 result.
        """
        self._finalize_input()
        val = self.current_value
        if val <= 0:
            self.set_error("Error")
            return 0.0
        result = math.log2(val)
        return self._set_result(result)

    # Power and root functions

    def square(self) -> float:
        """Compute the square of the current value.

        Returns:
            The squared result.
        """
        self._finalize_input()
        result = self.current_value ** 2
        return self._set_result(result)

    def cube(self) -> float:
        """Compute the cube of the current value.

        Returns:
            The cubed result.
        """
        self._finalize_input()
        result = self.current_value ** 3
        return self._set_result(result)

    def power(self) -> None:
        """Start a power operation (two-operand via operator)."""
        self.add_operator("**")

    def ten_power(self) -> float:
        """Compute 10 raised to the current value.

        Returns:
            The result of 10^current_value.
        """
        self._finalize_input()
        result = 10 ** self.current_value
        return self._set_result(result)

    def e_power(self) -> float:
        """Compute e raised to the current value.

        Returns:
            The result of e^current_value.
        """
        self._finalize_input()
        result = math.exp(self.current_value)
        return self._set_result(result)

    def square_root(self) -> float:
        """Compute the square root of the current value.

        Sets error if value is negative.

        Returns:
            The square root result.
        """
        self._finalize_input()
        val = self.current_value
        if val < 0:
            self.set_error("Error")
            return 0.0
        result = math.sqrt(val)
        return self._set_result(result)

    def cube_root(self) -> float:
        """Compute the cube root of the current value.

        Handles negative values correctly.

        Returns:
            The cube root result.
        """
        self._finalize_input()
        val = self.current_value
        sign = 1 if val >= 0 else -1
        result = sign * abs(val) ** (1 / 3)
        return self._set_result(result)

    def reciprocal(self) -> float:
        """Compute the reciprocal (1/x) of the current value.

        Sets error if value is zero.

        Returns:
            The reciprocal result.
        """
        self._finalize_input()
        val = self.current_value
        if val == 0:
            self.set_error("Error")
            return 0.0
        result = 1 / val
        return self._set_result(result)

    # Other functions

    def factorial(self) -> float:
        """Compute the factorial of the current value.

        Sets error if value is negative or not an integer.
        Handles values up to 170.

        Returns:
            The factorial result.
        """
        self._finalize_input()
        val = self.current_value
        if val < 0 or val != int(val):
            self.set_error("Error")
            return 0.0
        result = float(math.factorial(int(val)))
        return self._set_result(result)

    def absolute(self) -> float:
        """Compute the absolute value of the current value.

        Returns:
            The absolute value result.
        """
        self._finalize_input()
        result = abs(self.current_value)
        return self._set_result(result)

    # Parentheses

    def open_paren(self) -> None:
        """Insert an opening parenthesis into the token list."""
        self.pending_tokens.append("(")
        self.paren_depth += 1
        self._new_input = True
        self.expression += " ("

    def close_paren(self) -> None:
        """Insert a closing parenthesis into the token list."""
        if not self._new_input:
            self.pending_tokens.append(float(self.input_buffer))
        else:
            self.pending_tokens.append(self.current_value)
        self.pending_tokens.append(")")
        self.paren_depth -= 1
        self._new_input = True
        self.expression += " )"

    def evaluate(self) -> float:
        """Evaluate the expression, handling parentheses.

        Sets error if parentheses are mismatched.

        Returns:
            The computed result.
        """
        if self.paren_depth != 0:
            self.set_error("Error")
            self.pending_tokens = []
            self._new_input = True
            return 0.0
        return super().evaluate()

    def _evaluate_tokens(self, tokens: list) -> float:
        """Evaluate tokens with parenthesis support.

        Finds innermost parenthesized groups, evaluates them
        recursively, and replaces them with the result.

        Args:
            tokens: A list of tokens including parentheses.

        Returns:
            The computed result.

        Raises:
            ValueError: On division by zero or malformed expressions.
        """
        tokens = list(tokens)

        # Resolve parentheses from innermost outward
        while "(" in tokens:
            # Find the innermost opening paren
            last_open = -1
            for i, tok in enumerate(tokens):
                if tok == "(":
                    last_open = i
                elif tok == ")" and last_open != -1:
                    inner = tokens[last_open + 1:i]
                    result = super()._evaluate_tokens(inner)
                    tokens[last_open:i + 1] = [result]
                    break
            else:
                raise ValueError("Mismatched parentheses")

        return super()._evaluate_tokens(tokens)

    # Constants

    def insert_pi(self) -> None:
        """Insert the value of pi as the current value."""
        self.current_value = math.pi
        self.input_buffer = ""
        self._new_input = True

    def insert_e(self) -> None:
        """Insert the value of e as the current value."""
        self.current_value = math.e
        self.input_buffer = ""
        self._new_input = True

    def clear_all(self) -> None:
        """Reset all state except memory, including paren depth."""
        super().clear_all()
        self.paren_depth = 0
