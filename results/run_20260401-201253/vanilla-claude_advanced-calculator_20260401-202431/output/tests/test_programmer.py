"""Tests for programmer calculator mode."""

import pytest
from calculator.logic.programmer_logic import ProgrammerCalculator


@pytest.fixture
def calc():
    """Create a fresh ProgrammerCalculator instance."""
    return ProgrammerCalculator()


# --- Base Conversion ---

class TestBaseConversion:
    """Test base conversion functionality."""

    def test_dec_to_hex(self, calc):
        calc.input_digit("2")
        calc.input_digit("5")
        calc.input_digit("5")
        calc.set_base("HEX")
        assert calc.get_display_value() == "FF"

    def test_hex_to_dec(self, calc):
        calc.set_base("HEX")
        calc.input_digit("F")
        calc.input_digit("F")
        calc.set_base("DEC")
        assert calc.get_display_value() == "255"

    def test_hex_to_bin(self, calc):
        calc.set_base("HEX")
        calc.input_digit("F")
        calc.input_digit("F")
        calc.set_base("BIN")
        assert calc.get_display_value() == "11111111"

    def test_dec_to_oct(self, calc):
        calc.input_digit("2")
        calc.input_digit("5")
        calc.input_digit("5")
        calc.set_base("OCT")
        assert calc.get_display_value() == "377"

    def test_dec_to_bin(self, calc):
        calc.input_digit("1")
        calc.input_digit("6")
        calc.set_base("BIN")
        assert calc.get_display_value() == "10000"

    def test_zero_all_bases(self, calc):
        conversions = calc.get_base_conversions()
        assert conversions["DEC"] == "0"
        assert conversions["HEX"] == "0"
        assert conversions["OCT"] == "0"
        assert conversions["BIN"] == "0"

    def test_base_conversion_panel(self, calc):
        calc.input_digit("2")
        calc.input_digit("5")
        calc.input_digit("5")
        conversions = calc.get_base_conversions()
        assert conversions["DEC"] == "255"
        assert conversions["HEX"] == "FF"
        assert conversions["OCT"] == "377"
        assert conversions["BIN"] == "11111111"


# --- Arithmetic ---

class TestArithmetic:
    """Test programmer mode arithmetic."""

    def test_integer_division(self, calc):
        calc.input_digit("7")
        calc.input_operator("/")
        calc.input_digit("2")
        calc.evaluate()
        assert calc.get_current_int_value() == 3

    def test_modulo(self, calc):
        calc.input_digit("7")
        calc.input_operator("%")
        calc.input_digit("2")
        calc.evaluate()
        assert calc.get_current_int_value() == 1

    def test_addition(self, calc):
        calc.input_digit("1")
        calc.input_digit("0")
        calc.input_operator("+")
        calc.input_digit("5")
        calc.evaluate()
        assert calc.get_current_int_value() == 15

    def test_subtraction(self, calc):
        calc.input_digit("1")
        calc.input_digit("0")
        calc.input_operator("-")
        calc.input_digit("5")
        calc.evaluate()
        assert calc.get_current_int_value() == 5

    def test_multiplication(self, calc):
        calc.input_digit("3")
        calc.input_operator("*")
        calc.input_digit("4")
        calc.evaluate()
        assert calc.get_current_int_value() == 12


# --- Bitwise Operations ---

