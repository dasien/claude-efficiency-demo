"""Programmer calculator logic — base conversion, bitwise, word size."""

import math
from typing import Dict, Optional
from calculator.logic.base_logic import BaseCalculatorLogic


VALID_DIGITS = {
    2: set("01"),
    8: set("01234567"),
    10: set("0123456789"),
    16: set("0123456789ABCDEF"),
}

BITWISE_OPERATORS = {"AND", "OR", "XOR", "LSH", "RSH"}
ARITHMETIC_OPERATORS = {"+", "-", "*", "/", "MOD"}
ALL_OPERATORS = BITWISE_OPERATORS | ARITHMETIC_OPERATORS


class ProgrammerLogic(BaseCalculatorLogic):
    """Programmer mode with base conversion, bitwise ops, and word size."""

    WORD_SIZES = {8, 16, 32, 64}

    def __init__(self) -> None:
        super().__init__()
        self.current_base: int = 10
        self.word_size: int = 64
        self._pending_operator: str = ""
        self._left_operand: Optional[int] = None

    def all_clear(self) -> None:
        """Reset all state."""
        super().all_clear()
        self._pending_operator = ""
        self._left_operand = None

    def _clear_error(self) -> None:
        """Clear error state."""
        super()._clear_error()
        self._pending_operator = ""
        self._left_operand = None

    def clamp(self, value: int) -> int:
        """Clamp value to current word size using two's complement."""
        bits = self.word_size
        mask = (1 << bits) - 1
        value = value & mask
        # Convert to signed
        if value >= (1 << (bits - 1)):
            value -= (1 << bits)
        return value

    def get_current_int(self) -> int:
        """Return current display value as an integer in base 10."""
        if self.error:
            return 0
        try:
            return int(self.display_value, self.current_base)
        except (ValueError, OverflowError):
            return 0

    def get_current_value(self) -> float:
        """Return current display value as float (for mode switching)."""
        return float(self.get_current_int())

    def set_current_value(self, value: float) -> None:
        """Set value from float (for mode switching). Truncates to int."""
        int_val = int(value)
        int_val = self.clamp(int_val)
        self.display_value = self._int_to_base(int_val, self.current_base)
        self.input_mode = "result"

    def format_number(self, value: float) -> str:
        """Format number for programmer mode display."""
        int_val = int(value)
        int_val = self.clamp(int_val)
        return self._int_to_base(int_val, self.current_base)

    def _int_to_base(self, value: int, base: int) -> str:
        """Convert a signed integer to string in the given base."""
        if value == 0:
            return "0"

        negative = value < 0
        if negative:
            # For display in non-decimal bases, show two's complement
            if base != 10:
                # Convert to unsigned representation
                unsigned = value & ((1 << self.word_size) - 1)
                return self._unsigned_to_base(unsigned, base)
            else:
                return str(value)

        return self._unsigned_to_base(value, base)

    def _unsigned_to_base(self, value: int, base: int) -> str:
        """Convert unsigned integer to base string."""
        if value == 0:
            return "0"
        digits = "0123456789ABCDEF"
        result = ""
        while value > 0:
            result = digits[value % base] + result
            value //= base
        return result

    def set_base(self, base: int) -> None:
        """Switch to a new number base, converting the current value."""
        if base not in VALID_DIGITS:
            return
        current_int = self.get_current_int()
        self.current_base = base
        self.display_value = self._int_to_base(current_int, base)
        if self.input_mode == "typing":
            self.input_mode = "result"

    def set_word_size(self, bits: int) -> None:
        """Change word size, clamping current value."""
        if bits not in self.WORD_SIZES:
            return
        self.word_size = bits
        current_int = self.get_current_int()
        current_int = self.clamp(current_int)
        self.display_value = self._int_to_base(current_int, self.current_base)

    def get_all_bases(self) -> Dict[str, str]:
        """Return current value in all four bases."""
        val = self.get_current_int()
        return {
            "DEC": str(val),
            "HEX": self._int_to_base(val, 16) if val >= 0 else self._int_to_base(val, 16),
            "OCT": self._int_to_base(val, 8) if val >= 0 else self._int_to_base(val, 8),
            "BIN": self._int_to_base(val, 2) if val >= 0 else self._int_to_base(val, 2),
        }

    def input_digit(self, digit: str) -> None:
        """Handle digit input with base validation."""
        digit = digit.upper()
        if self.error:
            self._clear_error()

        if digit not in VALID_DIGITS[self.current_base]:
            return

        if self.input_mode in ("ready", "result"):
            self.display_value = digit
            self.input_mode = "typing"
        else:
            if self.display_value == "0":
                self.display_value = digit
            else:
                self.display_value += digit

    def input_decimal(self) -> None:
        """Decimal point is not allowed in programmer mode."""
        pass

    def input_operator(self, op: str) -> None:
        """Handle operator input."""
        if self.error:
            return

        current = self.get_current_int()

        if self._pending_operator and self.input_mode == "typing":
            # Evaluate pending operation first
            result = self._compute(self._left_operand, self._pending_operator, current)
            if result is None:
                self._set_error()
                return
            result = self.clamp(result)
            self._left_operand = result
            self.display_value = self._int_to_base(result, self.current_base)
        else:
            self._left_operand = current

        self._pending_operator = op
        self.input_mode = "ready"
        self._update_expression_str()

    def _update_expression_str(self) -> None:
        """Update expression display."""
        if self._left_operand is not None and self._pending_operator:
            left_str = self._int_to_base(self._left_operand, self.current_base)
            self._expression_str = f"{left_str} {self._pending_operator}"
        else:
            self._expression_str = ""

    def evaluate(self) -> None:
        """Evaluate the pending operation."""
        if self.error:
            return
        if not self._pending_operator or self._left_operand is None:
            self.input_mode = "result"
            return

        current = self.get_current_int()
        left_str = self._int_to_base(self._left_operand, self.current_base)
        right_str = self._int_to_base(current, self.current_base)
        self._expression_str = f"{left_str} {self._pending_operator} {right_str} ="

        result = self._compute(self._left_operand, self._pending_operator, current)
        if result is None:
            self._set_error()
            return

        result = self.clamp(result)
        self.display_value = self._int_to_base(result, self.current_base)
        self.input_mode = "result"
        self._pending_operator = ""
        self._left_operand = None

    def _compute(self, left: int, op: str, right: int) -> Optional[int]:
        """Compute a binary operation. Returns None on error."""
        try:
            if op == "+":
                return left + right
            elif op == "-":
                return left - right
            elif op == "*":
                return left * right
            elif op == "/":
                if right == 0:
                    return None
                return int(left / right)  # truncating division
            elif op == "MOD":
                if right == 0:
                    return None
                # Truncating modulo (matches C behavior)
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
                return left >> right
        except (OverflowError, ValueError):
            return None
        return None

    def bitwise_not(self) -> None:
        """Apply bitwise NOT to current value."""
        if self.error:
            return
        val = self.get_current_int()
        result = ~val
        result = self.clamp(result)
        self.display_value = self._int_to_base(result, self.current_base)
        self.input_mode = "result"

    def toggle_sign(self) -> None:
        """Toggle sign of current value."""
        if self.error:
            return
        val = self.get_current_int()
        if val == 0:
            return
        result = self.clamp(-val)
        self.display_value = self._int_to_base(result, self.current_base)

    def percent(self) -> None:
        """Percent is used as modulo operator in programmer mode."""
        self.input_operator("MOD")

    def is_valid_digit(self, digit: str) -> bool:
        """Check if a digit is valid for the current base."""
        return digit.upper() in VALID_DIGITS[self.current_base]

    def backspace(self) -> None:
        """Delete the last digit."""
        if self.error or self.input_mode != "typing":
            return
        if len(self.display_value) <= 1:
            self.display_value = "0"
            self.input_mode = "ready"
        else:
            self.display_value = self.display_value[:-1]
