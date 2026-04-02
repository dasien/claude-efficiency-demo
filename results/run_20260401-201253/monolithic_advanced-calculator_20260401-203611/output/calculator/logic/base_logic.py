"""Shared logic components: Memory, number formatting, and parsing."""

from __future__ import annotations

MAX_DISPLAY_DIGITS = 10


class Memory:
    """Calculator memory storage with MC, MR, M+, M-, MS operations."""

    def __init__(self) -> None:
        self._value: float = 0.0
        self._has_value: bool = False

    def store(self, value: float) -> None:
        """Store a value in memory, replacing any previous value."""
        self._value = value
        self._has_value = True

    def recall(self) -> float:
        """Return the stored memory value (0 if empty)."""
        return self._value

    def add(self, value: float) -> None:
        """Add a value to the stored memory value."""
        self._value += value
        self._has_value = True

    def subtract(self, value: float) -> None:
        """Subtract a value from the stored memory value."""
        self._value -= value
        self._has_value = True

    def clear(self) -> None:
        """Clear memory to zero."""
        self._value = 0.0
        self._has_value = False

    @property
    def has_value(self) -> bool:
        """Return True if a value is stored in memory."""
        return self._has_value


def format_number(value: float) -> str:
    """Format a numeric value for display.

    Args:
        value: The number to format.

    Returns:
        A string representation with integer cleanup,
        max 10 significant digits, and scientific notation
        for very large/small values.
    """
    if isinstance(value, float) and value == int(value):
        int_val = int(value)
        s = str(int_val)
        if len(s) > MAX_DISPLAY_DIGITS + 1:
            return f"{value:.{MAX_DISPLAY_DIGITS - 1}e}"
        return s

    s = str(value)
    if "e" in s.lower():
        return _format_scientific(value)

    if abs(value) >= 10 ** (MAX_DISPLAY_DIGITS + 1):
        return _format_scientific(value)

    if abs(value) < 1e-10 and value != 0:
        return _format_scientific(value)

    int_part_len = len(str(int(abs(value))))
    decimal_digits = max(0, MAX_DISPLAY_DIGITS - int_part_len)
    formatted = f"{value:.{decimal_digits}f}"
    if "." in formatted:
        formatted = formatted.rstrip("0").rstrip(".")
    if formatted == "-0":
        formatted = "0"
    return formatted


def _format_scientific(value: float) -> str:
    """Format a value in scientific notation with limited precision."""
    formatted = f"{value:.{MAX_DISPLAY_DIGITS - 1}e}"
    mantissa, exp = formatted.split("e")
    if "." in mantissa:
        mantissa = mantissa.rstrip("0").rstrip(".")
    return f"{mantissa}e{exp}"


def parse_number(text: str) -> float:
    """Parse display text back to a numeric value.

    Args:
        text: The display string to parse.

    Returns:
        The numeric value.

    Raises:
        ValueError: If the text cannot be parsed.
    """
    return float(text)
