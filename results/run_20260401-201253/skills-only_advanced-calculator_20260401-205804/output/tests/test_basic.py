"""Comprehensive tests for BasicLogic calculator."""

import pytest

from calculator.logic.basic_logic import BasicLogic


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _type_number(calc: BasicLogic, number: str) -> None:
    """Type a number (possibly with a decimal point) into the calculator."""
    for ch in number:
        if ch == ".":
            calc.input_decimal()
        else:
            calc.input_digit(ch)


# ---------------------------------------------------------------------------
# 1. Arithmetic (parametrized)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "left, op, right, expected",
    [
        ("2", "+", "3", "5"),
        ("10", "-", "3", "7"),
        ("4", "*", "5", "20"),
        ("10", "/", "4", "2.5"),
    ],
    ids=["add", "subtract", "multiply", "divide"],
)
def test_basic_arithmetic(left, op, right, expected):
    calc = BasicLogic()
    _type_number(calc, left)
    calc.input_operator(op)
    _type_number(calc, right)
    calc.evaluate()
    assert calc.display_value == expected


# ---------------------------------------------------------------------------
# 2. Operator precedence
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "sequence, expected",
    [
        # 2+3*4 = 14
        ([("d", "2"), ("o", "+"), ("d", "3"), ("o", "*"), ("d", "4")], "14"),
        # 10-2*3 = 4
        ([("d", "1"), ("d", "0"), ("o", "-"), ("d", "2"), ("o", "*"), ("d", "3")], "4"),
        # 2*3+4*5 = 26
        ([("d", "2"), ("o", "*"), ("d", "3"), ("o", "+"), ("d", "4"), ("o", "*"), ("d", "5")], "26"),
    ],
    ids=["2+3*4=14", "10-2*3=4", "2*3+4*5=26"],
)
def test_operator_precedence(sequence, expected):
    calc = BasicLogic()
    for kind, value in sequence:
        if kind == "d":
            calc.input_digit(value)
        elif kind == "o":
            calc.input_operator(value)
    calc.evaluate()
    assert calc.display_value == expected


# ---------------------------------------------------------------------------
# 3. Chained operations
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "sequence, expected",
    [
        # 1+2+3 = 6
        ([("d", "1"), ("o", "+"), ("d", "2"), ("o", "+"), ("d", "3")], "6"),
        # 10/2*3 = 15
        ([("d", "1"), ("d", "0"), ("o", "/"), ("d", "2"), ("o", "*"), ("d", "3")], "15"),
    ],
    ids=["1+2+3=6", "10/2*3=15"],
)
def test_chained_operations(sequence, expected):
    calc = BasicLogic()
    for kind, value in sequence:
        if kind == "d":
            calc.input_digit(value)
        elif kind == "o":
            calc.input_operator(value)
    calc.evaluate()
    assert calc.display_value == expected


# ---------------------------------------------------------------------------
# 4. Decimal input
# ---------------------------------------------------------------------------

def test_decimal_input():
    calc = BasicLogic()
    _type_number(calc, "0.5")
    calc.input_operator("+")
    _type_number(calc, "0.5")
    calc.evaluate()
    assert calc.display_value == "1"


# ---------------------------------------------------------------------------
# 5. Percentage
# ---------------------------------------------------------------------------

def test_percentage():
    calc = BasicLogic()
    _type_number(calc, "200")
    calc.percent()
    assert calc.display_value == "2"


# ---------------------------------------------------------------------------
# 6. Sign toggle
# ---------------------------------------------------------------------------

def test_sign_toggle():
    calc = BasicLogic()
    _type_number(calc, "5")
    calc.toggle_sign()
    assert calc.display_value == "-5"
    calc.toggle_sign()
    assert calc.display_value == "5"


# ---------------------------------------------------------------------------
# 7. Leading zeros
# ---------------------------------------------------------------------------

def test_leading_zeros():
    calc = BasicLogic()
    calc.input_digit("0")
    calc.input_digit("0")
    calc.input_digit("7")
    assert calc.display_value == "7"


# ---------------------------------------------------------------------------
# 8. Single decimal point
# ---------------------------------------------------------------------------

def test_single_decimal_point():
    calc = BasicLogic()
    calc.input_digit("1")
    calc.input_decimal()
    calc.input_decimal()  # second dot ignored
    calc.input_digit("5")
    assert calc.display_value == "1.5"


# ---------------------------------------------------------------------------
# 9. Backspace
# ---------------------------------------------------------------------------

def test_backspace():
    calc = BasicLogic()
    calc.input_digit("1")
    calc.input_digit("2")
    calc.input_digit("3")
    calc.backspace()
    assert calc.display_value == "12"


# ---------------------------------------------------------------------------
# 10. Clear entry (C)
# ---------------------------------------------------------------------------

def test_clear_entry():
    calc = BasicLogic()
    calc.input_digit("5")
    calc.input_operator("+")
    calc.input_digit("3")
    calc.clear_entry()
    calc.input_digit("2")
    calc.evaluate()
    assert calc.display_value == "7"


# ---------------------------------------------------------------------------
# 11. All clear (AC)
# ---------------------------------------------------------------------------

def test_all_clear():
    calc = BasicLogic()
    calc.input_digit("5")
    calc.input_operator("+")
    calc.input_digit("3")
    calc.all_clear()
    calc.input_digit("2")
    calc.evaluate()
    assert calc.display_value == "2"


# ---------------------------------------------------------------------------
# 12. Display formatting
# ---------------------------------------------------------------------------

def test_display_integer_no_trailing_zero():
    """4/2 should display '2', not '2.0'."""
    calc = BasicLogic()
    calc.input_digit("4")
    calc.input_operator("/")
    calc.input_digit("2")
    calc.evaluate()
    assert calc.display_value == "2"


def test_display_repeating_decimal_precision():
    """1/3 should have 10 significant digits."""
    calc = BasicLogic()
    calc.input_digit("1")
    calc.input_operator("/")
    calc.input_digit("3")
    calc.evaluate()
    # format_number uses f"{value:.10g}" which gives 10 significant digits
    # 1/3 = 0.3333333333 (10 significant digits)
    assert calc.display_value == "0.3333333333"
    assert len(calc.display_value.replace("0.", "")) == 10


# ---------------------------------------------------------------------------
# 13. Division by zero
# ---------------------------------------------------------------------------

def test_division_by_zero():
    calc = BasicLogic()
    _type_number(calc, "100")
    calc.input_operator("/")
    calc.input_digit("0")
    calc.evaluate()
    assert calc.display_value == "Error"
    assert calc.error is True


# ---------------------------------------------------------------------------
# 14. Error recovery — digit
# ---------------------------------------------------------------------------

def test_error_recovery_digit():
    calc = BasicLogic()
    _type_number(calc, "100")
    calc.input_operator("/")
    calc.input_digit("0")
    calc.evaluate()
    assert calc.display_value == "Error"
    calc.input_digit("5")
    assert calc.display_value == "5"
    assert calc.error is False


# ---------------------------------------------------------------------------
# 15. Error recovery — clear
# ---------------------------------------------------------------------------

def test_error_recovery_clear():
    calc = BasicLogic()
    _type_number(calc, "100")
    calc.input_operator("/")
    calc.input_digit("0")
    calc.evaluate()
    assert calc.display_value == "Error"
    calc.clear_entry()
    assert calc.display_value == "0"
    assert calc.error is False
