"""Tests for ProgrammerLogic: base conversion, integer arithmetic, bitwise, word size."""

import pytest
from calculator.logic.base_logic import NumberBase, WordSize
from calculator.logic.programmer_logic import ProgrammerLogic


# ── Helpers ──────────────────────────────────────────────────────

def _type_digits(calc: ProgrammerLogic, digits: str) -> None:
    """Type a sequence of digit characters into the calculator."""
    for ch in digits:
        calc.input_digit(ch)


# ── Base conversion ──────────────────────────────────────────────

class TestBaseConversion:
    """NB-1 through NB-7: switching between DEC, HEX, OCT, BIN."""

    def test_dec_255_to_hex(self):
        """NB-6: 255 DEC -> FF HEX."""
        calc = ProgrammerLogic()
        _type_digits(calc, "255")
        state = calc.set_base(NumberBase.HEX)
        assert state.main_display == "FF"

    def test_hex_ff_to_dec(self):
        """NB-6: FF HEX -> 255 DEC."""
        calc = ProgrammerLogic()
        calc.set_base(NumberBase.HEX)
        _type_digits(calc, "FF")
        state = calc.set_base(NumberBase.DEC)
        assert state.main_display == "255"

    def test_hex_ff_to_bin(self):
        """NB-6: FF HEX -> 11111111 BIN."""
        calc = ProgrammerLogic()
        calc.set_base(NumberBase.HEX)
        _type_digits(calc, "FF")
        state = calc.set_base(NumberBase.BIN)
        assert state.main_display == "11111111"

    def test_simultaneous_base_display(self):
        """NB-7: all four base representations shown simultaneously."""
        calc = ProgrammerLogic()
        _type_digits(calc, "255")
        state = calc.get_display_state()
        assert state.dec_value == "255"
        assert state.hex_value == "FF"
        assert state.oct_value == "377"
        assert state.bin_value == "11111111"

    def test_dec_to_oct(self):
        """8 DEC -> 10 OCT."""
        calc = ProgrammerLogic()
        _type_digits(calc, "8")
        state = calc.set_base(NumberBase.OCT)
        assert state.main_display == "10"


# ── Integer arithmetic ───────────────────────────────────────────

class TestIntegerArithmetic:
    """PM-1 through PM-4: integer division, modulo."""

    def test_integer_division_truncates(self):
        """PM-2: 7 / 2 = 3 (truncating division)."""
        calc = ProgrammerLogic()
        _type_digits(calc, "7")
        calc.input_operator("/")
        _type_digits(calc, "2")
        state = calc.evaluate()
        assert state.main_display == "3"

    def test_modulo(self):
        """PM-4: 7 % 2 = 1."""
        calc = ProgrammerLogic()
        _type_digits(calc, "7")
        calc.input_operator("%")
        _type_digits(calc, "2")
        state = calc.evaluate()
        assert state.main_display == "1"

    def test_addition(self):
        """10 + 5 = 15."""
        calc = ProgrammerLogic()
        _type_digits(calc, "10")
        calc.input_operator("+")
        _type_digits(calc, "5")
        state = calc.evaluate()
        assert state.main_display == "15"

    def test_subtraction(self):
        """10 - 3 = 7."""
        calc = ProgrammerLogic()
        _type_digits(calc, "10")
        calc.input_operator("-")
        _type_digits(calc, "3")
        state = calc.evaluate()
        assert state.main_display == "7"

    def test_multiplication(self):
        """6 * 7 = 42."""
        calc = ProgrammerLogic()
        _type_digits(calc, "6")
        calc.input_operator("*")
        _type_digits(calc, "7")
        state = calc.evaluate()
        assert state.main_display == "42"

    def test_division_by_zero_error(self):
        """7 / 0 -> Error."""
        calc = ProgrammerLogic()
        _type_digits(calc, "7")
        calc.input_operator("/")
        _type_digits(calc, "0")
        state = calc.evaluate()
        assert state.error is True

    def test_modulo_by_zero_error(self):
        """7 % 0 -> Error."""
        calc = ProgrammerLogic()
        _type_digits(calc, "7")
        calc.input_operator("%")
        _type_digits(calc, "0")
        state = calc.evaluate()
        assert state.error is True

    def test_decimal_input_is_noop(self):
        """PM-3: decimal point is ignored in programmer mode."""
        calc = ProgrammerLogic()
        _type_digits(calc, "5")
        state = calc.input_decimal()
        assert state.main_display == "5"


