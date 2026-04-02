"""Tests for BasicCalculator logic layer."""

import pytest

from calculator.logic.basic_logic import BasicCalculator


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def execute_steps(calc: BasicCalculator, steps: list[str]) -> None:
    """Drive a calculator through a sequence of step strings.

    Recognised steps:
        "0"-"9"  -> calc.append_digit(step)
        "+"      -> calc.add_operator("+")
        "-"      -> calc.add_operator("-")
        "*"      -> calc.add_operator("*")
        "/"      -> calc.add_operator("/")
        "="      -> calc.evaluate()
        "+/-"    -> calc.toggle_sign()
        "%"      -> calc.percentage()
        "C"      -> calc.clear_entry()
        "AC"     -> calc.clear_all()
        "BS"     -> calc.backspace()
        "."      -> calc.append_decimal()
    """
    operators = {"+", "-", "*", "/"}
    for step in steps:
        if step in "0123456789" and len(step) == 1:
            calc.append_digit(step)
        elif step in operators:
            calc.add_operator(step)
        elif step == "=":
            calc.evaluate()
        elif step == "+/-":
            calc.toggle_sign()
        elif step == "%":
            calc.percentage()
        elif step == "C":
            calc.clear_entry()
        elif step == "AC":
            calc.clear_all()
        elif step == "BS":
            calc.backspace()
        elif step == ".":
            calc.append_decimal()
        else:
            raise ValueError(f"Unknown step: {step!r}")


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def calc() -> BasicCalculator:
    """Return a fresh BasicCalculator instance."""
    return BasicCalculator()


# ---------------------------------------------------------------------------
# BA  Arithmetic tests
# ---------------------------------------------------------------------------

class TestArithmetic:
    """BA-1..6: basic arithmetic via parametrize."""

    @pytest.mark.parametrize(
        "steps, expected_display",
        [
            # BA-1  addition
            (["2", "+", "3", "="], "5"),
            # BA-2  subtraction  (10 - 3 = 7)
            (["1", "0", "-", "3", "="], "7"),
            # BA-3  multiplication
            (["4", "*", "5", "="], "20"),
            # BA-4  division with decimal result
            (["1", "0", "/", "4", "="], "2.5"),
            # BA-5  operator precedence  2+3*4 = 14
            (["2", "+", "3", "*", "4", "="], "14"),
        ],
        ids=["BA-1-add", "BA-2-sub", "BA-3-mul", "BA-4-div", "BA-5-precedence"],
    )
    def test_arithmetic(self, calc, steps, expected_display):
        execute_steps(calc, steps)
        assert calc.get_display_value() == expected_display

    def test_division_by_zero(self, calc):
        """BA-6: 100 / 0 = should enter error state."""
        execute_steps(calc, ["1", "0", "0", "/", "0", "="])
        assert calc.error is True


# ---------------------------------------------------------------------------
# NI  Numeric input tests
# ---------------------------------------------------------------------------

class TestNumericInput:
    """NI-1..6: digit entry, decimals, sign, percentage."""

    def test_leading_zeros_stripped(self, calc):
        """NI-1: 0, 0, 7 -> display '7'."""
        execute_steps(calc, ["0", "0", "7"])
        assert calc.get_display_value() == "7"

    def test_single_decimal_point(self, calc):
        """NI-2: '.', '.', '5' -> display '0.5'."""
        execute_steps(calc, [".", ".", "5"])
        assert calc.get_display_value() == "0.5"

    def test_toggle_sign(self, calc):
        """NI-3: 5, +/- -> display '-5'."""
        execute_steps(calc, ["5", "+/-"])
        assert calc.get_display_value() == "-5"

    def test_percentage(self, calc):
        """NI-4: 200% -> display '2'."""
        execute_steps(calc, ["2", "0", "0", "%"])
        assert calc.get_display_value() == "2"


# ---------------------------------------------------------------------------
# DI  Display formatting tests
# ---------------------------------------------------------------------------

