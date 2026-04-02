"""Tests for Programmer calculator mode: base conversion, word sizes, bitwise ops, int arithmetic."""

import pytest
from calculator.logic.programmer_logic import ProgrammerCalculator
from calculator.logic.base_logic import CalculatorError


def enter_number(calc, number_str):
    """Enter a multi-digit number into the calculator."""
    for ch in str(number_str):
        calc.append_digit(ch)


@pytest.fixture
def calc():
    return ProgrammerCalculator()


@pytest.fixture
def calc8():
    c = ProgrammerCalculator()
    c.set_word_size(8)
    return c


# =============================================================================
# Base Conversion
# =============================================================================

class TestBaseConversion:

    def test_dec_to_hex(self, calc):
        result = calc.format_in_base(255, 16)
        assert result == "FF"

    def test_dec_to_bin(self, calc):
        result = calc.format_in_base(255, 2)
        assert result == "11111111"

    def test_dec_to_oct(self, calc):
        result = calc.format_in_base(255, 8)
        assert result == "377"

    def test_zero_hex(self, calc):
        result = calc.format_in_base(0, 16)
        assert result == "0"

    def test_zero_bin(self, calc):
        result = calc.format_in_base(0, 2)
        assert result == "0"

    def test_negative_1_hex_8bit(self, calc8):
        result = calc8.format_in_base(-1, 16)
        assert result == "FF"

    def test_negative_1_bin_8bit(self, calc8):
        result = calc8.format_in_base(-1, 2)
        assert result == "11111111"

    def test_hex_input_to_dec(self, calc):
        """Enter FF in HEX, switch to DEC, expect 255."""
        calc.set_base(16)
        calc.append_digit("F")
        calc.append_digit("F")
        calc.set_base(10)
        assert calc.current_input == "255"

    def test_dec_input_to_hex(self, calc):
        """Enter 255 in DEC, switch to HEX, expect FF."""
        calc.set_base(10)
        enter_number(calc, "255")
        calc.set_base(16)
        assert calc.current_input == "FF"

    def test_hex_input_to_bin(self, calc):
        """Enter FF in HEX, switch to BIN, expect 11111111."""
        calc.set_base(16)
        calc.append_digit("F")
        calc.append_digit("F")
        calc.set_base(2)
        assert calc.current_input == "11111111"


class TestAllBasesDisplay:

    def test_all_bases_255(self, calc):
        result = calc.get_all_bases(255)
        assert result["DEC"] == "255"
        assert result["HEX"] == "FF"
        assert result["OCT"] == "377"
        assert result["BIN"] == "11111111"

    def test_all_bases_zero(self, calc):
        result = calc.get_all_bases(0)
        assert result["DEC"] == "0"
        assert result["HEX"] == "0"
        assert result["OCT"] == "0"
        assert result["BIN"] == "0"


# =============================================================================
# Valid Digits Per Base
# =============================================================================

class TestValidDigits:

    def test_bin_digits(self, calc):
        calc.set_base(2)
        assert calc.get_valid_digits() == {"0", "1"}

    def test_oct_digits(self, calc):
        calc.set_base(8)
        expected = {str(i) for i in range(8)}
        assert calc.get_valid_digits() == expected

    def test_dec_digits(self, calc):
        calc.set_base(10)
        expected = {str(i) for i in range(10)}
        assert calc.get_valid_digits() == expected

    def test_hex_digits(self, calc):
        calc.set_base(16)
        expected = {str(i) for i in range(10)} | {"A", "B", "C", "D", "E", "F"}
        assert calc.get_valid_digits() == expected

    def test_invalid_digit_rejected_in_bin(self, calc):
        calc.set_base(2)
        calc.current_input = "0"
        result = calc.append_digit("2")
        # Should not have changed (invalid digit is a no-op)
        assert "2" not in calc.current_input

    def test_invalid_digit_rejected_in_oct(self, calc):
        calc.set_base(8)
        calc.current_input = "0"
        result = calc.append_digit("9")
        assert "9" not in calc.current_input


# =============================================================================
# Word Size
# =============================================================================

class TestWordSize:

    def test_8bit_overflow_positive(self, calc8):
        """127 + 1 = -128 in 8-bit."""
        enter_number(calc8, "127")
        calc8.add_operator("+")
        enter_number(calc8, "1")
        result = calc8.evaluate()
        assert result == pytest.approx(-128)

    def test_8bit_overflow_negative(self, calc8):
        """-128 - 1 = 127 in 8-bit."""
        # Enter -128: enter 128 then toggle sign
        calc8.value = -128
        calc8.current_input = "-128"
        calc8.add_operator("-")
        enter_number(calc8, "1")
        result = calc8.evaluate()
        assert result == pytest.approx(127)

    def test_16bit_overflow(self, calc):
        calc.set_word_size(16)
        enter_number(calc, "32767")
        calc.add_operator("+")
        enter_number(calc, "1")
        result = calc.evaluate()
        assert result == pytest.approx(-32768)

    def test_apply_word_size_255_8bit(self, calc8):
        result = calc8._apply_word_size(255)
        assert result == -1

    def test_apply_word_size_128_8bit(self, calc8):
        result = calc8._apply_word_size(128)
        assert result == -128

    def test_apply_word_size_256_8bit(self, calc8):
        result = calc8._apply_word_size(256)
        assert result == 0

    def test_truncate_300_to_8bit(self, calc):
        """Switching from 64-bit with value 300 to 8-bit should give 44."""
        calc.set_word_size(64)
        enter_number(calc, "300")
        result = calc.set_word_size(8)
        assert result == 44

    def test_truncate_256_to_8bit(self, calc):
        """Switching from 64-bit with value 256 to 8-bit should give 0."""
        calc.set_word_size(64)
        enter_number(calc, "256")
        result = calc.set_word_size(8)
        assert result == 0


