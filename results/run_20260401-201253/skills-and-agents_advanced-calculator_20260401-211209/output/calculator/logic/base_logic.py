"""Base calculator with core state management and input handling."""


class BaseCalculator:
    """Base calculator providing state management, memory, and input handling.

    Manages the fundamental calculator state including current value,
    input buffer, memory, error state, and expression display.
    """

    def __init__(self) -> None:
        """Initialize the base calculator with default state."""
        self.current_value: float = 0.0
        self.expression: str = ""
        self.memory: float = 0.0
        self.has_memory: bool = False
        self.error: bool = False
        self.error_message: str = ""
        self.input_buffer: str = "0"
        self._new_input: bool = True

    def mc(self) -> None:
        """Clear memory."""
        self.memory = 0.0
        self.has_memory = False

    def mr(self) -> float:
        """Recall memory value into current value.

        Returns:
            The recalled memory value.
        """
        self.current_value = self.memory
        self.input_buffer = ""
        self._new_input = True
        return self.memory

    def m_plus(self) -> None:
        """Add current value to memory."""
        self.memory += self.current_value
        self.has_memory = True

    def m_minus(self) -> None:
        """Subtract current value from memory."""
        self.memory -= self.current_value
        self.has_memory = True

    def ms(self) -> None:
        """Store current value in memory."""
        self.memory = self.current_value
        self.has_memory = True

    def format_number(self, value: float) -> str:
        """Format a numeric value for display.

        Displays integers without decimal point and limits to 10
        significant digits.

        Args:
            value: The number to format.

        Returns:
            The formatted string representation.
        """
        if value == 0:
            return "0"
        formatted = f"{value:.10g}"
        return formatted

    def append_digit(self, digit: str) -> None:
        """Append a digit to the input buffer.

        If in error state, clears error and resets before appending.
        Handles leading zero suppression.

        Args:
            digit: A single digit character ('0'-'9').
        """
        if self.error:
            self.clear_error()
            self.clear_all()

        if self._new_input:
            self.input_buffer = ""
            self._new_input = False

        if self.input_buffer == "0" and digit != "0":
            self.input_buffer = digit
        elif self.input_buffer == "0" and digit == "0":
            pass
        else:
            self.input_buffer += digit

        self.current_value = float(self.input_buffer)

    def append_decimal(self) -> None:
        """Append a decimal point to the input buffer.

        If starting new input, begins with '0.'.
        """
        if self._new_input:
            self.input_buffer = "0."
            self._new_input = False
        elif "." not in self.input_buffer:
            self.input_buffer += "."

    def toggle_sign(self) -> None:
        """Negate the current value and update the input buffer."""
        self.current_value = -self.current_value
        if self.input_buffer.startswith("-"):
            self.input_buffer = self.input_buffer[1:]
        elif self.input_buffer and self.input_buffer != "0":
            self.input_buffer = "-" + self.input_buffer
        else:
            self.input_buffer = str(self.current_value)

    def percentage(self) -> None:
        """Divide current value by 100."""
        self.current_value /= 100
        self.input_buffer = self.format_number(self.current_value)
        self._new_input = True

    def backspace(self) -> None:
        """Remove the last character from the input buffer."""
        self.input_buffer = self.input_buffer[:-1]
        if not self.input_buffer or self.input_buffer == "-":
            self.input_buffer = "0"
        self.current_value = float(self.input_buffer)

    def clear_entry(self) -> None:
        """Clear the current entry, preserving expression and pending ops."""
        self.input_buffer = "0"
        self.current_value = 0.0
        self._new_input = True

    def clear_all(self) -> None:
        """Reset all state except memory."""
        self.current_value = 0.0
        self.expression = ""
        self.error = False
        self.error_message = ""
        self.input_buffer = "0"
        self._new_input = True

    def set_error(self, message: str = "Error") -> None:
        """Set the calculator into an error state.

        Args:
            message: The error message to display.
        """
        self.error = True
        self.error_message = message

    def clear_error(self) -> None:
        """Clear the error state."""
        self.error = False
        self.error_message = ""

    def get_display_value(self) -> str:
        """Get the current display value.

        Returns:
            The input buffer if actively inputting, otherwise the
            formatted current value.
        """
        if self.input_buffer and not self._new_input:
            return self.input_buffer
        return self.format_number(self.current_value)

    def get_expression_display(self) -> str:
        """Get the expression string for display.

        Returns:
            The current expression string.
        """
        return self.expression