class TestBitwiseOps:
    """Test bitwise operations."""

    def test_and(self, calc):
        calc.input_digit("1")
        calc.input_digit("2")
        calc.input_operator("AND")
        calc.input_digit("1")
        calc.input_digit("0")
        calc.evaluate()
        assert calc.get_current_int_value() == 8

    def test_or(self, calc):
        calc.input_digit("1")
        calc.input_digit("2")
        calc.input_operator("OR")
        calc.input_digit("1")
        calc.input_digit("0")
        calc.evaluate()
        assert calc.get_current_int_value() == 14

    def test_xor(self, calc):
        calc.input_digit("1")
        calc.input_digit("2")
        calc.input_operator("XOR")
        calc.input_digit("1")
        calc.input_digit("0")
        calc.evaluate()
        assert calc.get_current_int_value() == 6

    def test_not_zero_8bit(self, calc):
        calc.set_word_size(8)
        calc.input_digit("0")
        calc.bitwise_not()
        assert calc.get_current_int_value() == -1

    def test_left_shift(self, calc):
        calc.input_digit("1")
        calc.input_operator("LSH")
        calc.input_digit("4")
        calc.evaluate()
        assert calc.get_current_int_value() == 16

    def test_right_shift(self, calc):
        calc.input_digit("1")
        calc.input_digit("6")
        calc.input_operator("RSH")
        calc.input_digit("2")
        calc.evaluate()
        assert calc.get_current_int_value() == 4


# --- Hex Input ---

class TestHexInput:
    """Test hex digit input."""

    def test_hex_ff(self, calc):
        calc.set_base("HEX")
        calc.input_digit("F")
        calc.input_digit("F")
        assert calc.get_current_int_value() == 255

    def test_hex_a0(self, calc):
        calc.set_base("HEX")
        calc.input_digit("A")
        calc.input_digit("0")
        assert calc.get_current_int_value() == 160

    def test_invalid_digit_ignored(self, calc):
        calc.set_base("BIN")
        calc.input_digit("2")  # Should be ignored
        assert calc.get_display_value() == "0"


# --- Word Size ---

class TestWordSize:
    """Test word size constraints."""

    def test_8bit_max(self, calc):
        calc.set_word_size(8)
        calc.set_value(127)
        assert calc.get_current_int_value() == 127

    def test_8bit_overflow(self, calc):
        calc.set_word_size(8)
        calc.set_value(127)
        calc.input_operator("+")
        calc.input_digit("1")
        calc.evaluate()
        assert calc.get_current_int_value() == -128

    def test_truncation_64_to_8(self, calc):
        calc.set_value(300)
        calc.set_word_size(8)
        assert calc.get_current_int_value() == 44

    def test_8bit_underflow(self, calc):
        calc.set_word_size(8)
        calc.set_value(-128)
        calc.input_operator("-")
        calc.input_digit("1")
        calc.evaluate()
        assert calc.get_current_int_value() == 127

    def test_not_not_identity(self, calc):
        calc.set_word_size(8)
        calc.input_digit("5")
        calc.bitwise_not()
        calc.bitwise_not()
        assert calc.get_current_int_value() == 5

    def test_shift_by_zero(self, calc):
        calc.input_digit("5")
        calc.input_operator("LSH")
        calc.input_digit("0")
        calc.evaluate()
        assert calc.get_current_int_value() == 5

    def test_negative_one_8bit_hex(self, calc):
        calc.set_word_size(8)
        calc.set_value(-1)
        calc.set_base("HEX")
        assert calc.get_display_value() == "FF"


# --- Error Cases ---

class TestErrors:
    """Test error conditions."""

    def test_division_by_zero(self, calc):
        calc.input_digit("5")
        calc.input_operator("/")
        calc.input_digit("0")
        calc.evaluate()
        assert calc.error is True

    def test_modulo_by_zero(self, calc):
        calc.input_digit("5")
        calc.input_operator("%")
        calc.input_digit("0")
        calc.evaluate()
        assert calc.error is True


# --- Clear and Edit ---

class TestClearAndEdit:
    """Test clear and edit operations."""

    def test_all_clear(self, calc):
        calc.input_digit("5")
        calc.all_clear()
        assert calc.get_display_value() == "0"

    def test_clear_entry(self, calc):
        calc.input_digit("5")
        calc.clear_entry()
        assert calc.get_display_value() == "0"

    def test_backspace(self, calc):
        calc.input_digit("1")
        calc.input_digit("2")
        calc.input_digit("3")
        calc.backspace()
        assert calc.get_display_value() == "12"
