"""Tests for CalculatorLogic — business logic only, no GUI."""

import pytest

from calculator_logic import CalculatorLogic


@pytest.fixture
def calc() -> CalculatorLogic:
    """Provide a fresh calculator instance for each test."""
    return CalculatorLogic()


# --- Digit Input ---


class TestDigitInput:
    def test_single_digit(self, calc: CalculatorLogic) -> None:
        assert calc.input_digit("5") == "5"

    def test_multi_digit(self, calc: CalculatorLogic) -> None:
        calc.input_digit("1")
        calc.input_digit("2")
        assert calc.input_digit("3") == "123"

    def test_leading_zero_replaced(self, calc: CalculatorLogic) -> None:
        assert calc.input_digit("0") == "0"
        assert calc.input_digit("5") == "5"

    def test_zero_stays_zero(self, calc: CalculatorLogic) -> None:
        assert calc.input_digit("0") == "0"

    def test_digit_after_result_starts_fresh(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.input_equals()
        assert calc.input_digit("9") == "9"


# --- Decimal Input ---


class TestDecimalInput:
    def test_basic_decimal(self, calc: CalculatorLogic) -> None:
        calc.input_digit("3")
        calc.input_decimal()
        assert calc.input_digit("5") == "3.5"

    def test_leading_decimal(self, calc: CalculatorLogic) -> None:
        assert calc.input_decimal() == "0."
        assert calc.input_digit("5") == "0.5"

    def test_multiple_decimals_ignored(self, calc: CalculatorLogic) -> None:
        calc.input_digit("3")
        calc.input_decimal()
        calc.input_decimal()  # Should be ignored
        assert calc.input_digit("5") == "3.5"

    def test_decimal_after_result(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.input_equals()
        assert calc.input_decimal() == "0."


# --- Arithmetic Operations ---


class TestArithmetic:
    @pytest.mark.parametrize(
        "a, op, b, expected",
        [
            ("5", "+", "3", "8"),
            ("10", "-", "3", "7"),
            ("4", "*", "3", "12"),
            ("10", "/", "4", "2.5"),
            ("10", "/", "2", "5"),
            ("3", "-", "5", "-2"),
            ("0", "+", "0", "0"),
            ("5", "*", "0", "0"),
        ],
    )
    def test_basic_operations(
        self, calc: CalculatorLogic, a: str, op: str, b: str, expected: str
    ) -> None:
        for digit in a:
            calc.input_digit(digit)
        calc.input_operator(op)
        for digit in b:
            calc.input_digit(digit)
        assert calc.input_equals() == expected

    def test_float_operands(self, calc: CalculatorLogic) -> None:
        calc.input_digit("2")
        calc.input_decimal()
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_digit("1")
        calc.input_decimal()
        calc.input_digit("5")
        assert calc.input_equals() == "4"


# --- Clear ---


class TestClear:
    def test_clear_resets_display(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_digit("3")
        assert calc.input_clear() == "0"

    def test_clear_after_result(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.input_equals()
        assert calc.input_clear() == "0"

    def test_clear_resets_all_state(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.input_equals()
        calc.input_clear()
        # After clear, a new calculation should work fresh
        calc.input_digit("2")
        calc.input_operator("*")
        calc.input_digit("4")
        assert calc.input_equals() == "8"


# --- Backspace ---


class TestBackspace:
    def test_backspace_removes_digit(self, calc: CalculatorLogic) -> None:
        calc.input_digit("1")
        calc.input_digit("2")
        assert calc.input_backspace() == "1"

    def test_backspace_to_zero(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        assert calc.input_backspace() == "0"

    def test_backspace_on_zero(self, calc: CalculatorLogic) -> None:
        assert calc.input_backspace() == "0"

    def test_backspace_after_result_no_change(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.input_equals()
        assert calc.input_backspace() == "8"  # No change on result


# --- Chained Operations ---


class TestChainedOperations:
    def test_chained_add_multiply(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_digit("3")
        result = calc.input_operator("*")
        assert result == "8"  # Intermediate result
        calc.input_digit("2")
        assert calc.input_equals() == "16"

    def test_operator_after_result(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_digit("3")
        calc.input_equals()
        calc.input_operator("+")
        calc.input_digit("2")
        assert calc.input_equals() == "10"


# --- Repeated Equals ---


class TestRepeatedEquals:
    def test_repeated_equals(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_digit("3")
        assert calc.input_equals() == "8"
        assert calc.input_equals() == "11"
        assert calc.input_equals() == "14"

    def test_repeated_equals_multiply(self, calc: CalculatorLogic) -> None:
        calc.input_digit("2")
        calc.input_operator("*")
        calc.input_digit("3")
        assert calc.input_equals() == "6"
        assert calc.input_equals() == "18"


# --- Operator Replacement ---


class TestOperatorReplacement:
    def test_replace_operator(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_operator("-")  # Replace + with -
        calc.input_digit("3")
        assert calc.input_equals() == "2"


# --- Error Handling ---


class TestErrorHandling:
    def test_division_by_zero(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("/")
        calc.input_digit("0")
        assert calc.input_equals() == "Error"

    def test_clear_after_error(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("/")
        calc.input_digit("0")
        calc.input_equals()
        assert calc.input_clear() == "0"

    def test_digit_after_error(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("/")
        calc.input_digit("0")
        calc.input_equals()
        assert calc.input_digit("3") == "3"

    def test_operator_after_error(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("/")
        calc.input_digit("0")
        calc.input_equals()
        calc.input_operator("+")
        assert calc.get_display() == "0"

    def test_decimal_after_error(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("/")
        calc.input_digit("0")
        calc.input_equals()
        assert calc.input_decimal() == "0."

    def test_backspace_after_error(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("/")
        calc.input_digit("0")
        calc.input_equals()
        assert calc.input_backspace() == "0"

    def test_equals_after_error(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("/")
        calc.input_digit("0")
        calc.input_equals()
        assert calc.input_equals() == "0"

    def test_chained_division_by_zero(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        calc.input_operator("+")
        calc.input_digit("0")
        # Chaining: 5+0=5, then /0
        calc.input_operator("/")
        calc.input_digit("0")
        assert calc.input_equals() == "Error"


# --- Boundary Conditions ---


class TestBoundaryConditions:
    def test_large_numbers(self, calc: CalculatorLogic) -> None:
        for d in "99999999":
            calc.input_digit(d)
        calc.input_operator("*")
        for d in "99999999":
            calc.input_digit(d)
        # Float arithmetic: 99999999^2 = 9999999800000001, but float precision
        # rounds to 9999999800000000. This is expected calculator behavior.
        assert calc.input_equals() == "9999999800000000"

    def test_small_decimals(self, calc: CalculatorLogic) -> None:
        # 0.0001 + 0.0002 = 0.0003
        calc.input_digit("0")
        calc.input_decimal()
        for d in "0001":
            calc.input_digit(d)
        calc.input_operator("+")
        calc.input_digit("0")
        calc.input_decimal()
        for d in "0002":
            calc.input_digit(d)
        assert calc.input_equals() == "0.0003"

    def test_equals_with_no_operation(self, calc: CalculatorLogic) -> None:
        calc.input_digit("5")
        assert calc.input_equals() == "5"


# --- get_display ---


class TestGetDisplay:
    def test_initial_display(self, calc: CalculatorLogic) -> None:
        assert calc.get_display() == "0"

    def test_display_after_digit(self, calc: CalculatorLogic) -> None:
        calc.input_digit("7")
        assert calc.get_display() == "7"
