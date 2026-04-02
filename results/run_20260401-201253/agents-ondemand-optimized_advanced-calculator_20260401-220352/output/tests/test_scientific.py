"""Tests for Scientific calculator mode: trig, log, powers, roots, factorial, parens, constants."""

import math
import pytest
from calculator.logic.scientific_logic import ScientificCalculator
from calculator.logic.base_logic import CalculatorError


def enter_number(calc, number_str):
    """Enter a multi-digit number into the calculator."""
    for ch in str(number_str):
        if ch == ".":
            calc.append_decimal()
        elif ch == "-":
            pass
        else:
            calc.append_digit(ch)


@pytest.fixture
def calc():
    return ScientificCalculator()


# =============================================================================
# Trigonometric Functions -- Happy Path
# =============================================================================

class TestTrigFunctions:

    @pytest.mark.parametrize("func_name, value, angle_mode, expected", [
        ("sin", 90, "DEG", 1.0),
        ("sin", 0, "DEG", 0.0),
        ("sin", 30, "DEG", 0.5),
        ("cos", 0, "DEG", 1.0),
        ("cos", 60, "DEG", 0.5),
        ("tan", 45, "DEG", 1.0),
        ("tan", 0, "DEG", 0.0),
    ])
    def test_trig_deg(self, calc, func_name, value, angle_mode, expected):
        calc.angle_mode = angle_mode
        func = getattr(calc, func_name)
        result = func(float(value))
        assert result == pytest.approx(expected, abs=1e-10)

    def test_sin_rad_pi(self, calc):
        calc.angle_mode = "RAD"
        result = calc.sin(math.pi)
        assert result == pytest.approx(0.0, abs=1e-10)

    def test_cos_90_deg_near_zero(self, calc):
        calc.angle_mode = "DEG"
        result = calc.cos(90)
        assert result == pytest.approx(0.0, abs=1e-10)

    @pytest.mark.parametrize("func_name, value, angle_mode, expected", [
        ("asin", 1, "DEG", 90.0),
        ("asin", 0, "DEG", 0.0),
        ("acos", 1, "DEG", 0.0),
        ("acos", 0, "DEG", 90.0),
        ("atan", 1, "DEG", 45.0),
        ("atan", 0, "DEG", 0.0),
    ])
    def test_inverse_trig_deg(self, calc, func_name, value, angle_mode, expected):
        calc.angle_mode = angle_mode
        func = getattr(calc, func_name)
        result = func(float(value))
        assert result == pytest.approx(expected, abs=1e-10)

    def test_asin_rad(self, calc):
        calc.angle_mode = "RAD"
        result = calc.asin(1)
        assert result == pytest.approx(math.pi / 2, abs=1e-10)


# =============================================================================
# Trigonometric Functions -- Errors
# =============================================================================

class TestTrigErrors:

    def test_tan_90_deg_error(self, calc):
        calc.angle_mode = "DEG"
        with pytest.raises(CalculatorError):
            calc.tan(90)

    def test_asin_out_of_range_high(self, calc):
        with pytest.raises(CalculatorError):
            calc.asin(2)

    def test_asin_out_of_range_low(self, calc):
        with pytest.raises(CalculatorError):
            calc.asin(-2)

    def test_acos_out_of_range(self, calc):
        with pytest.raises(CalculatorError):
            calc.acos(1.5)


# =============================================================================
# Angle Mode Toggle
# =============================================================================

class TestAngleMode:

    def test_default_deg(self, calc):
        assert calc.angle_mode == "DEG"

    def test_toggle_to_rad(self, calc):
        result = calc.toggle_angle_mode()
        assert result == "RAD"

    def test_toggle_back_to_deg(self, calc):
        calc.toggle_angle_mode()
        result = calc.toggle_angle_mode()
        assert result == "DEG"


# =============================================================================
# Logarithmic Functions -- Happy Path
# =============================================================================

class TestLogFunctions:

    @pytest.mark.parametrize("func_name, value, expected", [
        ("log10", 100, 2.0),
        ("log10", 1, 0.0),
        ("log10", 10, 1.0),
        ("ln", 1, 0.0),
        ("log2", 256, 8.0),
        ("log2", 1, 0.0),
        ("log2", 2, 1.0),
    ])
    def test_log_happy_path(self, calc, func_name, value, expected):
        func = getattr(calc, func_name)
        result = func(float(value))
        assert result == pytest.approx(expected, abs=1e-10)

    def test_ln_e(self, calc):
        result = calc.ln(math.e)
        assert result == pytest.approx(1.0, abs=1e-10)


# =============================================================================
# Logarithmic Functions -- Errors
# =============================================================================

class TestLogErrors:

    @pytest.mark.parametrize("func_name, value", [
        ("log10", 0),
        ("log10", -1),
        ("ln", 0),
        ("ln", -5),
        ("log2", 0),
        ("log2", -1),
    ])
    def test_log_domain_error(self, calc, func_name, value):
        func = getattr(calc, func_name)
        with pytest.raises(CalculatorError):
            func(float(value))


# =============================================================================
# Power and Root Functions -- Happy Path
# =============================================================================

