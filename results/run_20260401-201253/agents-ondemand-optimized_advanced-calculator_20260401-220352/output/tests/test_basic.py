"""Tests for Basic calculator mode: arithmetic, input, display, clear, error recovery."""

import pytest
from calculator.logic.basic_logic import BasicCalculator
from calculator.logic.base_logic import CalculatorError, ExpressionParser


# --- Helpers ---

def enter_number(calc, number_str):
    """Enter a multi-digit number into the calculator."""
    for ch in str(number_str):
        if ch == ".":
            calc.append_decimal()
        elif ch == "-":
            pass  # handled via toggle_sign
        else:
            calc.append_digit(ch)


@pytest.fixture
def calc():
    return BasicCalculator()


# =============================================================================
# Arithmetic Operations
# =============================================================================

class TestBasicArithmetic:

    @pytest.mark.parametrize("a, op, b, expected", [
        (2, "+", 3, 5),
        (0, "+", 0, 0),
        (10, "-", 3, 7),
        (3, "-", 10, -7),
        (6, "*", 7, 42),
        (0, "*", 999, 0),
        (10, "/", 4, 2.5),
        (10, "/", 5, 2),
    ])
    def test_binary_operation(self, calc, a, op, b, expected):
        enter_number(calc, a)
        calc.add_operator(op)
        enter_number(calc, b)
        result = calc.evaluate()
        assert result == pytest.approx(expected)

    def test_negative_plus_positive(self, calc):
        enter_number(calc, 5)
        val = calc.get_current_value()
        val = calc.toggle_sign(val)
        calc.current_input = str(int(val))
        calc.add_operator("+")
        enter_number(calc, 3)
        result = calc.evaluate()
        assert result == pytest.approx(-2)


class TestOperatorPrecedence:

    @pytest.mark.parametrize("digits_ops, expected", [
        # 2 + 3 * 4 = 14
        ([("2", None), (None, "+"), ("3", None), (None, "*"), ("4", None)], 14),
        # 2 * 3 + 4 = 10
        ([("2", None), (None, "*"), ("3", None), (None, "+"), ("4", None)], 10),
        # 10 - 2 * 3 = 4
        ([("10", None), (None, "-"), ("2", None), (None, "*"), ("3", None)], 4),
        # 10 / 2 + 3 = 8
        ([("10", None), (None, "/"), ("2", None), (None, "+"), ("3", None)], 8),
    ])
    def test_precedence(self, digits_ops, expected):
        calc = BasicCalculator()
        for num, op in digits_ops:
            if num is not None:
                enter_number(calc, num)
            if op is not None:
                calc.add_operator(op)
        result = calc.evaluate()
        assert result == pytest.approx(expected)

    def test_chained_addition(self):
        calc = BasicCalculator()
        enter_number(calc, 1)
        calc.add_operator("+")
        enter_number(calc, 2)
        calc.add_operator("+")
        enter_number(calc, 3)
        calc.add_operator("+")
        enter_number(calc, 4)
        result = calc.evaluate()
        assert result == pytest.approx(10)

    def test_chained_multiplication(self):
        calc = BasicCalculator()
        enter_number(calc, 2)
        calc.add_operator("*")
        enter_number(calc, 3)
        calc.add_operator("*")
        enter_number(calc, 4)
        result = calc.evaluate()
        assert result == pytest.approx(24)


class TestArithmeticErrors:

    def test_division_by_zero(self, calc):
        enter_number(calc, 100)
        calc.add_operator("/")
        enter_number(calc, 0)
        with pytest.raises(CalculatorError):
            calc.evaluate()

    def test_zero_divided_by_zero(self, calc):
        enter_number(calc, 0)
        calc.add_operator("/")
        enter_number(calc, 0)
        with pytest.raises(CalculatorError):
            calc.evaluate()


# =============================================================================
# Numeric Input
# =============================================================================

class TestNumericInput:

    def test_leading_zeros_007(self, calc):
        calc.append_digit("0")
        calc.append_digit("0")
        calc.append_digit("7")
        assert calc.current_input == "7"

    def test_leading_zeros_000(self, calc):
        calc.append_digit("0")
        calc.append_digit("0")
        calc.append_digit("0")
        assert calc.current_input == "0"

    def test_double_decimal(self, calc):
        calc.append_decimal()
        calc.append_decimal()
        calc.append_digit("5")
        assert calc.current_input == "0.5"

    def test_decimal_in_middle(self, calc):
        calc.append_digit("1")
        calc.append_decimal()
        calc.append_digit("2")
        calc.append_decimal()
        calc.append_digit("3")
        assert calc.current_input == "1.23"

    def test_sign_toggle_positive(self, calc):
        result = calc.toggle_sign(5.0)
        assert result == -5.0

    def test_sign_toggle_negative(self, calc):
        result = calc.toggle_sign(-5.0)
        assert result == 5.0

    def test_sign_toggle_zero(self, calc):
        result = calc.toggle_sign(0.0)
        assert result == 0.0 or result == -0.0

    def test_percentage_200(self, calc):
        result = calc.percentage(200.0)
        assert result == pytest.approx(2.0)

    def test_percentage_50(self, calc):
        result = calc.percentage(50.0)
        assert result == pytest.approx(0.5)


