"""Shared data types, display formatting, and abstract base class for all calculator modes."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Mode(Enum):
    """Calculator operating mode."""
    BASIC = "basic"
    SCIENTIFIC = "scientific"
    PROGRAMMER = "programmer"


class AngleUnit(Enum):
    """Angle measurement unit for trig functions."""
    DEG = "deg"
    RAD = "rad"


class NumberBase(Enum):
    """Number base for programmer mode."""
    DEC = 10
    HEX = 16
    OCT = 8
    BIN = 2


class WordSize(Enum):
    """Word size for programmer mode."""
    BITS_8 = 8
    BITS_16 = 16
    BITS_32 = 32
    BITS_64 = 64


@dataclass
class DisplayState:
    """Immutable snapshot of everything the View needs to render."""
    main_display: str
    expression_display: str
    error: bool
    memory_indicator: bool

    # Scientific-specific
    angle_unit: AngleUnit = AngleUnit.DEG
    paren_depth: int = 0

    # Programmer-specific
    number_base: NumberBase = NumberBase.DEC
    word_size: WordSize = WordSize.BITS_64
    hex_value: str = ""
    dec_value: str = ""
    oct_value: str = ""
    bin_value: str = ""


class BaseLogic(ABC):
    """Abstract base class for all calculator modes.

    Owns memory storage, input buffer management, display formatting,
    and error state. Subclasses implement mode-specific evaluation.
    """

    def __init__(self) -> None:
        self._memory: float = 0.0
        self._current_input: str = "0"
        self._expression: str = ""
        self._error: bool = False
        self._new_input: bool = True

    # ── Memory operations ────────────────────────────────────────

    @property
    def has_memory(self) -> bool:
        """True if memory contains a nonzero value."""
        return self._memory != 0.0

    def memory_clear(self) -> DisplayState:
        """Clear the stored memory value to zero."""
        self._memory = 0.0
        return self.get_display_state()

    def memory_recall(self) -> DisplayState:
        """Display the stored memory value."""
        self._current_input = self.format_number(self._memory)
        self._new_input = True
        return self.get_display_state()

    def memory_add(self) -> DisplayState:
        """Add the current display value to memory."""
        self._memory += self.get_current_value()
        return self.get_display_state()

    def memory_subtract(self) -> DisplayState:
        """Subtract the current display value from memory."""
        self._memory -= self.get_current_value()
        return self.get_display_state()

    def memory_store(self) -> DisplayState:
        """Store the current display value in memory."""
        self._memory = self.get_current_value()
        return self.get_display_state()

    # ── Input operations ─────────────────────────────────────────

    def input_digit(self, digit: str) -> DisplayState:
        """Append a digit to the current input.

        Args:
            digit: A single character '0'-'9'.
        """
        if self._error:
            self._error = False
            self._current_input = "0"
            self._expression = ""
            self._new_input = True

        if self._new_input:
            self._current_input = digit
            self._new_input = False
        else:
            if self._current_input == "0":
                self._current_input = digit
            elif self._current_input == "-0":
                self._current_input = "-" + digit
            else:
                self._current_input += digit

        return self.get_display_state()

    def input_decimal(self) -> DisplayState:
        """Append a decimal point if not already present."""
        if self._error:
            self._error = False
            self._current_input = "0"
            self._expression = ""
            self._new_input = True

        if self._new_input:
            self._current_input = "0."
            self._new_input = False
        elif "." not in self._current_input:
            self._current_input += "."

        return self.get_display_state()

    def input_sign_toggle(self) -> DisplayState:
        """Toggle the sign of the current input."""
        if self._error:
            return self.get_display_state()

        if self._current_input.startswith("-"):
            self._current_input = self._current_input[1:]
        elif self._current_input != "0":
            self._current_input = "-" + self._current_input

        return self.get_display_state()

    def input_backspace(self) -> DisplayState:
        """Delete the last character from the current input."""
        if self._error:
            return self.get_display_state()

        if self._new_input:
            return self.get_display_state()

        self._current_input = self._current_input[:-1]
        if not self._current_input or self._current_input == "-":
            self._current_input = "0"
            self._new_input = True

        return self.get_display_state()

    # ── Clear operations ─────────────────────────────────────────

    def clear_entry(self) -> DisplayState:
        """Reset the current entry to 0 without clearing pending operations."""
        self._current_input = "0"
        self._error = False
        self._new_input = True
        return self.get_display_state()

    def clear_all(self) -> DisplayState:
        """Reset all state except memory."""
        self._current_input = "0"
        self._expression = ""
        self._error = False
        self._new_input = True
        return self.get_display_state()

    # ── Evaluation ───────────────────────────────────────────────

    @abstractmethod
    def evaluate(self) -> DisplayState:
        """Evaluate the current expression and return the result."""
        ...

    # ── State export (for mode switching) ────────────────────────

    def get_current_value(self) -> float:
        """Return the current numeric value."""
        try:
            return float(self._current_input)
        except (ValueError, OverflowError):
            return 0.0

    def set_current_value(self, value: float) -> DisplayState:
        """Set the current value from an external source (mode switch)."""
        self._current_input = self.format_number(value)
        self._expression = ""
        self._error = False
        self._new_input = True
        return self.get_display_state()

    # ── Display formatting ───────────────────────────────────────

    @staticmethod
    def format_number(value: float) -> str:
        """Format a number for display.

        Rules:
        - Integers display without decimal point (5 not 5.0)
        - Floats display with max 10 significant digits
        - Very large/small numbers use scientific notation
        """
        if value != value:  # NaN
            return "Error"
        if abs(value) == float('inf'):
            return "Error"

        # Check if it's effectively an integer
        try:
            if value == int(value) and abs(value) < 1e16:
                return str(int(value))
        except (OverflowError, ValueError):
            pass

        # Use g format for up to 10 significant digits
        formatted = f"{value:.10g}"
        return formatted

    # ── Snapshot ─────────────────────────────────────────────────

    @abstractmethod
    def get_display_state(self) -> DisplayState:
        """Build and return the current DisplayState for the View."""
        ...
