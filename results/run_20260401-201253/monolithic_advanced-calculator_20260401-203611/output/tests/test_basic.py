"""Tests for Basic mode calculator logic."""

import pytest

from calculator.logic.basic_logic import BasicCalculator


def _drive(calc: BasicCalculator, sequence: list[str]) -> str:
    """Drive a sequence of button actions and return display."""
    for action in sequence:
        if action.isdigit():
            calc.input_digit(action)
        elif action == ".":
            calc.input_decimal()
        elif action in ("+", "-", "*", "/"):
            calc.input_operator(action)
        elif action == "=":
            calc.input_equals()
        elif action == "C":
            calc.input_clear()
        elif action == "AC":
            calc.input_all_clear()
        elif action == "BS":
            calc.input_backspace()
        elif action == "%":
            calc.input_percent()
        elif action == "+/-":
            calc.input_negate()
    return calc.get_display()


class TestArithmeticHappyPath:
    """Happy path arithmetic tests."""

    @pytest.mark.parametrize("a,op,b,expected", [
        ("2", "+", "3", "5"),
        ("10", "-", "3", "7"),
        ("4", "*", "5", "20"),
        ("10", "/", "4", "2.5"),
        ("0", "+", "0", "0"),
        ("100", "/", "10", "10"),
    ])
    def test_simple_arithmetic(
        self, a: str, op: str, b: str, expected: str
    ) -> None:
        calc = BasicCalculator()
        result = _drive(calc, list(a) + [op] + list(b) + ["="])
        assert result == expected

    def test_chained_addition(self) -> None:
        calc = BasicCalculator()
        result = _drive(calc, ["1", "+", "2", "+", "3", "="])
        assert result == "6"

    def test_operator_precedence_mul_before_add(self) -> None:
        calc = BasicCalculator()
        # 2 + 3 * 4 = 14
        result = _drive(
            calc, ["2", "+", "3", "*", "4", "="]
        )
        assert result == "14"

    def test_operator_precedence_complex(self) -> None:
        calc = BasicCalculator()
        # 2 * 3 + 4 * 5 = 26
        result = _drive(
            calc,
            ["2", "*", "3", "+", "4", "*", "5", "="],
        )
        assert result == "26"

    def test_subtraction_negative_result(self) -> None:
        calc = BasicCalculator()
        result = _drive(calc, ["3", "-", "5", "="])
        assert result == "-2"


class TestNumericInput:
    """Numeric input handling tests."""

    def test_leading_zeros(self) -> None:
        calc = BasicCalculator()
        result = _drive(calc, ["0", "0", "7"])
        assert result == "7"

    def test_double_decimal(self) -> None:
        calc = BasicCalculator()
        calc.input_decimal()
        calc.input_decimal()
        calc.input_digit("5")
        assert calc.get_display() == "0.5"

    def test_negate_positive(self) -> None:
        calc = BasicCalculator()
        result = _drive(calc, ["5", "+/-"])
        assert result == "-5"

    def test_negate_double(self) -> None:
        calc = BasicCalculator()
        result = _drive(calc, ["5", "+/-", "+/-"])
        assert result == "5"

    def test_percent(self) -> None:
        calc = BasicCalculator()
        result = _drive(calc, ["2", "0", "0", "%"])
        assert result == "2"

    def test_decimal_number(self) -> None:
        calc = BasicCalculator()
        result = _drive(calc, ["3", ".", "1", "4"])
        assert result == "3.14"


class TestDisplayFormatting:
    """Display formatting tests."""

    def test_integer_result_no_decimal(self) -> None:
        calc = BasicCalculator()
        result = _drive(calc, ["4", "/", "2", "="])
        assert result == "2"
        assert "." not in result

    def test_float_result_precision(self) -> None:
        calc = BasicCalculator()
        result = _drive(calc, ["1", "/", "3", "="])
        assert result.startswith("0.333333333")

    def test_negative_display(self) -> None:
        calc = BasicCalculator()
        result = _drive(calc, ["0", "-", "5", "="])
        assert result == "-5"


class TestClearAndEdit:
    """Clear and edit function tests."""

    def test_clear_entry(self) -> None:
        calc = BasicCalculator()
        # 5 + 3, clear, 2 = should give 7 (5 + 2)
        result = _drive(
            calc, ["5", "+", "3", "C", "2", "="]
        )
        assert result == "7"

    def test_all_clear(self) -> None:
        calc = BasicCalculator()
        # 5 + 3, AC, 2 = should give 2
        result = _drive(
            calc, ["5", "+", "3", "AC", "2", "="]
        )
        assert result == "2"

    def test_backspace(self) -> None:
        calc = BasicCalculator()
        result = _drive(calc, ["1", "2", "3", "BS"])
        assert result == "12"

    def test_backspace_to_zero(self) -> None:
        calc = BasicCalculator()
        result = _drive(calc, ["5", "BS"])
        assert result == "0"


class TestErrorCases:
    """Error condition tests."""

    def test_division_by_zero(self) -> None:
        calc = BasicCalculator()
        _drive(calc, ["1", "0", "0", "/", "0", "="])
        assert calc.is_error()
        assert calc.get_display() == "Error"

    def test_error_recovery_digit(self) -> None:
        calc = BasicCalculator()
        _drive(calc, ["1", "/", "0", "="])
        assert calc.is_error()
        calc.input_digit("5")
        assert not calc.is_error()
        assert calc.get_display() == "5"

    def test_error_recovery_clear(self) -> None:
        calc = BasicCalculator()
        _drive(calc, ["1", "/", "0", "="])
        assert calc.is_error()
        calc.input_clear()
        assert not calc.is_error()
        assert calc.get_display() == "0"

    def test_error_recovery_all_clear(self) -> None:
        calc = BasicCalculator()
        _drive(calc, ["1", "/", "0", "="])
        assert calc.is_error()
        calc.input_all_clear()
        assert not calc.is_error()
        assert calc.get_display() == "0"


class TestValueAccess:
    """Value get/set tests for mode switching."""

    def test_get_value(self) -> None:
        calc = BasicCalculator()
        _drive(calc, ["3", ".", "1", "4"])
        assert abs(calc.get_value() - 3.14) < 0.001

    def test_set_value(self) -> None:
        calc = BasicCalculator()
        calc.set_value(42.5)
        assert calc.get_display() == "42.5"

    def test_set_value_integer(self) -> None:
        calc = BasicCalculator()
        calc.set_value(100.0)
        assert calc.get_display() == "100"
