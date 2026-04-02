"""Comprehensive pytest test suite for CalculatorLogic."""

import pytest

from calculator_logic import CalculatorLogic


@pytest.fixture
def calc():
    """Return a fresh CalculatorLogic instance."""
    return CalculatorLogic()


# ---------------------------------------------------------------------------
# 1. Basic operations
# ---------------------------------------------------------------------------

class TestBasicOperations:
    """Test each arithmetic operator individually."""

    def test_addition(self, calc):
        for d in "2+3":
            if d.isdigit():
                calc.add_digit(d)
            else:
                calc.add_operator(d)
        assert calc.evaluate() == "5"

    def test_subtraction(self, calc):
        for d in "10-4":
            if d.isdigit():
                calc.add_digit(d)
            else:
                calc.add_operator(d)
        assert calc.evaluate() == "6"

    def test_multiplication(self, calc):
        for d in "3*4":
            if d.isdigit():
                calc.add_digit(d)
            else:
                calc.add_operator(d)
        assert calc.evaluate() == "12"

    def test_division(self, calc):
        for d in "8/2":
            if d.isdigit():
                calc.add_digit(d)
            else:
                calc.add_operator(d)
        assert calc.evaluate() == "4"

    def test_division_with_float_result(self, calc):
        for d in "7/2":
            if d.isdigit():
                calc.add_digit(d)
            else:
                calc.add_operator(d)
        assert calc.evaluate() == "3.5"


# ---------------------------------------------------------------------------
# 2. Display
# ---------------------------------------------------------------------------

class TestDisplay:
    """Test get_display behavior."""

    def test_initial_display_is_zero(self, calc):
        assert calc.get_display() == "0"

    def test_display_shows_expression_while_building(self, calc):
        calc.add_digit("1")
        calc.add_operator("+")
        calc.add_digit("2")
        assert calc.get_display() == "1+2"

    def test_display_after_evaluate(self, calc):
        calc.add_digit("5")
        calc.evaluate()
        assert calc.get_display() == "5"


# ---------------------------------------------------------------------------
# 3. Digit input
# ---------------------------------------------------------------------------

class TestDigitInput:
    """Test digit input behavior."""

    def test_single_digit(self, calc):
        calc.add_digit("7")
        assert calc.get_display() == "7"

    def test_multi_digit_number(self, calc):
        calc.add_digit("1")
        calc.add_digit("2")
        calc.add_digit("3")
        assert calc.get_display() == "123"

    def test_starts_fresh_after_result(self, calc):
        calc.add_digit("5")
        calc.add_operator("+")
        calc.add_digit("3")
        calc.evaluate()
        # Now type a new digit -- expression should start fresh
        calc.add_digit("9")
        assert calc.get_display() == "9"


# ---------------------------------------------------------------------------
# 4. Operator handling
# ---------------------------------------------------------------------------

class TestOperatorHandling:
    """Test operator replacement, leading minus, chaining."""

    def test_operator_replacement(self, calc):
        calc.add_digit("5")
        calc.add_operator("+")
        calc.add_operator("-")
        assert calc.get_display() == "5-"

    def test_leading_minus(self, calc):
        calc.add_operator("-")
        assert calc.get_display() == "-"

    def test_leading_non_minus_ignored(self, calc):
        calc.add_operator("+")
        assert calc.get_display() == "0"

    def test_leading_multiply_ignored(self, calc):
        calc.add_operator("*")
        assert calc.get_display() == "0"

    def test_operator_after_result_continues(self, calc):
        calc.add_digit("3")
        calc.add_operator("+")
        calc.add_digit("2")
        calc.evaluate()  # "5"
        calc.add_operator("+")
        assert calc.get_display() == "5+"


# ---------------------------------------------------------------------------
# 5. Decimal handling
# ---------------------------------------------------------------------------

