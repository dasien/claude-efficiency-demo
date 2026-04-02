"""Tests for mode switching: value preservation, truncation, memory persistence."""

import pytest
from calculator.logic.basic_logic import BasicCalculator
from calculator.logic.scientific_logic import ScientificCalculator
from calculator.logic.programmer_logic import ProgrammerCalculator


def enter_number(calc, number_str):
    """Enter a multi-digit number into the calculator."""
    for ch in str(number_str):
        if ch == ".":
            calc.append_decimal()
        else:
            calc.append_digit(ch)


# =============================================================================
# Value Preservation: Basic <-> Scientific
# =============================================================================

class TestBasicScientificSwitch:

    def test_basic_to_scientific_preserves_value(self):
        """MS-3: Switching Basic -> Scientific preserves 3.14."""
        basic = BasicCalculator()
        enter_number(basic, "3.14")
        value = basic.get_current_value()

        sci = ScientificCalculator()
        sci.current_input = str(value)
        assert sci.get_current_value() == pytest.approx(3.14)

    def test_scientific_to_basic_preserves_value(self):
        """MS-3: Switching Scientific -> Basic preserves 2.718."""
        sci = ScientificCalculator()
        enter_number(sci, "2.718")
        value = sci.get_current_value()

        basic = BasicCalculator()
        basic.current_input = str(value)
        assert basic.get_current_value() == pytest.approx(2.718)


# =============================================================================
# Value Truncation: -> Programmer
# =============================================================================

class TestToProgrammerSwitch:

    def test_basic_to_programmer_truncates(self):
        """MS-4: Switching Basic(3.14) -> Programmer gives 3."""
        basic = BasicCalculator()
        enter_number(basic, "3.14")
        value = basic.get_current_value()

        prog = ProgrammerCalculator()
        int_val = int(value)
        prog.value = int_val
        prog.current_input = str(int_val)
        assert prog.get_current_value() == pytest.approx(3)

    def test_scientific_to_programmer_truncates_negative(self):
        """MS-4: Switching Scientific(-7.9) -> Programmer gives -7."""
        sci = ScientificCalculator()
        # Enter 7.9 and negate
        enter_number(sci, "7.9")
        value = sci.get_current_value()
        value = sci.toggle_sign(value)

        prog = ProgrammerCalculator()
        int_val = int(value)
        prog.value = int_val
        prog.current_input = str(int_val)
        assert prog.get_current_value() == pytest.approx(-7)


# =============================================================================
# Value Preservation: Programmer -> Basic/Scientific
# =============================================================================

class TestFromProgrammerSwitch:

    def test_programmer_dec_to_basic(self):
        """MS-5: Switching Programmer(255 DEC) -> Basic gives 255."""
        prog = ProgrammerCalculator()
        enter_number(prog, "255")
        value = prog.get_current_value()

        basic = BasicCalculator()
        basic.current_input = str(int(value))
        assert basic.get_current_value() == pytest.approx(255)

    def test_programmer_hex_to_basic(self):
        """MS-5: Programmer showing FF (hex) -> Basic gives 255."""
        prog = ProgrammerCalculator()
        prog.set_base(16)
        prog.append_digit("F")
        prog.append_digit("F")
        value = prog.get_current_value()  # Should be 255.0

        basic = BasicCalculator()
        basic.current_input = str(int(value))
        assert basic.get_current_value() == pytest.approx(255)


# =============================================================================
# Memory Persistence Across Mode Switches
# =============================================================================

class TestMemoryPersistence:

    def test_memory_basic_to_scientific(self):
        """MF-7: Memory stored in Basic persists to Scientific."""
        basic = BasicCalculator()
        basic.memory_store(42.0)
        assert basic.has_memory is True

        # Simulate mode switch: transfer memory
        sci = ScientificCalculator()
        sci.memory = basic.memory
        sci.has_memory = basic.has_memory
        assert sci.memory_recall() == pytest.approx(42.0)

    def test_memory_basic_to_programmer(self):
        """MF-7: Memory stored in Basic persists to Programmer."""
        basic = BasicCalculator()
        basic.memory_store(42.0)

        prog = ProgrammerCalculator()
        prog.memory = basic.memory
        prog.has_memory = basic.has_memory
        assert prog.memory_recall() == pytest.approx(42.0)

    def test_has_memory_persists(self):
        """MF-7: has_memory flag persists across mode switches."""
        basic = BasicCalculator()
        basic.memory_store(42.0)
        assert basic.has_memory is True

        sci = ScientificCalculator()
        sci.memory = basic.memory
        sci.has_memory = basic.has_memory
        assert sci.has_memory is True
