"""Tests for scientific calculator mode."""

import math
import pytest
from calculator.logic.scientific_logic import ScientificCalculator


@pytest.fixture
def calc():
    """Create a fresh ScientificCalculator instance."""
    return ScientificCalculator()


# --- Trigonometry (Degrees) ---

class TestTrigDegrees:
    """Test trigonometric functions in degree mode."""

    def test_sin_0(self, calc):
        calc.input_digit("0")
        calc.sin()
        assert calc.get_current_value() == 0

    def test_sin_90(self, calc):
        calc.input_digit("9")
        calc.input_digit("0")
        calc.sin()
        assert calc.get_current_value() == 1.0

    def test_cos_0(self, calc):
        calc.input_digit("0")
        calc.cos()
        assert calc.get_current_value() == 1.0

    def test_cos_90(self, calc):
        calc.input_digit("9")
        calc.input_digit("0")
        calc.cos()
        assert calc.get_current_value() == 0.0

    def test_tan_45(self, calc):
        calc.input_digit("4")
        calc.input_digit("5")
        calc.tan()
        assert abs(calc.get_current_value() - 1.0) < 1e-10

    def test_asin_1(self, calc):
        calc.input_digit("1")
        calc.asin()
        assert abs(calc.get_current_value() - 90.0) < 1e-10

    def test_acos_1(self, calc):
        calc.input_digit("1")
        calc.acos()
        assert abs(calc.get_current_value() - 0.0) < 1e-10

    def test_atan_1(self, calc):
        calc.input_digit("1")
        calc.atan()
        assert abs(calc.get_current_value() - 45.0) < 1e-10


# --- Trigonometry (Radians) ---

class TestTrigRadians:
    """Test trigonometric functions in radian mode."""

    def test_sin_pi_radians(self, calc):
        calc.toggle_angle_mode()
        assert calc.angle_mode == "RAD"
        calc.insert_pi()
        calc.sin()
        assert abs(calc.get_current_value()) < 1e-10

    def test_cos_pi_radians(self, calc):
        calc.toggle_angle_mode()
        calc.insert_pi()
        calc.cos()
        assert abs(calc.get_current_value() - (-1.0)) < 1e-10

    def test_sin_0_radians(self, calc):
        calc.toggle_angle_mode()
        calc.input_digit("0")
        calc.sin()
        assert calc.get_current_value() == 0.0


# --- Logarithms ---

class TestLogarithms:
    """Test logarithmic functions."""

    def test_log_100(self, calc):
        calc.input_digit("1")
        calc.input_digit("0")
        calc.input_digit("0")
        calc.log()
        assert calc.get_current_value() == 2.0

    def test_ln_e(self, calc):
        calc.insert_e()
        calc.ln()
        assert abs(calc.get_current_value() - 1.0) < 1e-10

    def test_log2_256(self, calc):
        calc.input_digit("2")
        calc.input_digit("5")
        calc.input_digit("6")
        calc.log2()
        assert calc.get_current_value() == 8.0


# --- Powers and Roots ---

class TestPowersAndRoots:
    """Test power and root functions."""

    def test_square(self, calc):
        calc.input_digit("5")
        calc.square()
        assert calc.get_current_value() == 25.0

    def test_cube(self, calc):
        calc.input_digit("2")
        calc.cube()
        assert calc.get_current_value() == 8.0

    def test_power(self, calc):
        # 2^10 = 1024
        calc.input_digit("2")
        calc.power()  # This calls input_operator("**")
        calc.input_digit("1")
        calc.input_digit("0")
        calc.evaluate()
        assert calc.get_current_value() == 1024.0

    def test_ten_power(self, calc):
        calc.input_digit("3")
        calc.ten_power()
        assert calc.get_current_value() == 1000.0

    def test_e_power(self, calc):
        calc.input_digit("1")
        calc.e_power()
        assert abs(calc.get_current_value() - math.e) < 1e-10

    def test_sqrt(self, calc):
        calc.input_digit("1")
        calc.input_digit("4")
        calc.input_digit("4")
        calc.sqrt()
        assert calc.get_current_value() == 12.0

    def test_cbrt(self, calc):
        calc.input_digit("2")
        calc.input_digit("7")
        calc.cbrt()
        assert abs(calc.get_current_value() - 3.0) < 1e-10

    def test_reciprocal(self, calc):
        calc.input_digit("4")
        calc.reciprocal()
        assert calc.get_current_value() == 0.25