# ── Bitwise operations ──────────────────────────────────────────

class TestBitwiseOperations:
    """BW-1 through BW-6: AND, OR, XOR, NOT, LSH, RSH."""

    def test_and(self):
        """BW-1: 12 AND 10 = 8."""
        calc = ProgrammerLogic()
        _type_digits(calc, "12")
        calc.bitwise_and()
        _type_digits(calc, "10")
        state = calc.evaluate()
        assert state.main_display == "8"

    def test_or(self):
        """BW-2: 12 OR 10 = 14."""
        calc = ProgrammerLogic()
        _type_digits(calc, "12")
        calc.bitwise_or()
        _type_digits(calc, "10")
        state = calc.evaluate()
        assert state.main_display == "14"

    def test_xor(self):
        """BW-3: 12 XOR 10 = 6."""
        calc = ProgrammerLogic()
        _type_digits(calc, "12")
        calc.bitwise_xor()
        _type_digits(calc, "10")
        state = calc.evaluate()
        assert state.main_display == "6"

    def test_not_zero_8bit(self):
        """BW-4: NOT 0 in 8-bit = -1 (all bits set)."""
        calc = ProgrammerLogic()
        calc.set_word_size(WordSize.BITS_8)
        _type_digits(calc, "0")
        state = calc.bitwise_not()
        assert state.main_display == "-1"

    def test_left_shift(self):
        """BW-5: 1 LSH 4 = 16."""
        calc = ProgrammerLogic()
        _type_digits(calc, "1")
        calc.left_shift()
        _type_digits(calc, "4")
        state = calc.evaluate()
        assert state.main_display == "16"

    def test_right_shift(self):
        """BW-6: 16 RSH 2 = 4."""
        calc = ProgrammerLogic()
        _type_digits(calc, "16")
        calc.right_shift()
        _type_digits(calc, "2")
        state = calc.evaluate()
        assert state.main_display == "4"


# ── Word size ────────────────────────────────────────────────────

class TestWordSize:
    """WS-1 through WS-3: overflow wrapping, word size change truncation."""

    def test_8bit_overflow_wraps(self):
        """WS-3: 127 + 1 = -128 in 8-bit mode."""
        calc = ProgrammerLogic()
        calc.set_word_size(WordSize.BITS_8)
        _type_digits(calc, "127")
        calc.input_operator("+")
        _type_digits(calc, "1")
        state = calc.evaluate()
        assert state.main_display == "-128"

    def test_word_size_change_truncates(self):
        """WS: switching from 64-bit to 8-bit with value 300 truncates."""
        calc = ProgrammerLogic()
        _type_digits(calc, "300")
        state = calc.set_word_size(WordSize.BITS_8)
        # 300 in 8-bit two's complement: 300 & 0xFF = 44, which is positive
        assert state.main_display == "44"

    def test_16bit_range(self):
        """16-bit max is 32767, overflow wraps."""
        calc = ProgrammerLogic()
        calc.set_word_size(WordSize.BITS_16)
        _type_digits(calc, "32767")
        calc.input_operator("+")
        _type_digits(calc, "1")
        state = calc.evaluate()
        assert state.main_display == "-32768"

    def test_word_size_displayed(self):
        """Word size is in the display state."""
        calc = ProgrammerLogic()
        assert calc.get_display_state().word_size == WordSize.BITS_64
        calc.set_word_size(WordSize.BITS_8)
        assert calc.get_display_state().word_size == WordSize.BITS_8


# ── Button enabling ──────────────────────────────────────────────