# =============================================================================
# Display Formatting
# =============================================================================

class TestDisplayFormatting:

    def test_integer_result_no_decimal(self, calc):
        enter_number(calc, 4)
        calc.add_operator("/")
        enter_number(calc, 2)
        result = calc.evaluate()
        formatted = calc.format_number(result)
        assert formatted == "2"
        assert "." not in formatted

    def test_float_5_displays_as_5(self, calc):
        formatted = calc.format_number(5.0)
        assert formatted == "5"

    def test_one_third_precision(self, calc):
        enter_number(calc, 1)
        calc.add_operator("/")
        enter_number(calc, 3)
        result = calc.evaluate()
        formatted = calc.format_number(result)
        assert formatted.startswith("0.333333333")

    def test_scientific_notation_large(self, calc):
        large = 9999999999.0 * 9999999999.0
        formatted = calc.format_number(large)
        assert "e" in formatted.lower() or "E" in formatted


# =============================================================================
# Clear and Edit
# =============================================================================

class TestClearAndEdit:

    def test_clear_entry(self, calc):
        """5 + 3, C, 2 = should give 7 (5+2)."""
        enter_number(calc, 5)
        calc.add_operator("+")
        enter_number(calc, 3)
        calc.clear_entry()
        enter_number(calc, 2)
        result = calc.evaluate()
        assert result == pytest.approx(7)

    def test_all_clear(self, calc):
        """5 + 3, AC, 2 = should give 2."""
        enter_number(calc, 5)
        calc.add_operator("+")
        enter_number(calc, 3)
        calc.all_clear()
        enter_number(calc, 2)
        result = calc.evaluate()
        assert result == pytest.approx(2)

    def test_backspace(self, calc):
        calc.append_digit("1")
        calc.append_digit("2")
        calc.append_digit("3")
        result = calc.backspace()
        assert result == "12"

    def test_backspace_single_digit(self, calc):
        calc.append_digit("5")
        result = calc.backspace()
        assert result == "0"


# =============================================================================
# Error Recovery
# =============================================================================

class TestErrorRecovery:

    def test_digit_clears_error(self, calc):
        enter_number(calc, 10)
        calc.add_operator("/")
        enter_number(calc, 0)
        with pytest.raises(CalculatorError):
            calc.evaluate()
        calc.error_state = True
        calc.append_digit("5")
        assert calc.error_state is False

    def test_clear_entry_clears_error(self, calc):
        calc.error_state = True
        calc.clear_entry()
        assert calc.error_state is False

    def test_all_clear_clears_error(self, calc):
        calc.error_state = True
        calc.all_clear()
        assert calc.error_state is False


# =============================================================================
# Expression Parser (direct unit tests)
# =============================================================================

class TestExpressionParser:

    @pytest.fixture
    def parser(self):
        return ExpressionParser()

    @pytest.mark.parametrize("tokens, expected", [
        ([2, "+", 3], 5),
        ([10, "-", 3], 7),
        ([6, "*", 7], 42),
        ([10, "/", 4], 2.5),
        ([2, "+", 3, "*", 4], 14),
        ([2, "*", 3, "+", 4], 10),
        ([10, "-", 2, "*", 3], 4),
        (["(", 2, "+", 3, ")", "*", 4], 20),
        ([2, "*", "(", 3, "+", 4, ")"], 14),
        (["(", "(", 2, "+", 3, ")", "*", "(", 4, "+", 1, ")", ")"], 25),
        ([42], 42),
    ])
    def test_parse_happy_path(self, parser, tokens, expected):
        result = parser.parse(tokens)
        assert result == pytest.approx(expected)

    def test_division_by_zero(self, parser):
        with pytest.raises(CalculatorError):
            parser.parse([10, "/", 0])

    def test_unmatched_open_paren(self, parser):
        with pytest.raises(CalculatorError):
            parser.parse(["(", 2, "+", 3])

    def test_unmatched_close_paren(self, parser):
        with pytest.raises(CalculatorError):
            parser.parse([2, "+", 3, ")"])

    def test_empty_expression(self, parser):
        with pytest.raises(CalculatorError):
            parser.parse([])

    def test_leading_operator(self, parser):
        with pytest.raises(CalculatorError):
            parser.parse(["+", 3])

    @pytest.mark.parametrize("tokens, expected", [
        ([12, "AND", 10], 8),
        ([12, "OR", 10], 14),
        ([12, "XOR", 10], 6),
        ([1, "LSH", 4], 16),
        ([16, "RSH", 2], 4),
        ([7, "MOD", 2], 1),
    ])
    def test_programmer_operators(self, parser, tokens, expected):
        result = parser.parse(tokens)
        assert result == pytest.approx(expected)
