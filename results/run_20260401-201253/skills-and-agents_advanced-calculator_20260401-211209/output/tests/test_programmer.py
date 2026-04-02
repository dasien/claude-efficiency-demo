"""Tests for ProgrammerCalculator logic layer."""

import pytest

from calculator.logic.programmer_logic import ProgrammerCalculator


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def execute_steps(calc: ProgrammerCalculator, steps: list[str]) -> None:
    """Drive a programmer calculator through a sequence of step strings.

    Recognised steps:
        "0"-"9"      -> calc.append_digit(step)
        "+", "-", "*", "/", "%"  -> calc.add_operator(step)
        "AND", "OR", "XOR", "LSH", "RSH" -> calc.add_operator(step)
        "="          -> calc.evaluate()
        "A"-"F"      -> calc.append_hex_digit(step)
        "."          -> calc.append_decimal()
    """
    arithmetic_ops = {"+", "-", "*", "/", "%"}
    bitwise_ops = {"AND", "OR", "XOR", "LSH", "RSH"}
    hex_digits = {"A", "B", "C", "D", "E", "F"}
    for step in steps:
        if step in arithmetic_ops or step in bitwise_ops:
            calc.add_operator(step)
        elif step == "=":
            calc.evaluate()
        elif step in hex_digits:
            calc.append_hex_digit(step)
        elif step == ".":
            calc.append_decimal()
        elif step in {str(d) for d in range(10)}:
            calc.append_digit(step)
        else:
            raise ValueError(f"Unknown step: {step!r}")


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def calc() -> ProgrammerCalculator:
    """Return a fresh ProgrammerCalculator instance."""
    return ProgrammerCalculator()


# ---------------------------------------------------------------------------
# NB-1..8: Base Conversion (parametrized)
# ---------------------------------------------------------------------------

class TestBaseConversion:
    """Tests for base conversion display and valid digits."""

    @pytest.mark.parametrize(
        "base, expected",
        [
            ("HEX", "FF"),
            ("BIN", "11111111"),
            ("OCT", "377"),
            ("DEC", "255"),
        ],
        ids=["NB-1-hex", "NB-2-bin", "NB-3-oct", "NB-4-dec"],
    )
    def test_get_value_in_base(self, calc, base, expected):
        """Setting value to 255 displays correctly in each base."""
        execute_steps(calc, ["2", "5", "5"])
        assert calc.get_value_in_base(base) == expected

    def test_get_all_bases(self, calc):
        """get_all_bases returns correct dict for value 255."""
        execute_steps(calc, ["2", "5", "5"])
        result = calc.get_all_bases()
        assert result == {
            "DEC": "255",
            "HEX": "FF",
            "BIN": "11111111",
            "OCT": "377",
        }

    @pytest.mark.parametrize(
        "base, expected_digits",
        [
            ("BIN", {"0", "1"}),
            ("OCT", {str(d) for d in range(8)}),
            ("DEC", {str(d) for d in range(10)}),
            ("HEX", {str(d) for d in range(10)} | {"A", "B", "C", "D", "E", "F"}),
        ],
        ids=["NB-5-bin-digits", "NB-6-oct-digits", "NB-7-dec-digits", "NB-8-hex-digits"],
    )
    def test_get_valid_digits(self, calc, base, expected_digits):
        """get_valid_digits returns the correct set for each base."""
        calc.set_base(base)
        assert calc.get_valid_digits() == expected_digits


# ---------------------------------------------------------------------------
# HX-1..3: Hex Input
# ---------------------------------------------------------------------------

class TestHexInput:
    """Tests for hex digit input."""

    def test_hex_input_ff(self, calc):
        """HX-1: In HEX mode, appending F,F yields value 255."""
        calc.set_base("HEX")
        calc.append_hex_digit("F")
        calc.append_hex_digit("F")
        assert calc.current_value == 255

    def test_hex_display_uppercase(self, calc):
        """HX-2: Hex digits display as uppercase."""
        calc.set_base("HEX")
        calc.append_hex_digit("f")
        calc.append_hex_digit("f")
        display = calc.get_value_in_base("HEX")
        assert display == "FF"
        assert display == display.upper()

    def test_hex_digit_ignored_in_dec_mode(self, calc):
        """HX-3: Hex digits are no-op when not in HEX mode."""
        calc.set_base("DEC")
        calc.append_hex_digit("A")
        assert calc.current_value == 0


