"""Tests for BasicLogic: arithmetic, numeric input, display formatting, clear, edge cases, errors."""

import pytest
from calculator.logic.basic_logic import BasicLogic


# ── Helpers ──────────────────────────────────────────────────────

def _type_number(calc: BasicLogic, number_str: str) -> None:
    """Type a number string (digits, decimal, sign) into the calculator."""
    for ch in number_str:
        if ch == ".":
            calc.input_decimal()
        elif ch == "-":
            calc.input_sign_toggle()
        else:
            calc.input_digit(ch)


def _compute(calc: BasicLogic, expr: str) -> str:
    """Build an expression like '2+3' and press equals, return main_display.

    Supports digits, '.', operators (+, -, *, /), and '=' to evaluate.
    Negative numbers should be entered via sign toggle before a number.
    """
    for ch in expr:
        if ch in "0123456789":
            calc.input_digit(ch)
        elif ch == ".":
            calc.input_decimal()
        elif ch in "+-*/":
            calc.input_operator(ch)
        elif ch == "=":
            calc.evaluate()
    state = calc.get_display_state()
    return state.main_display


# ── Happy path arithmetic ────────────────────────────────────────

class TestArithmeticHappyPath:
    """BA-1 through BA-6: basic four-function arithmetic with precedence."""

    @pytest.mark.parametrize("expr, expected", [
        ("2+3=", "5"),
        ("1+1=", "2"),
        ("9+0=", "9"),
        ("100+200=", "300"),
    ])
    def test_addition(self, expr, expected):
        calc = BasicLogic()
        assert _compute(calc, expr) == expected

    @pytest.mark.parametrize("expr, expected", [
        ("10-3=", "7"),
        ("5-5=", "0"),
        ("0-7=", "-7"),
    ])
    def test_subtraction(self, expr, expected):
        calc = BasicLogic()
        assert _compute(calc, expr) == expected

    @pytest.mark.parametrize("expr, expected", [
        ("3*4=", "12"),
        ("0*999=", "0"),
        ("7*1=", "7"),
    ])
    def test_multiplication(self, expr, expected):
        calc = BasicLogic()
        assert _compute(calc, expr) == expected

    @pytest.mark.parametrize("expr, expected", [
        ("10/4=", "2.5"),
        ("9/3=", "3"),
        ("4/2=", "2"),
    ])
    def test_division(self, expr, expected):
        calc = BasicLogic()
        assert _compute(calc, expr) == expected

    def test_operator_precedence(self):
        """BA-5/BA-6: 2 + 3 * 4 = 14, not 20."""
        calc = BasicLogic()
        assert _compute(calc, "2+3*4=") == "14"

    def test_chained_operations(self):
        """Chained: 1 + 2 + 3 = 6."""
        calc = BasicLogic()
        assert _compute(calc, "1+2+3=") == "6"

    def test_chained_mixed_operations(self):
        """10 - 2 * 3 = 4 (precedence: 10 - 6)."""
        calc = BasicLogic()
        assert _compute(calc, "10-2*3=") == "4"

    def test_chained_after_eval(self):
        """After evaluation, operator chains with result: 2+3= then +4=."""
        calc = BasicLogic()
        _compute(calc, "2+3=")
        # Now chain: 5 + 4 = 9
        calc.input_operator("+")
        calc.input_digit("4")
        state = calc.evaluate()
        assert state.main_display == "9"


# ── Numeric input ────────────────────────────────────────────────

