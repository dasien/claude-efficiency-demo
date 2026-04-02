"""Tests for mode switching: value preservation, truncation, memory across modes."""

import pytest
from calculator.logic.basic_logic import BasicLogic
from calculator.logic.scientific_logic import ScientificLogic
from calculator.logic.programmer_logic import ProgrammerLogic
from calculator.logic.base_logic import NumberBase


# ── Helpers ──────────────────────────────────────────────────────

def _type_digits(calc, digits: str) -> None:
    """Type a sequence of digit characters."""
    for ch in digits:
        if ch == ".":
            calc.input_decimal()
        else:
            calc.input_digit(ch)


def _switch_mode(source, target_class):
    """Transfer value from source calculator to a new target calculator.

    Returns the new calculator instance with the value set.
    """
    value = source.get_current_value()
    target = target_class()
    # Preserve memory
    target._memory = source._memory
    target.set_current_value(value)
    return target


# ── Basic <-> Scientific ─────────────────────────────────────────

class TestBasicScientificSwitch:
    """MS-3: value preserved when switching between Basic and Scientific."""

    def test_basic_to_scientific_preserves_value(self):
        """MS-3: switching Basic -> Scientific preserves display value."""
        basic = BasicLogic()
        _type_digits(basic, "42")
        sci = _switch_mode(basic, ScientificLogic)
        state = sci.get_display_state()
        assert state.main_display == "42"

    def test_scientific_to_basic_preserves_value(self):
        """MS-3: switching Scientific -> Basic preserves display value."""
        sci = ScientificLogic()
        _type_digits(sci, "99")
        basic = _switch_mode(sci, BasicLogic)
        state = basic.get_display_state()
        assert state.main_display == "99"

    def test_float_preserved_basic_to_scientific(self):
        """Float values are preserved between Basic and Scientific."""
        basic = BasicLogic()
        _type_digits(basic, "3.14")
        sci = _switch_mode(basic, ScientificLogic)
        state = sci.get_display_state()
        assert state.main_display == "3.14"

    def test_float_preserved_scientific_to_basic(self):
        """Float values are preserved between Scientific and Basic."""
        sci = ScientificLogic()
        _type_digits(sci, "2.718")
        basic = _switch_mode(sci, BasicLogic)
        state = basic.get_display_state()
        assert state.main_display == "2.718"


# ── Basic/Scientific -> Programmer ───────────────────────────────

class TestToProgrammerSwitch:
    """MS-4: value truncated to integer when switching to Programmer."""

    def test_basic_to_programmer_truncates_float(self):
        """MS-4: 3.14 in Basic -> 3 in Programmer."""
        basic = BasicLogic()
        _type_digits(basic, "3.14")
        prog = _switch_mode(basic, ProgrammerLogic)
        state = prog.get_display_state()
        assert state.main_display == "3"

    def test_scientific_to_programmer_truncates(self):
        """MS-4: 9.99 in Scientific -> 9 in Programmer."""
        sci = ScientificLogic()
        _type_digits(sci, "9.99")
        prog = _switch_mode(sci, ProgrammerLogic)
        state = prog.get_display_state()
        assert state.main_display == "9"

    def test_integer_preserved_to_programmer(self):
        """Integer values are preserved when going to Programmer."""
        basic = BasicLogic()
        _type_digits(basic, "42")
        prog = _switch_mode(basic, ProgrammerLogic)
        state = prog.get_display_state()
        assert state.main_display == "42"

    def test_negative_float_truncated_to_programmer(self):
        """Negative float truncated: -3.99 -> -3."""
        basic = BasicLogic()
        _type_digits(basic, "3.99")
        basic.input_sign_toggle()
        prog = _switch_mode(basic, ProgrammerLogic)
        state = prog.get_display_state()
        assert state.main_display == "-3"


# ── Programmer -> Basic/Scientific ───────────────────────────────

class TestFromProgrammerSwitch:
    """MS-5: integer value preserved when switching from Programmer."""

    def test_programmer_hex_ff_to_basic(self):
        """MS-5: FF (hex 255) in Programmer -> 255 in Basic."""
        prog = ProgrammerLogic()
        prog.set_base(NumberBase.HEX)
        _type_digits(prog, "FF")
        basic = _switch_mode(prog, BasicLogic)
        state = basic.get_display_state()
        assert state.main_display == "255"

    def test_programmer_dec_to_scientific(self):
        """Programmer 100 -> Scientific 100."""
        prog = ProgrammerLogic()
        _type_digits(prog, "100")
        sci = _switch_mode(prog, ScientificLogic)
        state = sci.get_display_state()
        assert state.main_display == "100"

    def test_programmer_negative_to_basic(self):
        """Negative programmer value preserved to basic."""
        prog = ProgrammerLogic()
        _type_digits(prog, "5")
        prog.input_sign_toggle()
        basic = _switch_mode(prog, BasicLogic)
        state = basic.get_display_state()
        assert state.main_display == "-5"


# ── Memory preserved across mode switches ────────────────────────

class TestMemoryAcrossModes:
    """MF-7: memory persists across mode switches."""

    def test_memory_from_basic_to_scientific(self):
        """Store in Basic, recall in Scientific."""
        basic = BasicLogic()
        _type_digits(basic, "42")
        basic.memory_store()
        sci = _switch_mode(basic, ScientificLogic)
        state = sci.memory_recall()
        assert state.main_display == "42"

    def test_memory_from_scientific_to_basic(self):
        """Store in Scientific, recall in Basic."""
        sci = ScientificLogic()
        _type_digits(sci, "99")
        sci.memory_store()
        basic = _switch_mode(sci, BasicLogic)
        state = basic.memory_recall()
        assert state.main_display == "99"

    def test_memory_from_basic_to_programmer(self):
        """Store in Basic, recall in Programmer (float memory -> int display)."""
        basic = BasicLogic()
        _type_digits(basic, "50")
        basic.memory_store()
        prog = _switch_mode(basic, ProgrammerLogic)
        state = prog.memory_recall()
        assert state.main_display == "50"

    def test_has_memory_preserved(self):
        """has_memory flag preserved after mode switch."""
        basic = BasicLogic()
        _type_digits(basic, "5")
        basic.memory_store()
        sci = _switch_mode(basic, ScientificLogic)
        assert sci.has_memory is True


# ── Error state cleared on switch ────────────────────────────────

class TestErrorClearedOnSwitch:
    """Error state is cleared when switching modes (set_current_value resets error)."""

    def test_error_cleared_basic_to_scientific(self):
        """Error in Basic is cleared when switching to Scientific."""
        basic = BasicLogic()
        _type_digits(basic, "1")
        basic.input_operator("/")
        _type_digits(basic, "0")
        basic.evaluate()
        assert basic.get_display_state().error is True
        # Switch: get_current_value returns 0.0 on error (can't parse "Error")
        sci = ScientificLogic()
        sci.set_current_value(0.0)
        state = sci.get_display_state()
        assert state.error is False

    def test_error_cleared_scientific_to_programmer(self):
        """Error in Scientific is cleared when switching to Programmer."""
        sci = ScientificLogic()
        _type_digits(sci, "1")
        sci.input_sign_toggle()
        sci.root_square()  # sqrt(-1) -> Error
        assert sci.get_display_state().error is True
        prog = ProgrammerLogic()
        prog.set_current_value(0.0)
        state = prog.get_display_state()
        assert state.error is False
