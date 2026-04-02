"""Tests for memory functions: MC/MR/M+/M-/MS, indicator, persistence."""

import pytest
from calculator.logic.basic_logic import BasicCalculator
from calculator.logic.scientific_logic import ScientificCalculator
from calculator.logic.programmer_logic import ProgrammerCalculator


@pytest.fixture
def calc():
    return BasicCalculator()


# =============================================================================
# Memory Functions -- Happy Path
# =============================================================================

class TestMemoryFunctions:

    def test_store_and_recall(self, calc):
        calc.memory_store(5.0)
        assert calc.memory_recall() == pytest.approx(5.0)

    def test_memory_add(self, calc):
        calc.memory_store(5.0)
        calc.memory_add(3.0)
        assert calc.memory_recall() == pytest.approx(8.0)

    def test_memory_subtract(self, calc):
        calc.memory_store(10.0)
        calc.memory_subtract(3.0)
        assert calc.memory_recall() == pytest.approx(7.0)

    def test_memory_clear(self, calc):
        calc.memory_store(5.0)
        calc.memory_clear()
        assert calc.memory_recall() == pytest.approx(0.0)

    def test_indicator_on_store(self, calc):
        calc.memory_store(5.0)
        assert calc.has_memory is True

    def test_indicator_off_after_clear(self, calc):
        calc.memory_store(5.0)
        calc.memory_clear()
        assert calc.has_memory is False

    def test_indicator_on_after_add(self, calc):
        calc.memory_add(3.0)
        assert calc.has_memory is True

    def test_indicator_on_after_subtract(self, calc):
        calc.memory_subtract(3.0)
        assert calc.has_memory is True


# =============================================================================
# Memory Functions -- Edge Cases
# =============================================================================

class TestMemoryEdgeCases:

    def test_recall_without_store(self, calc):
        assert calc.memory_recall() == pytest.approx(0.0)

    def test_overwrite_store(self, calc):
        calc.memory_store(5.0)
        calc.memory_store(10.0)
        assert calc.memory_recall() == pytest.approx(10.0)

    def test_negative_store(self, calc):
        calc.memory_store(-5.0)
        assert calc.memory_recall() == pytest.approx(-5.0)

    def test_add_negative(self, calc):
        calc.memory_store(10.0)
        calc.memory_add(-3.0)
        assert calc.memory_recall() == pytest.approx(7.0)

    def test_memory_has_memory_false_initially(self, calc):
        assert calc.has_memory is False


# =============================================================================
# Memory Across Different Calculator Types
# =============================================================================

class TestMemoryAcrossTypes:

    def test_scientific_memory(self):
        calc = ScientificCalculator()
        calc.memory_store(42.0)
        assert calc.memory_recall() == pytest.approx(42.0)
        assert calc.has_memory is True

    def test_programmer_memory(self):
        calc = ProgrammerCalculator()
        calc.memory_store(42.0)
        assert calc.memory_recall() == pytest.approx(42.0)
        assert calc.has_memory is True
