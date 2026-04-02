"""Tests for memory functions across all modes."""

import pytest
from calculator.logic.basic_logic import BasicCalculator
from calculator.logic.scientific_logic import ScientificCalculator
from calculator.logic.programmer_logic import ProgrammerCalculator


@pytest.fixture
def basic():
    return BasicCalculator()


@pytest.fixture
def scientific():
    return ScientificCalculator()


@pytest.fixture
def programmer():
    return ProgrammerCalculator()


class TestBasicMemory:
    """Test memory operations in basic mode."""

    def test_store_and_recall(self, basic):
        basic.input_digit("5")
        basic.memory_store()
        basic.all_clear()
        basic.memory_recall()
        assert basic.get_display_value() == "5"

    def test_memory_add(self, basic):
        basic.input_digit("5")
        basic.memory_store()
        basic.input_digit("3")
        basic.memory_add()
        basic.memory_recall()
        assert basic.get_display_value() == "8"

    def test_memory_subtract(self, basic):
        basic.input_digit("1")
        basic.input_digit("0")
        basic.memory_store()
        basic.input_digit("3")
        basic.memory_subtract()
        basic.memory_recall()
        assert basic.get_display_value() == "7"

    def test_memory_clear(self, basic):
        basic.input_digit("5")
        basic.memory_store()
        assert basic.has_memory is True
        basic.memory_clear()
        assert basic.has_memory is False

    def test_memory_indicator(self, basic):
        assert basic.has_memory is False
        basic.input_digit("5")
        basic.memory_store()
        assert basic.has_memory is True


class TestCrossModeMemory:
    """Test memory persistence across mode switches (simulated)."""

    def test_basic_to_scientific(self, basic, scientific):
        # Store in basic
        basic.input_digit("5")
        basic.memory_store()

        # Simulate mode switch: transfer memory
        scientific.memory = basic.memory
        scientific.has_memory = basic.has_memory

        scientific.memory_recall()
        assert scientific.get_display_value() == "5"

    def test_basic_to_programmer(self, basic, programmer):
        basic.input_digit("5")
        basic.memory_store()

        programmer.memory = basic.memory
        programmer.has_memory = basic.has_memory

        programmer.memory_recall()
        assert programmer.get_current_int_value() == 5
