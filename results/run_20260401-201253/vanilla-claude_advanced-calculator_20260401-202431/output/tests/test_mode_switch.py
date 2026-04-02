"""Tests for mode switching with value preservation."""

import pytest
from calculator.logic.basic_logic import BasicCalculator
from calculator.logic.scientific_logic import ScientificCalculator
from calculator.logic.programmer_logic import ProgrammerCalculator


class TestModeSwitching:
    """Test value preservation when switching modes."""

    def test_basic_to_scientific(self):
        basic = BasicCalculator()
        scientific = ScientificCalculator()

        basic.input_digit("3")
        basic.input_decimal()
        basic.input_digit("1")
        basic.input_digit("4")

        value = basic.get_current_value()
        scientific.set_value(value)
        assert abs(scientific.get_current_value() - 3.14) < 1e-10

    def test_scientific_to_basic(self):
        scientific = ScientificCalculator()
        basic = BasicCalculator()

        scientific.input_digit("2")
        scientific.input_decimal()
        scientific.input_digit("5")

        value = scientific.get_current_value()
        basic.set_value(value)
        assert basic.get_current_value() == 2.5

    def test_basic_to_programmer_truncates(self):
        basic = BasicCalculator()
        programmer = ProgrammerCalculator()

        basic.input_digit("3")
        basic.input_decimal()
        basic.input_digit("1")
        basic.input_digit("4")

        value = basic.get_current_value()
        programmer.set_value(int(value))
        assert programmer.get_current_int_value() == 3

    def test_programmer_to_basic(self):
        programmer = ProgrammerCalculator()
        basic = BasicCalculator()

        programmer.input_digit("2")
        programmer.input_digit("5")
        programmer.input_digit("5")

        value = float(programmer.get_current_int_value())
        basic.set_value(value)
        assert basic.get_current_value() == 255.0

    def test_programmer_hex_to_basic(self):
        programmer = ProgrammerCalculator()
        basic = BasicCalculator()

        programmer.set_base("HEX")
        programmer.input_digit("F")
        programmer.input_digit("F")

        value = float(programmer.get_current_int_value())
        basic.set_value(value)
        assert basic.get_current_value() == 255.0

    def test_memory_preserved_across_modes(self):
        basic = BasicCalculator()
        scientific = ScientificCalculator()

        basic.input_digit("4")
        basic.input_digit("2")
        basic.memory_store()

        # Transfer memory
        scientific.memory = basic.memory
        scientific.has_memory = basic.has_memory

        assert scientific.has_memory is True
        scientific.memory_recall()
        assert scientific.get_current_value() == 42.0
