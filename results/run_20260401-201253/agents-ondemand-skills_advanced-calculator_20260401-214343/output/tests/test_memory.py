"""Tests for memory functions: MS, MR, M+, M-, MC across all logic classes."""

import pytest
from calculator.logic.basic_logic import BasicLogic
from calculator.logic.scientific_logic import ScientificLogic
from calculator.logic.programmer_logic import ProgrammerLogic


# ── Helpers ──────────────────────────────────────────────────────

def _type_digits(calc, digits: str) -> None:
    """Type a sequence of digit characters."""
    for ch in digits:
        calc.input_digit(ch)


# ── Memory Store and Recall ──────────────────────────────────────

class TestMemoryStoreRecall:
    """MF-2, MF-5: store and recall."""

    def test_store_and_recall(self):
        """Store 5, recall shows 5."""
        calc = BasicLogic()
        _type_digits(calc, "5")
        calc.memory_store()
        calc.clear_all()
        state = calc.memory_recall()
        assert state.main_display == "5"

    def test_store_replaces_previous(self):
        """Storing overwrites previous memory."""
        calc = BasicLogic()
        _type_digits(calc, "5")
        calc.memory_store()
        calc.clear_all()
        _type_digits(calc, "10")
        calc.memory_store()
        calc.clear_all()
        state = calc.memory_recall()
        assert state.main_display == "10"


# ── Memory Add ───────────────────────────────────────────────────

class TestMemoryAdd:
    """MF-3: M+ adds display to memory."""

    def test_memory_add(self):
        """Store 5, add 3, recall shows 8."""
        calc = BasicLogic()
        _type_digits(calc, "5")
        calc.memory_store()
        calc.clear_all()
        _type_digits(calc, "3")
        calc.memory_add()
        state = calc.memory_recall()
        assert state.main_display == "8"

    def test_memory_add_from_zero(self):
        """M+ on empty memory (0) with display 7 -> recall 7."""
        calc = BasicLogic()
        _type_digits(calc, "7")
        calc.memory_add()
        calc.clear_all()
        state = calc.memory_recall()
        assert state.main_display == "7"


# ── Memory Subtract ──────────────────────────────────────────────

class TestMemorySubtract:
    """MF-4: M- subtracts display from memory."""

    def test_memory_subtract(self):
        """Store 10, subtract 3, recall shows 7."""
        calc = BasicLogic()
        _type_digits(calc, "10")
        calc.memory_store()
        calc.clear_all()
        _type_digits(calc, "3")
        calc.memory_subtract()
        state = calc.memory_recall()
        assert state.main_display == "7"


# ── Memory Clear ─────────────────────────────────────────────────

class TestMemoryClear:
    """MF-1: MC clears memory."""

    def test_memory_clear_removes_indicator(self):
        """After MC, has_memory is False and indicator is off."""
        calc = BasicLogic()
        _type_digits(calc, "5")
        calc.memory_store()
        assert calc.has_memory is True
        calc.memory_clear()
        assert calc.has_memory is False
        state = calc.get_display_state()
        assert state.memory_indicator is False

    def test_recall_after_clear_is_zero(self):
        """After MC, recall gives 0."""
        calc = BasicLogic()
        _type_digits(calc, "5")
        calc.memory_store()
        calc.memory_clear()
        state = calc.memory_recall()
        assert state.main_display == "0"


# ── Memory Indicator ─────────────────────────────────────────────

class TestMemoryIndicator:
    """MF-6: visual indicator for memory."""

    def test_no_memory_initially(self):
        """Initially, no memory is stored."""
        calc = BasicLogic()
        assert calc.has_memory is False
        assert calc.get_display_state().memory_indicator is False

    def test_indicator_after_store(self):
        """After storing, indicator is on."""
        calc = BasicLogic()
        _type_digits(calc, "5")
        calc.memory_store()
        assert calc.has_memory is True
        assert calc.get_display_state().memory_indicator is True

    def test_indicator_off_when_zero_stored(self):
        """Storing 0 means has_memory is False (0.0 == 0)."""
        calc = BasicLogic()
        _type_digits(calc, "0")
        calc.memory_store()
        assert calc.has_memory is False


# ── Memory persists across clear_all ─────────────────────────────

class TestMemoryPersistence:
    """Memory is NOT cleared by clear_all (only MC clears it)."""

    def test_memory_survives_clear_all(self):
        calc = BasicLogic()
        _type_digits(calc, "42")
        calc.memory_store()
        calc.clear_all()
        assert calc.has_memory is True
        state = calc.memory_recall()
        assert state.main_display == "42"


# ── Memory works with all logic classes ──────────────────────────

class TestMemoryAllModes:
    """Memory operations work identically on Basic, Scientific, Programmer."""

    @pytest.mark.parametrize("LogicClass", [BasicLogic, ScientificLogic, ProgrammerLogic])
    def test_store_recall(self, LogicClass):
        calc = LogicClass()
        _type_digits(calc, "9")
        calc.memory_store()
        calc.clear_all()
        state = calc.memory_recall()
        assert state.main_display == "9"

    @pytest.mark.parametrize("LogicClass", [BasicLogic, ScientificLogic, ProgrammerLogic])
    def test_memory_add(self, LogicClass):
        calc = LogicClass()
        _type_digits(calc, "4")
        calc.memory_store()
        calc.clear_all()
        _type_digits(calc, "6")
        calc.memory_add()
        state = calc.memory_recall()
        assert state.main_display == "10"

    @pytest.mark.parametrize("LogicClass", [BasicLogic, ScientificLogic, ProgrammerLogic])
    def test_memory_subtract(self, LogicClass):
        calc = LogicClass()
        _type_digits(calc, "10")
        calc.memory_store()
        calc.clear_all()
        _type_digits(calc, "3")
        calc.memory_subtract()
        state = calc.memory_recall()
        assert state.main_display == "7"

    @pytest.mark.parametrize("LogicClass", [BasicLogic, ScientificLogic, ProgrammerLogic])
    def test_memory_clear(self, LogicClass):
        calc = LogicClass()
        _type_digits(calc, "5")
        calc.memory_store()
        calc.memory_clear()
        assert calc.has_memory is False

    @pytest.mark.parametrize("LogicClass", [BasicLogic, ScientificLogic, ProgrammerLogic])
    def test_has_memory_property(self, LogicClass):
        calc = LogicClass()
        assert calc.has_memory is False
        _type_digits(calc, "1")
        calc.memory_store()
        assert calc.has_memory is True
