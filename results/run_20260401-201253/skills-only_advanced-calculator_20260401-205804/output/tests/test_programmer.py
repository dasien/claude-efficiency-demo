"""Comprehensive tests for ProgrammerLogic class."""

import pytest

from calculator.logic.programmer_logic import ProgrammerLogic


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _enter_digits(calc: ProgrammerLogic, digits: str) -> None:
    """Type a sequence of digit characters into the calculator."""
    for ch in digits:
        calc.input_digit(ch)


def _make_calc(**kwargs) -> ProgrammerLogic:
    """Create a ProgrammerLogic with optional overrides applied."""
    calc = ProgrammerLogic()
    for key, value in kwargs.items():
        setattr(calc, key, value)
    return calc


# ---------------------------------------------------------------------------
# Base conversion
# ---------------------------------------------------------------------------

class TestBaseConversion:
    """Tests for converting values between number bases."""

    @pytest.mark.parametrize(
        "target_base, expected",
        [
            (16, "FF"),
            (8, "377"),
            (2, "11111111"),
        ],
        ids=["hex", "oct", "bin"],
    )
    def test_dec_255_to_other_bases(self, target_base: int, expected: str) -> None:
        calc = ProgrammerLogic()
        _enter_digits(calc, "255")
        assert calc.display_value == "255"
        calc.set_base(target_base)
        assert calc.display_value == expected

    @pytest.mark.parametrize("base", [2, 8, 10, 16], ids=["bin", "oct", "dec", "hex"])
    def test_zero_converts_to_zero_in_all_bases(self, base: int) -> None:
        calc = ProgrammerLogic()
        # display starts at "0"
        calc.set_base(base)
        assert calc.display_value == "0"

    def test_get_all_bases_for_255(self) -> None:
        calc = ProgrammerLogic()
        _enter_digits(calc, "255")
        bases = calc.get_all_bases()
        assert bases == {
            "DEC": "255",
            "HEX": "FF",
            "OCT": "377",
            "BIN": "11111111",
        }


# ---------------------------------------------------------------------------
# Digit validation
# ---------------------------------------------------------------------------

class TestDigitValidation:
    """Tests for rejecting invalid digits in each base."""

    def test_bin_rejects_2(self) -> None:
        calc = ProgrammerLogic()
        calc.set_base(2)
        calc.input_digit("2")
        assert calc.display_value == "0"

    def test_oct_rejects_8(self) -> None:
        calc = ProgrammerLogic()
        calc.set_base(8)
        calc.input_digit("8")
        assert calc.display_value == "0"

    def test_dec_rejects_A(self) -> None:
        calc = ProgrammerLogic()
        calc.input_digit("A")
        assert calc.display_value == "0"

    def test_hex_accepts_A(self) -> None:
        calc = ProgrammerLogic()
        calc.set_base(16)
        calc.input_digit("A")
        assert calc.display_value == "A"


# ---------------------------------------------------------------------------
# Word size / overflow
# ---------------------------------------------------------------------------

class TestWordSize:
    """Tests for overflow wrapping and word-size clamping."""

    @pytest.mark.parametrize(
        "word_size, start_val, op, operand, expected",
        [
            (8, "127", "+", "1", -128),
            (8, "-128", "-", "1", 127),
            (16, "32767", "+", "1", -32768),
        ],
        ids=["8bit-overflow-pos", "8bit-overflow-neg", "16bit-overflow-pos"],
    )
    def test_overflow_wraps(
        self,
        word_size: int,
        start_val: str,
        op: str,
        operand: str,
        expected: int,
    ) -> None:
        calc = ProgrammerLogic()
        calc.word_size = word_size
        calc.display_value = start_val
        calc.input_mode = "typing"
        calc.input_operator(op)
        _enter_digits(calc, operand)
        calc.evaluate()
        assert calc.get_current_int() == expected

    def test_word_size_change_clamps_value(self) -> None:
        calc = ProgrammerLogic()
        calc.word_size = 64
        _enter_digits(calc, "300")
        calc.set_word_size(8)
        assert calc.get_current_int() == 44


# ---------------------------------------------------------------------------
# Bitwise operations
# ---------------------------------------------------------------------------

class TestBitwiseOperations:
    """Tests for bitwise AND, OR, XOR, NOT, LSH, RSH."""

    @pytest.mark.parametrize(
        "left, op, right, expected",
        [
            ("12", "AND", "10", 8),
            ("12", "OR", "10", 14),
            ("12", "XOR", "10", 6),
            ("1", "LSH", "4", 16),
            ("16", "RSH", "2", 4),
        ],
        ids=["AND", "OR", "XOR", "LSH", "RSH"],
    )
    def test_binary_bitwise(
        self, left: str, op: str, right: str, expected: int
    ) -> None:
        calc = ProgrammerLogic()
        _enter_digits(calc, left)
        calc.input_operator(op)
        _enter_digits(calc, right)
        calc.evaluate()
        assert calc.get_current_int() == expected

    @pytest.mark.parametrize(
        "value, expected",
        [
            ("0", -1),
            ("1", -2),
        ],
        ids=["NOT_0", "NOT_1"],
    )
    def test_bitwise_not(self, value: str, expected: int) -> None:
        calc = ProgrammerLogic()
        calc.word_size = 8
        _enter_digits(calc, value)
        calc.bitwise_not()
        assert calc.get_current_int() == expected


# ---------------------------------------------------------------------------
# Integer arithmetic
# ---------------------------------------------------------------------------

class TestIntegerArithmetic:
    """Tests for +, -, *, /, MOD with integer semantics."""

    @pytest.mark.parametrize(
        "left, op, right, expected",
        [
            ("10", "+", "20", 30),
            ("20", "-", "30", -10),
            ("3", "*", "4", 12),
            ("7", "/", "2", 3),
            ("7", "MOD", "2", 1),
        ],
        ids=["add", "sub", "mul", "trunc_div", "mod"],
    )
    def test_arithmetic(
        self, left: str, op: str, right: str, expected: int
    ) -> None:
        calc = ProgrammerLogic()
        _enter_digits(calc, left)
        calc.input_operator(op)
        _enter_digits(calc, right)
        calc.evaluate()
        assert calc.get_current_int() == expected

    def test_negative_truncating_division(self) -> None:
        """Verify -7/2 truncates toward zero, giving -3 (not -4)."""
        calc = ProgrammerLogic()
        _enter_digits(calc, "7")
        calc.toggle_sign()
        calc.input_operator("/")
        _enter_digits(calc, "2")
        calc.evaluate()
        assert calc.get_current_int() == -3


# ---------------------------------------------------------------------------
# Error cases
# ---------------------------------------------------------------------------

class TestErrorCases:
    """Tests for division and modulo by zero."""

    @pytest.mark.parametrize(
        "op",
        ["/", "MOD"],
        ids=["div_by_zero", "mod_by_zero"],
    )
    def test_division_by_zero_sets_error(self, op: str) -> None:
        calc = ProgrammerLogic()
        _enter_digits(calc, "5")
        calc.input_operator(op)
        _enter_digits(calc, "0")
        calc.evaluate()
        assert calc.error is True
        assert calc.display_value == "Error"


# ---------------------------------------------------------------------------
# No decimal
# ---------------------------------------------------------------------------

class TestNoDecimal:
    """Programmer mode must ignore decimal point input."""

    def test_input_decimal_has_no_effect(self) -> None:
        calc = ProgrammerLogic()
        _enter_digits(calc, "5")
        calc.input_decimal()
        assert "." not in calc.display_value
        assert calc.display_value == "5"
