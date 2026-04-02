"""Scientific calculator logic extending basic arithmetic with
trigonometric, logarithmic, power/root, factorial, and parentheses
support.
"""

import math
from typing import Callable, List

from calculator.logic.base_logic import AngleUnit, DisplayState
from calculator.logic.basic_logic import BasicLogic


# Threshold for rounding near-zero trig results to exactly zero.
_NEAR_ZERO_THRESHOLD = 1e-10


class ScientificLogic(BasicLogic):
    """Scientific mode calculator logic.

    Extends BasicLogic with trigonometric functions, logarithms,
    powers and roots, constants, factorial, absolute value, and
    parenthesized sub-expressions.
    """

    def __init__(self) -> None:
        super().__init__()
        self._angle_unit: AngleUnit = AngleUnit.DEG
        self._paren_depth: int = 0
        self._paren_stack: list = []

    # ── Angle mode ──────────────────────────────────────────────

    @property
    def angle_unit(self) -> AngleUnit:
        """Return the current angle unit (DEG or RAD)."""
        return self._angle_unit

    def toggle_angle_unit(self) -> DisplayState:
        """Toggle between DEG and RAD angle modes."""
        if self._angle_unit == AngleUnit.DEG:
            self._angle_unit = AngleUnit.RAD
        else:
            self._angle_unit = AngleUnit.DEG
        return self.get_display_state()

    # ── Unary helper ────────────────────────────────────────────

    def _apply_unary(
        self, fn_name: str, fn: Callable[[float], float]
    ) -> DisplayState:
        """Apply a unary function to the current value.

        Args:
            fn_name: Display name of the function (e.g. "sin").
            fn: Callable that takes a float and returns a float.
                Should raise ValueError/OverflowError/ZeroDivisionError
                on invalid input.

        Returns:
            The updated DisplayState.
        """
        if self._error:
            return self.get_display_state()
        try:
            value = self.get_current_value()
            result = fn(value)
            self._current_input = self.format_number(result)
            self._expression = f"{fn_name}({self.format_number(value)})"
            self._new_input = True
        except (ValueError, OverflowError, ZeroDivisionError):
            self._error = True
            self._current_input = "Error"
        return self.get_display_state()

    # ── Trigonometric functions ──────────────────────────────────

    def _to_radians(self, value: float) -> float:
        """Convert *value* to radians if the current unit is DEG."""
        if self._angle_unit == AngleUnit.DEG:
            return math.radians(value)
        return value

    def _from_radians(self, value: float) -> float:
        """Convert *value* from radians to degrees if unit is DEG."""
        if self._angle_unit == AngleUnit.DEG:
            return math.degrees(value)
        return value

    @staticmethod
    def _round_near_zero(value: float) -> float:
        """Round values very close to zero to exactly 0."""
        if abs(value) < _NEAR_ZERO_THRESHOLD:
            return 0.0
        return value

    def trig_sin(self) -> DisplayState:
        """Compute the sine of the current value."""
        def _sin(v: float) -> float:
            rad = self._to_radians(v)
            return self._round_near_zero(math.sin(rad))
        return self._apply_unary("sin", _sin)

    def trig_cos(self) -> DisplayState:
        """Compute the cosine of the current value."""
        def _cos(v: float) -> float:
            rad = self._to_radians(v)
            return self._round_near_zero(math.cos(rad))
        return self._apply_unary("cos", _cos)

    def trig_tan(self) -> DisplayState:
        """Compute the tangent of the current value.

        Produces Error for values where tangent is undefined
        (e.g. 90 degrees).
        """
        def _tan(v: float) -> float:
            if (
                self._angle_unit == AngleUnit.DEG
                and v % 180 == 90
            ):
                raise ValueError("tan undefined at 90 + k*180 deg")
            rad = self._to_radians(v)
            return self._round_near_zero(math.tan(rad))
        return self._apply_unary("tan", _tan)

    def trig_asin(self) -> DisplayState:
        """Compute the inverse sine (arcsin) of the current value.

        Produces Error if |value| > 1.
        """
        def _asin(v: float) -> float:
            if abs(v) > 1:
                raise ValueError("asin domain error")
            result = math.asin(v)
            return self._round_near_zero(self._from_radians(result))
        return self._apply_unary("asin", _asin)

    def trig_acos(self) -> DisplayState:
        """Compute the inverse cosine (arccos) of the current value.

        Produces Error if |value| > 1.
        """
        def _acos(v: float) -> float:
            if abs(v) > 1:
                raise ValueError("acos domain error")
            result = math.acos(v)
            return self._round_near_zero(self._from_radians(result))
        return self._apply_unary("acos", _acos)

    def trig_atan(self) -> DisplayState:
        """Compute the inverse tangent (arctan) of the current value."""
        def _atan(v: float) -> float:
            result = math.atan(v)
            return self._round_near_zero(self._from_radians(result))
        return self._apply_unary("atan", _atan)

    # ── Logarithmic functions ───────────────────────────────────

    def log_base10(self) -> DisplayState:
        """Compute the base-10 logarithm. Error if value <= 0."""
        def _log10(v: float) -> float:
            if v <= 0:
                raise ValueError("log domain error")
            return math.log10(v)
        return self._apply_unary("log", _log10)

    def log_natural(self) -> DisplayState:
        """Compute the natural logarithm. Error if value <= 0."""
        def _ln(v: float) -> float:
            if v <= 0:
                raise ValueError("ln domain error")
            return math.log(v)
        return self._apply_unary("ln", _ln)

    def log_base2(self) -> DisplayState:
        """Compute the base-2 logarithm. Error if value <= 0."""
        def _log2(v: float) -> float:
            if v <= 0:
                raise ValueError("log2 domain error")
            return math.log2(v)
        return self._apply_unary("log₂", _log2)

    # ── Power and root functions ────────────────────────────────

    def power_square(self) -> DisplayState:
        """Square the current value (x^2)."""
        return self._apply_unary("sqr", lambda v: v ** 2)

    def power_cube(self) -> DisplayState:
        """Cube the current value (x^3)."""
        return self._apply_unary("cube", lambda v: v ** 3)

    def power_n(self) -> DisplayState:
        """Set up x^n as a binary operator.

        Delegates to input_operator so the user can enter the
        exponent before pressing equals.
        """
        return self.input_operator("**")

    def power_10x(self) -> DisplayState:
        """Compute 10 raised to the current value."""
        return self._apply_unary("10^", lambda v: 10 ** v)

    def power_ex(self) -> DisplayState:
        """Compute e raised to the current value."""
        return self._apply_unary("e^", lambda v: math.exp(v))

    def root_square(self) -> DisplayState:
        """Compute the square root. Error if value < 0."""
        def _sqrt(v: float) -> float:
            if v < 0:
                raise ValueError("sqrt of negative")
            return math.sqrt(v)
        return self._apply_unary("√", _sqrt)

    def root_cube(self) -> DisplayState:
        """Compute the cube root, handling negative values."""
        def _cbrt(v: float) -> float:
            return math.copysign(abs(v) ** (1 / 3), v)
        return self._apply_unary("³√", _cbrt)

    def reciprocal(self) -> DisplayState:
        """Compute the reciprocal (1/x). Error if value == 0."""
        def _recip(v: float) -> float:
            if v == 0:
                raise ZeroDivisionError("reciprocal of zero")
            return 1 / v
        return self._apply_unary("1/", _recip)

    # ── Constants ───────────────────────────────────────────────

    def insert_pi(self) -> DisplayState:
        """Insert the value of pi into the current input."""
        self._current_input = self.format_number(math.pi)
        self._new_input = True
        return self.get_display_state()

    def insert_e(self) -> DisplayState:
        """Insert the value of Euler's number into the current input."""
        self._current_input = self.format_number(math.e)
        self._new_input = True
        return self.get_display_state()

    # ── Factorial and absolute value ────────────────────────────

    def factorial(self) -> DisplayState:
        """Compute n! for the current value.

        Produces Error if the value is negative, non-integer, or
        greater than 170 (which overflows a float).
        """
        def _factorial(v: float) -> float:
            if v < 0:
                raise ValueError("factorial of negative")
            if v != int(v):
                raise ValueError("factorial of non-integer")
            n = int(v)
            if n > 170:
                raise OverflowError("factorial too large for float")
            return float(math.factorial(n))
        return self._apply_unary("fact", _factorial)

    def absolute_value(self) -> DisplayState:
        """Compute the absolute value of the current input."""
        return self._apply_unary("|x|", lambda v: abs(v))

    # ── Parentheses ─────────────────────────────────────────────

    def open_paren(self) -> DisplayState:
        """Open a parenthesized sub-expression.

        Pushes the current tokens, pending operator, and expression
        onto the paren stack, then resets to a clean inner state.
        """
        if self._error:
            return self.get_display_state()

        self._paren_stack.append({
            "tokens": self._tokens,
            "pending_op": self._pending_op,
            "expression": self._expression,
        })
        self._tokens = []
        self._pending_op = ""
        self._expression = ""
        self._new_input = True
        self._current_input = "0"
        self._paren_depth += 1
        return self.get_display_state()

    def close_paren(self) -> DisplayState:
        """Close a parenthesized sub-expression.

        Evaluates the inner expression, pops the parent state, and
        sets the result as the current input. Produces Error if there
        is no matching open parenthesis.
        """
        if self._error:
            return self.get_display_state()

        if self._paren_depth == 0:
            self._error = True
            self._current_input = "Error"
            return self.get_display_state()

        # Finalize inner expression: push current value with any
        # pending operator, then evaluate.
        current_value = self.get_current_value()
        if self._pending_op:
            self._tokens.append(current_value)
            self._tokens.append(self._pending_op)
            self._pending_op = ""
        # Push final operand
        if not self._tokens or isinstance(
            self._tokens[-1], str
        ):
            self._tokens.append(current_value)

        try:
            inner_result = self._evaluate_tokens(self._tokens)
        except (ValueError, OverflowError, ZeroDivisionError):
            self._error = True
            self._current_input = "Error"
            return self.get_display_state()

        # Restore parent state
        parent = self._paren_stack.pop()
        self._tokens = parent["tokens"]
        self._pending_op = parent["pending_op"]
        self._expression = parent["expression"]
        self._paren_depth -= 1

        self._current_input = self.format_number(inner_result)
        self._new_input = True
        return self.get_display_state()

    # ── Evaluate override (paren check) ─────────────────────────

    def evaluate(self) -> DisplayState:
        """Evaluate the full expression.

        Produces Error if there are unclosed parentheses.
        """
        if self._paren_depth > 0:
            self._error = True
            self._current_input = "Error"
            self._paren_depth = 0
            self._paren_stack = []
            self._tokens = []
            self._pending_op = ""
            return self.get_display_state()
        return super().evaluate()

    # ── Token evaluation override (** support) ──────────────────

    def _evaluate_tokens(self, tokens: list) -> float:
        """Evaluate a token list with three-pass precedence.

        Pass 0: ** (right-to-left associativity)
        Pass 1: * and / (left-to-right, inherited)
        Pass 2: + and - (left-to-right, inherited)

        Args:
            tokens: Alternating list of [number, op, number, ...].

        Returns:
            The computed result as a float.
        """
        # Pass 0: handle ** with right-to-left associativity
        tokens = list(tokens)  # shallow copy
        tokens = self._evaluate_power_pass(tokens)
        # Delegate remaining passes to parent
        return super()._evaluate_tokens(tokens)

    @staticmethod
    def _evaluate_power_pass(tokens: list) -> list:
        """Evaluate all ** operators right-to-left.

        Args:
            tokens: Token list with numbers and operator strings.

        Returns:
            A new token list with ** operators resolved.
        """
        # Find rightmost ** and evaluate, repeat until none remain.
        # This achieves right-to-left associativity: 2**3**2 = 2**(3**2) = 512
        while "**" in tokens:
            # Find the rightmost ** operator
            idx = -1
            for i in range(len(tokens) - 1, -1, -1):
                if tokens[i] == "**":
                    idx = i
                    break
            left = tokens[idx - 1]
            right = tokens[idx + 1]
            result = left ** right
            tokens = tokens[: idx - 1] + [result] + tokens[idx + 2 :]
        return tokens

    # ── Clear override ──────────────────────────────────────────

    def clear_all(self) -> DisplayState:
        """Reset all state including parentheses, but not memory."""
        self._paren_depth = 0
        self._paren_stack = []
        return super().clear_all()

    # ── Display state ───────────────────────────────────────────

    def get_display_state(self) -> DisplayState:
        """Build and return the current DisplayState for the View.

        Extends the parent state with angle_unit and paren_depth.
        """
        return DisplayState(
            main_display=self._current_input,
            expression_display=self._expression,
            error=self._error,
            memory_indicator=self.has_memory,
            angle_unit=self._angle_unit,
            paren_depth=self._paren_depth,
        )
