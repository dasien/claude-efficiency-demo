"""Tests for Programmer mode calculator logic."""

import pytest

from calculator.logic.programmer_logic import (
    ProgrammerCalculator,
)


class TestBaseConversion:
    """Base conversion tests."""

    def test_dec_to_hex(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(255)
        calc.set_base("HEX")
        assert calc.get_display() == "FF"

    def test_hex_to_dec(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_base("HEX")
        calc.input_digit("F")
        calc.input_digit("F")
        calc.set_base("DEC")
        assert calc.get_display() == "255"

    def test_dec_to_bin(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(255)
        calc.set_base("BIN")
        assert calc.get_display() == "11111111"

    def test_dec_to_oct(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(255)
        calc.set_base("OCT")
        assert calc.get_display() == "377"

    def test_hex_to_bin(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_base("HEX")
        calc.input_digit("F")
        calc.input_digit("F")
        calc.set_base("BIN")
        assert calc.get_display() == "11111111"

    def test_all_bases(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(255)
        bases = calc.get_all_bases()
        assert bases["DEC"] == "255"
        assert bases["HEX"] == "FF"
        assert bases["OCT"] == "377"
        assert bases["BIN"] == "11111111"


class TestValidDigits:
    """Valid digit enforcement tests."""

    def test_bin_valid_digits(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_base("BIN")
        valid = calc.get_valid_digits()
        assert "0" in valid
        assert "1" in valid
        assert "2" not in valid

    def test_oct_valid_digits(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_base("OCT")
        valid = calc.get_valid_digits()
        assert "7" in valid
        assert "8" not in valid

    def test_dec_valid_digits(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_base("DEC")
        valid = calc.get_valid_digits()
        assert "9" in valid
        assert "A" not in valid

    def test_hex_valid_digits(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_base("HEX")
        valid = calc.get_valid_digits()
        assert "F" in valid
        assert "G" not in valid

    def test_invalid_digit_ignored(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_base("BIN")
        calc.input_digit("5")
        assert calc.get_display() == "0"


class TestWordSize:
    """Word size constraint tests."""

    def test_8bit_max(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_word_size(8)
        calc.set_value(127)
        assert calc.get_value() == 127

    def test_8bit_overflow(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_word_size(8)
        # 127 + 1 = -128
        calc.set_value(127)
        calc.input_operator("+")
        calc.input_digit("1")
        calc.input_equals()
        assert calc.get_value() == -128

    def test_8bit_underflow(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_word_size(8)
        calc.set_value(-128)
        calc.input_operator("-")
        calc.input_digit("1")
        calc.input_equals()
        assert calc.get_value() == 127

    def test_16bit_max(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_word_size(16)
        calc.set_value(32767)
        assert calc.get_value() == 32767

    def test_word_size_change_truncates(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_word_size(64)
        calc.set_value(300)
        calc.set_word_size(8)
        assert calc.get_value() == 44

    def test_constrain_value(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_word_size(8)
        assert calc.constrain_value(256) == 0
        assert calc.constrain_value(128) == -128
        assert calc.constrain_value(-129) == 127


class TestBitwiseOperations:
    """Bitwise operation tests."""

    def test_and(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(12)
        calc.input_operator("AND")
        calc.input_digit("1")
        calc.input_digit("0")
        calc.input_equals()
        assert calc.get_value() == 8

    def test_or(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(12)
        calc.input_operator("OR")
        calc.input_digit("1")
        calc.input_digit("0")
        calc.input_equals()
        assert calc.get_value() == 14

    def test_xor(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(12)
        calc.input_operator("XOR")
        calc.input_digit("1")
        calc.input_digit("0")
        calc.input_equals()
        assert calc.get_value() == 6

    def test_not_zero_8bit(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_word_size(8)
        calc.set_value(0)
        calc.apply_not()
        assert calc.get_value() == -1

    def test_lshift(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(1)
        calc.input_operator("LSH")
        calc.input_digit("4")
        calc.input_equals()
        assert calc.get_value() == 16

    def test_rshift(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(16)
        calc.input_operator("RSH")
        calc.input_digit("2")
        calc.input_equals()
        assert calc.get_value() == 4


class TestIntegerArithmetic:
    """Integer arithmetic tests."""

    def test_integer_division(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(7)
        calc.input_operator("/")
        calc.input_digit("2")
        calc.input_equals()
        assert calc.get_value() == 3

    def test_modulo(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(7)
        calc.input_operator("%")
        calc.input_digit("2")
        calc.input_equals()
        assert calc.get_value() == 1

    def test_addition(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(10)
        calc.input_operator("+")
        calc.input_digit("2")
        calc.input_digit("0")
        calc.input_equals()
        assert calc.get_value() == 30

    def test_subtraction(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(20)
        calc.input_operator("-")
        calc.input_digit("7")
        calc.input_equals()
        assert calc.get_value() == 13

    def test_multiplication(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(6)
        calc.input_operator("*")
        calc.input_digit("7")
        calc.input_equals()
        assert calc.get_value() == 42


class TestProgrammerErrors:
    """Error condition tests."""

    def test_division_by_zero(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(5)
        calc.input_operator("/")
        calc.input_digit("0")
        calc.input_equals()
        assert calc.is_error()

    def test_modulo_by_zero(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(5)
        calc.input_operator("%")
        calc.input_digit("0")
        calc.input_equals()
        assert calc.is_error()

    def test_error_recovery(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(5)
        calc.input_operator("/")
        calc.input_digit("0")
        calc.input_equals()
        assert calc.is_error()
        calc.input_digit("3")
        assert not calc.is_error()


class TestNegate:
    """Negate tests for programmer mode."""

    def test_negate(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_value(5)
        calc.input_negate()
        assert calc.get_value() == -5

    def test_negate_8bit(self) -> None:
        calc = ProgrammerCalculator()
        calc.set_word_size(8)
        calc.set_value(5)
        calc.input_negate()
        assert calc.get_value() == -5