# ---------------------------------------------------------------------------
# BW-1..6: Bitwise Operations (parametrized)
# ---------------------------------------------------------------------------

class TestBitwiseOperations:
    """Tests for bitwise operations."""

    @pytest.mark.parametrize(
        "first, op, second, expected",
        [
            (12, "AND", 10, 8),
            (12, "OR", 10, 14),
            (12, "XOR", 10, 6),
            (1, "LSH", 4, 16),
            (16, "RSH", 2, 4),
        ],
        ids=["BW-1-and", "BW-2-or", "BW-3-xor", "BW-4-lsh", "BW-5-rsh"],
    )
    def test_bitwise_binary_ops(self, calc, first, op, second, expected):
        """Binary bitwise operations produce correct results."""
        # Enter first operand digit by digit
        for ch in str(first):
            calc.append_digit(ch)
        calc.add_operator(op)
        for ch in str(second):
            calc.append_digit(ch)
        result = calc.evaluate()
        assert result == expected

    def test_bitwise_not_zero_8bit(self, calc):
        """BW-6: NOT 0 in 8-bit word size yields -1."""
        calc.set_word_size(8)
        calc.current_value = 0
        calc.bitwise_not()
        assert calc.current_value == -1


# ---------------------------------------------------------------------------
# WS-1..4: Word Size (parametrized)
# ---------------------------------------------------------------------------

class TestWordSize:
    """Tests for word size masking and overflow."""

    @pytest.mark.parametrize(
        "value, expected",
        [
            (128, -128),
            (256, 0),
            (300, 44),
        ],
        ids=["WS-1-128", "WS-2-256", "WS-3-300"],
    )
    def test_mask_value_8bit(self, calc, value, expected):
        """mask_value with word_size=8 produces correct signed result."""
        calc.word_size = 8
        assert calc.mask_value(value) == expected

    def test_overflow_wraps_8bit(self, calc):
        """WS-4: 127 + 1 = -128 in 8-bit mode (overflow wraps)."""
        calc.set_word_size(8)
        execute_steps(calc, ["1", "2", "7", "+", "1", "="])
        assert calc.current_value == -128

    @pytest.mark.parametrize("bits", [8, 16, 32, 64], ids=["8bit", "16bit", "32bit", "64bit"])
    def test_all_word_sizes_accepted(self, calc, bits):
        """All standard word sizes are accepted without error."""
        calc.set_word_size(bits)
        assert calc.word_size == bits


# ---------------------------------------------------------------------------
# PM-1..4: Integer Arithmetic (parametrized)
# ---------------------------------------------------------------------------

class TestIntegerArithmetic:
    """Tests for programmer integer arithmetic."""

    @pytest.mark.parametrize(
        "steps, expected",
        [
            (["7", "/", "2", "="], 3),
            (["7", "%", "2", "="], 1),
            (["3", "+", "4", "="], 7),
            (["1", "0", "-", "3", "="], 7),
            (["3", "*", "4", "="], 12),
        ],
        ids=["PM-1-int-div", "PM-2-modulo", "PM-3-add", "PM-4-sub", "PM-5-mul"],
    )
    def test_integer_arithmetic(self, calc, steps, expected):
        """Basic integer arithmetic operations produce correct results."""
        execute_steps(calc, steps)
        assert calc.current_value == expected


# ---------------------------------------------------------------------------
# PM-3: No Decimal
# ---------------------------------------------------------------------------

class TestNoDecimal:
    """Tests that decimal point is a no-op in programmer mode."""

    def test_append_decimal_noop(self, calc):
        """append_decimal does nothing in programmer calculator."""
        execute_steps(calc, ["3"])
        calc.append_decimal()
        # Value should remain integer 3, input buffer should not contain '.'
        assert calc.current_value == 3
        assert "." not in calc.input_buffer


# ---------------------------------------------------------------------------
# Error Cases
# ---------------------------------------------------------------------------

class TestErrorCases:
    """Tests for error conditions."""

    def test_division_by_zero(self, calc):
        """Integer division by zero sets error state."""
        execute_steps(calc, ["7", "/", "0", "="])
        assert calc.error is True

    def test_modulo_by_zero(self, calc):
        """Modulo by zero sets error state."""
        execute_steps(calc, ["7", "%", "0", "="])
        assert calc.error is True
