"""Programmer calculator with base conversion and bitwise operations."""

from calculator.logic.base_logic import BaseCalculator

BASE_MAP = {
    "BIN": 2,
    "OCT": 8,
    "DEC": 10,
    "HEX": 16,
}


class ProgrammerCalculator(BaseCalculator):
    """Calculator for programmer operations with multiple bases.

    Supports binary, octal, decimal, and hexadecimal input/output,
    bitwise operations, and configurable word sizes with proper
    two's complement signed integer handling.
    """

    def __init__(self) -> None:
        """Initialize the programmer calculator."""
        super().__init__()
        self.base: str = "DEC"
        self.word_size: int = 64
        self.current_value: int = 0
        self.pending_tokens: list = []

    def set_base(self, base: str) -> None:
        """Set the numeric base for input and display.

        Args:
            base: One of 'BIN', 'OCT', 'DEC', 'HEX'.
        """
        self.base = base

    def get_value_in_base(self, base: str) -> str:
        """Format the current value for display in a given base.

        Uses unsigned representation for non-decimal bases via
        two's complement masking.

        Args:
            base: One of 'BIN', 'OCT', 'DEC', 'HEX'.

        Returns:
            The formatted string representation.
        """
        value = self.current_value
        if base == "DEC":
            return str(value)
        mask = (1 << self.word_size) - 1
        unsigned = value & mask
        if base == "HEX":
            return format(unsigned, "X")
        if base == "OCT":
            return format(unsigned, "o")
        if base == "BIN":
            return format(unsigned, "b")
        return str(value)

    def get_all_bases(self) -> dict:
        """Get the current value formatted in all four bases.

        Returns:
            A dict with keys 'BIN', 'OCT', 'DEC', 'HEX' and their
            string representations.
        """
        return {
            "BIN": self.get_value_in_base("BIN"),
            "OCT": self.get_value_in_base("OCT"),
            "DEC": self.get_value_in_base("DEC"),
            "HEX": self.get_value_in_base("HEX"),
        }

    def get_valid_digits(self) -> set:
        """Get the set of valid digit characters for the current base.

        Returns:
            A set of valid digit strings.
        """
        if self.base == "BIN":
            return {"0", "1"}
        if self.base == "OCT":
            return {str(d) for d in range(8)}
        if self.base == "DEC":
            return {str(d) for d in range(10)}
        if self.base == "HEX":
            return {str(d) for d in range(10)} | {
                "A", "B", "C", "D", "E", "F"
            }
        return set()

    def set_word_size(self, bits: int) -> None:
        """Set the word size and apply masking to the current value.

        Args:
            bits: The word size in bits (e.g. 8, 16, 32, 64).
        """
        self.word_size = bits
        self.current_value = self.mask_value(self.current_value)

    def mask_value(self, value: int) -> int:
        """Apply two's complement masking for the current word size.

        Args:
            value: The integer value to mask.

        Returns:
            The masked signed integer value.
        """
        bits = self.word_size
        mask = (1 << bits) - 1
        value = value & mask
        if value & (1 << (bits - 1)):
            value -= (1 << bits)
        return value

    def add_operator(self, op: str) -> None:
        """Finalize current input and add an operator.

        Args:
            op: The operator string ('+', '-', '*', '/', '%',
                'AND', 'OR', 'XOR', 'LSH', 'RSH').
        """
        if not self._new_input:
            base_int = BASE_MAP.get(self.base, 10)
            self.pending_tokens.append(int(self.input_buffer, base_int))
        elif self.pending_tokens or self.current_value != 0:
            if not self.pending_tokens or not isinstance(
                self.pending_tokens[-1], str
            ):
                self.pending_tokens.append(self.current_value)

        self.pending_tokens.append(op)
        self.input_buffer = "0"
        self._new_input = True
        self.expression += (
            f" {self.format_number(self.current_value)} {op}"
        )

    def evaluate(self) -> int:
        """Evaluate the pending expression and return the result.

        Returns:
            The computed integer result after masking.
        """
        try:
            if not self._new_input:
                base_int = BASE_MAP.get(self.base, 10)
                self.pending_tokens.append(
                    int(self.input_buffer, base_int)
                )
            elif not self.pending_tokens:
                return self.current_value
            else:
                self.pending_tokens.append(self.current_value)

            result = self._evaluate_tokens(self.pending_tokens)
            result = self.mask_value(result)
            self.current_value = result
            self.pending_tokens = []
            self.expression += (
                f" {self.format_number(self.current_value)} ="
            )
            self._new_input = True
            self.input_buffer = "0"
            return result
        except (ValueError, ZeroDivisionError, OverflowError):
            self.set_error("Error")
            self.pending_tokens = []
            self._new_input = True
            return 0

    def _evaluate_tokens(self, tokens: list) -> int:
        """Evaluate tokens with programmer-specific operator precedence.

        Multi-pass evaluation:
        1. LSH, RSH
        2. *, /, %
        3. +, -
        4. AND
        5. XOR
        6. OR

        Args:
            tokens: A list of alternating int values and operator strings.

        Returns:
            The computed integer result.

        Raises:
            ValueError: On division by zero.
        """
        tokens = list(tokens)

        passes = [
            {"LSH", "RSH"},
            {"*", "/", "%"},
            {"+", "-"},
            {"AND"},
            {"XOR"},
            {"OR"},
        ]

        for ops in passes:
            i = 1
            while i < len(tokens):
                if isinstance(tokens[i], str) and tokens[i] in ops:
                    left = tokens[i - 1]
                    op = tokens[i]
                    right = tokens[i + 1]
                    result = self._apply_op(op, left, right)
                    tokens[i - 1:i + 2] = [result]
                else:
                    i += 1

        return int(tokens[0])

    def _apply_op(self, op: str, left: int, right: int) -> int:
        """Apply a single operator to two integer operands.

        Args:
            op: The operator string.
            left: The left operand.
            right: The right operand.

        Returns:
            The integer result.

        Raises:
            ValueError: On division by zero.
        """
        if op == "+":
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            if right == 0:
                raise ValueError("Division by zero")
            return int(left / right)
        if op == "%":
            if right == 0:
                raise ValueError("Division by zero")
            return int(left % right)
        if op == "AND":
            return left & right
        if op == "OR":
            return left | right
        if op == "XOR":
            return left ^ right
        if op == "LSH":
            return left << right
        if op == "RSH":
            return left >> right
        return 0

    def bitwise_and(self) -> None:
        """Start a bitwise AND operation."""
        self.add_operator("AND")

    def bitwise_or(self) -> None:
        """Start a bitwise OR operation."""
        self.add_operator("OR")

    def bitwise_xor(self) -> None:
        """Start a bitwise XOR operation."""
        self.add_operator("XOR")

    def bitwise_not(self) -> int:
        """Compute the bitwise NOT of the current value.

        Returns:
            The bitwise complement after masking.
        """
        self.current_value = self.mask_value(~self.current_value)
        self.input_buffer = ""
        self._new_input = True
        return self.current_value

    def left_shift(self) -> None:
        """Start a left shift operation."""
        self.add_operator("LSH")

    def right_shift(self) -> None:
        """Start a right shift operation."""
        self.add_operator("RSH")

    def append_hex_digit(self, digit: str) -> None:
        """Append a hexadecimal digit when in HEX base.

        Args:
            digit: A hex digit character ('A'-'F').
        """
        if self.base != "HEX":
            return
        digit = digit.upper()
        if digit not in {"A", "B", "C", "D", "E", "F"}:
            return

        if self.error:
            self.clear_error()
            self.clear_all()

        if self._new_input:
            self.input_buffer = ""
            self._new_input = False

        if self.input_buffer == "0":
            self.input_buffer = digit
        else:
            self.input_buffer += digit

        self.current_value = int(self.input_buffer, 16)

    def append_digit(self, digit: str) -> None:
        """Append a digit in the current base.

        Parses the input buffer using the current base's radix.

        Args:
            digit: A single digit character valid for the current base.
        """
        if digit not in self.get_valid_digits():
            return

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

        base_int = BASE_MAP.get(self.base, 10)
        self.current_value = int(self.input_buffer, base_int)

    def append_decimal(self) -> None:
        """No-op for programmer calculator (integers only)."""
        pass

    def toggle_sign(self) -> None:
        """Negate the current value and apply masking."""
        self.current_value = self.mask_value(-self.current_value)
        self.input_buffer = ""
        self._new_input = True

    def format_number(self, value: ...) -> str:
        """Format an integer value for display in the current base.

        Args:
            value: The integer to format.

        Returns:
            The formatted string in the current base.
        """
        return self.get_value_in_base(self.base)

    def get_display_value(self) -> str:
        """Get the current display value.

        Returns:
            The input buffer if actively inputting, otherwise the
            formatted current value in the current base.
        """
        if not self._new_input and self.input_buffer:
            return self.input_buffer
        return self.get_value_in_base(self.base)

    def percentage(self) -> None:
        """No-op in programmer mode. Modulo is handled via add_operator."""
        pass

    def clear_all(self) -> None:
        """Reset all state except memory, including pending tokens."""
        super().clear_all()
        self.pending_tokens = []
        self.current_value = 0
