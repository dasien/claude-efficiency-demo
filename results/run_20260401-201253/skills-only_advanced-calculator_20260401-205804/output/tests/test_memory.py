"""Tests for memory functions across all calculator modes."""

import pytest
from calculator.logic.basic_logic import BasicLogic
from calculator.logic.scientific_logic import ScientificLogic
from calculator.logic.programmer_logic import ProgrammerLogic


class TestMemoryBasic:
    """Memory operations in basic mode."""

    def test_memory_store_and_recall(self):
        calc = BasicLogic()
        calc.input_digit("5")
        calc.memory_store()
        assert calc.has_memory is True
        calc.input_digit("9")  # type something else
        calc.memory_recall()
        assert calc.display_value == "5"

    def test_memory_clear(self):
        calc = BasicLogic()
        calc.input_digit("5")
        calc.memory_store()
        assert calc.has_memory is True
        calc.memory_clear()
        assert calc.has_memory is False
        calc.memory_recall()
        assert calc.display_value == "0"

    def test_memory_add(self):
        calc = BasicLogic()
        calc.input_digit("5")
        calc.memory_store()
        calc.input_digit("3")
        calc.memory_add()
        calc.memory_recall()
        assert calc.display_value == "8"

    def test_memory_subtract(self):
        calc = BasicLogic()
        calc.input_digit("1")
        calc.input_digit("0")
        calc.memory_store()
        calc.input_digit("3")
        calc.memory_subtract()
        calc.memory_recall()
        assert calc.display_value == "7"

    def test_has_memory_initially_false(self):
        calc = BasicLogic()
        assert calc.has_memory is False

    def test_memory_indicator_after_store(self):
        calc = BasicLogic()
        calc.input_digit("5")
        calc.memory_store()
        assert calc.has_memory is True

    def test_memory_indicator_after_clear(self):
        calc = BasicLogic()
        calc.input_digit("5")
        calc.memory_store()
        calc.memory_clear()
        assert calc.has_memory is False

    def test_memory_add_without_store(self):
        calc = BasicLogic()
        calc.input_digit("5")
        calc.memory_add()
        assert calc.has_memory is True
        calc.memory_recall()
        assert calc.display_value == "5"

    def test_memory_subtract_without_store(self):
        calc = BasicLogic()
        calc.input_digit("3")
        calc.memory_subtract()
        calc.memory_recall()
        assert calc.display_value == "-3"


class TestMemoryScientific:
    """Memory operations in scientific mode."""

    def test_memory_store_recall(self):
        calc = ScientificLogic()
        calc.input_digit("4")
        calc.input_digit("2")
        calc.memory_store()
        calc.input_digit("0")
        calc.memory_recall()
        assert calc.display_value == "42"

    def test_memory_with_scientific_function(self):
        calc = ScientificLogic()
        calc.display_value = "25"
        calc.input_mode = "typing"
        calc.apply_function("sqrt")
        calc.memory_store()
        calc.input_digit("0")
        calc.memory_recall()
        assert calc.display_value == "5"


class TestMemoryProgrammer:
    """Memory operations in programmer mode."""

    def test_memory_store_recall(self):
        calc = ProgrammerLogic()
        calc.input_digit("1")
        calc.input_digit("0")
        calc.memory_store()
        calc.input_digit("0")
        calc.memory_recall()
        assert calc.get_current_int() == 10

    def test_memory_in_hex_mode(self):
        calc = ProgrammerLogic()
        calc.set_base(16)
        calc.input_digit("F")
        calc.input_digit("F")
        calc.memory_store()
        calc.input_digit("0")
        calc.memory_recall()
        assert calc.get_current_int() == 255


class TestMemoryAcrossModes:
    """Memory persists across mode switches."""

    def test_basic_to_scientific(self):
        basic = BasicLogic()
        basic.input_digit("4")
        basic.input_digit("2")
        basic.memory_store()

        sci = ScientificLogic()
        sci.memory = basic.memory
        sci.has_memory = basic.has_memory
        sci.memory_recall()
        assert sci.display_value == "42"
        assert sci.has_memory is True

    def test_scientific_to_basic(self):
        sci = ScientificLogic()
        sci.input_digit("9")
        sci.input_digit("9")
        sci.memory_store()

        basic = BasicLogic()
        basic.memory = sci.memory
        basic.has_memory = sci.has_memory
        basic.memory_recall()
        assert basic.display_value == "99"

    def test_basic_to_programmer(self):
        basic = BasicLogic()
        basic.input_digit("7")
        basic.memory_store()

        prog = ProgrammerLogic()
        prog.memory = basic.memory
        prog.has_memory = basic.has_memory
        prog.memory_recall()
        assert prog.get_current_int() == 7

    def test_memory_persists_through_mode_switch(self):
        calc = BasicLogic()
        calc.input_digit("5")
        calc.memory_store()
        assert calc.has_memory is True

        # Simulate mode switch: transfer memory
        new_calc = ScientificLogic()
        new_calc.memory = calc.memory
        new_calc.has_memory = calc.has_memory
        assert new_calc.has_memory is True
        new_calc.memory_recall()
        assert new_calc.display_value == "5"
