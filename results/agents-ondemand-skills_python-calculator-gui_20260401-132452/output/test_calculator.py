"""Comprehensive tests for CalculatorLogic."""

import pytest
from calculator_logic import CalculatorLogic


@pytest.fixture
def calc():
    """Return a fresh CalculatorLogic instance."""
    return CalculatorLogic()


# ---------------------------------------------------------------------------
# Happy Path - Basic Arithmetic
# ---------------------------------------------------------------------------

class TestBasicArithmetic:
    """Basic arithmetic operations on the calculator."""

    def test_addition(self, calc):
        calc.append_digit("2")
        calc.append_operator("+")
        calc.append_digit("3")
        assert calc.evaluate() == "5"

    def test_subtraction(self, calc):
        calc.append_digit("9")
        calc.append_operator("-")
        calc.append_digit("4")
        assert calc.evaluate() == "5"

    def test_multiplication(self, calc):
        calc.append_digit("3")
        calc.append_operator("*")
        calc.append_digit("7")
        assert calc.evaluate() == "21"

    def test_division(self, calc):
        calc.append_digit("8")
        calc.append_operator("/")
        calc.append_digit("2")
        assert calc.evaluate() == "4"

    def test_multi_digit(self, calc):
        calc.append_digit("1")
        calc.append_digit("2")
        calc.append_operator("+")
        calc.append_digit("3")
        calc.append_digit("4")
        assert calc.evaluate() == "46"

    def test_division_producing_decimal(self, calc):
        calc.append_digit("7")
        calc.append_operator("/")
        calc.append_digit("2")
        assert calc.evaluate() == "3.5"

    def test_get_display_reflects_current_entry(self, calc):
        assert calc.get_display() == "0"
        calc.append_digit("5")
        assert calc.get_display() == "5"
        calc.append_operator("+")
        assert calc.get_display() == "5+"
        calc.append_digit("3")
        assert calc.get_display() == "5+3"


# ---------------------------------------------------------------------------
# Chained Operations
# ---------------------------------------------------------------------------

class TestChainedOperations:
    """Operations that chain multiple operators before evaluating."""

    def test_chained_addition(self, calc):
        # 1+2+3=6
        calc.append_digit("1")
        calc.append_operator("+")
        calc.append_digit("2")
        calc.append_operator("+")
        calc.append_digit("3")
        assert calc.evaluate() == "6"

    def test_evaluate_then_continue(self, calc):
        # 2+3= (5), then +1= (6)
        calc.append_digit("2")
        calc.append_operator("+")
        calc.append_digit("3")
        assert calc.evaluate() == "5"
        calc.append_operator("+")
        calc.append_digit("1")
        assert calc.evaluate() == "6"


# ---------------------------------------------------------------------------
# Decimal Numbers
# ---------------------------------------------------------------------------

class TestDecimalNumbers:
    """Decimal entry and arithmetic."""

    def test_simple_decimal_entry(self, calc):
        calc.append_digit("1")
        calc.append_decimal()
        calc.append_digit("5")
        assert calc.get_display() == "1.5"

    def test_decimal_arithmetic(self, calc):
        calc.append_digit("1")
        calc.append_decimal()
        calc.append_digit("5")
        calc.append_operator("+")
        calc.append_digit("2")
        calc.append_decimal()
        calc.append_digit("5")
        assert calc.evaluate() == "4"

    def test_leading_decimal_becomes_zero_dot(self, calc):
        # Pressing '.' first should give "0."
        calc.append_decimal()
        calc.append_digit("5")
        assert calc.get_display() == "0.5"

    def test_multiple_decimal_points_ignored(self, calc):
        # 1.2.3 should become 1.23 (second dot ignored)
        calc.append_digit("1")
        calc.append_decimal()
        calc.append_digit("2")
        calc.append_decimal()  # ignored
        calc.append_digit("3")
        assert calc.get_display() == "1.23"


# ---------------------------------------------------------------------------
# Error Cases
# ---------------------------------------------------------------------------

