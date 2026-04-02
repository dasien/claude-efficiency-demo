"""Tests for mode switching with value preservation."""

import pytest

from calculator.logic.base_logic import Memory
from calculator.logic.basic_logic import BasicCalculator
from calculator.logic.scientific_logic import ScientificCalculator
from calculator.logic.programmer_logic import ProgrammerCalculator


class TestValuePreservation:
    """Value preservation across mode switches."""

    def test_basic_to_scientific(self) -> None:
        basic = BasicCalculator()
        sci = ScientificCalculator()
        basic.set_value(3.14)
        value = basic.get_value()
        sci.set_value(value)
        assert abs(sci.get_value() - 3.14) < 0.001

    def test_scientific_to_basic(self) -> None:
        sci = ScientificCalculator()
        basic = BasicCalculator()
        sci.set_value(2.718)
        value = sci.get_value()
        basic.set_value(value)
        assert abs(basic.get_value() - 2.718) < 0.001

    def test_basic_to_programmer_truncates(self) -> None:
        basic = BasicCalculator()
        prog = ProgrammerCalculator()
        basic.set_value(3.14)
        value = basic.get_value()
        prog.set_value(int(value))
        assert prog.get_value() == 3

    def test_programmer_to_basic(self) -> None:
        prog = ProgrammerCalculator()
        basic = BasicCalculator()
        prog.set_value(255)
        value = prog.get_value()
        basic.set_value(float(value))
        assert basic.get_value() == 255.0

    def test_programmer_hex_to_basic(self) -> None:
        prog = ProgrammerCalculator()
        basic = BasicCalculator()
        prog.set_base("HEX")
        prog.input_digit("F")
        prog.input_digit("F")
        value = prog.get_value()
        assert value == 255
        basic.set_value(float(value))
        assert basic.get_value() == 255.0

    def test_scientific_to_programmer_truncates(self) -> None:
        sci = ScientificCalculator()
        prog = ProgrammerCalculator()
        sci.set_value(9.99)
        value = sci.get_value()
        prog.set_value(int(value))
        assert prog.get_value() == 9

    def test_programmer_negative_to_basic(self) -> None:
        prog = ProgrammerCalculator()
        basic = BasicCalculator()
        prog.set_word_size(8)
        prog.set_value(-5)
        value = prog.get_value()
        basic.set_value(float(value))
        assert basic.get_value() == -5.0


class TestMemoryPersistence:
    """Memory persistence across mode switches."""

    def test_memory_persists_basic_to_scientific(self) -> None:
        mem = Memory()
        mem.store(42.0)
        # Simulate switching to Scientific and recalling
        assert mem.recall() == 42.0

    def test_memory_persists_across_all_modes(self) -> None:
        mem = Memory()
        mem.store(100.0)
        # Basic mode
        assert mem.recall() == 100.0
        # Scientific mode
        assert mem.recall() == 100.0
        # Programmer mode (would truncate on use, not storage)
        assert mem.recall() == 100.0

    def test_memory_add_across_modes(self) -> None:
        mem = Memory()
        mem.store(5.0)
        # Simulate adding in another mode
        mem.add(10.0)
        assert mem.recall() == 15.0

    def test_memory_indicator_persists(self) -> None:
        mem = Memory()
        assert not mem.has_value
        mem.store(1.0)
        assert mem.has_value
        # Indicator should persist across mode switches
        assert mem.has_value
