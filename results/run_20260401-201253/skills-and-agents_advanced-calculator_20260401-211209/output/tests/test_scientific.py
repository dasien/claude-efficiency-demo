"""Comprehensive tests for the ScientificCalculator logic."""

import math

import pytest

from calculator.logic.scientific_logic import ScientificCalculator


@pytest.fixture
def calc() -> ScientificCalculator:
    """Return a fresh ScientificCalculator instance."""
    return ScientificCalculator()


# ---------------------------------------------------------------------------
# Helper to prepare a unary operation
# ---------------------------------------------------------------------------

def _set_value(calc: ScientificCalculator, value: float) -> None:
    """Set current_value and mark as ready for unary operation."""
    calc.current_value = value
    calc._new_input = True


# ---------------------------------------------------------------------------
# TR-1..8  Trigonometric functions (parametrized)
# ---------------------------------------------------------------------------

class TestTrigFunctions:
    """Tests for trig functions in DEG and RAD modes."""

    @pytest.mark.parametrize(
        "method, input_val, expected",
        [
            ("sin", 90, 1),
            ("sin", 0, 0),
            ("cos", 0, 1),
            ("cos", 60, 0.5),
        ],
        ids=["TR-1 sin(90)=1", "TR-2 sin(0)=0", "TR-3 cos(0)=1", "TR-4 cos(60)=0.5"],
    )
    def test_trig_deg(self, calc, method, input_val, expected):
        _set_value(calc, input_val)
        result = getattr(calc, method)()
        assert result == pytest.approx(expected)
        assert calc.current_value == pytest.approx(expected)

    @pytest.mark.parametrize(
        "method, input_val, expected",
        [
            ("asin", 1, 90),
            ("acos", 0.5, 60),
            ("atan", 1, 45),
        ],
        ids=["TR-5 asin(1)=90", "TR-6 acos(0.5)=60", "TR-7 atan(1)=45"],
    )
    def test_inverse_trig_deg(self, calc, method, input_val, expected):
        _set_value(calc, input_val)
        result = getattr(calc, method)()
        assert result == pytest.approx(expected)
        assert calc.current_value == pytest.approx(expected)

    def test_sin_pi_rad(self, calc):
        """TR-8: sin(pi) in RAD mode should be approximately 0."""
        calc.toggle_angle_mode()  # switch to RAD
        _set_value(calc, math.pi)
        result = calc.sin()
        assert result == pytest.approx(0, abs=1e-9)

    def test_toggle_angle_mode(self, calc):
        """Angle mode starts DEG, toggles to RAD, then back to DEG."""
        assert calc.angle_mode == "DEG"
        assert calc.toggle_angle_mode() == "RAD"
        assert calc.toggle_angle_mode() == "DEG"


# ---------------------------------------------------------------------------
# Trig error cases
# ---------------------------------------------------------------------------

class TestTrigErrors:
    """Tests for trig functions that should produce error states."""

    def test_tan_90_deg_error(self, calc):
        _set_value(calc, 90)
        calc.tan()
        assert calc.error is True

    def test_asin_out_of_range(self, calc):
        _set_value(calc, 2)
        calc.asin()
        assert calc.error is True

    def test_acos_out_of_range(self, calc):
        _set_value(calc, 2)
        calc.acos()
        assert calc.error is True


# ---------------------------------------------------------------------------
# LG-1..3  Logarithmic functions (parametrized)
# ---------------------------------------------------------------------------

class TestLogarithmic:
    """Tests for log, ln, and log2."""

    @pytest.mark.parametrize(
        "method, input_val, expected",
        [
            ("log", 100, 2),
            ("log", 1, 0),
            ("ln", math.e, 1),
            ("log2", 256, 8),
        ],
        ids=["LG-1 log(100)=2", "LG-2 log(1)=0", "LG-3 ln(e)=1", "LG-4 log2(256)=8"],
    )
    def test_log_functions(self, calc, method, input_val, expected):
        _set_value(calc, input_val)
        result = getattr(calc, method)()
        assert result == pytest.approx(expected)
        assert calc.current_value == pytest.approx(expected)


class TestLogErrors:
    """Tests for logarithmic error cases."""

    @pytest.mark.parametrize(
        "method, input_val",
        [
            ("log", 0),
            ("log", -1),
            ("ln", 0),
            ("log2", -5),
        ],
        ids=["log(0)", "log(-1)", "ln(0)", "log2(-5)"],
    )
    def test_log_errors(self, calc, method, input_val):
        _set_value(calc, input_val)
        getattr(calc, method)()
        assert calc.error is True


# ---------------------------------------------------------------------------
# PW-1..8  Powers and Roots (parametrized)
# ---------------------------------------------------------------------------

