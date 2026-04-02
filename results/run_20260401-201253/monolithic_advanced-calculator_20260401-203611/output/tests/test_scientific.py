"""Tests for Scientific mode calculator logic."""

import math

import pytest

from calculator.logic.scientific_logic import ScientificCalculator


def _make_calc(
    value: float = 0.0, angle_mode: str = "DEG"
) -> ScientificCalculator:
    """Create a ScientificCalculator with a preset value."""
    calc = ScientificCalculator()
    calc.set_angle_mode(angle_mode)
    if value != 0.0:
        calc.set_value(value)
    return calc


class TestTrigDegree:
    """Trigonometric functions in degree mode."""

    @pytest.mark.parametrize("angle,expected", [
        (0, 0.0),
        (90, 1.0),
        (180, 0.0),
        (270, -1.0),
    ])
    def test_sin_degrees(
        self, angle: int, expected: float
    ) -> None:
        calc = _make_calc(float(angle))
        calc.apply_sin()
        assert abs(calc.get_value() - expected) < 1e-9

    @pytest.mark.parametrize("angle,expected", [
        (0, 1.0),
        (90, 0.0),
        (180, -1.0),
    ])
    def test_cos_degrees(
        self, angle: int, expected: float
    ) -> None:
        calc = _make_calc(float(angle))
        calc.apply_cos()
        assert abs(calc.get_value() - expected) < 1e-9

    def test_tan_45_degrees(self) -> None:
        calc = _make_calc(45.0)
        calc.apply_tan()
        assert abs(calc.get_value() - 1.0) < 1e-9

    def test_asin_1_degrees(self) -> None:
        calc = _make_calc(1.0)
        calc.apply_asin()
        assert abs(calc.get_value() - 90.0) < 1e-9

    def test_acos_1_degrees(self) -> None:
        calc = _make_calc(1.0)
        calc.apply_acos()
        assert abs(calc.get_value()) < 1e-9

    def test_atan_1_degrees(self) -> None:
        calc = _make_calc(1.0)
        calc.apply_atan()
        assert abs(calc.get_value() - 45.0) < 1e-9


class TestTrigRadian:
    """Trigonometric functions in radian mode."""

    def test_sin_pi_radians(self) -> None:
        calc = _make_calc(math.pi, "RAD")
        calc.apply_sin()
        assert abs(calc.get_value()) < 1e-9

    def test_cos_pi_radians(self) -> None:
        calc = _make_calc(math.pi, "RAD")
        calc.apply_cos()
        assert abs(calc.get_value() - (-1.0)) < 1e-9

    def test_sin_pi_half_radians(self) -> None:
        calc = _make_calc(math.pi / 2, "RAD")
        calc.apply_sin()
        assert abs(calc.get_value() - 1.0) < 1e-9


class TestTrigErrors:
    """Trigonometric error cases."""

    def test_tan_90_degrees_error(self) -> None:
        calc = _make_calc(90.0)
        calc.apply_tan()
        assert calc.is_error()

    def test_asin_out_of_range(self) -> None:
        calc = _make_calc(2.0)
        calc.apply_asin()
        assert calc.is_error()

    def test_acos_out_of_range(self) -> None:
        calc = _make_calc(-2.0)
        calc.apply_acos()
        assert calc.is_error()


class TestLogarithmic:
    """Logarithmic function tests."""

    @pytest.mark.parametrize("value,expected", [
        (100.0, 2.0),
        (1.0, 0.0),
        (1000.0, 3.0),
    ])
    def test_log10(self, value: float, expected: float) -> None:
        calc = _make_calc(value)
        calc.apply_log()
        assert abs(calc.get_value() - expected) < 1e-9

    def test_ln_e(self) -> None:
        calc = _make_calc(math.e)
        calc.apply_ln()
        assert abs(calc.get_value() - 1.0) < 1e-9

    def test_log2_256(self) -> None:
        calc = _make_calc(256.0)
        calc.apply_log2()
        assert abs(calc.get_value() - 8.0) < 1e-9

    @pytest.mark.parametrize("func_name", [
        "apply_log", "apply_ln", "apply_log2",
    ])
    def test_log_zero_error(self, func_name: str) -> None:
        calc = _make_calc(0.0)
        getattr(calc, func_name)()
        assert calc.is_error()

    @pytest.mark.parametrize("func_name", [
        "apply_log", "apply_ln", "apply_log2",
    ])
    def test_log_negative_error(self, func_name: str) -> None:
        calc = _make_calc(-1.0)
        getattr(calc, func_name)()
        assert calc.is_error()


