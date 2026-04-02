"""Tests for CalculatorLogic class."""

import pytest
from calculator_logic import CalculatorLogic


def build_expression(logic: CalculatorLogic, expr: str) -> None:
    """Append each character in expr to the logic instance."""
    for char in expr:
        logic.append_to_expression(char)


# ---------------------------------------------------------------------------
# 3.1 Happy Path -- Basic Operations
# ---------------------------------------------------------------------------

class TestHappyPath:

    @pytest.mark.parametrize("expression, expected", [
        ("2+3", "5"),           # HP-01
        ("9-4", "5"),           # HP-02
        ("6*7", "42"),          # HP-03
        ("8/2", "4"),           # HP-04
        ("7/2", "3.5"),         # HP-05
        ("12+34", "46"),        # HP-06
        ("1.5+2.5", "4"),       # HP-07
        ("5.5-2.3", "3.2"),     # HP-08
        ("3+1.5", "4.5"),       # HP-09
        ("2+3*4", "14"),        # HP-10
        ("1+2+3+4", "10"),      # HP-11
        ("10-6/3", "8"),        # HP-13
        ("5", "5"),             # HP-14
        ("0", "0"),             # HP-15
    ], ids=[
        "HP-01-addition", "HP-02-subtraction", "HP-03-multiplication",
        "HP-04-division-exact", "HP-05-division-float", "HP-06-multi-digit",
        "HP-07-float-addition", "HP-08-float-subtraction", "HP-09-mixed",
        "HP-10-multi-ops", "HP-11-multiple-additions",
        "HP-13-precedence-div", "HP-14-single-digit", "HP-15-zero",
    ])
    def test_basic_operations(self, expression: str, expected: str) -> None:
        logic = CalculatorLogic()
        build_expression(logic, expression)
        assert logic.evaluate() == expected


# ---------------------------------------------------------------------------
# 3.2 Expression Building
# ---------------------------------------------------------------------------

class TestExpressionBuilding:

    def test_append_single_digit(self) -> None:
        logic = CalculatorLogic()
        logic.append_to_expression("5")
        assert logic.get_expression() == "5"

    def test_append_multiple_digits(self) -> None:
        logic = CalculatorLogic()
        logic.append_to_expression("1")
        logic.append_to_expression("2")
        assert logic.get_expression() == "12"

    def test_append_digit_then_operator(self) -> None:
        logic = CalculatorLogic()
        logic.append_to_expression("5")
        logic.append_to_expression("+")
        assert logic.get_expression() == "5+"

    def test_append_decimal(self) -> None:
        logic = CalculatorLogic()
        logic.append_to_expression("1")
        logic.append_to_expression(".")
        assert logic.get_expression() == "1."

    def test_build_full_expression(self) -> None:
        logic = CalculatorLogic()
        build_expression(logic, "12+34")
        assert logic.get_expression() == "12+34"

    def test_get_expression_returns_current_state(self) -> None:
        logic = CalculatorLogic()
        logic.append_to_expression("7")
        assert logic.get_expression() == "7"


# ---------------------------------------------------------------------------
# 3.3 Clear Functionality
# ---------------------------------------------------------------------------

class TestClear:

    def test_clear_empties_expression(self) -> None:
        logic = CalculatorLogic()
        build_expression(logic, "123")
        logic.clear()
        assert logic.get_expression() == ""

    def test_clear_after_partial_expression(self) -> None:
        logic = CalculatorLogic()
        build_expression(logic, "5+")
        logic.clear()
        assert logic.get_expression() == ""

    def test_clear_after_evaluation(self) -> None:
        logic = CalculatorLogic()
        build_expression(logic, "2+3")
        logic.evaluate()
        logic.clear()
        assert logic.get_expression() == ""

    def test_clear_after_error(self) -> None:
        logic = CalculatorLogic()
        build_expression(logic, "5/0")
        logic.evaluate()
        logic.clear()
        assert logic.get_expression() == ""

    def test_input_works_after_clear(self) -> None:
        logic = CalculatorLogic()
        logic.append_to_expression("5")
        logic.clear()
        logic.append_to_expression("3")
        assert logic.evaluate() == "3"

    def test_input_works_after_error_then_clear(self) -> None:
        logic = CalculatorLogic()
        build_expression(logic, "1/0")
        logic.evaluate()
        logic.clear()
        build_expression(logic, "2+3")
        assert logic.evaluate() == "5"


# ---------------------------------------------------------------------------
# 3.4 Result Chaining
# ---------------------------------------------------------------------------

