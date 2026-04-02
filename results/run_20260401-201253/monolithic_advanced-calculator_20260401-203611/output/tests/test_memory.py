"""Tests for memory functions."""

import pytest

from calculator.logic.base_logic import Memory


class TestMemoryBasicOps:
    """Basic memory operation tests."""

    def test_store_and_recall(self) -> None:
        mem = Memory()
        mem.store(5.0)
        assert mem.recall() == 5.0

    def test_memory_add(self) -> None:
        mem = Memory()
        mem.store(5.0)
        mem.add(3.0)
        assert mem.recall() == 8.0

    def test_memory_subtract(self) -> None:
        mem = Memory()
        mem.store(10.0)
        mem.subtract(3.0)
        assert mem.recall() == 7.0

    def test_memory_clear(self) -> None:
        mem = Memory()
        mem.store(5.0)
        assert mem.has_value
        mem.clear()
        assert not mem.has_value
        assert mem.recall() == 0.0

    def test_has_value_indicator(self) -> None:
        mem = Memory()
        assert not mem.has_value
        mem.store(5.0)
        assert mem.has_value
        mem.clear()
        assert not mem.has_value


class TestMemoryEdgeCases:
    """Memory edge case tests."""

    def test_recall_empty(self) -> None:
        mem = Memory()
        assert mem.recall() == 0.0

    def test_multiple_stores(self) -> None:
        mem = Memory()
        mem.store(5.0)
        mem.store(10.0)
        assert mem.recall() == 10.0

    def test_add_to_empty(self) -> None:
        mem = Memory()
        mem.add(5.0)
        assert mem.recall() == 5.0
        assert mem.has_value

    def test_subtract_from_empty(self) -> None:
        mem = Memory()
        mem.subtract(5.0)
        assert mem.recall() == -5.0
        assert mem.has_value

    def test_store_zero(self) -> None:
        mem = Memory()
        mem.store(0.0)
        assert mem.has_value
        assert mem.recall() == 0.0

    def test_store_negative(self) -> None:
        mem = Memory()
        mem.store(-42.5)
        assert mem.recall() == -42.5

    def test_multiple_adds(self) -> None:
        mem = Memory()
        mem.add(1.0)
        mem.add(2.0)
        mem.add(3.0)
        assert mem.recall() == 6.0