class TestDecimalHandling:
    """Test decimal point behavior."""

    def test_single_decimal(self, calc):
        calc.add_digit("3")
        calc.add_decimal()
        calc.add_digit("5")
        assert calc.get_display() == "3.5"

    def test_prevents_duplicate_decimal(self, calc):
        calc.add_digit("3")
        calc.add_decimal()
        calc.add_decimal()
        calc.add_digit("5")
        assert calc.get_display() == "3.5"

    def test_leading_zero_added(self, calc):
        calc.add_decimal()
        assert calc.get_display() == "0."

    def test_decimal_after_operator(self, calc):
        calc.add_digit("1")
        calc.add_operator("+")
        calc.add_decimal()
        assert calc.get_display() == "1+0."

    def test_decimal_allowed_in_second_number(self, calc):
        calc.add_digit("1")
        calc.add_decimal()
        calc.add_digit("5")
        calc.add_operator("+")
        calc.add_digit("2")
        calc.add_decimal()
        calc.add_digit("3")
        assert calc.get_display() == "1.5+2.3"

    def test_decimal_after_result_starts_fresh(self, calc):
        calc.add_digit("5")
        calc.evaluate()
        calc.add_decimal()
        assert calc.get_display() == "0."


# ---------------------------------------------------------------------------
# 6. Evaluation
# ---------------------------------------------------------------------------

class TestEvaluation:
    """Test evaluate results and formatting."""

    def test_integer_formatting_no_trailing_dot_zero(self, calc):
        calc.add_digit("4")
        calc.add_operator("+")
        calc.add_digit("6")
        assert calc.evaluate() == "10"

    def test_float_precision(self, calc):
        calc.add_digit("1")
        calc.add_operator("/")
        calc.add_digit("3")
        result = calc.evaluate()
        assert result.startswith("0.333333333")

    def test_negative_result(self, calc):
        calc.add_digit("3")
        calc.add_operator("-")
        calc.add_digit("5")
        assert calc.evaluate() == "-2"

    def test_multiplication_of_decimals(self, calc):
        # 0.1 * 0.1 -- floating point should be handled
        for ch in "0":
            calc.add_digit(ch)
        calc.add_decimal()
        calc.add_digit("1")
        calc.add_operator("*")
        calc.add_digit("0")
        calc.add_decimal()
        calc.add_digit("1")
        assert calc.evaluate() == "0.01"


# ---------------------------------------------------------------------------
# 7. Error handling
# ---------------------------------------------------------------------------

class TestErrorHandling:
    """Test error conditions."""

    def test_division_by_zero(self, calc):
        calc.add_digit("5")
        calc.add_operator("/")
        calc.add_digit("0")
        assert calc.evaluate() == "Error"

    def test_empty_expression_evaluates_to_zero(self, calc):
        assert calc.evaluate() == "0"


# ---------------------------------------------------------------------------
# 8. Clear
# ---------------------------------------------------------------------------

class TestClear:
    """Test clear resets state."""

    def test_clear_resets_expression(self, calc):
        calc.add_digit("5")
        calc.add_operator("+")
        calc.add_digit("3")
        calc.clear()
        assert calc.get_display() == "0"

    def test_clear_after_result(self, calc):
        calc.add_digit("1")
        calc.evaluate()
        calc.clear()
        assert calc.get_display() == "0"

    def test_clear_allows_new_input(self, calc):
        calc.add_digit("9")
        calc.clear()
        calc.add_digit("4")
        assert calc.get_display() == "4"


# ---------------------------------------------------------------------------
# 9. Toggle sign
# ---------------------------------------------------------------------------

class TestToggleSign:
    """Test toggle_sign behavior."""

    def test_positive_to_negative(self, calc):
        calc.add_digit("5")
        calc.toggle_sign()
        assert calc.get_display() == "-5"

    def test_negative_to_positive(self, calc):
        calc.add_digit("5")
        calc.toggle_sign()
        calc.toggle_sign()
        assert calc.get_display() == "5"

    def test_toggle_on_empty_does_nothing(self, calc):
        calc.toggle_sign()
        assert calc.get_display() == "0"

    def test_toggle_sign_after_result(self, calc):
        calc.add_digit("3")
        calc.add_operator("+")
        calc.add_digit("2")
        calc.evaluate()  # "5"
        calc.toggle_sign()
        assert calc.get_display() == "-5"


# ---------------------------------------------------------------------------
# 10. Percent
# ---------------------------------------------------------------------------

class TestPercent:
    """Test add_percent behavior."""

    def test_percent_basic(self, calc):
        calc.add_digit("5")
        calc.add_digit("0")
        calc.add_percent()
        assert calc.get_display() == "0.5"

    def test_percent_on_empty_does_nothing(self, calc):
        calc.add_percent()
        assert calc.get_display() == "0"

    def test_percent_small_number(self, calc):
        calc.add_digit("1")
        calc.add_percent()
        assert calc.get_display() == "0.01"


