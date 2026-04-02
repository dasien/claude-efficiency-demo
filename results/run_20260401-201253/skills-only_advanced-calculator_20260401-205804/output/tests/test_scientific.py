"""Comprehensive tests for the ScientificLogic calculator class."""

import math

import pytest

from calculator.logic.scientific_logic import ScientificLogic


@pytest.fixture
def calc():
    """Return a fresh ScientificLogic instance in DEG mode."""
    return ScientificLogic()


# ---------------------------------------------------------------------------
# Trig in DEG mode (parametrized)
# ---------------------------------------------------------------------------

class TestTrigDeg:
    """Trigonometric functions in DEG mode."""

    @pytest.mark.parametrize("angle, expected", [
        (0, 0),
        (90, 1),
        (180, 0),
        (270, -1),
    ])
    def test_sin_deg(self, calc, angle, expected):
        calc.display_value = str(angle)
        calc.input_mode = "typing"
        calc.apply_function("sin")
        assert calc.get_current_value() == pytest.approx(expected)

    @pytest.mark.parametrize("angle, expected", [
        (0, 1),
        (90, 0),
        (180, -1),
    ])
    def test_cos_deg(self, calc, angle, expected):
        calc.display_value = str(angle)
        calc.input_mode = "typing"
        calc.apply_function("cos")
        assert calc.get_current_value() == pytest.approx(expected)

    @pytest.mark.parametrize("angle, expected", [
        (0, 0),
        (45, 1),
    ])
    def test_tan_deg(self, calc, angle, expected):
        calc.display_value = str(angle)
        calc.input_mode = "typing"
        calc.apply_function("tan")
        assert calc.get_current_value() == pytest.approx(expected)

    @pytest.mark.parametrize("value, func, expected", [
        (1, "asin", 90),
        (1, "acos", 0),
        (1, "atan", 45),
    ])
    def test_inverse_trig_deg(self, calc, value, func, expected):
        calc.display_value = str(value)
        calc.input_mode = "typing"
        calc.apply_function(func)
        assert calc.get_current_value() == pytest.approx(expected)


# ---------------------------------------------------------------------------
# Trig in RAD mode
# ---------------------------------------------------------------------------

class TestTrigRad:
    """Trigonometric functions in RAD mode."""

    def test_sin_rad_zero(self, calc):
        calc.toggle_angle_mode()
        assert calc.angle_mode == "RAD"
        calc.display_value = "0"
        calc.input_mode = "typing"
        calc.apply_function("sin")
        assert calc.get_current_value() == pytest.approx(0)

    def test_cos_rad_zero(self, calc):
        calc.toggle_angle_mode()
        calc.display_value = "0"
        calc.input_mode = "typing"
        calc.apply_function("cos")
        assert calc.get_current_value() == pytest.approx(1)


# ---------------------------------------------------------------------------
# Log functions (parametrized)
# ---------------------------------------------------------------------------

class TestLogFunctions:
    """Logarithmic functions."""

    @pytest.mark.parametrize("value, expected", [
        (100, 2),
        (1000, 3),
    ])
    def test_log10(self, calc, value, expected):
        calc.display_value = str(value)
        calc.input_mode = "typing"
        calc.apply_function("log")
        assert calc.get_current_value() == pytest.approx(expected)

    def test_ln_of_1(self, calc):
        calc.display_value = "1"
        calc.input_mode = "typing"
        calc.apply_function("ln")
        assert calc.get_current_value() == pytest.approx(0)

    def test_ln_of_e(self, calc):
        calc.display_value = str(math.e)
        calc.input_mode = "typing"
        calc.apply_function("ln")
        assert calc.get_current_value() == pytest.approx(1)

    def test_log2_of_256(self, calc):
        calc.display_value = "256"
        calc.input_mode = "typing"
        calc.apply_function("log2")
        assert calc.get_current_value() == pytest.approx(8)


# ---------------------------------------------------------------------------
# Power / Root
# ---------------------------------------------------------------------------

class TestPowerRoot:
    """Power and root functions."""

    def test_x2(self, calc):
        calc.display_value = "5"
        calc.input_mode = "typing"
        calc.apply_function("x2")
        assert calc.get_current_value() == pytest.approx(25)

    def test_x3(self, calc):
        calc.display_value = "3"
        calc.input_mode = "typing"
        calc.apply_function("x3")
        assert calc.get_current_value() == pytest.approx(27)

    def test_xn_power(self, calc):
        """2^10 = 1024 using input_power as binary operator."""
        calc.input_digit("2")
        calc.input_power()
        calc.input_digit("1")
        calc.input_digit("0")
        calc.evaluate()
        assert calc.get_current_value() == pytest.approx(1024)

    def test_xn_power_via_tokens(self, calc):
        """2^10 = 1024 — workaround exercising _evaluate_tokens directly."""
        calc._tokens = [2.0, "**"]
        calc.display_value = "10"
        calc.input_mode = "typing"
        # Manually append current and evaluate via the token engine
        tokens = list(calc._tokens) + [calc.get_current_value()]
        result = calc._evaluate_tokens(tokens)
        assert result == pytest.approx(1024)

    def test_10x(self, calc):
        calc.display_value = "3"
        calc.input_mode = "typing"
        calc.apply_function("10x")
        assert calc.get_current_value() == pytest.approx(1000)

    def test_ex(self, calc):
        calc.display_value = "1"
        calc.input_mode = "typing"
        calc.apply_function("ex")
        assert calc.get_current_value() == pytest.approx(2.71828, rel=1e-4)

    def test_sqrt_144(self, calc):
        calc.display_value = "144"
        calc.input_mode = "typing"
        calc.apply_function("sqrt")
        assert calc.get_current_value() == pytest.approx(12)

    def test_sqrt_0(self, calc):
        calc.display_value = "0"
        calc.input_mode = "typing"
        calc.apply_function("sqrt")
        assert calc.get_current_value() == pytest.approx(0)

    def test_cbrt_27(self, calc):
        calc.display_value = "27"
        calc.input_mode = "typing"
        calc.apply_function("cbrt")
        assert calc.get_current_value() == pytest.approx(3)

    def test_cbrt_neg8(self, calc):
        calc.display_value = "-8"
        calc.input_mode = "typing"
        calc.apply_function("cbrt")
        assert calc.get_current_value() == pytest.approx(-2)

    def test_recip(self, calc):
        calc.display_value = "4"
        calc.input_mode = "typing"
        calc.apply_function("recip")
        assert calc.get_current_value() == pytest.approx(0.25)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