class TestErrorCases:
    """Division by zero and error state management."""

    def test_division_by_zero_shows_error(self, calc):
        calc.append_digit("5")
        calc.append_operator("/")
        calc.append_digit("0")
        result = calc.evaluate()
        assert result == "Error"

    def test_has_error_true_after_division_by_zero(self, calc):
        calc.append_digit("5")
        calc.append_operator("/")
        calc.append_digit("0")
        calc.evaluate()
        assert calc.has_error() is True

    def test_has_error_false_on_success(self, calc):
        calc.append_digit("2")
        calc.append_operator("+")
        calc.append_digit("3")
        calc.evaluate()
        assert calc.has_error() is False

    def test_auto_recovery_after_error(self, calc):
        # After error, pressing a digit starts fresh
        calc.append_digit("5")
        calc.append_operator("/")
        calc.append_digit("0")
        calc.evaluate()
        assert calc.has_error() is True
        calc.append_digit("7")
        assert calc.has_error() is False
        assert calc.get_display() == "7"

    def test_clear_after_error_recovers(self, calc):
        calc.append_digit("5")
        calc.append_operator("/")
        calc.append_digit("0")
        calc.evaluate()
        assert calc.has_error() is True
        calc.clear()
        assert calc.has_error() is False
        assert calc.get_display() == "0"


# ---------------------------------------------------------------------------
# Consecutive Operators (last wins)
# ---------------------------------------------------------------------------

class TestConsecutiveOperators:
    """When multiple operators are pressed, the last one should win."""

    def test_two_operators_last_wins(self, calc):
        # 5+-3= should behave as 5-3=2
        calc.append_digit("5")
        calc.append_operator("+")
        calc.append_operator("-")
        calc.append_digit("3")
        assert calc.evaluate() == "2"

    def test_triple_operator_replacement(self, calc):
        # 4+*-1= should behave as 4-1=3
        calc.append_digit("4")
        calc.append_operator("+")
        calc.append_operator("*")
        calc.append_operator("-")
        calc.append_digit("1")
        assert calc.evaluate() == "3"


# ---------------------------------------------------------------------------
# Clear Behavior
# ---------------------------------------------------------------------------

class TestClearBehavior:
    """Clear resets the calculator state."""

    def test_clear_returns_zero(self, calc):
        assert calc.clear() == "0"

    def test_clear_mid_expression(self, calc):
        calc.append_digit("5")
        calc.append_operator("+")
        calc.append_digit("3")
        calc.clear()
        assert calc.get_display() == "0"

    def test_clear_then_new_expression(self, calc):
        calc.append_digit("5")
        calc.append_operator("+")
        calc.clear()
        calc.append_digit("2")
        calc.append_operator("*")
        calc.append_digit("3")
        assert calc.evaluate() == "6"


# ---------------------------------------------------------------------------
# Boundary Conditions
# ---------------------------------------------------------------------------

class TestBoundaryConditions:
    """Edge cases and boundary conditions."""

    def test_large_numbers(self, calc):
        for d in "999999999":
            calc.append_digit(d)
        calc.append_operator("+")
        calc.append_digit("1")
        assert calc.evaluate() == "1000000000"

    def test_empty_expression_evaluate(self, calc):
        # Evaluating with nothing entered should not crash
        result = calc.evaluate()
        assert result == "0"

    def test_integer_results_no_decimal_suffix(self, calc):
        # 4/2 = 2, not 2.0
        calc.append_digit("4")
        calc.append_operator("/")
        calc.append_digit("2")
        assert calc.evaluate() == "2"

    def test_initial_display_is_zero(self, calc):
        assert calc.get_display() == "0"

    def test_just_evaluated_flag_digit_starts_fresh(self, calc):
        # After evaluation, typing a new digit replaces the result
        calc.append_digit("3")
        calc.append_operator("+")
        calc.append_digit("4")
        calc.evaluate()
        calc.append_digit("9")
        assert calc.get_display() == "9"
