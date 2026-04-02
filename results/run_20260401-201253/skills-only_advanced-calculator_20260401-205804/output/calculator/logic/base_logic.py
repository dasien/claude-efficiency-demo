"""Base calculator logic shared across all modes."""

import math
from typing import Optional


class BaseCalculatorLogic:
    """Base class for calculator logic with shared state and operations."""

    MAX_DIGITS = 10

    def __init__(self) -> None:
        self.display_value: str = "0"
        self.expression: list = []
        self.memory: float = 0.0
        self.has_memory: bool = False
        self.error: bool = False
        self.input_mode: str = "ready"  # "ready", "typing", "result", "error"
        self._expression_str: str = ""

    @property
    def expression_display(self) -> str:
        """Return the expression string for display."""
        return self._expression_str

    def get_current_value(self) -> float:
        """Return the current display value as a float."""
        if self.error:
            return 0.0
        try:
            return float(self.display_value)
        except (ValueError, OverflowError):
            return 0.0

    def set_current_value(self, value: float) -> None:
        """Set the display value from a float."""
        self.display_value = self.format_number(value)
        self.input_mode = "result"

    def format_number(self, value: float) -> str:
        """Format a number for display with proper precision."""
        if math.isinf(value) or math.isnan(value):
            return "Error"

        # Check if integer
        if value == int(value) and abs(value) < 1e15:
            int_val = int(value)
            s = str(int_val)
            if len(s) <= self.MAX_DIGITS + 1:  # +1 for possible minus
                return s

        # Check if needs scientific notation
        abs_val = abs(value)
        if abs_val != 0 and (abs_val >= 1e10 or abs_val < 1e-10):
            return f"{value:.6e}"

        # Regular float formatting with up to 10 significant digits
        formatted = f"{value:.{self.MAX_DIGITS}g}"
        return formatted

    def input_digit(self, digit: str) -> None:
        """Handle digit input (0-9)."""
        if self.error:
            self._clear_error()

        if self.input_mode in ("ready", "result"):
            self.display_value = digit
            self.input_mode = "typing"
        else:
            if self.display_value == "0" and digit == "0":
                return
            if self.display_value == "0":
                self.display_value = digit
            else:
                if len(self.display_value.replace("-", "").replace(".", "")) >= self.MAX_DIGITS:
                    return
                self.display_value += digit

    def input_decimal(self) -> None:
        """Handle decimal point input."""
        if self.error:
            self._clear_error()

        if self.input_mode in ("ready", "result"):
            self.display_value = "0."
            self.input_mode = "typing"
        elif "." not in self.display_value:
            self.display_value += "."

    def backspace(self) -> None:
        """Delete the last digit."""
        if self.error or self.input_mode != "typing":
            return
        if len(self.display_value) == 1 or (len(self.display_value) == 2 and self.display_value[0] == "-"):
            self.display_value = "0"
            self.input_mode = "ready"
        else:
            self.display_value = self.display_value[:-1]

    def clear_entry(self) -> None:
        """Clear current entry (C) without clearing pending operation."""
        if self.error:
            self._clear_error()
            return
        self.display_value = "0"
        self.input_mode = "ready"

    def all_clear(self) -> None:
        """Reset all state (AC)."""
        self.display_value = "0"
        self.expression = []
        self._expression_str = ""
        self.error = False
        self.input_mode = "ready"

    def toggle_sign(self) -> None:
        """Toggle the sign of the current value (+/-)."""
        if self.error:
            return
        val = self.get_current_value()
        if val == 0:
            return
        val = -val
        self.display_value = self.format_number(val)

    def percent(self) -> None:
        """Divide the current value by 100."""
        if self.error:
            return
        val = self.get_current_value() / 100.0
        self.display_value = self.format_number(val)
        self.input_mode = "result"

    def _set_error(self) -> None:
        """Set error state."""
        self.display_value = "Error"
        self.error = True
        self.input_mode = "error"

    def _clear_error(self) -> None:
        """Clear error state."""
        self.error = False
        self.display_value = "0"
        self.input_mode = "ready"
        self.expression = []
        self._expression_str = ""

    # Memory operations

    def memory_store(self) -> None:
        """Store current display value in memory (MS)."""
        if self.error:
            return
        self.memory = self.get_current_value()
        self.has_memory = True
        self.input_mode = "result"

    def memory_recall(self) -> None:
        """Recall memory value to display (MR)."""
        self.display_value = self.format_number(self.memory)
        self.input_mode = "result"

    def memory_add(self) -> None:
        """Add current display value to memory (M+)."""
        if self.error:
            return
        self.memory += self.get_current_value()
        self.has_memory = True

    def memory_subtract(self) -> None:
        """Subtract current display value from memory (M-)."""
        if self.error:
            return
        self.memory -= self.get_current_value()
        self.has_memory = True

    def memory_clear(self) -> None:
        """Clear memory (MC)."""
        self.memory = 0.0
        self.has_memory = False