class TestButtonEnabling:
    """NB-8: only valid digits enabled for current base."""

    def test_bin_disables_2_through_f(self):
        """In BIN mode, only 0 and 1 are enabled."""
        calc = ProgrammerLogic()
        calc.set_base(NumberBase.BIN)
        buttons = calc.get_button_enabled_state()
        assert buttons["0"] is True
        assert buttons["1"] is True
        for d in "23456789":
            assert buttons[d.upper()] is False, f"Digit {d} should be disabled in BIN"
        for d in "ABCDEF":
            assert buttons[d] is False, f"Digit {d} should be disabled in BIN"

    def test_oct_disables_8_through_f(self):
        """In OCT mode, 0-7 enabled, 8-9 and A-F disabled."""
        calc = ProgrammerLogic()
        calc.set_base(NumberBase.OCT)
        buttons = calc.get_button_enabled_state()
        for d in "01234567":
            assert buttons[d.upper()] is True, f"Digit {d} should be enabled in OCT"
        for d in "89":
            assert buttons[d.upper()] is False, f"Digit {d} should be disabled in OCT"
        for d in "ABCDEF":
            assert buttons[d] is False, f"Digit {d} should be disabled in OCT"

    def test_dec_disables_a_through_f(self):
        """In DEC mode, 0-9 enabled, A-F disabled."""
        calc = ProgrammerLogic()
        buttons = calc.get_button_enabled_state()
        for d in "0123456789":
            assert buttons[d.upper()] is True
        for d in "ABCDEF":
            assert buttons[d] is False

    def test_hex_enables_all(self):
        """In HEX mode, all 0-F enabled."""
        calc = ProgrammerLogic()
        calc.set_base(NumberBase.HEX)
        buttons = calc.get_button_enabled_state()
        for d in "0123456789ABCDEF":
            assert buttons[d] is True, f"Digit {d} should be enabled in HEX"


# ── Hex input ────────────────────────────────────────────────────

class TestHexInput:
    """HX-1 through HX-3: entering hex digits A-F."""

    def test_enter_hex_digits(self):
        """Entering A-F in HEX mode works."""
        calc = ProgrammerLogic()
        calc.set_base(NumberBase.HEX)
        _type_digits(calc, "A")
        state = calc.get_display_state()
        assert state.main_display == "A"

    def test_hex_digits_uppercase(self):
        """HX-3: hex digits display uppercase."""
        calc = ProgrammerLogic()
        calc.set_base(NumberBase.HEX)
        # Type lowercase, should display uppercase
        _type_digits(calc, "ff")
        state = calc.get_display_state()
        assert state.main_display == "FF"

    def test_hex_digit_invalid_in_dec(self):
        """Hex digits are ignored in DEC mode."""
        calc = ProgrammerLogic()
        _type_digits(calc, "A")
        state = calc.get_display_state()
        assert state.main_display == "0"


# ── Edge cases ───────────────────────────────────────────────────

class TestProgrammerEdgeCases:
    """Negative numbers in different bases, sign toggle, backspace."""

    def test_negative_in_hex(self):
        """Negative value displayed in hex uses two's complement."""
        calc = ProgrammerLogic()
        calc.set_word_size(WordSize.BITS_8)
        _type_digits(calc, "1")
        calc.input_sign_toggle()
        state = calc.set_base(NumberBase.HEX)
        # -1 in 8-bit = 0xFF = "FF"
        assert state.main_display == "FF"

    def test_negative_in_bin(self):
        """Negative value displayed in bin uses two's complement."""
        calc = ProgrammerLogic()
        calc.set_word_size(WordSize.BITS_8)
        _type_digits(calc, "1")
        calc.input_sign_toggle()
        state = calc.set_base(NumberBase.BIN)
        # -1 in 8-bit = 0b11111111
        assert state.main_display == "11111111"

    def test_backspace(self):
        """Backspace removes last digit."""
        calc = ProgrammerLogic()
        _type_digits(calc, "123")
        state = calc.input_backspace()
        assert state.main_display == "12"

    def test_backspace_to_zero(self):
        """Backspace on single digit goes to 0."""
        calc = ProgrammerLogic()
        _type_digits(calc, "5")
        state = calc.input_backspace()
        assert state.main_display == "0"

    def test_clear_all(self):
        """Clear all resets to 0."""
        calc = ProgrammerLogic()
        _type_digits(calc, "255")
        state = calc.clear_all()
        assert state.main_display == "0"
        assert state.dec_value == "0"

    def test_evaluate_no_pending_op(self):
        """Evaluate with no pending op does nothing special."""
        calc = ProgrammerLogic()
        _type_digits(calc, "42")
        state = calc.evaluate()
        assert state.main_display == "42"
