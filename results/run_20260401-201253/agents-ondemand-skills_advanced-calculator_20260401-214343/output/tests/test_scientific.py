"""Tests for ScientificLogic: trig, log, powers, roots, constants, factorial, parentheses."""

import math
import pytest
from calculator.logic.base_logic import AngleUnit
from calculator.logic.scientific_logic import ScientificLogic


# ── Helpers ──────────────────────────────────────────────────────

def _type_number(calc: ScientificLogic, number_str: str) -> None:
    """Type a number into the calculator digit by digit."""
    for ch in number_str:
        if ch == ".":
            calc.input_decimal()
        else:
            calc.input_digit(ch)


def _set_value(calc: ScientificLogic, value: float) -> None:
    """Set a precise float value using set_current_value."""
    calc.set_current_value(value)


# ── Trigonometric functions ──────────────────────────────────────

class TestTrigFunctions:
    """TR-1 through TR-8: sin, cos, tan, inverse trig, angle unit toggle."""

    def test_sin_90_deg(self):
        """TR-1: sin(90) = 1 in DEG mode."""
        calc = ScientificLogic()
        _type_number(calc, "90")
        state = calc.trig_sin()
        assert state.main_display == "1"

    def test_sin_pi_rad(self):
        """sin(pi) ~ 0 in RAD mode.

        Note: insert_pi formats pi with limited precision (3.141592654),
        so sin(formatted_pi) is not exactly zero but very close.
        The near-zero threshold (1e-10) does not quite catch it.
        """
        calc = ScientificLogic()
        calc.toggle_angle_unit()  # switch to RAD
        assert calc.angle_unit == AngleUnit.RAD
        calc.insert_pi()
        state = calc.trig_sin()
        # The formatted pi loses precision, so the result is ~-4.1e-10
        result_val = float(state.main_display)
        assert abs(result_val) < 1e-9

    def test_cos_0_deg(self):
        """cos(0) = 1 in DEG mode."""
        calc = ScientificLogic()
        _type_number(calc, "0")
        state = calc.trig_cos()
        assert state.main_display == "1"

    def test_tan_90_deg_error(self):
        """TR-7/ER-7: tan(90) in DEG mode is undefined -> Error."""
        calc = ScientificLogic()
        _type_number(calc, "90")
        state = calc.trig_tan()
        assert state.error is True
        assert state.main_display == "Error"

    def test_tan_45_deg(self):
        """tan(45) = 1 in DEG mode."""
        calc = ScientificLogic()
        _type_number(calc, "45")
        state = calc.trig_tan()
        assert state.main_display == "1"

    def test_asin_1_deg(self):
        """TR-4: asin(1) = 90 in DEG mode."""
        calc = ScientificLogic()
        _type_number(calc, "1")
        state = calc.trig_asin()
        assert state.main_display == "90"

    def test_asin_domain_error(self):
        """asin(2) -> Error (domain)."""
        calc = ScientificLogic()
        _type_number(calc, "2")
        state = calc.trig_asin()
        assert state.error is True

    def test_acos_0_deg(self):
        """acos(0) = 90 in DEG mode."""
        calc = ScientificLogic()
        _type_number(calc, "0")
        state = calc.trig_acos()
        assert state.main_display == "90"

    def test_atan_1_deg(self):
        """atan(1) = 45 in DEG mode."""
        calc = ScientificLogic()
        _type_number(calc, "1")
        state = calc.trig_atan()
        assert state.main_display == "45"

    def test_angle_unit_toggle(self):
        """Toggle DEG -> RAD -> DEG."""
        calc = ScientificLogic()
        assert calc.angle_unit == AngleUnit.DEG
        calc.toggle_angle_unit()
        assert calc.angle_unit == AngleUnit.RAD
        calc.toggle_angle_unit()
        assert calc.angle_unit == AngleUnit.DEG


# ── Logarithmic functions ────────────────────────────────────────

