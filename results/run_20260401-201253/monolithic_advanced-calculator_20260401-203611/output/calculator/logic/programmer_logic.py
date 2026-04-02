"""Programmer calculator logic: base conversion, bitwise ops, word size."""

from __future__ import annotations

from enum import Enum

WORD_SIZES = {8, 16, 32, 64}

VALID_DIGITS = {
    "BIN": set("01"),
    "OCT": set("01234567"),
    "DEC": set("0123456789"),
    "HEX": set("0123456789ABCDEF"),
}

BASE_RADIX = {"BIN": 2, "OCT": 8, "DEC": 10, "HEX": 16}

# Operator precedence for programmer mode
_PRECEDENCE = {
    "+": 1, "-": 1,
    "*": 2, "/": 2, "%": 2,
    "AND": 0, "OR": 0, "XOR": 0,
    "LSH": 1, "RSH": 1,
}


class ProgrammerCalculator:
    """Programmer mode calculator with base conversion and bitwise ops.

    All values are integers constrained to the selected word size
    using two's complement representation.
    """

    def __init__(self) -> None:
        self._current_input: str = "0"
        self._base: str = "DEC"
        self._word_size: int = 64
        self._tokens: list[int] = []
        self._operators: list[str] = []
        self._new_input: bool = True
        self._error: bool = False
        self._expression_display: str = ""
        self._just_evaluated: bool = False

    # --- Base mode ---

    def set_base(self, base: str) -> None:
        """Set the number base (DEC, HEX, OCT, BIN)."""
        value = self.get_value()
        self._base = base.upper()
        self._current_input = self._int_to_base_str(value)
        self._new_input = True

    def get_base(self) -> str:
        """Return the current base mode."""
        return self._base

    # --- Word size ---

    def set_word_size(self, bits: int) -> None:
        """Set the word size (8, 16, 32, or 64)."""
        if bits not in WORD_SIZES:
            return
        self._word_size = bits
        value = self.constrain_value(self.get_value())
        self._current_input = self._int_to_base_str(value)
        self._new_input = True

    def get_word_size(self) -> int:
        """Return the current word size in bits."""
        return self._word_size

    def constrain_value(self, value: int) -> int:
        """Constrain a value to the current word size (two's complement)."""
        mask = (1 << self._word_size) - 1
        value = value & mask
        if value >= (1 << (self._word_size - 1)):
            value -= (1 << self._word_size)
        return value

    # --- Input ---

    def input_digit(self, digit: str) -> None:
        """Append a digit to current input, validating for current base."""
        digit = digit.upper()
        if self._error:
            self._clear_error()
        if digit not in VALID_DIGITS[self._base]:
            return
        if self._just_evaluated:
            self.input_all_clear()
        if self._new_input:
            self._current_input = digit
            self._new_input = False
        else:
            if self._current_input == "0":
                self._current_input = digit
            else:
                self._current_input += digit
        # Constrain on input
        value = self.constrain_value(self._parse_input())
        self._current_input = self._int_to_base_str(value)

    def input_negate(self) -> None:
        """Toggle the sign of the current value."""
        if self._error:
            return
        value = self.get_value()
        result = self.constrain_value(-value)
        self._current_input = self._int_to_base_str(result)
        self._just_evaluated = False

    # --- Operators ---

    def input_operator(self, op: str) -> None:
        """Handle an operator (+, -, *, /, %, AND, OR, XOR, LSH, RSH)."""
        if self._error:
            return
        self._push_current_number()
        self._expression_display += (
            f" {self._current_input} {op} "
        )
        op_prec = _PRECEDENCE.get(op, 0)
        while (
            self._operators
            and self._operators[-1] in _PRECEDENCE
            and _PRECEDENCE[self._operators[-1]] >= op_prec
        ):
            self._apply_top_operator()
            if self._error:
                return
        self._operators.append(op)
        self._new_input = True
        self._just_evaluated = False

    def input_equals(self) -> None:
        """Evaluate the full expression."""
        if self._error:
            return
        self._push_current_number()
        while self._operators:
            self._apply_top_operator()
            if self._error:
                return
        if self._tokens:
            result = self.constrain_value(self._tokens[-1])
            self._current_input = self._int_to_base_str(result)
            self._tokens = []
            self._operators = []
            self._expression_display = ""
            self._new_input = True
            self._just_evaluated = True

    # --- Unary operations ---

    def apply_not(self) -> None:
        """Bitwise NOT of the current value."""
        if self._error:
            return
        value = self.get_value()
        result = self.constrain_value(~value)
        self._current_input = self._int_to_base_str(result)
        self._new_input = True
        self._just_evaluated = False

    # --- Clear/edit ---

    def input_clear(self) -> None:
        """Clear current entry."""
        self._current_input = "0"
        self._new_input = True
        self._error = False

    def input_all_clear(self) -> None:
        """Reset all state."""
        self._current_input = "0"
        self._tokens = []
        self._operators = []
        self._new_input = True
        self._error = False
        self._expression_display = ""
        self._just_evaluated = False

    def input_backspace(self) -> None:
        """Delete the last character from current input."""
        if self._error:
            self._clear_error()
            return
        if self._new_input:
            return
        if len(self._current_input) <= 1:
            self._current_input = "0"
            self._new_input = True
        else:
            self._current_input = self._current_input[:-1]

    # --- Display and value access ---

    def get_display(self) -> str:
        """Return the formatted current value for display."""
        if self._error:
            return "Error"
        return self._current_input

    def get_expression(self) -> str:
        """Return the expression string for secondary display."""
        return self._expression_display

    def get_value(self) -> int:
        """Return the current value as a Python int."""
        if self._error:
            return 0
        return self._parse_input()

    def set_value(self, value: int) -> None:
        """Set the current value (for mode switching)."""
        value = self.constrain_value(value)
        self._current_input = self._int_to_base_str(value)
        self._new_input = True
        self._just_evaluated = False

    def is_error(self) -> bool:
        """Return whether the calculator is in an error state."""
        return self._error

    # --- Base conversion ---

    def get_all_bases(self, value: int | None = None) -> dict[str, str]:
        """Return the value represented in all four bases.

        Args:
            value: The integer value. If None, uses current value.

        Returns:
            Dict with keys DEC, HEX, OCT, BIN and string values.
        """
        if value is None:
            value = self.get_value()
        value = self.constrain_value(value)
        mask = (1 << self._word_size) - 1
        unsigned = value & mask
        return {
            "DEC": str(value),
            "HEX": format(unsigned, "X"),
            "OCT": format(unsigned, "o"),
            "BIN": format(unsigned, "b"),
        }

    def get_valid_digits(self) -> list[str]:
        """Return which digits are valid for the current base."""
        digits = sorted(VALID_DIGITS[self._base])
        return digits

    # --- Internal helpers ---

    def _parse_input(self) -> int:
        """Parse the current input string as an integer in current base."""
        try:
            text = self._current_input.strip()
            if not text or text == "-":
                return 0
            radix = BASE_RADIX[self._base]
            if self._base == "DEC":
                return int(text, 10)
            unsigned = int(text, radix)
            # Interpret as two's complement
            if unsigned >= (1 << (self._word_size - 1)):
                return unsigned - (1 << self._word_size)
            return unsigned
        except ValueError:
            return 0

    def _int_to_base_str(self, value: int) -> str:
        """Convert an integer to a string in the current base."""
        value = self.constrain_value(value)
        if self._base == "DEC":
            return str(value)
        mask = (1 << self._word_size) - 1
        unsigned = value & mask
        if self._base == "HEX":
            return format(unsigned, "X")
        elif self._base == "OCT":
            return format(unsigned, "o")
        elif self._base == "BIN":
            return format(unsigned, "b")
        return str(value)

    def _push_current_number(self) -> None:
        """Push the current value onto the token stack."""
        value = self._parse_input()
        if not self._new_input or not self._tokens:
            self._tokens.append(value)
        self._new_input = True

    def _apply_top_operator(self) -> None:
        """Pop the top operator and apply it."""
        if len(self._tokens) < 2 or not self._operators:
            self._error = True
            return
        op = self._operators.pop()
        b = self._tokens.pop()
        a = self._tokens.pop()
        result = self._evaluate_binary(a, op, b)
        if result is None:
            self._error = True
            return
        self._tokens.append(self.constrain_value(result))

    def _evaluate_binary(
        self, a: int, op: str, b: int
    ) -> int | None:
        """Evaluate a binary operation on integers."""
        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            return a * b
        elif op == "/":
            if b == 0:
                return None
            return int(a / b)  # Truncating division
        elif op == "%":
            if b == 0:
                return None
            return a % b
        elif op == "AND":
            return a & b
        elif op == "OR":
            return a | b
        elif op == "XOR":
            return a ^ b
        elif op == "LSH":
            return a << b
        elif op == "RSH":
            return a >> b
        return None

    def _clear_error(self) -> None:
        """Clear error state and reset for new input."""
        self._error = False
        self._current_input = "0"
        self._tokens = []
        self._operators = []
        self._expression_display = ""
        self._new_input = True
        self._just_evaluated = False