class TestChaining:

    def test_operator_after_result_continues(self) -> None:
        """RC-01: After eval, appending operator continues from result."""
        logic = CalculatorLogic()
        build_expression(logic, "2+3")
        logic.evaluate()
        logic.append_to_expression("+")
        logic.append_to_expression("4")
        assert logic.evaluate() == "9"

    def test_digit_after_result_starts_fresh(self) -> None:
        """RC-02: After eval, appending digit starts fresh expression."""
        logic = CalculatorLogic()
        build_expression(logic, "2+3")
        logic.evaluate()
        logic.append_to_expression("7")
        assert logic.get_expression() == "7"

    def test_multiple_chains(self) -> None:
        """RC-03: Chain multiple evaluations."""
        logic = CalculatorLogic()
        build_expression(logic, "1+1")
        logic.evaluate()
        logic.append_to_expression("+")
        logic.append_to_expression("1")
        logic.evaluate()
        logic.append_to_expression("+")
        logic.append_to_expression("1")
        assert logic.evaluate() == "4"


# ---------------------------------------------------------------------------
# 3.5 Edge Cases
# ---------------------------------------------------------------------------

class TestEdgeCases:

    def test_division_by_zero(self) -> None:
        """EC-01"""
        logic = CalculatorLogic()
        build_expression(logic, "5/0")
        assert logic.evaluate() == "Error"

    def test_division_by_zero_in_complex_expr(self) -> None:
        """EC-02"""
        logic = CalculatorLogic()
        build_expression(logic, "3+5/0")
        assert logic.evaluate() == "Error"

    def test_empty_expression_evaluation(self) -> None:
        """EC-03: Evaluating empty expression returns Error."""
        logic = CalculatorLogic()
        assert logic.evaluate() == "Error"

    def test_consecutive_operators_replace(self) -> None:
        """EC-04: Consecutive operators -- implementation replaces last operator.
        So '5+' then '*' becomes '5*', then '3' -> '5*3' = 15."""
        logic = CalculatorLogic()
        logic.append_to_expression("5")
        logic.append_to_expression("+")
        logic.append_to_expression("*")
        logic.append_to_expression("3")
        assert logic.evaluate() == "15"

    def test_trailing_operator(self) -> None:
        """EC-05: Expression ending in operator is a syntax error."""
        logic = CalculatorLogic()
        build_expression(logic, "5+")
        assert logic.evaluate() == "Error"

    def test_leading_operator_ignored(self) -> None:
        """EC-06/07: Leading operator is ignored by append_operator when expression is empty."""
        logic = CalculatorLogic()
        logic.append_to_expression("+")
        assert logic.get_expression() == ""

        logic2 = CalculatorLogic()
        logic2.append_to_expression("-")
        assert logic2.get_expression() == ""

    def test_multiple_decimal_points_prevented(self) -> None:
        """EC-08: Second decimal in same number is silently ignored."""
        logic = CalculatorLogic()
        build_expression(logic, "1.2")
        logic.append_to_expression(".")
        logic.append_to_expression("3")
        # The second dot is ignored, so expression is "1.23"
        assert logic.get_expression() == "1.23"
        assert logic.evaluate() == "1.23"

    def test_decimal_without_leading_digit(self) -> None:
        """EC-09: .5+.5 should work since Python supports it."""
        logic = CalculatorLogic()
        build_expression(logic, ".5+.5")
        assert logic.evaluate() == "1"

    def test_operator_only(self) -> None:
        """EC-10: Just an operator, expression stays empty because append_operator
        ignores operators on empty expression."""
        logic = CalculatorLogic()
        logic.append_to_expression("+")
        assert logic.evaluate() == "Error"

    def test_multiple_operators_replaced(self) -> None:
        """EC-11: '5*' then '/' replaces -> '5/3' = 1.6666..."""
        logic = CalculatorLogic()
        logic.append_to_expression("5")
        logic.append_to_expression("*")
        logic.append_to_expression("/")
        logic.append_to_expression("3")
        result = logic.evaluate()
        assert float(result) == pytest.approx(5 / 3)


# ---------------------------------------------------------------------------
# 3.6 Boundary Conditions
# ---------------------------------------------------------------------------