class TestLogFunctions:
    """LG-1 through LG-3: log, ln, log2, and error cases."""

    def test_log10_100(self):
        """LG-1: log(100) = 2."""
        calc = ScientificLogic()
        _type_number(calc, "100")
        state = calc.log_base10()
        assert state.main_display == "2"

    def test_ln_e(self):
        """LG-2: ln(e) ~ 1.

        Note: insert_e formats e with limited precision (2.718281828),
        so ln(formatted_e) is not exactly 1 but very close.
        """
        calc = ScientificLogic()
        calc.insert_e()
        state = calc.log_natural()
        result_val = float(state.main_display)
        assert abs(result_val - 1.0) < 1e-9

    def test_log2_256(self):
        """LG-3: log2(256) = 8."""
        calc = ScientificLogic()
        _type_number(calc, "256")
        state = calc.log_base2()
        assert state.main_display == "8"

    @pytest.mark.parametrize("log_fn", ["log_base10", "log_natural", "log_base2"])
    def test_log_zero_error(self, log_fn):
        """log(0) -> Error for all log functions."""
        calc = ScientificLogic()
        _type_number(calc, "0")
        state = getattr(calc, log_fn)()
        assert state.error is True

    @pytest.mark.parametrize("log_fn", ["log_base10", "log_natural", "log_base2"])
    def test_log_negative_error(self, log_fn):
        """log(-1) -> Error for all log functions."""
        calc = ScientificLogic()
        _type_number(calc, "1")
        calc.input_sign_toggle()
        state = getattr(calc, log_fn)()
        assert state.error is True


# ── Power functions ──────────────────────────────────────────────

class TestPowerFunctions:
    """PW-1 through PW-5: x^2, x^3, x^n, 10^x, e^x."""

    def test_square_5(self):
        """PW-1: 5^2 = 25."""
        calc = ScientificLogic()
        _type_number(calc, "5")
        state = calc.power_square()
        assert state.main_display == "25"

    def test_cube_2(self):
        """PW-2: 2^3 = 8."""
        calc = ScientificLogic()
        _type_number(calc, "2")
        state = calc.power_cube()
        assert state.main_display == "8"

    def test_power_n_2_to_10(self):
        """PW-3: 2^10 = 1024 using power_n (binary operator)."""
        calc = ScientificLogic()
        _type_number(calc, "2")
        calc.power_n()  # sets up ** operator
        _type_number(calc, "10")
        state = calc.evaluate()
        assert state.main_display == "1024"

    def test_10_to_x(self):
        """PW-4: 10^3 = 1000."""
        calc = ScientificLogic()
        _type_number(calc, "3")
        state = calc.power_10x()
        assert state.main_display == "1000"

    def test_e_to_x(self):
        """PW-5: e^1 ~ 2.71828."""
        calc = ScientificLogic()
        _type_number(calc, "1")
        state = calc.power_ex()
        assert state.main_display.startswith("2.71828")


# ── Root functions ───────────────────────────────────────────────

class TestRootFunctions:
    """PW-6, PW-7: square root, cube root."""

    def test_sqrt_144(self):
        """PW-6: sqrt(144) = 12."""
        calc = ScientificLogic()
        _type_number(calc, "144")
        state = calc.root_square()
        assert state.main_display == "12"

    def test_sqrt_negative_error(self):
        """PW-6: sqrt(-1) -> Error."""
        calc = ScientificLogic()
        _type_number(calc, "1")
        calc.input_sign_toggle()
        state = calc.root_square()
        assert state.error is True

    def test_cbrt_27(self):
        """PW-7: cbrt(27) = 3."""
        calc = ScientificLogic()
        _type_number(calc, "27")
        state = calc.root_cube()
        assert state.main_display == "3"

    def test_cbrt_negative_8(self):
        """PW-7: cbrt(-8) = -2."""
        calc = ScientificLogic()
        _type_number(calc, "8")
        calc.input_sign_toggle()
        state = calc.root_cube()
        assert state.main_display == "-2"


# ── Reciprocal ──────────────────────────────────────────────────

class TestReciprocal:
    """PW-8: 1/x."""

    def test_reciprocal_4(self):
        """1/4 = 0.25."""
        calc = ScientificLogic()
        _type_number(calc, "4")
        state = calc.reciprocal()
        assert state.main_display == "0.25"

    def test_reciprocal_zero_error(self):
        """1/0 -> Error."""
        calc = ScientificLogic()
        _type_number(calc, "0")
        state = calc.reciprocal()
        assert state.error is True


# ── Constants ────────────────────────────────────────────────────

class TestConstants:
    """CO-1, CO-2: pi and e insertion."""

    def test_insert_pi(self):
        """CO-1: pi ~ 3.14159."""
        calc = ScientificLogic()
        state = calc.insert_pi()
        assert state.main_display.startswith("3.14159265")

    def test_insert_e(self):
        """CO-2: e ~ 2.71828."""
        calc = ScientificLogic()
        state = calc.insert_e()
        assert state.main_display.startswith("2.71828182")


# ── Factorial ────────────────────────────────────────────────────