class TestNumericInput:
    """NI-1 through NI-6: digits, decimal, sign toggle, percentage."""

    def test_leading_zeros_suppressed(self):
        """NI-4: pressing 0,0,7 displays 7."""
        calc = BasicLogic()
        calc.input_digit("0")
        calc.input_digit("0")
        state = calc.input_digit("7")
        assert state.main_display == "7"

    def test_double_decimal_gives_0_5(self):
        """NI-3: pressing .,.,5 displays 0.5 (second dot ignored)."""
        calc = BasicLogic()
        calc.input_decimal()
        calc.input_decimal()
        state = calc.input_digit("5")
        assert state.main_display == "0.5"

    def test_sign_toggle(self):
        """NI-5: pressing 5, +/- displays -5."""
        calc = BasicLogic()
        calc.input_digit("5")
        state = calc.input_sign_toggle()
        assert state.main_display == "-5"

    def test_sign_toggle_zero_stays_zero(self):
        """Toggling sign of 0 keeps it 0."""
        calc = BasicLogic()
        state = calc.input_sign_toggle()
        assert state.main_display == "0"

    def test_sign_toggle_twice_returns_positive(self):
        calc = BasicLogic()
        calc.input_digit("5")
        calc.input_sign_toggle()
        state = calc.input_sign_toggle()
        assert state.main_display == "5"

    def test_percentage(self):
        """NI-6: 200 % displays 2."""
        calc = BasicLogic()
        calc.input_digit("2")
        calc.input_digit("0")
        calc.input_digit("0")
        state = calc.input_percent()
        assert state.main_display == "2"

    def test_percentage_decimal(self):
        """50 % = 0.5."""
        calc = BasicLogic()
        calc.input_digit("5")
        calc.input_digit("0")
        state = calc.input_percent()
        assert state.main_display == "0.5"


# ── Display formatting ──────────────────────────────────────────

class TestDisplayFormatting:
    """DI-1 through DI-6: integer display, precision, scientific notation."""

    def test_integer_without_decimal(self):
        """DI-3: 4 / 2 = displays 2, not 2.0."""
        calc = BasicLogic()
        assert _compute(calc, "4/2=") == "2"

    def test_float_precision(self):
        """DI-4: 1/3 displays up to 10 significant digits."""
        calc = BasicLogic()
        result = _compute(calc, "1/3=")
        # format_number uses .10g which gives "0.3333333333"
        assert result == "0.3333333333"

    def test_scientific_notation_large(self):
        """DI-5: very large numbers use scientific notation."""
        from calculator.logic.base_logic import BaseLogic
        # 1e20 is beyond 1e16, so it should be scientific
        formatted = BaseLogic.format_number(1e20)
        assert "e" in formatted or "E" in formatted

    def test_format_integer_value(self):
        """format_number(5.0) returns '5'."""
        from calculator.logic.base_logic import BaseLogic
        assert BaseLogic.format_number(5.0) == "5"

    def test_format_nan(self):
        """format_number(NaN) returns 'Error'."""
        from calculator.logic.base_logic import BaseLogic
        assert BaseLogic.format_number(float("nan")) == "Error"

    def test_format_inf(self):
        """format_number(inf) returns 'Error'."""
        from calculator.logic.base_logic import BaseLogic
        assert BaseLogic.format_number(float("inf")) == "Error"


# ── Clear and backspace ─────────────────────────────────────────

class TestClearAndBackspace:
    """CE-1 through CE-3: C, AC, Backspace."""

    def test_clear_entry_preserves_pending_op(self):
        """CE-1: 5 + 3, C, 2, = gives 7 (5+2)."""
        calc = BasicLogic()
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.clear_entry()
        calc.input_digit("2")
        state = calc.evaluate()
        assert state.main_display == "7"

    def test_all_clear_resets_everything(self):
        """CE-2: 5 + 3, AC, 2, = gives 2."""
        calc = BasicLogic()
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.clear_all()
        calc.input_digit("2")
        state = calc.evaluate()
        assert state.main_display == "2"

    def test_backspace(self):
        """CE-3: 1,2,3, Backspace displays 12."""
        calc = BasicLogic()
        calc.input_digit("1")
        calc.input_digit("2")
        calc.input_digit("3")
        state = calc.input_backspace()
        assert state.main_display == "12"

    def test_backspace_to_zero(self):
        """Backspace on single digit goes to 0."""
        calc = BasicLogic()
        calc.input_digit("5")
        state = calc.input_backspace()
        assert state.main_display == "0"

    def test_backspace_in_error_does_nothing(self):
        """Backspace during error state does nothing."""
        calc = BasicLogic()
        # Cause error
        calc.input_digit("1")
        calc.input_operator("/")
        calc.input_digit("0")
        calc.evaluate()
        state = calc.input_backspace()
        assert state.error is True

    def test_backspace_after_new_input_does_nothing(self):
        """Backspace when _new_input is True does nothing."""
        calc = BasicLogic()
        # Initial state: _new_input is True, display is "0"
        state = calc.input_backspace()
        assert state.main_display == "0"