class TestPowersAndRoots:
    """Tests for power and root functions."""

    @pytest.mark.parametrize(
        "method, input_val, expected",
        [
            ("square", 5, 25),
            ("cube", 3, 27),
            ("ten_power", 3, 1000),
            ("e_power", 0, 1),
            ("e_power", 1, math.e),
            ("square_root", 144, 12),
            ("cube_root", 27, 3),
            ("cube_root", -8, -2),
            ("reciprocal", 4, 0.25),
        ],
        ids=[
            "PW-1 square(5)=25",
            "PW-2 cube(3)=27",
            "PW-4 10^3=1000",
            "PW-5 e^0=1",
            "PW-6 e^1=e",
            "PW-7 sqrt(144)=12",
            "PW-8 cbrt(27)=3",
            "PW-8b cbrt(-8)=-2",
            "PW-9 1/4=0.25",
        ],
    )
    def test_power_root_functions(self, calc, method, input_val, expected):
        _set_value(calc, input_val)
        result = getattr(calc, method)()
        assert result == pytest.approx(expected)
        assert calc.current_value == pytest.approx(expected)

    def test_power_two_operand(self, calc):
        """PW-3: 2 ** 10 = 1024 using power(), append_digit, evaluate."""
        _set_value(calc, 2)
        calc.power()
        calc.append_digit("1")
        calc.append_digit("0")
        result = calc.evaluate()
        assert result == pytest.approx(1024)


class TestPowerRootErrors:
    """Tests for power/root error cases."""

    def test_square_root_negative(self, calc):
        _set_value(calc, -1)
        calc.square_root()
        assert calc.error is True

    def test_reciprocal_zero(self, calc):
        _set_value(calc, 0)
        calc.reciprocal()
        assert calc.error is True


# ---------------------------------------------------------------------------
# CO-1..2  Constants
# ---------------------------------------------------------------------------

class TestConstants:
    """Tests for pi and e constant insertion."""

    def test_insert_pi(self, calc):
        calc.insert_pi()
        assert calc.current_value == pytest.approx(math.pi)

    def test_insert_e(self, calc):
        calc.insert_e()
        assert calc.current_value == pytest.approx(math.e)

    def test_e_then_e_power(self, calc):
        """Insert e, then compute e^e which is approximately 15.1542622414."""
        calc.insert_e()
        result = calc.e_power()
        assert result == pytest.approx(math.e ** math.e, rel=1e-9)
        assert result == pytest.approx(15.1542622414, rel=1e-6)


# ---------------------------------------------------------------------------
# FA-1..4  Factorial
# ---------------------------------------------------------------------------

class TestFactorial:
    """Tests for the factorial function."""

    @pytest.mark.parametrize(
        "input_val, expected",
        [
            (5, 120),
            (0, 1),
        ],
        ids=["FA-1 5!=120", "FA-2 0!=1"],
    )
    def test_factorial_valid(self, calc, input_val, expected):
        _set_value(calc, input_val)
        result = calc.factorial()
        assert result == pytest.approx(expected)

    def test_factorial_170_succeeds(self, calc):
        """NF-4: factorial(170) should succeed without error."""
        _set_value(calc, 170)
        result = calc.factorial()
        assert calc.error is False
        assert result == pytest.approx(float(math.factorial(170)))

    def test_factorial_negative_error(self, calc):
        _set_value(calc, -3)
        calc.factorial()
        assert calc.error is True

    def test_factorial_non_integer_error(self, calc):
        _set_value(calc, 3.5)
        calc.factorial()
        assert calc.error is True


# ---------------------------------------------------------------------------
# FA-4  Absolute value
# ---------------------------------------------------------------------------

class TestAbsoluteValue:
    """Tests for the absolute value function."""

    @pytest.mark.parametrize(
        "input_val, expected",
        [
            (-7, 7),
            (7, 7),
            (0, 0),
        ],
        ids=["abs(-7)=7", "abs(7)=7", "abs(0)=0"],
    )
    def test_absolute(self, calc, input_val, expected):
        _set_value(calc, input_val)
        result = calc.absolute()
        assert result == pytest.approx(expected)


# ---------------------------------------------------------------------------
# PA-1..4  Parentheses
# ---------------------------------------------------------------------------

class TestParentheses:
    """Tests for parenthesized expression evaluation."""

    def test_paren_2_plus_3_times_4(self, calc):
        """PA-1: (2+3)*4 = 20."""
        calc.open_paren()
        calc.append_digit("2")
        calc.add_operator("+")
        calc.append_digit("3")
        calc.close_paren()
        calc.add_operator("*")
        calc.append_digit("4")
        result = calc.evaluate()
        assert result == pytest.approx(20)

    def test_paren_2_times_3_plus_4(self, calc):
        """PA-2: 2*(3+4) = 14."""
        calc.append_digit("2")
        calc.add_operator("*")
        calc.open_paren()
        calc.append_digit("3")
        calc.add_operator("+")
        calc.append_digit("4")
        calc.close_paren()
        result = calc.evaluate()
        assert result == pytest.approx(14)

    def test_nested_parens(self, calc):
        """PA-3: ((2+3)*(4+1)) = 25."""
        calc.open_paren()
        calc.open_paren()
        calc.append_digit("2")
        calc.add_operator("+")
        calc.append_digit("3")
        calc.close_paren()
        calc.add_operator("*")
        calc.open_paren()
        calc.append_digit("4")
        calc.add_operator("+")
        calc.append_digit("1")
        calc.close_paren()
        calc.close_paren()
        result = calc.evaluate()
        assert result == pytest.approx(25)

    def test_mismatched_paren_error(self, calc):
        """PA-4: (2+3 without closing paren should error on evaluate."""
        calc.open_paren()
        calc.append_digit("2")
        calc.add_operator("+")
        calc.append_digit("3")
        calc.evaluate()
        assert calc.error is True