# =============================================================================
# Bitwise Operations
# =============================================================================

class TestBitwiseOps:

    @pytest.mark.parametrize("op, a, b, word_size, expected", [
        ("and", 12, 10, 64, 8),
        ("and", 0xFF, 0x0F, 64, 15),
        ("or", 12, 10, 64, 14),
        ("xor", 12, 10, 64, 6),
    ])
    def test_binary_bitwise(self, op, a, b, word_size, expected):
        calc = ProgrammerCalculator()
        calc.set_word_size(word_size)
        func = getattr(calc, f"bitwise_{op}")
        result = func(a, b)
        assert result == expected

    def test_not_0_8bit(self, calc8):
        result = calc8.bitwise_not(0)
        assert result == -1

    def test_not_neg1_8bit(self, calc8):
        result = calc8.bitwise_not(-1)
        assert result == 0

    @pytest.mark.parametrize("a, n, word_size, expected", [
        (1, 4, 64, 16),
        (1, 7, 8, -128),
    ])
    def test_left_shift(self, a, n, word_size, expected):
        calc = ProgrammerCalculator()
        calc.set_word_size(word_size)
        result = calc.left_shift(a, n)
        assert result == expected

    @pytest.mark.parametrize("a, n, word_size, expected", [
        (16, 2, 64, 4),
        (-128, 7, 8, -1),
    ])
    def test_right_shift(self, a, n, word_size, expected):
        calc = ProgrammerCalculator()
        calc.set_word_size(word_size)
        result = calc.right_shift(a, n)
        assert result == expected


# =============================================================================
# Integer Arithmetic
# =============================================================================

class TestIntegerArithmetic:

    @pytest.mark.parametrize("a, op, b, expected", [
        (5, "+", 3, 8),
        (5, "-", 3, 2),
        (6, "*", 7, 42),
    ])
    def test_basic_int_ops(self, calc, a, op, b, expected):
        enter_number(calc, str(a))
        calc.add_operator(op)
        enter_number(calc, str(b))
        result = calc.evaluate()
        assert result == pytest.approx(expected)

    def test_integer_division_7_2(self, calc):
        enter_number(calc, "7")
        calc.add_operator("/")
        enter_number(calc, "2")
        result = calc.evaluate()
        assert result == pytest.approx(3)

    def test_integer_division_neg7_2(self, calc):
        """Truncating division: -7 / 2 = -3."""
        calc.value = -7
        calc.current_input = "-7"
        calc.add_operator("/")
        enter_number(calc, "2")
        result = calc.evaluate()
        assert result == pytest.approx(-3)

    def test_integer_division_7_neg2(self, calc):
        """Truncating division: 7 / -2 = -3."""
        enter_number(calc, "7")
        calc.add_operator("/")
        calc.value = -2
        calc.current_input = "-2"
        calc.add_operator("*")  # This won't work, let's use a direct approach
        # Reset and try differently
        calc2 = ProgrammerCalculator()
        calc2.expression = [7.0, "/", -2.0]
        result = calc2.evaluate()
        assert result == pytest.approx(-3)

    def test_modulo(self, calc):
        enter_number(calc, "7")
        calc.add_operator("MOD")
        enter_number(calc, "2")
        result = calc.evaluate()
        assert result == pytest.approx(1)

    def test_modulo_10_3(self, calc):
        enter_number(calc, "10")
        calc.add_operator("MOD")
        enter_number(calc, "3")
        result = calc.evaluate()
        assert result == pytest.approx(1)


class TestIntegerArithmeticErrors:

    def test_div_by_zero(self, calc):
        enter_number(calc, "5")
        calc.add_operator("/")
        enter_number(calc, "0")
        with pytest.raises(CalculatorError):
            calc.evaluate()

    def test_mod_by_zero(self, calc):
        enter_number(calc, "5")
        calc.add_operator("MOD")
        enter_number(calc, "0")
        with pytest.raises(CalculatorError):
            calc.evaluate()


# =============================================================================
# No Decimal Point
# =============================================================================

class TestNoDecimalPoint:

    def test_append_decimal_is_noop(self, calc):
        calc.current_input = "5"
        result = calc.append_decimal()
        assert "." not in result
