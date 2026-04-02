"""Tests for value and memory transfer between calculator modes."""

import pytest

from calculator.logic.basic_logic import BasicCalculator
from calculator.logic.scientific_logic import ScientificCalculator
from calculator.logic.programmer_logic import ProgrammerCalculator


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def transfer_value(source, target):
    """Transfer value from source calculator to target calculator.

    Rules:
        - Basic <-> Scientific: preserve float
        - To Programmer: int(value), then mask_value
        - From Programmer: float(value)
    """
    if isinstance(target, ProgrammerCalculator):
        target.current_value = target.mask_value(int(source.current_value))
    elif isinstance(source, ProgrammerCalculator):
        target.current_value = float(source.current_value)
    else:
        # Basic <-> Scientific: preserve float
        target.current_value = source.current_value


def transfer_memory(source, target):
    """Transfer memory state from source to target calculator."""
    target.memory = source.memory
    target.has_memory = source.has_memory


# ---------------------------------------------------------------------------
# MS-3..5: Value Preservation (parametrized)
# ---------------------------------------------------------------------------

class TestValuePreservation:
    """Tests for value transfer between calculator modes."""

    @pytest.mark.parametrize(
        "source_cls, target_cls, source_value, expected",
        [
            (BasicCalculator, ScientificCalculator, 3.14, 3.14),
            (ScientificCalculator, ProgrammerCalculator, 3.14, 3),
            (ProgrammerCalculator, BasicCalculator, 255, 255.0),
        ],
        ids=["MS-3-basic-to-sci", "MS-4-sci-to-prog", "MS-5-prog-to-basic"],
    )
    def test_value_transfer(self, source_cls, target_cls, source_value, expected):
        """Value transfers correctly between calculator modes."""
        source = source_cls()
        source.current_value = source_value
        target = target_cls()
        transfer_value(source, target)
        assert target.current_value == expected

    def test_programmer_hex_to_basic(self):
        """MS-5b: Programmer hex FF (255) transfers to Basic as 255.0."""
        source = ProgrammerCalculator()
        source.set_base("HEX")
        source.append_hex_digit("F")
        source.append_hex_digit("F")
        assert source.current_value == 255

        target = BasicCalculator()
        transfer_value(source, target)
        assert target.current_value == 255.0


# ---------------------------------------------------------------------------
# Memory Preservation
# ---------------------------------------------------------------------------

class TestMemoryPreservation:
    """Tests for memory transfer between calculator modes."""

    def test_memory_basic_to_scientific(self):
        """Store 42 in Basic, transfer memory to Scientific, recall returns 42."""
        basic = BasicCalculator()
        basic.current_value = 42.0
        basic.ms()
        assert basic.has_memory is True

        sci = ScientificCalculator()
        transfer_memory(basic, sci)
        assert sci.has_memory is True
        recalled = sci.mr()
        assert recalled == 42.0

    def test_memory_basic_to_programmer(self):
        """Store 42 in Basic, transfer to Programmer, recall returns 42."""
        basic = BasicCalculator()
        basic.current_value = 42.0
        basic.ms()

        prog = ProgrammerCalculator()
        transfer_memory(basic, prog)
        assert prog.has_memory is True
        recalled = prog.mr()
        assert recalled == 42.0


# ---------------------------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Edge cases for mode switching."""

    @pytest.mark.parametrize(
        "source_cls, target_cls",
        [
            (BasicCalculator, ScientificCalculator),
            (ScientificCalculator, BasicCalculator),
            (BasicCalculator, ProgrammerCalculator),
            (ProgrammerCalculator, BasicCalculator),
            (ScientificCalculator, ProgrammerCalculator),
            (ProgrammerCalculator, ScientificCalculator),
        ],
        ids=[
            "basic-to-sci",
            "sci-to-basic",
            "basic-to-prog",
            "prog-to-basic",
            "sci-to-prog",
            "prog-to-sci",
        ],
    )
    def test_transfer_zero(self, source_cls, target_cls):
        """Transferring 0 between all mode pairs works correctly."""
        source = source_cls()
        source.current_value = 0 if isinstance(source, ProgrammerCalculator) else 0.0
        target = target_cls()
        transfer_value(source, target)
        if isinstance(target, ProgrammerCalculator):
            assert target.current_value == 0
        else:
            assert target.current_value == 0.0

    def test_negative_programmer_to_basic(self):
        """Transfer negative value from Programmer to Basic."""
        prog = ProgrammerCalculator()
        prog.set_word_size(8)
        prog.current_value = prog.mask_value(200)  # 200 in 8-bit -> -56
        assert prog.current_value == -56

        basic = BasicCalculator()
        transfer_value(prog, basic)
        assert basic.current_value == -56.0

    def test_large_float_to_programmer(self):
        """Large float is truncated and masked when transferred to Programmer."""
        sci = ScientificCalculator()
        sci.current_value = 99999.99

        prog = ProgrammerCalculator()
        prog.set_word_size(8)
        transfer_value(sci, prog)
        # int(99999.99) = 99999, mask to 8-bit signed
        expected = prog.mask_value(99999)
        assert prog.current_value == expected

    def test_8bit_negative_128_to_basic(self):
        """Transfer -128 from 8-bit Programmer to Basic yields -128.0."""
        prog = ProgrammerCalculator()
        prog.set_word_size(8)
        prog.current_value = -128

        basic = BasicCalculator()
        transfer_value(prog, basic)
        assert basic.current_value == -128.0
