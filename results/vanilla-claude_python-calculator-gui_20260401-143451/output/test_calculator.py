"""Tests for CalculatorLogic — no GUI dependencies."""

import pytest

from calculator_logic import CalculatorLogic


@pytest.fixture
def calc():
    return CalculatorLogic()


# --- Happy Path: Basic Operations ---


class TestBasicOperations:
    def test_single_digit(self, calc):
        calc.append_digit("1")
        assert calc.get_expression() == "1"
        assert calc.get_result() == "0"

    def test_multi_digit(self, calc):
        for d in "123":
            calc.append_digit(d)
        assert calc.get_expression() == "123"

    def test_addition(self, calc):
        calc.append_digit("5")
        calc.append_operator("+")
        calc.append_digit("3")
        calc.evaluate()
        assert calc.get_result() == "8"
        assert calc.get_expression() == "5+3="

    def test_subtraction(self, calc):
        calc.append_digit("9")
        calc.append_operator("-")
        calc.append_digit("4")
        calc.evaluate()
        assert calc.get_result() == "5"

    def test_multiplication(self, calc):
        calc.append_digit("6")
        calc.append_operator("*")
        calc.append_digit("7")
        calc.evaluate()
        assert calc.get_result() == "42"

    def test_division(self, calc):
        calc.append_digit("8")
        calc.append_operator("/")
        calc.append_digit("2")
        calc.evaluate()
        assert calc.get_result() == "4"

    def test_chained_operations(self, calc):
        # 2 + 3 * 4 = 14 (standard precedence)
        calc.append_digit("2")
        calc.append_operator("+")
        calc.append_digit("3")
        calc.append_operator("*")
        calc.append_digit("4")
        calc.evaluate()
        assert calc.get_result() == "14"

    def test_decimal_addition(self, calc):
        calc.append_digit("1")
        calc.append_decimal()
        calc.append_digit("5")
        calc.append_operator("+")
        calc.append_digit("2")
        calc.append_decimal()
        calc.append_digit("5")
        calc.evaluate()
        assert calc.get_result() == "4"

    def test_clear(self, calc):
        calc.append_digit("5")
        calc.append_operator("+")
        calc.append_digit("3")
        calc.clear()
        assert calc.get_expression() == ""
        assert calc.get_result() == "0"


# --- Edge Cases ---


class TestEdgeCases:
    def test_multiple_decimals_ignored(self, calc):
        calc.append_digit("1")
        calc.append_decimal()
        calc.append_decimal()  # should be ignored
        calc.append_digit("2")
        assert calc.get_expression() == "1.2"

    def test_consecutive_operators_replaced(self, calc):
        calc.append_digit("5")
        calc.append_operator("+")
        calc.append_operator("*")
        assert calc.get_expression() == "5*"

    def test_equals_empty_expression(self, calc):
        calc.evaluate()
        assert calc.get_expression() == ""
        assert calc.get_result() == "0"

    def test_continue_from_result_with_operator(self, calc):
        calc.append_digit("5")
        calc.append_operator("+")
        calc.append_digit("3")
        calc.evaluate()
        assert calc.get_result() == "8"
        calc.append_operator("*")
        calc.append_digit("2")
        calc.evaluate()
        assert calc.get_result() == "16"
        assert calc.get_expression() == "8*2="

    def test_new_number_after_result(self, calc):
        calc.append_digit("5")
        calc.append_operator("+")
        calc.append_digit("3")
        calc.evaluate()
        calc.append_digit("9")
        assert calc.get_expression() == "9"
        assert calc.get_result() == "0"

    def test_clear_after_error(self, calc):
        calc.append_digit("5")
        calc.append_operator("/")
        calc.append_digit("0")
        calc.evaluate()
        assert calc.get_result() == "Error"
        calc.clear()
        assert calc.get_expression() == ""
        assert calc.get_result() == "0"

    def test_digit_after_error(self, calc):
        calc.append_digit("5")
        calc.append_operator("/")
        calc.append_digit("0")
        calc.evaluate()
        assert calc.get_result() == "Error"
        calc.append_digit("3")
        assert calc.get_expression() == "3"
        assert calc.get_result() == "0"

    def test_operator_on_empty_expression(self, calc):
        calc.append_operator("+")
        assert calc.get_expression() == ""

    def test_multiple_equals(self, calc):
        calc.append_digit("3")
        calc.append_operator("+")
        calc.append_digit("2")
        calc.evaluate()
        assert calc.get_result() == "5"
        calc.evaluate()  # second equals does nothing
        assert calc.get_result() == "5"

    def test_decimal_at_start(self, calc):
        calc.append_decimal()
        calc.append_digit("5")
        assert calc.get_expression() == "0.5"

    def test_decimal_after_operator(self, calc):
        calc.append_digit("1")
        calc.append_operator("+")
        calc.append_decimal()
        calc.append_digit("5")
        assert calc.get_expression() == "1+0.5"

    def test_evaluate_trailing_operator(self, calc):
        calc.append_digit("5")
        calc.append_operator("+")
        calc.evaluate()
        # Should evaluate "5" (strip trailing operator)
        assert calc.get_result() == "5"


