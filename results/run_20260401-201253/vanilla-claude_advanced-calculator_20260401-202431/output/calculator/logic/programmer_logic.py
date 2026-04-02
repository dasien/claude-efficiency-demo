"""Programmer calculator logic with base conversion, bitwise ops, and word sizes."""

from typing import Dict, List, Optional


class ProgrammerCalculator:
    """Programmer mode calculator for integer math in multiple bases."""

    WORD_SIZES = {8, 16, 32, 64}
    BASES = {"DEC", "HEX", "OCT", "BIN"}
    BASE_RADIX = {"DEC": 10, "HEX": 16, "OCT": 8, "BIN": 2}
    VALID_DIGITS = {
        "DEC": set("0123456789"),
        "HEX": set("0123456789ABCDEF"),
        "OCT": set("01234567"),
        "BIN": set("01"),
    }

    def __init__(self) -> None:
        """Initialize programmer calculator state."""
        self._value: int = 0
        self._base: str = "DEC"
        self._word_size: int = 64
        self._current_input: str = "0"
        self._new_input: bool = True
        self._error: bool = False
        self._error_message: str = ""
        self._expression: str = ""
        self._memory: float = 0.0
        self._has_memory: bool = False

        # Operation state
        self._pending_operator: Optional[str] = None
        self._operand: Optional[int] = None
        self._last_operator: Optional[str] = None
        self._last_operand: Optional[int] = None

    @property
    def error(self) -> bool:
        """Whether the calculator is in an error state."""
        return self._error

    @property
    def has_memory(self) -> bool:
        """Whether a value is stored in memory."""
        return self._has_memory

    @has_memory.setter
    def has_memory(self, value: bool) -> None:
        """Set has_memory flag."""
        self._has_memory = value

    @property
    def memory(self) -> float:
        """The current memory value."""
        return self._memory

    @memory.setter
    def memory(self, value: float) -> None:
        """Set memory value."""
        self._memory = value

    @property
    def base(self) -> str:
        """Current number base."""
        return self._base

    @property
    def word_size(self) -> int:
        """Current word size in bits."""
        return self._word_size

    def _set_error(self, message: str = "Error") -> None:
        """Put calculator into error state."""
        self._error = True
        self._error_message = message

    def _clear_error(self) -> None:
        """Clear error state."""
        self._error = False
        self._error_message = ""

    def truncate_to_word_size(self, value: int) -> int:
        """Truncate a value to the current word size using two's complement."""
        bits = self._word_size
        mask = (1 << bits) - 1
        value = value & mask
        # Convert to signed
        if value >= (1 << (bits - 1)):
            value -= (1 << bits)
        return value

    def _max_value(self) -> int:
        """Maximum positive value for current word size."""
        return (1 << (self._word_size - 1)) - 1

    def _min_value(self) -> int:
        """Minimum negative value for current word size."""
        return -(1 << (self._word_size - 1))

    def get_display_value(self) -> str:
        """Return the string to show in the main display."""
        if self._error:
            return self._error_message
        if self._new_input:
            return self._format_value(self._value)
        return self._current_input

    def get_expression(self) -> str:
        """Return the expression string."""
        return self._expression

    def get_current_int_value(self) -> int:
        """Return the current integer value."""
        if self._new_input:
            return self._value
        return self._parse_input(self._current_input)

    def _parse_input(self, text: str) -> int:
        """Parse the current input string in the current base."""
        if not text or text == "0":
            return 0
        negative = text.startswith("-")
        digits = text.lstrip("-")
        if not digits:
            return 0
        try:
            radix = self.BASE_RADIX[self._base]
            val = int(digits, radix)
            if negative:
                val = -val
            return self.truncate_to_word_size(val)
        except ValueError:
            return 0

    def _format_value(self, value: int) -> str:
        """Format an integer value in the current base."""
        value = self.truncate_to_word_size(value)
        if self._base == "DEC":
            return str(value)
        # For non-decimal, show unsigned representation
        bits = self._word_size
        mask = (1 << bits) - 1
        unsigned = value & mask
        if self._base == "HEX":
            return format(unsigned, "X")
        elif self._base == "OCT":
            return format(unsigned, "o")
        elif self._base == "BIN":
            return format(unsigned, "b")
        return str(value)

    def get_base_conversions(self) -> Dict[str, str]:
        """Return the current value formatted in all four bases."""
        value = self.get_current_int_value()
        value = self.truncate_to_word_size(value)
        bits = self._word_size
        mask = (1 << bits) - 1
        unsigned = value & mask
        return {
            "DEC": str(value),
            "HEX": format(unsigned, "X"),
            "OCT": format(unsigned, "o"),
            "BIN": format(unsigned, "b"),
        }

    def set_base(self, base: str) -> None:
        """Switch to a different number base, preserving the current value."""
        if base not in self.BASES:
            return
        # Capture value before switching
        value = self.get_current_int_value()
        self._base = base
        self._value = self.truncate_to_word_size(value)
        self._current_input = self._format_value(self._value)
        self._new_input = True

    def set_word_size(self, bits: int) -> None:
        """Change the word size, truncating the current value."""
        if bits not in self.WORD_SIZES:
            return
        self._word_size = bits
        value = self.get_current_int_value()
        self._value = self.truncate_to_word_size(value)
        self._current_input = self._format_value(self._value)
        self._new_input = True

    def input_digit(self, digit: str) -> None:
        """Handle a digit input (0-9, A-F)."""
        digit = digit.upper()
        if self._error:
            self._clear_error()
            self._current_input = "0"
            self._new_input = True

        if digit not in self.VALID_DIGITS[self._base]:
            return

        if self._new_input:
            self._current_input = "0"
            self._new_input = False

        if self._current_input == "0":
            self._current_input = digit
        elif self._current_input == "-0":
            self._current_input = "-" + digit
        else:
            self._current_input += digit

        # Enforce word size limit
        parsed = self._parse_input(self._current_input)
        self._value = parsed

    def input_operator(self, op: str) -> None:
        """Handle an operator input (+, -, *, /, %, AND, OR, XOR, LSH, RSH)."""
        if self._error:
            return

        current_val = self.get_current_int_value()

        if self._pending_operator is not None and not self._new_input:
            # Evaluate pending operation
            result = self._apply_op(self._operand, self._pending_operator, current_val)
            if result is None:
                self._set_error("Error")
                return
            self._value = self.truncate_to_word_size(result)
        else:
            self._value = current_val

        self._operand = self._value
        self._pending_operator = op
        self._new_input = True
        self._current_input = self._format_value(self._value)
        self._expression = f"{self._format_value(self._operand)} {op} "

    def evaluate(self) -> None:
        """Evaluate the pending operation."""
        if self._error:
            return

        current_val = self.get_current_int_value()

        if self._pending_operator is not None:
            right = current_val if not self._new_input else current_val
            if not self._new_input:
                self._last_operator = self._pending_operator
                self._last_operand = current_val
            elif self._last_operator is None:
                # Operator but no new operand typed - use current as operand
                self._last_operator = self._pending_operator
                self._last_operand = current_val

            result = self._apply_op(self._operand, self._pending_operator, right)
            if result is None:
                self._set_error("Error")
                return
            self._value = self.truncate_to_word_size(result)
            self._pending_operator = None
            self._operand = None
        elif self._last_operator is not None and self._last_operand is not None:
            # Repeated equals
            result = self._apply_op(current_val, self._last_operator, self._last_operand)
            if result is None:
                self._set_error("Error")
                return
            self._value = self.truncate_to_word_size(result)
        else:
            self._value = current_val

        self._current_input = self._format_value(self._value)
        self._new_input = True
        self._expression = ""

    def _apply_op(self, left: int, op: str, right: int) -> Optional[int]:
        """Apply a binary operator to two integer operands."""
        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            if right == 0:
                return None
            # Truncating division (toward zero)
            if (left < 0) != (right < 0) and left % right != 0:
                return -(abs(left) // abs(right))
            return left // right
        elif op == "%":
            if right == 0:
                return None
            result = abs(left) % abs(right)
            if left < 0:
                result = -result
            return result
        elif op == "AND":
            return left & right
        elif op == "OR":
            return left | right
        elif op == "XOR":
            return left ^ right
        elif op == "LSH":
            return left << right
        elif op == "RSH":
            # Arithmetic right shift
            return left >> right
        return None

    def bitwise_not(self) -> None:
        """Compute bitwise NOT of current value."""
        if self._error:
            return
        value = self.get_current_int_value()
        result = ~value
        self._value = self.truncate_to_word_size(result)
        self._current_input = self._format_value(self._value)
        self._new_input = True

    def toggle_sign(self) -> None:
        """Toggle the sign of the current value."""
        if self._error:
            return
        value = self.get_current_int_value()
        self._value = self.truncate_to_word_size(-value)
        self._current_input = self._format_value(self._value)
        self._new_input = True

    def clear_entry(self) -> None:
        """Clear current entry."""
        if self._error:
            self._clear_error()
        self._current_input = "0"
        self._value = 0
        self._new_input = True

    def all_clear(self) -> None:
        """Reset all state."""
        self._clear_error()
        self._value = 0
        self._current_input = "0"
        self._new_input = True
        self._expression = ""
        self._pending_operator = None
        self._operand = None
        self._last_operator = None
        self._last_operand = None

    def backspace(self) -> None:
        """Delete the last character from the current input."""
        if self._error:
            self._clear_error()
            self._current_input = "0"
            self._value = 0
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
        self._value = self._parse_input(self._current_input)

    # Memory operations

    def memory_clear(self) -> None:
        """Clear memory."""
        self._memory = 0.0
        self._has_memory = False

    def memory_recall(self) -> None:
        """Recall memory value."""
        if self._error:
            self._clear_error()
        self._value = int(self._memory)
        self._value = self.truncate_to_word_size(self._value)
        self._current_input = self._format_value(self._value)
        self._new_input = True

    def memory_add(self) -> None:
        """Add current value to memory."""
        self._memory += float(self.get_current_int_value())
        self._has_memory = True

    def memory_subtract(self) -> None:
        """Subtract current value from memory."""
        self._memory -= float(self.get_current_int_value())
        self._has_memory = True

    def memory_store(self) -> None:
        """Store current value in memory."""
        self._memory = float(self.get_current_int_value())
        self._has_memory = True

    def set_value(self, value: int) -> None:
        """Set the current value directly."""
        self._value = self.truncate_to_word_size(value)
        self._current_input = self._format_value(self._value)
        self._new_input = True

    def get_value(self) -> int:
        """Get the current integer value."""
        return self.get_current_int_value()
