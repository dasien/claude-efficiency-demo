"""Tests for mode switching with value and state preservation."""

import pytest
from calculator.logic.basic_logic import BasicLogic
from calculator.logic.scientific_logic import ScientificLogic
from calculator.logic.programmer_logic import ProgrammerLogic


def switch_basic_to_scientific(basic: BasicLogic) -> ScientificLogic:
    """Simulate switching from basic to scientific mode."""
    value = basic.get_current_value()
    sci = ScientificLogic()
    sci.memory = basic.memory
    sci.has_memory = basic.has_memory
    sci.set_current_value(value)
    return sci


def switch_scientific_to_basic(sci: ScientificLogic) -> BasicLogic:
    """Simulate switching from scientific to basic mode."""
    value = sci.get_current_value()
    basic = BasicLogic()
    basic.memory = sci.memory
    basic.has_memory = sci.has_memory
    basic.set_current_value(value)
    return basic


def switch_basic_to_programmer(basic: BasicLogic) -> ProgrammerLogic:
    """Simulate switching from basic to programmer mode (truncate to int)."""
    value = basic.get_current_value()
    prog = ProgrammerLogic()
    prog.memory = basic.memory
    prog.has_memory = basic.has_memory
    prog.set_current_value(float(int(value)))
    return prog


def switch_programmer_to_basic(prog: ProgrammerLogic) -> BasicLogic:
    """Simulate switching from programmer to basic mode."""
    value = prog.get_current_value()
    basic = BasicLogic()
    basic.memory = prog.memory
    basic.has_memory = prog.has_memory
    basic.set_current_value(value)
    return basic


class TestValuePreservation:
    """Value is preserved when switching modes."""

    def test_basic_to_scientific_preserves_float(self):
        basic = BasicLogic()
        basic.input_digit("3")
        basic.input_decimal()
        basic.input_digit("1")
        basic.input_digit("4")
        sci = switch_basic_to_scientific(basic)
        assert sci.get_current_value() == pytest.approx(3.14)

    def test_scientific_to_basic_preserves_float(self):
        sci = ScientificLogic()
        sci.input_digit("2")
        sci.input_decimal()
        sci.input_digit("5")
        basic = switch_scientific_to_basic(sci)
        assert basic.get_current_value() == pytest.approx(2.5)

    def test_basic_to_programmer_truncates_to_int(self):
        basic = BasicLogic()
        basic.input_digit("3")
        basic.input_decimal()
        basic.input_digit("1")
        basic.input_digit("4")
        prog = switch_basic_to_programmer(basic)
        assert prog.get_current_int() == 3

    def test_programmer_to_basic_preserves_int(self):
        prog = ProgrammerLogic()
        prog.input_digit("2")
        prog.input_digit("5")
        prog.input_digit("5")
        basic = switch_programmer_to_basic(prog)
        assert basic.get_current_value() == 255.0
        assert basic.display_value == "255"

    def test_programmer_hex_to_basic(self):
        prog = ProgrammerLogic()
        prog.set_base(16)
        prog.input_digit("F")
        prog.input_digit("F")
        basic = switch_programmer_to_basic(prog)
        assert basic.get_current_value() == 255.0

    def test_basic_zero_preserved(self):
        basic = BasicLogic()
        sci = switch_basic_to_scientific(basic)
        assert sci.get_current_value() == 0.0

    def test_negative_value_preserved(self):
        basic = BasicLogic()
        basic.input_digit("5")
        basic.toggle_sign()
        sci = switch_basic_to_scientific(basic)
        assert sci.get_current_value() == -5.0


class TestStateReset:
    """Expression and error state are cleared on mode switch."""

    def test_expression_cleared_on_switch(self):
        basic = BasicLogic()
        basic.input_digit("5")
        basic.input_operator("+")
        basic.input_digit("3")
        # Don't evaluate — pending expression
        sci = switch_basic_to_scientific(basic)
        # The new logic should have clean expression state
        assert sci._tokens == []
        assert sci._pending_operator == ""

    def test_error_cleared_on_switch(self):
        basic = BasicLogic()
        basic.input_digit("1")
        basic.input_operator("/")
        basic.input_digit("0")
        basic.evaluate()
        assert basic.error is True
        # Switch — new logic starts clean
        sci = ScientificLogic()
        sci.memory = basic.memory
        sci.has_memory = basic.has_memory
        assert sci.error is False

    def test_memory_preserved_on_switch(self):
        basic = BasicLogic()
        basic.input_digit("4")
        basic.input_digit("2")
        basic.memory_store()
        sci = switch_basic_to_scientific(basic)
        assert sci.has_memory is True
        assert sci.memory == 42.0

    def test_memory_preserved_through_programmer(self):
        basic = BasicLogic()
        basic.input_digit("7")
        basic.memory_store()
        prog = switch_basic_to_programmer(basic)
        assert prog.has_memory is True
        assert prog.memory == 7.0
        basic2 = switch_programmer_to_basic(prog)
        assert basic2.has_memory is True
        assert basic2.memory == 7.0