class TestConstants:
    """Mathematical constants."""

    def test_pi(self, calc):
        calc.insert_constant("pi")
        assert calc.get_current_value() == pytest.approx(3.14159265, rel=1e-7)

    def test_e(self, calc):
        calc.insert_constant("e")
        assert calc.get_current_value() == pytest.approx(2.71828182, rel=1e-7)


# ---------------------------------------------------------------------------
# Factorial
# ---------------------------------------------------------------------------

class TestFactorial:
    """Factorial function."""

    @pytest.mark.parametrize("value, expected", [
        (0, 1),
        (1, 1),
        (5, 120),
        (10, 3628800),
    ])
    def test_factorial(self, calc, value, expected):
        calc.display_value = str(value)
        calc.input_mode = "typing"
        calc.apply_function("fact")
        assert calc.get_current_value() == pytest.approx(expected)


# ---------------------------------------------------------------------------
# Absolute value
# ---------------------------------------------------------------------------

class TestAbsoluteValue:
    """Absolute value function."""

    def test_abs_negative(self, calc):
        calc.display_value = "-7"
        calc.input_mode = "typing"
        calc.apply_function("abs")
        assert calc.get_current_value() == pytest.approx(7)

    def test_abs_zero(self, calc):
        calc.display_value = "0"
        calc.input_mode = "typing"
        calc.apply_function("abs")
        assert calc.get_current_value() == pytest.approx(0)


# ---------------------------------------------------------------------------
# Parentheses
# ---------------------------------------------------------------------------

class TestParentheses:
    """Parenthesized expressions."""

    def test_paren_2_plus_3_times_4(self, calc):
        """(2+3)*4 = 20"""
        calc.open_paren()
        calc.input_digit("2")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.close_paren()
        calc.input_operator("*")
        calc.input_digit("4")
        calc.evaluate()
        assert calc.get_current_value() == pytest.approx(20)

    def test_paren_2_times_3_plus_4(self, calc):
        """2*(3+4) = 14"""
        calc.input_digit("2")
        calc.input_operator("*")
        calc.open_paren()
        calc.input_digit("3")
        calc.input_operator("+")
        calc.input_digit("4")
        calc.close_paren()
        calc.evaluate()
        assert calc.get_current_value() == pytest.approx(14)

    def test_nested_parens(self, calc):
        """((2+3)*(4+1)) = 25"""
        calc.open_paren()
        calc.open_paren()
        calc.input_digit("2")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.close_paren()
        calc.input_operator("*")
        calc.open_paren()
        calc.input_digit("4")
        calc.input_operator("+")
        calc.input_digit("1")
        calc.close_paren()
        calc.close_paren()
        calc.evaluate()
        assert calc.get_current_value() == pytest.approx(25)


# ---------------------------------------------------------------------------
# Error cases
# ---------------------------------------------------------------------------

class TestErrors:
    """Error conditions that should produce Error state."""

    def test_tan_90_deg_error(self, calc):
        calc.display_value = "90"
        calc.input_mode = "typing"
        calc.apply_function("tan")
        assert calc.error is True

    def test_sqrt_negative_error(self, calc):
        calc.display_value = "-1"
        calc.input_mode = "typing"
        calc.apply_function("sqrt")
        assert calc.error is True

    def test_log_zero_error(self, calc):
        calc.display_value = "0"
        calc.input_mode = "typing"
        calc.apply_function("log")
        assert calc.error is True

    def test_log_negative_error(self, calc):
        calc.display_value = "-1"
        calc.input_mode = "typing"
        calc.apply_function("log")
        assert calc.error is True

    def test_factorial_negative_error(self, calc):
        calc.display_value = "-3"
        calc.input_mode = "typing"
        calc.apply_function("fact")
        assert calc.error is True

    def test_factorial_non_integer_error(self, calc):
        calc.display_value = "3.5"
        calc.input_mode = "typing"
        calc.apply_function("fact")
        assert calc.error is True

    def test_recip_zero_error(self, calc):
        calc.display_value = "0"
        calc.input_mode = "typing"
        calc.apply_function("recip")
        assert calc.error is True

    def test_mismatched_parens_error(self, calc):
        """Evaluating with unclosed parentheses should error."""
        calc.open_paren()
        calc.input_digit("2")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.evaluate()
        assert calc.error is True
