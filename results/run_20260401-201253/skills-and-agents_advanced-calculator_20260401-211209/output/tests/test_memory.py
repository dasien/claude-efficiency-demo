"""Tests for memory functions across calculator types."""

import pytest

from calculator.logic.basic_logic import BasicCalculator
from calculator.logic.scientific_logic import ScientificCalculator
from calculator.logic.programmer_logic import ProgrammerCalculator


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def basic_calc() -> BasicCalculator:
    """Return a fresh BasicCalculator."""
    return BasicCalculator()


@pytest.fixture
def sci_calc() -> ScientificCalculator:
    """Return a fresh ScientificCalculator."""
    return ScientificCalculator()


@pytest.fixture
def prog_calc() -> ProgrammerCalculator:
    """Return a fresh ProgrammerCalculator."""
    return ProgrammerCalculator()


# ---------------------------------------------------------------------------
# MF-1..6  Memory operations (using BasicCalculator)
# ---------------------------------------------------------------------------

class TestMemoryOperations:
    """MF-1..6: core memory store / clear / recall / plus / minus."""

    def test_ms_stores_value_and_sets_flag(self, basic_calc):
        """MF-1: ms() stores current value, has_memory becomes True."""
        basic_calc.current_value = 42.0
        basic_calc.ms()
        assert basic_calc.has_memory is True
        assert basic_calc.memory == 42.0

    def test_mc_clears_memory(self, basic_calc):
        """MF-2: mc() clears memory and sets has_memory False."""
        basic_calc.current_value = 10.0
        basic_calc.ms()
        basic_calc.mc()
        assert basic_calc.has_memory is False
        assert basic_calc.memory == 0.0

    def test_mr_returns_stored_value(self, basic_calc):
        """MF-3: mr() returns the value previously stored."""
        basic_calc.current_value = 7.5
        basic_calc.ms()
        basic_calc.current_value = 0.0
        result = basic_calc.mr()
        assert result == 7.5
        assert basic_calc.current_value == 7.5

    def test_m_plus_adds_to_memory(self, basic_calc):
        """MF-4: store 5, then m_plus with current_value=3, mr returns 8."""
        basic_calc.current_value = 5.0
        basic_calc.ms()
        basic_calc.current_value = 3.0
        basic_calc.m_plus()
        result = basic_calc.mr()
        assert result == 8.0

    def test_m_minus_subtracts_from_memory(self, basic_calc):
        """MF-5: store 10, then m_minus with current_value=3, mr returns 7."""
        basic_calc.current_value = 10.0
        basic_calc.ms()
        basic_calc.current_value = 3.0
        basic_calc.m_minus()
        result = basic_calc.mr()
        assert result == 7.0


# ---------------------------------------------------------------------------
# MF-7  Memory across calculator types
# ---------------------------------------------------------------------------

class TestMemoryAcrossTypes:
    """MF-7: memory behaves identically across all calculator types."""

    @pytest.mark.parametrize(
        "calc_fixture",
        ["basic_calc", "sci_calc", "prog_calc"],
        ids=["basic", "scientific", "programmer"],
    )
    def test_store_and_recall(self, calc_fixture, request):
        """Store and recall works on every calculator type."""
        calc = request.getfixturevalue(calc_fixture)
        calc.current_value = 99.0
        calc.ms()
        assert calc.has_memory is True
        calc.current_value = 0.0
        result = calc.mr()
        assert result == 99.0

    def test_memory_transfer_between_modes(self, basic_calc, sci_calc):
        """Simulate mode switch: store in basic, copy to scientific, recall."""
        basic_calc.current_value = 55.0
        basic_calc.ms()

        # Simulate mode switch by copying memory
        sci_calc.memory = basic_calc.memory
        sci_calc.has_memory = basic_calc.has_memory

        result = sci_calc.mr()
        assert result == 55.0


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestMemoryEdgeCases:
    """Edge-case behaviour of the memory subsystem."""

    def test_mr_with_no_stored_value_returns_zero(self, basic_calc):
        """mr() with no prior ms() returns 0."""
        result = basic_calc.mr()
        assert result == 0.0

    def test_m_plus_with_no_stored_value(self, basic_calc):
        """m_plus when memory is 0 (no prior store) adds to zero."""
        basic_calc.current_value = 4.0
        basic_calc.m_plus()
        result = basic_calc.mr()
        assert result == 4.0

    def test_m_minus_with_no_stored_value(self, basic_calc):
        """m_minus when memory is 0 subtracts from zero."""
        basic_calc.current_value = 3.0
        basic_calc.m_minus()
        result = basic_calc.mr()
        assert result == -3.0

    def test_mc_when_already_clear_is_noop(self, basic_calc):
        """mc() on already-clear memory is a harmless no-op."""
        basic_calc.mc()
        assert basic_calc.has_memory is False
        assert basic_calc.memory == 0.0

    def test_multiple_ms_overwrites(self, basic_calc):
        """Multiple ms() calls overwrite previous stored value."""
        basic_calc.current_value = 1.0
        basic_calc.ms()
        basic_calc.current_value = 2.0
        basic_calc.ms()
        basic_calc.current_value = 3.0
        basic_calc.ms()
        result = basic_calc.mr()
        assert result == 3.0