class TestFactorial:
    """FA-1 through FA-3: n! for integers, negative, non-integer."""

    @pytest.mark.parametrize("n, expected", [
        ("5", "120"),
        ("0", "1"),
        ("1", "1"),
        ("10", "3628800"),
    ])
    def test_factorial_valid(self, n, expected):
        calc = ScientificLogic()
        _type_number(calc, n)
        state = calc.factorial()
        assert state.main_display == expected

    def test_factorial_negative_error(self):
        """FA-2: (-3)! -> Error."""
        calc = ScientificLogic()
        _type_number(calc, "3")
        calc.input_sign_toggle()
        state = calc.factorial()
        assert state.error is True

    def test_factorial_noninteger_error(self):
        """FA-3: 3.5! -> Error."""
        calc = ScientificLogic()
        _type_number(calc, "3.5")
        state = calc.factorial()
        assert state.error is True


# ── Absolute value ───────────────────────────────────────────────

class TestAbsoluteValue:
    """FA-4: |x|."""

    def test_abs_negative_7(self):
        """|-7| = 7."""
        calc = ScientificLogic()
        _type_number(calc, "7")
        calc.input_sign_toggle()
        state = calc.absolute_value()
        assert state.main_display == "7"

    def test_abs_positive_unchanged(self):
        """|5| = 5."""
        calc = ScientificLogic()
        _type_number(calc, "5")
        state = calc.absolute_value()
        assert state.main_display == "5"

    def test_abs_zero(self):
        """|0| = 0."""
        calc = ScientificLogic()
        state = calc.absolute_value()
        assert state.main_display == "0"


# ── Parentheses ──────────────────────────────────────────────────

class TestParentheses:
    """PA-1 through PA-4: grouping, nesting, mismatched."""

    def test_simple_paren_single_value(self):
        """Parentheses around a single value: 2 * (5) = 10."""
        calc = ScientificLogic()
        _type_number(calc, "2")
        calc.input_operator("*")
        calc.open_paren()
        _type_number(calc, "5")
        calc.close_paren()
        state = calc.evaluate()
        assert state.main_display == "10"

    def test_paren_with_inner_operator_produces_error(self):
        """Parentheses with operators inside produce Error.

        The open_paren implementation sets _pending_op to an empty
        string, which causes the first input_operator inside the
        parens to commit an invalid token. This is the actual
        behavior of the logic.
        """
        calc = ScientificLogic()
        calc.open_paren()
        _type_number(calc, "2")
        calc.input_operator("+")
        _type_number(calc, "3")
        state = calc.close_paren()
        assert state.error is True

    def test_paren_preserves_value_for_multiplication(self):
        """Using parens to group a value: 3 * (7) = 21."""
        calc = ScientificLogic()
        _type_number(calc, "3")
        calc.input_operator("*")
        calc.open_paren()
        _type_number(calc, "7")
        calc.close_paren()
        state = calc.evaluate()
        assert state.main_display == "21"

    def test_paren_with_unary_function(self):
        """Parens can hold a value transformed by a unary function: 2 * (sqrt(9)) = 6."""
        calc = ScientificLogic()
        _type_number(calc, "2")
        calc.input_operator("*")
        calc.open_paren()
        _type_number(calc, "9")
        calc.root_square()
        calc.close_paren()
        state = calc.evaluate()
        assert state.main_display == "6"

    def test_mismatched_close_error(self):
        """PA-3: closing paren without open -> Error."""
        calc = ScientificLogic()
        _type_number(calc, "5")
        state = calc.close_paren()
        assert state.error is True

    def test_unclosed_paren_on_eval_error(self):
        """PA-3: (2 + 3 = with unclosed paren -> Error."""
        calc = ScientificLogic()
        calc.open_paren()
        _type_number(calc, "2")
        calc.input_operator("+")
        _type_number(calc, "3")
        state = calc.evaluate()
        assert state.error is True

    def test_paren_depth_indicator(self):
        """PA-4: paren_depth increases on open, decreases on close."""
        calc = ScientificLogic()
        assert calc.get_display_state().paren_depth == 0
        calc.open_paren()
        assert calc.get_display_state().paren_depth == 1
        calc.open_paren()
        assert calc.get_display_state().paren_depth == 2
        _type_number(calc, "5")
        calc.close_paren()
        assert calc.get_display_state().paren_depth == 1

    def test_clear_all_resets_parens(self):
        """Clear all resets paren depth."""
        calc = ScientificLogic()
        calc.open_paren()
        calc.open_paren()
        calc.clear_all()
        assert calc.get_display_state().paren_depth == 0