# --- Error Cases ---


class TestErrorCases:
    def test_division_by_zero(self, calc):
        calc.append_digit("5")
        calc.append_operator("/")
        calc.append_digit("0")
        calc.evaluate()
        assert calc.get_result() == "Error"

    def test_division_by_zero_decimal(self, calc):
        calc.append_digit("1")
        calc.append_operator("/")
        calc.append_digit("0")
        calc.append_decimal()
        calc.append_digit("0")
        calc.evaluate()
        assert calc.get_result() == "Error"


# --- Boundary Conditions ---


class TestBoundaryConditions:
    def test_large_numbers(self, calc):
        for _ in range(10):
            calc.append_digit("9")
        calc.append_operator("*")
        for _ in range(10):
            calc.append_digit("9")
        calc.evaluate()
        expected = str(9999999999 * 9999999999)
        assert calc.get_result() == expected

    def test_small_decimals(self, calc):
        # 0.001 + 0.002 = 0.003
        calc.append_digit("0")
        calc.append_decimal()
        calc.append_digit("0")
        calc.append_digit("0")
        calc.append_digit("1")
        calc.append_operator("+")
        calc.append_digit("0")
        calc.append_decimal()
        calc.append_digit("0")
        calc.append_digit("0")
        calc.append_digit("2")
        calc.evaluate()
        assert calc.get_result() == "0.003"

    def test_whole_number_formatting(self, calc):
        # 4.0 + 1.0 = 5 (not 5.0)
        calc.append_digit("4")
        calc.append_decimal()
        calc.append_digit("0")
        calc.append_operator("+")
        calc.append_digit("1")
        calc.append_decimal()
        calc.append_digit("0")
        calc.evaluate()
        assert calc.get_result() == "5"

    def test_decimal_result_formatting(self, calc):
        # 7 / 2 = 3.5
        calc.append_digit("7")
        calc.append_operator("/")
        calc.append_digit("2")
        calc.evaluate()
        assert calc.get_result() == "3.5"


# --- Result Continuation ---


class TestResultContinuation:
    def test_operator_after_result(self, calc):
        # 3 + 2 = 5, then + 1 = 6
        calc.append_digit("3")
        calc.append_operator("+")
        calc.append_digit("2")
        calc.evaluate()
        assert calc.get_result() == "5"
        calc.append_operator("+")
        calc.append_digit("1")
        calc.evaluate()
        assert calc.get_result() == "6"
        assert calc.get_expression() == "5+1="

    def test_digit_after_result_starts_fresh(self, calc):
        calc.append_digit("3")
        calc.append_operator("+")
        calc.append_digit("2")
        calc.evaluate()
        calc.append_digit("7")
        assert calc.get_expression() == "7"
        assert calc.get_result() == "0"

    def test_decimal_after_result_starts_fresh(self, calc):
        calc.append_digit("3")
        calc.append_operator("+")
        calc.append_digit("2")
        calc.evaluate()
        calc.append_decimal()
        assert calc.get_expression() == "0."
        assert calc.get_result() == "0"


# --- Invalid operator ---


class TestInvalidInput:
    def test_invalid_operator_ignored(self, calc):
        calc.append_digit("5")
        calc.append_operator("^")
        assert calc.get_expression() == "5"