# --- Factorial and Absolute ---

class TestFactorialAndAbsolute:
    """Test factorial and absolute value."""

    def test_factorial_5(self, calc):
        calc.input_digit("5")
        calc.factorial()
        assert calc.get_current_value() == 120.0

    def test_factorial_0(self, calc):
        calc.input_digit("0")
        calc.factorial()
        assert calc.get_current_value() == 1.0

    def test_factorial_170(self, calc):
        for d in "170":
            calc.input_digit(d)
        calc.factorial()
        assert not calc.error

    def test_absolute_negative(self, calc):
        calc.input_digit("7")
        calc.toggle_sign()
        calc.absolute()
        assert calc.get_current_value() == 7.0


# --- Constants ---

class TestConstants:
    """Test constant insertion."""

    def test_pi(self, calc):
        calc.insert_pi()
        assert abs(calc.get_current_value() - math.pi) < 1e-10

    def test_e(self, calc):
        calc.insert_e()
        assert abs(calc.get_current_value() - math.e) < 1e-10

    def test_e_then_e_power(self, calc):
        calc.insert_e()
        calc.e_power()
        expected = math.e ** math.e
        assert abs(calc.get_current_value() - expected) < 1e-6


# --- Parentheses ---

class TestParentheses:
    """Test parenthesis grouping."""

    def test_simple_parens(self, calc):
        # (2 + 3) * 4 = 20
        calc.open_paren()
        calc.input_digit("2")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.close_paren()
        calc.input_operator("*")
        calc.input_digit("4")
        calc.evaluate()
        assert calc.get_current_value() == 20.0

    def test_parens_right(self, calc):
        # 2 * (3 + 4) = 14
        calc.input_digit("2")
        calc.input_operator("*")
        calc.open_paren()
        calc.input_digit("3")
        calc.input_operator("+")
        calc.input_digit("4")
        calc.close_paren()
        calc.evaluate()
        assert calc.get_current_value() == 14.0

    def test_nested_parens(self, calc):
        # ((2 + 3) * (4 + 1)) = 25
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
        assert calc.get_current_value() == 25.0


# --- Error Cases ---

class TestErrors:
    """Test error conditions in scientific mode."""

    def test_sqrt_negative(self, calc):
        calc.input_digit("1")
        calc.toggle_sign()
        calc.sqrt()
        assert calc.error is True
        assert calc.get_display_value() == "Error"

    def test_log_zero(self, calc):
        calc.input_digit("0")
        calc.log()
        assert calc.error is True

    def test_log_negative(self, calc):
        calc.input_digit("1")
        calc.toggle_sign()
        calc.log()
        assert calc.error is True

    def test_ln_zero(self, calc):
        calc.input_digit("0")
        calc.ln()
        assert calc.error is True

    def test_tan_90_degrees(self, calc):
        calc.input_digit("9")
        calc.input_digit("0")
        calc.tan()
        assert calc.error is True

    def test_factorial_negative(self, calc):
        calc.input_digit("3")
        calc.toggle_sign()
        calc.factorial()
        assert calc.error is True

    def test_factorial_non_integer(self, calc):
        calc.input_digit("3")
        calc.input_decimal()
        calc.input_digit("5")
        calc.factorial()
        assert calc.error is True

    def test_reciprocal_zero(self, calc):
        calc.input_digit("0")
        calc.reciprocal()
        assert calc.error is True

    def test_mismatched_parens(self, calc):
        calc.open_paren()
        calc.input_digit("2")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.evaluate()
        assert calc.error is True

    def test_asin_out_of_range(self, calc):
        calc.input_digit("2")
        calc.asin()
        assert calc.error is True

    def test_acos_out_of_range(self, calc):
        calc.input_digit("2")
        calc.acos()
        assert calc.error is True
