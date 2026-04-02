"""Base calculator logic shared across all modes."""

import math
from typing import Optional


class BaseCalculator:
    """Base class providing shared calculator state and operations."""

    def __init__(self) -> None:
        """Initialize calculator state."""
        self._current_input: str = "0"
        self._computed_value: Optional[float] = None
        self._expression: str = ""
        self._memory: float = 0.0
        self._has_memory: bool = False
        self._error: bool = False
        self._error_message: str = ""
        self._new_input: bool = True  # Next digit replaces display

    @property
    def error(self) -> bool:
        """Whether the calculator is in an error state."""
        return self._error

    @property
    def has_memory(self) -> bool:
        """Whether a value is stored in memory."""
        return self._has_memory

    @property
    def memory(self) -> float:
        """The current memory value."""
        return self._memory

    @memory.setter
    def memory(self, value: float) -> None:
        """Set memory value."""
        self._memory = value

    @has_memory.setter
    def has_memory(self, value: bool) -> None:
        """Set has_memory flag."""
        self._has_memory = value

    def _set_error(self, message: str = "Error") -> None:
        """Put the calculator into an error state."""
        self._error = True
        self._error_message = message

    def _clear_error(self) -> None:
        """Clear the error state."""
        self._error = False
        self._error_message = ""

    def get_display_value(self) -> str:
        """Return the string to show in the main display."""
        if self._error:
            return self._error_message
        if self._computed_value is not None and self._new_input:
            return self.format_number(self._computed_value)
        return self._current_input

    def get_expression(self) -> str:
        """Return the expression string for the secondary display."""
        return self._expression

    def get_current_value(self) -> float:
        """Return the current numeric value (input or computed)."""
        if self._computed_value is not None and self._new_input:
            return self._computed_value
        try:
            return float(self._current_input)
        except (ValueError, OverflowError):
            return 0.0

    def set_value(self, value: float) -> None:
        """Set the current displayed value directly."""
        self._computed_value = value
        self._current_input = self.format_number(value)
        self._new_input = True

    def input_digit(self, digit: str) -> None:
        """Handle a digit input (0-9)."""
        if self._error:
            self._clear_error()
            self._current_input = "0"
            self._expression = ""
            self._new_input = True

        if self._new_input:
            self._current_input = "0"
            self._new_input = False
            self._computed_value = None

        if self._current_input == "0" and digit != "0":
            self._current_input = digit
        elif self._current_input == "0" and digit == "0":
            pass  # Prevent leading zeros
        elif self._current_input == "-0":
            self._current_input = "-" + digit
        else:
            self._current_input += digit

    def input_decimal(self) -> None:
        """Handle decimal point input."""
        if self._error:
            self._clear_error()
            self._current_input = "0"
            self._new_input = True

        if self._new_input:
            self._current_input = "0"
            self._new_input = False
            self._computed_value = None

        if "." not in self._current_input:
            self._current_input += "."

    def toggle_sign(self) -> None:
        """Toggle the sign of the current value."""
        if self._error:
            return

        if self._new_input and self._computed_value is not None:
            self._computed_value = -self._computed_value
            self._current_input = self.format_number(self._computed_value)
            return

        if self._current_input.startswith("-"):
            self._current_input = self._current_input[1:]
        elif self._current_input != "0":
            self._current_input = "-" + self._current_input

    def percent(self) -> None:
        """Divide the current value by 100."""
        if self._error:
            return
        value = self.get_current_value() / 100.0
        self._computed_value = value
        self._current_input = self.format_number(value)
        self._new_input = True

    def backspace(self) -> None:
        """Delete the last character from the current input."""
        if self._error:
            self._clear_error()
            self._current_input = "0"
            self._new_input = True
            return

        if self._new_input:
            return

        if len(self._current_input) <= 1 or (
            len(self._current_input) == 2 and self._current_input.startswith("-")
        ):
            self._current_input = "0"
        else:
            self._current_input = self._current_input[:-1]

    def clear_entry(self) -> None:
        """Clear the current entry (C button)."""
        if self._error:
            self._clear_error()
        self._current_input = "0"
        self._new_input = True
        self._computed_value = None

    def all_clear(self) -> None:
        """Reset all state (AC button)."""
        self._clear_error()
        self._current_input = "0"
        self._computed_value = None
        self._expression = ""
        self._new_input = True

    # Memory operations

    def memory_clear(self) -> None:
        """Clear memory (MC)."""
        self._memory = 0.0
        self._has_memory = False

    def memory_recall(self) -> None:
        """Recall memory value (MR)."""
        if self._error:
            self._clear_error()
        self._computed_value = self._memory
        self._current_input = self.format_number(self._memory)
        self._new_input = True

    def memory_add(self) -> None:
        """Add display value to memory (M+)."""
        self._memory += self.get_current_value()
        self._has_memory = True
        self._new_input = True

    def memory_subtract(self) -> None:
        """Subtract display value from memory (M-)."""
        self._memory -= self.get_current_value()
        self._has_memory = True
        self._new_input = True

    def memory_store(self) -> None:
        """Store display value in memory (MS)."""
        self._memory = self.get_current_value()
        self._has_memory = True
        self._new_input = True

    @staticmethod
    def format_number(value: float) -> str:
        """Format a number for display.

        - Integers display without decimal point.
        - Floats display with up to 10 significant digits.
        - Very large/small numbers use scientific notation.
        """
        if math.isnan(value) or math.isinf(value):
            return "Error"

        # Check if it's an integer value
        if value == int(value) and abs(value) < 1e15:
            return str(int(value))

        # Very large or very small numbers: scientific notation
        abs_val = abs(value)
        if abs_val >= 1e15 or (abs_val != 0 and abs_val < 1e-10):
            formatted = f"{value:.10g}"
            return formatted

        # Normal float: up to 10 significant digits
        formatted = f"{value:.10g}"
        return formatted