class TestDisplayFormatting:
    """DI-1..6: integer display, precision, scientific notation."""

    def test_integer_display_no_trailing_zero(self, calc):
        """DI-1: 4/2 = display '2' not '2.0'."""
        execute_steps(calc, ["4", "/", "2", "="])
        assert calc.get_display_value() == "2"

    def test_repeating_decimal_precision(self, calc):
        """DI-2: 1/3 = display '0.3333333333' (10 significant digits)."""
        execute_steps(calc, ["1", "/", "3", "="])
        assert calc.get_display_value() == "0.3333333333"

    def test_scientific_notation_large_result(self, calc):
        """DI-3: 9999999999 * 9999999999 -> scientific notation."""
        execute_steps(calc, list("9999999999") + ["*"] + list("9999999999") + ["="])
        display = calc.get_display_value()
        assert "e" in display or "E" in display


# ---------------------------------------------------------------------------
# CE  Clear and edit tests
# ---------------------------------------------------------------------------

class TestClearAndEdit:
    """CE-1..3: clear entry, clear all, backspace."""

    def test_clear_entry_preserves_operation(self, calc):
        """CE-1: 5+3 C 2= -> 7 (5+2)."""
        execute_steps(calc, ["5", "+", "3", "C", "2", "="])
        assert calc.get_display_value() == "7"

    def test_clear_entry_resets_display(self, calc):
        """CE-1 sub: after C display is '0'."""
        execute_steps(calc, ["5", "+", "3", "C"])
        assert calc.get_display_value() == "0"

    def test_clear_all_resets_everything(self, calc):
        """CE-2: 5+3 AC 2= -> 2."""
        execute_steps(calc, ["5", "+", "3", "AC", "2", "="])
        assert calc.get_display_value() == "2"

    def test_clear_all_resets_display(self, calc):
        """CE-2 sub: after AC display is '0'."""
        execute_steps(calc, ["5", "+", "3", "AC"])
        assert calc.get_display_value() == "0"

    def test_backspace(self, calc):
        """CE-3: 1,2,3 BS -> '12'."""
        execute_steps(calc, ["1", "2", "3", "BS"])
        assert calc.get_display_value() == "12"


# ---------------------------------------------------------------------------
# RC  Error recovery tests
# ---------------------------------------------------------------------------

class TestErrorRecovery:
    """RC-1..2: recovery from error state."""

    def test_digit_clears_error(self, calc):
        """RC-1: after error, pressing 5 clears error, display '5'."""
        execute_steps(calc, ["1", "0", "0", "/", "0", "="])
        assert calc.error is True
        execute_steps(calc, ["5"])
        assert calc.error is False
        assert calc.get_display_value() == "5"

    def test_ac_clears_error(self, calc):
        """RC-2: after error, pressing AC clears error, display '0'."""
        execute_steps(calc, ["1", "0", "0", "/", "0", "="])
        assert calc.error is True
        execute_steps(calc, ["AC"])
        assert calc.error is False
        assert calc.get_display_value() == "0"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Miscellaneous edge-case behaviour."""

    def test_equals_with_no_expression(self, calc):
        """Pressing = with no prior input -> display '0'."""
        execute_steps(calc, ["="])
        assert calc.get_display_value() == "0"

    def test_backspace_single_digit(self, calc):
        """Backspace on a single digit -> '0'."""
        execute_steps(calc, ["5", "BS"])
        assert calc.get_display_value() == "0"

    def test_sign_toggle_on_zero(self, calc):
        """Toggle sign on 0 -> '0' (or '-0' acceptable)."""
        execute_steps(calc, ["+/-"])
        display = calc.get_display_value()
        assert display in ("0", "-0")

    def test_multiple_decimal_points_ignored(self, calc):
        """Only the first decimal point is accepted."""
        execute_steps(calc, ["1", ".", "2", ".", "3"])
        assert calc.get_display_value() == "1.23"
