"""Tests for calculator business logic."""

import pytest

from calculator_logic import CalculatorLogic, format_result, safe_eval


class TestSafeEval:
    """Tests for the safe_eval function."""

    def test_simple_addition(self) -> None:
        assert safe_eval("2+3") == 5

    def test_simple_subtraction(self) -> None:
        assert safe_eval("10-4") == 6

    def test_simple_multiplication(self) -> None:
        assert safe_eval("3*7") == 21

    def test_simple_division(self) -> None:
        assert safe_eval("8/2") == 4.0

    def test_operator_precedence(self) -> None:
        assert safe_eval("2+3*4") == 14

    def test_parentheses(self) -> None:
        assert safe_eval("(2+3)*4") == 20

    def test_negative_number(self) -> None:
        assert safe_eval("-5") == -5

    def test_decimal_numbers(self) -> None:
        assert safe_eval("1.5+2.5") == 4.0

    def test_division_by_zero(self) -> None:
        with pytest.raises(ZeroDivisionError):
            safe_eval("5/0")

    def test_empty_expression(self) -> None:
        with pytest.raises(ValueError):
            safe_eval("")

    def test_whitespace_only(self) -> None:
        with pytest.raises(ValueError):
            safe_eval("   ")

    def test_rejects_function_calls(self) -> None:
        with pytest.raises((ValueError, SyntaxError)):
            safe_eval("__import__('os').system('ls')")

    def test_rejects_names(self) -> None:
        with pytest.raises(ValueError):
            safe_eval("x + 1")

    def test_large_numbers(self) -> None:
        result = safe_eval("100000*100000")
        assert result == 10000000000


class TestFormatResult:
    """Tests for the format_result function."""

    def test_integer(self) -> None:
        assert format_result(5) == "5"

    def test_float_whole_number(self) -> None:
        assert format_result(4.0) == "4"

    def test_float_with_decimals(self) -> None:
        assert format_result(3.14) == "3.14"

    def test_zero(self) -> None:
        assert format_result(0) == "0"

    def test_negative_integer(self) -> None:
        assert format_result(-7) == "-7"

    def test_negative_float(self) -> None:
        assert format_result(-3.5) == "-3.5"


class TestCalculatorLogicBasicOps:
    """Tests for basic arithmetic operations via CalculatorLogic."""

    def test_addition(self) -> None:
        calc = CalculatorLogic()
        calc.add_character("2")
        calc.add_character("+")
        calc.add_character("3")
        assert calc.evaluate() == "5"

    def test_subtraction(self) -> None:
        calc = CalculatorLogic()
        calc.add_character("1")
        calc.add_character("0")
        calc.add_character("-")
        calc.add_character("4")
        assert calc.evaluate() == "6"

    def test_multiplication(self) -> None:
        calc = CalculatorLogic()
        calc.add_character("3")
        calc.add_character("*")
        calc.add_character("7")
        assert calc.evaluate() == "21"

    def test_division(self) -> None:
        calc = CalculatorLogic()
        calc.add_character("8")
        calc.add_character("/")
        calc.add_character("2")
        assert calc.evaluate() == "4"

    def test_operator_precedence(self) -> None:
        calc = CalculatorLogic()
        for char in "2+3*4":
            calc.add_character(char)
        assert calc.evaluate() == "14"

    def test_decimal_addition(self) -> None:
        calc = CalculatorLogic()
        for char in "1.5+2.5":
            calc.add_character(char)
        assert calc.evaluate() == "4"

    def test_small_decimal_addition(self) -> None:
        calc = CalculatorLogic()
        for char in "0.1+0.2":
            calc.add_character(char)
        result = calc.evaluate()
        assert float(result) == pytest.approx(0.3, abs=1e-10)


class TestCalculatorLogicDisplay:
    """Tests for display behavior."""

    def test_initial_display(self) -> None:
        calc = CalculatorLogic()
        assert calc.display_text == "0"

    def test_single_digit(self) -> None:
        calc = CalculatorLogic()
        calc.add_character("5")
        assert calc.display_text == "5"

    def test_multi_digit(self) -> None:
        calc = CalculatorLogic()
        for char in "123":
            calc.add_character(char)
        assert calc.display_text == "123"

    def test_expression_building(self) -> None:
        calc = CalculatorLogic()
        for char in "5+3":
            calc.add_character(char)
        assert calc.display_text == "5+3"