class TestPowersAndRoots:
    """Power and root function tests."""

    def test_square(self) -> None:
        calc = _make_calc(5.0)
        calc.apply_square()
        assert abs(calc.get_value() - 25.0) < 1e-9

    def test_cube(self) -> None:
        calc = _make_calc(3.0)
        calc.apply_cube()
        assert abs(calc.get_value() - 27.0) < 1e-9

    def test_power(self) -> None:
        calc = ScientificCalculator()
        # 2 ^ 10 = 1024
        calc.input_digit("2")
        calc.input_power()
        calc.input_digit("1")
        calc.input_digit("0")
        calc.input_equals()
        assert abs(calc.get_value() - 1024.0) < 1e-9

    def test_ten_power(self) -> None:
        calc = _make_calc(3.0)
        calc.apply_ten_power()
        assert abs(calc.get_value() - 1000.0) < 1e-9

    def test_e_power_zero(self) -> None:
        calc = _make_calc(0.0)
        calc.apply_e_power()
        assert abs(calc.get_value() - 1.0) < 1e-9

    def test_sqrt(self) -> None:
        calc = _make_calc(144.0)
        calc.apply_sqrt()
        assert abs(calc.get_value() - 12.0) < 1e-9

    def test_cbrt(self) -> None:
        calc = _make_calc(27.0)
        calc.apply_cbrt()
        assert abs(calc.get_value() - 3.0) < 1e-9

    def test_reciprocal(self) -> None:
        calc = _make_calc(4.0)
        calc.apply_reciprocal()
        assert abs(calc.get_value() - 0.25) < 1e-9

    def test_sqrt_negative_error(self) -> None:
        calc = _make_calc(-1.0)
        calc.apply_sqrt()
        assert calc.is_error()

    def test_reciprocal_zero_error(self) -> None:
        calc = _make_calc(0.0)
        calc.apply_reciprocal()
        assert calc.is_error()


class TestConstants:
    """Constant insertion tests."""

    def test_pi(self) -> None:
        calc = ScientificCalculator()
        calc.input_pi()
        assert abs(calc.get_value() - math.pi) < 1e-6

    def test_e(self) -> None:
        calc = ScientificCalculator()
        calc.input_e()
        assert abs(calc.get_value() - math.e) < 1e-6


class TestFactorialAndAbs:
    """Factorial and absolute value tests."""

    @pytest.mark.parametrize("n,expected", [
        (5, 120.0),
        (0, 1.0),
        (1, 1.0),
        (10, 3628800.0),
    ])
    def test_factorial(self, n: int, expected: float) -> None:
        calc = _make_calc(float(n))
        calc.apply_factorial()
        assert abs(calc.get_value() - expected) < 1e-9

    def test_factorial_170(self) -> None:
        calc = _make_calc(170.0)
        calc.apply_factorial()
        assert not calc.is_error()
        assert calc.get_value() > 0

    def test_factorial_negative_error(self) -> None:
        calc = _make_calc(-3.0)
        calc.apply_factorial()
        assert calc.is_error()

    def test_factorial_float_error(self) -> None:
        calc = _make_calc(3.5)
        calc.apply_factorial()
        assert calc.is_error()

    def test_abs_negative(self) -> None:
        calc = _make_calc(-7.0)
        calc.apply_abs()
        assert abs(calc.get_value() - 7.0) < 1e-9

    def test_abs_positive(self) -> None:
        calc = _make_calc(7.0)
        calc.apply_abs()
        assert abs(calc.get_value() - 7.0) < 1e-9


class TestParentheses:
    """Parenthesis grouping tests."""

    def test_simple_grouping(self) -> None:
        calc = ScientificCalculator()
        # (2 + 3) * 4 = 20
        calc.input_open_paren()
        calc.input_digit("2")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.input_close_paren()
        calc.input_operator("*")
        calc.input_digit("4")
        calc.input_equals()
        assert abs(calc.get_value() - 20.0) < 1e-9

    def test_right_grouping(self) -> None:
        calc = ScientificCalculator()
        # 2 * (3 + 4) = 14
        calc.input_digit("2")
        calc.input_operator("*")
        calc.input_open_paren()
        calc.input_digit("3")
        calc.input_operator("+")
        calc.input_digit("4")
        calc.input_close_paren()
        calc.input_equals()
        assert abs(calc.get_value() - 14.0) < 1e-9

    def test_nested_parens(self) -> None:
        calc = ScientificCalculator()
        # ((2 + 3) * (4 + 1)) = 25
        calc.input_open_paren()
        calc.input_open_paren()
        calc.input_digit("2")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.input_close_paren()
        calc.input_operator("*")
        calc.input_open_paren()
        calc.input_digit("4")
        calc.input_operator("+")
        calc.input_digit("1")
        calc.input_close_paren()
        calc.input_close_paren()
        calc.input_equals()
        assert abs(calc.get_value() - 25.0) < 1e-9

    def test_mismatched_paren_error(self) -> None:
        calc = ScientificCalculator()
        # (2 + 3 = (missing close paren)
        calc.input_open_paren()
        calc.input_digit("2")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.input_equals()
        assert calc.is_error()

    def test_paren_depth(self) -> None:
        calc = ScientificCalculator()
        assert calc.get_paren_depth() == 0
        calc.input_open_paren()
        assert calc.get_paren_depth() == 1
        calc.input_open_paren()
        assert calc.get_paren_depth() == 2


class TestAngleMode:
    """Angle mode toggle tests."""

    def test_default_deg(self) -> None:
        calc = ScientificCalculator()
        assert calc.get_angle_mode() == "DEG"

    def test_toggle(self) -> None:
        calc = ScientificCalculator()
        calc.toggle_angle_mode()
        assert calc.get_angle_mode() == "RAD"
        calc.toggle_angle_mode()
        assert calc.get_angle_mode() == "DEG"