class TestPowerAndRoot:

    @pytest.mark.parametrize("func_name, args, expected", [
        ("square", (5,), 25),
        ("square", (-3,), 9),
        ("square", (0,), 0),
        ("cube", (3,), 27),
        ("cube", (-2,), -8),
        ("power", (2, 10), 1024),
        ("power", (5, 0), 1),
        ("ten_to_x", (3,), 1000),
        ("ten_to_x", (0,), 1),
        ("e_to_x", (0,), 1.0),
        ("sqrt", (144,), 12),
        ("sqrt", (0,), 0),
        ("sqrt", (2,), math.sqrt(2)),
        ("reciprocal", (4,), 0.25),
        ("reciprocal", (-2,), -0.5),
    ])
    def test_power_root_happy(self, calc, func_name, args, expected):
        func = getattr(calc, func_name)
        result = func(*[float(a) for a in args])
        assert result == pytest.approx(expected, abs=1e-10)

    def test_e_to_1(self, calc):
        result = calc.e_to_x(1.0)
        assert result == pytest.approx(math.e, abs=1e-10)

    def test_cbrt_27(self, calc):
        result = calc.cbrt(27.0)
        assert result == pytest.approx(3.0, abs=1e-10)

    def test_cbrt_negative_8(self, calc):
        result = calc.cbrt(-8.0)
        assert result == pytest.approx(-2.0, abs=1e-10)


# =============================================================================
# Power and Root Functions -- Errors
# =============================================================================

class TestPowerRootErrors:

    def test_sqrt_negative(self, calc):
        with pytest.raises(CalculatorError):
            calc.sqrt(-1.0)

    def test_reciprocal_zero(self, calc):
        with pytest.raises(CalculatorError):
            calc.reciprocal(0.0)


# =============================================================================
# Constants
# =============================================================================

class TestConstants:

    def test_pi(self, calc):
        assert calc.get_pi() == pytest.approx(math.pi)

    def test_e(self, calc):
        assert calc.get_e() == pytest.approx(math.e)


# =============================================================================
# Factorial and Absolute Value
# =============================================================================

class TestFactorialAndAbsolute:

    @pytest.mark.parametrize("value, expected", [
        (0, 1),
        (1, 1),
        (5, 120),
        (10, 3628800),
    ])
    def test_factorial_happy(self, calc, value, expected):
        result = calc.factorial(float(value))
        assert result == pytest.approx(expected)

    def test_factorial_170(self, calc):
        """Factorial of 170 should not crash (NF-4)."""
        result = calc.factorial(170.0)
        assert result > 0

    @pytest.mark.parametrize("value", [-3, 3.5, -1.5])
    def test_factorial_error(self, calc, value):
        with pytest.raises(CalculatorError):
            calc.factorial(float(value))

    @pytest.mark.parametrize("value, expected", [
        (-7, 7),
        (7, 7),
        (0, 0),
        (-3.14, 3.14),
    ])
    def test_absolute_value(self, calc, value, expected):
        result = calc.absolute_value(float(value))
        assert result == pytest.approx(expected)


# =============================================================================
# Parentheses
# =============================================================================

class TestParentheses:

    def test_grouped_addition_times(self, calc):
        """(2 + 3) * 4 = 20"""
        calc.open_paren()
        enter_number(calc, 2)
        calc.add_operator("+")
        enter_number(calc, 3)
        calc.close_paren()
        calc.add_operator("*")
        enter_number(calc, 4)
        result = calc.evaluate()
        assert result == pytest.approx(20)

    def test_times_grouped_addition(self, calc):
        """2 * (3 + 4) = 14"""
        enter_number(calc, 2)
        calc.add_operator("*")
        calc.open_paren()
        enter_number(calc, 3)
        calc.add_operator("+")
        enter_number(calc, 4)
        calc.close_paren()
        result = calc.evaluate()
        assert result == pytest.approx(14)

    def test_nested_parens(self, calc):
        """((2 + 3) * (4 + 1)) = 25"""
        calc.open_paren()
        calc.open_paren()
        enter_number(calc, 2)
        calc.add_operator("+")
        enter_number(calc, 3)
        calc.close_paren()
        calc.add_operator("*")
        calc.open_paren()
        enter_number(calc, 4)
        calc.add_operator("+")
        enter_number(calc, 1)
        calc.close_paren()
        calc.close_paren()
        result = calc.evaluate()
        assert result == pytest.approx(25)

    def test_nested_parens_2(self, calc):
        """((1 + 2) * (3 + 4)) = 21"""
        calc.open_paren()
        calc.open_paren()
        enter_number(calc, 1)
        calc.add_operator("+")
        enter_number(calc, 2)
        calc.close_paren()
        calc.add_operator("*")
        calc.open_paren()
        enter_number(calc, 3)
        calc.add_operator("+")
        enter_number(calc, 4)
        calc.close_paren()
        calc.close_paren()
        result = calc.evaluate()
        assert result == pytest.approx(21)


class TestParenthesesErrors:

    def test_unmatched_open_paren(self, calc):
        """(2 + 3 = should raise error."""
        calc.open_paren()
        enter_number(calc, 2)
        calc.add_operator("+")
        enter_number(calc, 3)
        with pytest.raises(CalculatorError):
            calc.evaluate()

    def test_unmatched_close_paren(self, calc):
        """2 + 3) should raise error."""
        enter_number(calc, 2)
        calc.add_operator("+")
        enter_number(calc, 3)
        with pytest.raises(CalculatorError):
            calc.close_paren()