# ---------------------------------------------------------------------------
# 11. Backspace
# ---------------------------------------------------------------------------

class TestBackspace:
    """Test backspace behavior."""

    def test_removes_last_character(self, calc):
        calc.add_digit("1")
        calc.add_digit("2")
        calc.add_digit("3")
        calc.backspace()
        assert calc.get_display() == "12"

    def test_backspace_to_empty_shows_zero(self, calc):
        calc.add_digit("5")
        calc.backspace()
        assert calc.get_display() == "0"

    def test_backspace_clears_after_result(self, calc):
        calc.add_digit("2")
        calc.add_operator("+")
        calc.add_digit("3")
        calc.evaluate()  # "5"
        calc.backspace()
        # After result, backspace clears entirely
        assert calc.get_display() == "0"

    def test_backspace_removes_operator(self, calc):
        calc.add_digit("5")
        calc.add_operator("+")
        calc.backspace()
        assert calc.get_display() == "5"


# ---------------------------------------------------------------------------
# 12. Chained operations
# ---------------------------------------------------------------------------

class TestChainedOperations:
    """Test continuing calculations from a result."""

    def test_chain_addition(self, calc):
        calc.add_digit("2")
        calc.add_operator("+")
        calc.add_digit("3")
        calc.evaluate()  # "5"
        calc.add_operator("+")
        calc.add_digit("4")
        assert calc.evaluate() == "9"

    def test_chain_multiplication(self, calc):
        calc.add_digit("3")
        calc.add_operator("*")
        calc.add_digit("2")
        calc.evaluate()  # "6"
        calc.add_operator("*")
        calc.add_digit("3")
        assert calc.evaluate() == "18"

    def test_chain_multiple_times(self, calc):
        calc.add_digit("1")
        calc.add_operator("+")
        calc.add_digit("1")
        calc.evaluate()  # "2"
        calc.add_operator("+")
        calc.add_digit("1")
        calc.evaluate()  # "3"
        calc.add_operator("+")
        calc.add_digit("1")
        assert calc.evaluate() == "4"


# ---------------------------------------------------------------------------
# 13. Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Test edge cases and unusual inputs."""

    def test_trailing_operator_stripped_before_eval(self, calc):
        calc.add_digit("5")
        calc.add_operator("+")
        assert calc.evaluate() == "5"

    def test_multiple_trailing_operators_stripped(self, calc):
        calc.add_digit("7")
        calc.add_operator("+")
        calc.add_operator("-")
        # The second operator replaces the first, so expression is "7-"
        assert calc.evaluate() == "7"

    def test_very_large_number(self, calc):
        for d in "99999999999":
            calc.add_digit(d)
        calc.add_operator("*")
        for d in "99999999999":
            calc.add_digit(d)
        result = calc.evaluate()
        # Should produce a valid numeric result, not Error
        assert result != "Error"
        assert int(result) == 99999999999 * 99999999999

    def test_only_operator_evaluates_to_zero(self, calc):
        calc.add_operator("-")
        # Expression is "-", rstrip("+-*/") yields "", so result is "0"
        assert calc.evaluate() == "0"

    def test_zero_division_resets_state(self, calc):
        calc.add_digit("1")
        calc.add_operator("/")
        calc.add_digit("0")
        calc.evaluate()  # "Error"
        # After error, typing a new digit should start fresh
        calc.add_digit("7")
        assert calc.get_display() == "7"

    def test_evaluate_twice_returns_same(self, calc):
        calc.add_digit("4")
        first = calc.evaluate()
        second = calc.evaluate()
        assert first == "4"
        assert second == "4"

    def test_operator_replacement_chain(self, calc):
        calc.add_digit("8")
        calc.add_operator("+")
        calc.add_operator("*")
        calc.add_operator("/")
        assert calc.get_display() == "8/"

    def test_complex_expression(self, calc):
        # 2+3*4 = 14 (operator precedence)
        for ch in "2+3*4":
            if ch.isdigit():
                calc.add_digit(ch)
            else:
                calc.add_operator(ch)
        assert calc.evaluate() == "14"

    def test_decimal_result_no_trailing_zeros(self, calc):
        # 1/4 = 0.25, not 0.2500000000
        calc.add_digit("1")
        calc.add_operator("/")
        calc.add_digit("4")
        assert calc.evaluate() == "0.25"