class TestBoundary:

    def test_very_large_result(self) -> None:
        """BC-01"""
        logic = CalculatorLogic()
        build_expression(logic, "999999999*999999999")
        assert logic.evaluate() == "999999998000000001"

    def test_very_small_float(self) -> None:
        """BC-02"""
        logic = CalculatorLogic()
        build_expression(logic, "0.0000001+0.0000002")
        result = logic.evaluate()
        assert float(result) == pytest.approx(3e-07)

    def test_result_is_zero(self) -> None:
        """BC-03"""
        logic = CalculatorLogic()
        build_expression(logic, "5-5")
        assert logic.evaluate() == "0"

    def test_negative_result(self) -> None:
        """BC-04"""
        logic = CalculatorLogic()
        build_expression(logic, "3-7")
        assert logic.evaluate() == "-4"

    def test_long_expression(self) -> None:
        """BC-05"""
        logic = CalculatorLogic()
        build_expression(logic, "1+1+1+1+1+1+1+1+1+1")
        assert logic.evaluate() == "10"

    def test_float_whole_number_result(self) -> None:
        """BC-06: Float result that is a whole number displays without decimal."""
        logic = CalculatorLogic()
        build_expression(logic, "2.0+3.0")
        assert logic.evaluate() == "5"

    def test_divide_many_decimal_places(self) -> None:
        """BC-07"""
        logic = CalculatorLogic()
        build_expression(logic, "10/3")
        result = logic.evaluate()
        assert float(result) == pytest.approx(10 / 3)

    def test_multiply_by_zero(self) -> None:
        """BC-08"""
        logic = CalculatorLogic()
        build_expression(logic, "12345*0")
        assert logic.evaluate() == "0"

    def test_add_zero(self) -> None:
        """BC-09"""
        logic = CalculatorLogic()
        build_expression(logic, "42+0")
        assert logic.evaluate() == "42"


# ---------------------------------------------------------------------------
# 3.7 Error Recovery
# ---------------------------------------------------------------------------

class TestErrorRecovery:

    def test_error_then_clear_then_valid(self) -> None:
        """ER-01"""
        logic = CalculatorLogic()
        build_expression(logic, "1/0")
        logic.evaluate()
        logic.clear()
        build_expression(logic, "2+3")
        assert logic.evaluate() == "5"

    def test_multiple_errors_then_recovery(self) -> None:
        """ER-02"""
        logic = CalculatorLogic()
        # First error: empty eval (since operators on empty are ignored)
        logic.evaluate()
        logic.clear()
        # Second error: division by zero via direct expression if possible
        build_expression(logic, "1/0")
        logic.evaluate()
        logic.clear()
        build_expression(logic, "4+4")
        assert logic.evaluate() == "8"

    def test_clear_during_error_shows_empty(self) -> None:
        """ER-03"""
        logic = CalculatorLogic()
        build_expression(logic, "5/0")
        logic.evaluate()
        result = logic.clear()
        assert result == ""
        assert logic.get_expression() == ""


# ---------------------------------------------------------------------------
# Decimal Operations (from task requirements)
# ---------------------------------------------------------------------------

class TestDecimalOperations:

    def test_decimal_addition(self) -> None:
        logic = CalculatorLogic()
        build_expression(logic, "1.5+2.5")
        assert logic.evaluate() == "4"

    def test_floating_point_precision(self) -> None:
        """0.1+0.2 in Python gives ~0.30000000000000004."""
        logic = CalculatorLogic()
        build_expression(logic, "0.1+0.2")
        result = logic.evaluate()
        assert float(result) == pytest.approx(0.3)


# ---------------------------------------------------------------------------
# Additional: get_display_text and property tests
# ---------------------------------------------------------------------------

class TestDisplayAndProperties:

    def test_display_text_before_eval(self) -> None:
        logic = CalculatorLogic()
        build_expression(logic, "2+3")
        assert logic.get_display_text() == "2+3"

    def test_display_text_after_eval(self) -> None:
        logic = CalculatorLogic()
        build_expression(logic, "2+3")
        logic.evaluate()
        assert logic.get_display_text() == "5"

    def test_expression_property(self) -> None:
        logic = CalculatorLogic()
        build_expression(logic, "42")
        assert logic.expression == "42"

    def test_result_property(self) -> None:
        logic = CalculatorLogic()
        build_expression(logic, "2+3")
        logic.evaluate()
        assert logic.result == "5"

    def test_clear_returns_empty(self) -> None:
        logic = CalculatorLogic()
        build_expression(logic, "123")
        assert logic.clear() == ""

    def test_display_text_empty_after_clear(self) -> None:
        logic = CalculatorLogic()
        build_expression(logic, "2+3")
        logic.evaluate()
        logic.clear()
        assert logic.get_display_text() == ""

    def test_append_number_returns_expression(self) -> None:
        logic = CalculatorLogic()
        result = logic.append_number("5")
        assert result == "5"

    def test_append_operator_returns_expression(self) -> None:
        logic = CalculatorLogic()
        logic.append_number("5")
        result = logic.append_operator("+")
        assert result == "5+"

    def test_digit_after_error_starts_fresh(self) -> None:
        """After an error, typing a digit starts a fresh expression."""
        logic = CalculatorLogic()
        build_expression(logic, "1/0")
        logic.evaluate()
        logic.append_to_expression("5")
        assert logic.get_expression() == "5"

    def test_operator_after_error_stays_empty(self) -> None:
        """After an error, typing an operator clears and stays empty."""
        logic = CalculatorLogic()
        build_expression(logic, "1/0")
        logic.evaluate()
        logic.append_to_expression("+")
        assert logic.get_expression() == ""