# ── Edge cases ───────────────────────────────────────────────────

class TestEdgeCases:
    """Large numbers, many chained operators, equals with no expression."""

    def test_very_large_number_multiplication(self):
        """Large number multiplication doesn't crash."""
        calc = BasicLogic()
        # 9999999 * 9999999
        for d in "9999999":
            calc.input_digit(d)
        calc.input_operator("*")
        for d in "9999999":
            calc.input_digit(d)
        state = calc.evaluate()
        assert not state.error
        # Result should be representable
        assert state.main_display != "Error"

    def test_many_chained_additions(self):
        """1+1+1+1+1+1+1+1+1+1= gives 10."""
        calc = BasicLogic()
        calc.input_digit("1")
        for _ in range(9):
            calc.input_operator("+")
            calc.input_digit("1")
        state = calc.evaluate()
        assert state.main_display == "10"

    def test_equals_with_no_expression(self):
        """Pressing = with just a number shows that number."""
        calc = BasicLogic()
        calc.input_digit("5")
        state = calc.evaluate()
        assert state.main_display == "5"

    def test_equals_repeats_nothing_crashes(self):
        """Pressing = twice doesn't crash."""
        calc = BasicLogic()
        calc.input_digit("5")
        calc.evaluate()
        state = calc.evaluate()
        assert state.main_display == "5"

    def test_operator_replacement(self):
        """Pressing + then * replaces the operator."""
        calc = BasicLogic()
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_operator("*")
        calc.input_digit("3")
        state = calc.evaluate()
        assert state.main_display == "15"


# ── Error cases ──────────────────────────────────────────────────

class TestErrorCases:
    """ER-1, RC-1, RC-2: division by zero, error recovery."""

    def test_division_by_zero(self):
        """ER-1: 100 / 0 = displays Error."""
        calc = BasicLogic()
        result = _compute(calc, "100/0=")
        assert result == "Error"
        assert calc.get_display_state().error is True

    def test_error_recovery_digit_clears_error(self):
        """RC-1: after Error, pressing a digit clears error and starts new number."""
        calc = BasicLogic()
        _compute(calc, "1/0=")
        assert calc.get_display_state().error is True
        state = calc.input_digit("5")
        assert state.error is False
        assert state.main_display == "5"

    def test_error_recovery_clear_entry(self):
        """RC-2: after Error, pressing C clears the error."""
        calc = BasicLogic()
        _compute(calc, "1/0=")
        state = calc.clear_entry()
        assert state.error is False
        assert state.main_display == "0"

    def test_error_recovery_all_clear(self):
        """RC-2: after Error, pressing AC clears the error."""
        calc = BasicLogic()
        _compute(calc, "1/0=")
        state = calc.clear_all()
        assert state.error is False
        assert state.main_display == "0"

    def test_operator_in_error_ignored(self):
        """Pressing an operator while in error does nothing."""
        calc = BasicLogic()
        _compute(calc, "1/0=")
        state = calc.input_operator("+")
        assert state.error is True

    def test_sign_toggle_in_error_ignored(self):
        """Pressing +/- while in error does nothing."""
        calc = BasicLogic()
        _compute(calc, "1/0=")
        state = calc.input_sign_toggle()
        assert state.error is True

    def test_decimal_after_error_clears_it(self):
        """Pressing decimal after error clears it."""
        calc = BasicLogic()
        _compute(calc, "1/0=")
        state = calc.input_decimal()
        assert state.error is False
        assert state.main_display == "0."
