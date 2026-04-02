"""Tests for basic calculator mode."""

import pytest
from calculator.logic.basic_logic import BasicCalculator


@pytest.fixture
def calc():
    """Create a fresh BasicCalculator instance."""
    return BasicCalculator()


# --- Happy Path: Arithmetic ---

class TestArithmetic:
    """Test basic arithmetic operations."""

    def test_addition(self, calc):
        calc.input_digit("2")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.evaluate()
        assert calc.get_display_value() == "5"

    def test_subtraction(self, calc):
        calc.input_digit("1")
        calc.input_digit("0")
        calc.input_operator("-")
        calc.input_digit("3")
        calc.evaluate()
        assert calc.get_display_value() == "7"

    def test_multiplication(self, calc):
        calc.input_digit("4")
        calc.input_operator("*")
        calc.input_digit("5")
        calc.evaluate()
        assert calc.get_display_value() == "20"

    def test_division(self, calc):
        calc.input_digit("1")
        calc.input_digit("0")
        calc.input_operator("/")
        calc.input_digit("4")
        calc.evaluate()
        assert calc.get_display_value() == "2.5"

    def test_operator_precedence(self, calc):
        # 2 + 3 * 4 = 14
        calc.input_digit("2")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.input_operator("*")
        calc.input_digit("4")
        calc.evaluate()
        assert calc.get_display_value() == "14"

    def test_chained_addition(self, calc):
        calc.input_digit("1")
        calc.input_operator("+")
        calc.input_digit("2")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.evaluate()
        assert calc.get_display_value() == "6"

    def test_multiple_precedence(self, calc):
        # 2 * 3 + 4 * 5 = 26
        calc.input_digit("2")
        calc.input_operator("*")
        calc.input_digit("3")
        calc.input_operator("+")
        calc.input_digit("4")
        calc.input_operator("*")
        calc.input_digit("5")
        calc.evaluate()
        assert calc.get_display_value() == "26"


# --- Happy Path: Numeric Input ---

class TestNumericInput:
    """Test numeric input handling."""

    def test_single_digit(self, calc):
        calc.input_digit("5")
        assert calc.get_display_value() == "5"

    def test_multi_digit(self, calc):
        calc.input_digit("1")
        calc.input_digit("2")
        calc.input_digit("3")
        assert calc.get_display_value() == "123"

    def test_decimal(self, calc):
        calc.input_digit("3")
        calc.input_decimal()
        calc.input_digit("1")
        calc.input_digit("4")
        assert calc.get_display_value() == "3.14"

    def test_leading_zero_prevention(self, calc):
        calc.input_digit("0")
        calc.input_digit("0")
        calc.input_digit("7")
        assert calc.get_display_value() == "7"

    def test_decimal_leading_zero(self, calc):
        calc.input_decimal()
        calc.input_digit("5")
        assert calc.get_display_value() == "0.5"

    def test_sign_toggle(self, calc):
        calc.input_digit("5")
        calc.toggle_sign()
        assert calc.get_display_value() == "-5"

    def test_sign_toggle_back(self, calc):
        calc.input_digit("5")
        calc.toggle_sign()
        calc.toggle_sign()
        assert calc.get_display_value() == "5"

    def test_percent(self, calc):
        calc.input_digit("2")
        calc.input_digit("0")
        calc.input_digit("0")
        calc.percent()
        assert calc.get_display_value() == "2"


# --- Happy Path: Display Formatting ---

class TestDisplayFormatting:
    """Test number display formatting."""

    def test_integer_result_no_decimal(self, calc):
        calc.input_digit("4")
        calc.input_operator("/")
        calc.input_digit("2")
        calc.evaluate()
        assert calc.get_display_value() == "2"

    def test_float_precision(self, calc):
        calc.input_digit("1")
        calc.input_operator("/")
        calc.input_digit("3")
        calc.evaluate()
        display = calc.get_display_value()
        assert display.startswith("0.333333333")

    def test_scientific_notation_large(self, calc):
        # 9999999999 * 9999999999
        for d in "9999999999":
            calc.input_digit(d)
        calc.input_operator("*")
        for d in "9999999999":
            calc.input_digit(d)
        calc.evaluate()
        display = calc.get_display_value()
        assert "e" in display.lower() or "E" in display


# --- Happy Path: Clear and Edit ---

class TestClearAndEdit:
    """Test clear and edit operations."""

    def test_clear_entry(self, calc):
        # 5 + 3, C, 2, = should give 7 (5 + 2)
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.clear_entry()
        calc.input_digit("2")
        calc.evaluate()
        assert calc.get_display_value() == "7"

    def test_all_clear(self, calc):
        # 5 + 3, AC, 2, = should give 2
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.all_clear()
        calc.input_digit("2")
        calc.evaluate()
        assert calc.get_display_value() == "2"

    def test_backspace(self, calc):
        calc.input_digit("1")
        calc.input_digit("2")
        calc.input_digit("3")
        calc.backspace()
        assert calc.get_display_value() == "12"

    def test_backspace_to_zero(self, calc):
        calc.input_digit("5")
        calc.backspace()
        assert calc.get_display_value() == "0"


# --- Edge Cases ---

class TestEdgeCases:
    """Test edge cases."""

    def test_double_decimal_ignored(self, calc):
        calc.input_digit("1")
        calc.input_decimal()
        calc.input_decimal()
        calc.input_digit("5")
        assert calc.get_display_value() == "1.5"

    def test_equals_with_no_op(self, calc):
        calc.input_digit("5")
        calc.evaluate()
        assert calc.get_display_value() == "5"

    def test_sign_toggle_zero(self, calc):
        calc.toggle_sign()
        assert calc.get_display_value() == "0"

    def test_negative_number_arithmetic(self, calc):
        calc.input_digit("5")
        calc.toggle_sign()
        calc.input_operator("+")
        calc.input_digit("3")
        calc.evaluate()
        assert calc.get_display_value() == "-2"


# --- Error Cases ---

class TestErrors:
    """Test error conditions."""

    def test_division_by_zero(self, calc):
        calc.input_digit("5")
        calc.input_operator("/")
        calc.input_digit("0")
        calc.evaluate()
        assert calc.get_display_value() == "Error"
        assert calc.error is True

    def test_error_recovery_digit(self, calc):
        calc.input_digit("5")
        calc.input_operator("/")
        calc.input_digit("0")
        calc.evaluate()
        assert calc.error is True
        calc.input_digit("5")
        assert calc.error is False
        assert calc.get_display_value() == "5"

    def test_error_recovery_clear(self, calc):
        calc.input_digit("5")
        calc.input_operator("/")
        calc.input_digit("0")
        calc.evaluate()
        assert calc.error is True
        calc.clear_entry()
        assert calc.error is False
        assert calc.get_display_value() == "0"

    def test_error_recovery_all_clear(self, calc):
        calc.input_digit("5")
        calc.input_operator("/")
        calc.input_digit("0")
        calc.evaluate()
        calc.all_clear()
        assert calc.error is False
        assert calc.get_display_value() == "0"