class TestCalculatorLogicEdgeCases:
    """Tests for edge cases."""

    def test_division_by_zero(self) -> None:
        calc = CalculatorLogic()
        for char in "5/0":
            calc.add_character(char)
        assert calc.evaluate() == "Error"

    def test_multiple_decimals_in_number(self) -> None:
        calc = CalculatorLogic()
        calc.add_character("3")
        calc.add_character(".")
        calc.add_character("2")
        calc.add_character(".")
        calc.add_character("1")
        assert calc.display_text == "3.21"

    def test_leading_minus(self) -> None:
        calc = CalculatorLogic()
        calc.add_character("-")
        calc.add_character("5")
        assert calc.evaluate() == "-5"

    def test_leading_plus_ignored(self) -> None:
        calc = CalculatorLogic()
        calc.add_character("+")
        assert calc.display_text == "0"

    def test_evaluate_empty(self) -> None:
        calc = CalculatorLogic()
        assert calc.evaluate() == "0"

    def test_consecutive_operators_replaced(self) -> None:
        calc = CalculatorLogic()
        calc.add_character("5")
        calc.add_character("+")
        calc.add_character("+")
        calc.add_character("3")
        assert calc.evaluate() == "8"

    def test_consecutive_operators_different(self) -> None:
        calc = CalculatorLogic()
        calc.add_character("5")
        calc.add_character("+")
        calc.add_character("-")
        calc.add_character("3")
        assert calc.evaluate() == "2"

    def test_trailing_operator(self) -> None:
        calc = CalculatorLogic()
        calc.add_character("5")
        calc.add_character("+")
        result = calc.evaluate()
        assert result == "5"

    def test_large_numbers(self) -> None:
        calc = CalculatorLogic()
        for char in "100000*100000":
            calc.add_character(char)
        assert calc.evaluate() == "10000000000"

    def test_small_decimals(self) -> None:
        calc = CalculatorLogic()
        for char in "0.001+0.002":
            calc.add_character(char)
        assert calc.evaluate() == "0.003"

    def test_decimal_after_operator(self) -> None:
        calc = CalculatorLogic()
        for char in "5+":
            calc.add_character(char)
        calc.add_character(".")
        calc.add_character("5")
        assert calc.display_text == "5+0.5"


class TestCalculatorLogicErrorCases:
    """Tests for error handling."""

    def test_division_by_zero_shows_error(self) -> None:
        calc = CalculatorLogic()
        for char in "5/0":
            calc.add_character(char)
        assert calc.evaluate() == "Error"

    def test_invalid_expression(self) -> None:
        calc = CalculatorLogic()
        calc.add_character("*")
        calc.add_character("*")
        assert calc.evaluate() in ("Error", "0")

    def test_recovery_after_error(self) -> None:
        calc = CalculatorLogic()
        for char in "5/0":
            calc.add_character(char)
        calc.evaluate()
        calc.add_character("3")
        assert calc.display_text == "3"


class TestCalculatorLogicStateManagement:
    """Tests for state transitions."""

    def test_clear_after_evaluation(self) -> None:
        calc = CalculatorLogic()
        for char in "2+3":
            calc.add_character(char)
        calc.evaluate()
        assert calc.clear() == "0"

    def test_chain_with_operator(self) -> None:
        calc = CalculatorLogic()
        for char in "2+3":
            calc.add_character(char)
        calc.evaluate()  # "5"
        calc.add_character("+")
        calc.add_character("4")
        assert calc.evaluate() == "9"

    def test_new_digit_after_eval(self) -> None:
        calc = CalculatorLogic()
        for char in "2+3":
            calc.add_character(char)
        calc.evaluate()  # "5"
        calc.add_character("7")
        assert calc.display_text == "7"

    def test_backspace_removes_last(self) -> None:
        calc = CalculatorLogic()
        for char in "123":
            calc.add_character(char)
        calc.backspace()
        assert calc.display_text == "12"

    def test_backspace_to_empty(self) -> None:
        calc = CalculatorLogic()
        calc.add_character("5")
        calc.backspace()
        assert calc.display_text == "0"

    def test_backspace_after_eval_clears(self) -> None:
        calc = CalculatorLogic()
        for char in "2+3":
            calc.add_character(char)
        calc.evaluate()
        calc.backspace()
        assert calc.display_text == "0"

    def test_clear_resets_completely(self) -> None:
        calc = CalculatorLogic()
        for char in "2+3":
            calc.add_character(char)
        calc.clear()
        assert calc.display_text == "0"
        calc.add_character("5")
        assert calc.display_text == "5"


class TestCalculatorLogicBoundary:
    """Tests for boundary conditions."""

    def test_repeating_decimal(self) -> None:
        calc = CalculatorLogic()
        for char in "1/3":
            calc.add_character(char)
        result = calc.evaluate()
        assert float(result) == pytest.approx(1 / 3, rel=1e-4)

    def test_zero_plus_zero(self) -> None:
        calc = CalculatorLogic()
        for char in "0+0":
            calc.add_character(char)
        assert calc.evaluate() == "0"

    def test_parentheses(self) -> None:
        calc = CalculatorLogic()
        for char in "(2+3)*4":
            calc.add_character(char)
        assert calc.evaluate() == "20"

    def test_multiple_operations(self) -> None:
        calc = CalculatorLogic()
        for char in "1+2+3+4":
            calc.add_character(char)
        assert calc.evaluate() == "10"

    def test_decimal_after_eval(self) -> None:
        calc = CalculatorLogic()
        for char in "2+3":
            calc.add_character(char)
        calc.evaluate()  # "5"
        calc.add_character(".")
        calc.add_character("5")
        assert calc.display_text == "0.5"
