"""Programmer mode logic: integer-only arithmetic in multiple bases."""

from typing import Dict

from calculator.logic.base_logic import (
    BaseLogic,
    DisplayState,
    NumberBase,
    WordSize,
)


class ProgrammerLogic(BaseLogic):
    """Integer-only calculator with multiple base support and bitwise ops.

    Internal value is always a Python int, masked to the current word
    size using two's complement on every mutation.
    """

    # Valid digit characters per base (lowercase for lookup)
    _VALID_DIGITS: Dict[NumberBase, str] = {
        NumberBase.BIN: "01",
        NumberBase.OCT: "01234567",
        NumberBase.DEC: "0123456789",
        NumberBase.HEX: "0123456789abcdef",
    }

    def __init__(self) -> None:
        super().__init__()
        self._int_value: int = 0
        self._number_base: NumberBase = NumberBase.DEC
        self._word_size: WordSize = WordSize.BITS_64
        self._pending_op: str = ""
        self._first_operand: int = 0
        self._expression: str = ""
        self._current_input: str = "0"

    # ── Two's complement masking ────────────────────────────────

    def _mask(self, value: int) -> int:
        """Apply two's complement masking for the current word size.

        Args:
            value: The integer value to mask.

        Returns:
            The value constrained to the current word size range.
        """
        bits = self._word_size.value
        mask = (1 << bits) - 1
        value = value & mask
        if value >= (1 << (bits - 1)):
            value -= (1 << bits)
        return value

    # ── Base conversion / formatting ────────────────────────────

    @staticmethod
    def _format_in_base(value: int, base: NumberBase) -> str:
        """Format an integer value for display in the given base.

        Args:
            value: The integer to format.
            base: The target number base.

        Returns:
            String representation (uppercase hex, no prefix).
        """
        if base == NumberBase.DEC:
            return str(value)
        # For non-decimal bases, work with the unsigned bit pattern
        # so negative values display as their two's complement form
        # is not needed here because we always store masked values
        # that are already in signed range.  For display in hex/oct/bin
        # we want the unsigned representation of negative numbers.
        if value < 0:
            # We need to figure out the word size from the value itself.
            # Since this is a static method, we handle it by computing
            # based on the magnitude.  However, callers should pass
            # already-masked values so we can infer the word size.
            # This path should not normally be reached from instance
            # methods because they call _format_value_in_base instead.
            return str(value)

        if base == NumberBase.HEX:
            return format(value, "X")
        elif base == NumberBase.OCT:
            return format(value, "o")
        elif base == NumberBase.BIN:
            return format(value, "b")
        return str(value)

    def _format_value_in_base(self, value: int, base: NumberBase) -> str:
        """Format a masked value for display in the given base.

        Handles negative values by converting to unsigned representation
        for non-decimal bases using the current word size.

        Args:
            value: The masked integer value.
            base: The target number base.

        Returns:
            String representation suitable for display.
        """
        if base == NumberBase.DEC:
            return str(value)

        # Convert negative to unsigned for hex/oct/bin display
        if value < 0:
            bits = self._word_size.value
            value = value + (1 << bits)

        if base == NumberBase.HEX:
            return format(value, "X")
        elif base == NumberBase.OCT:
            return format(value, "o")
        elif base == NumberBase.BIN:
            return format(value, "b")
        return str(value)

    def set_base(self, base: NumberBase) -> DisplayState:
        """Change the current number base and update display.

        Args:
            base: The new number base.

        Returns:
            Updated display state.
        """
        self._number_base = base
        self._current_input = self._format_value_in_base(
            self._int_value, self._number_base
        )
        self._new_input = True
        return self.get_display_state()

    def set_word_size(self, ws: WordSize) -> DisplayState:
        """Change the current word size and mask the existing value.

        Args:
            ws: The new word size.

        Returns:
            Updated display state.
        """
        self._word_size = ws
        self._int_value = self._mask(self._int_value)
        self._first_operand = self._mask(self._first_operand)
        self._current_input = self._format_value_in_base(
            self._int_value, self._number_base
        )
        self._new_input = True
        return self.get_display_state()

    # ── Input handling ──────────────────────────────────────────

    def input_digit(self, digit: str) -> DisplayState:
        """Append a digit to the current input in the current base.

        Validates that the digit is valid for the current base.
        Builds up _current_input and updates _int_value by parsing
        the full input string.

        Args:
            digit: A single character digit (0-9 or A-F).

        Returns:
            Updated display state.
        """
        if self._error:
            self._error = False
            self._current_input = "0"
            self._expression = ""
            self._new_input = True

        # Validate digit for current base
        if digit.lower() not in self._VALID_DIGITS[self._number_base]:
            return self.get_display_state()

        if self._new_input:
            self._current_input = digit.upper() if self._number_base == NumberBase.HEX else digit
            self._new_input = False
        else:
            if self._current_input == "0":
                self._current_input = digit.upper() if self._number_base == NumberBase.HEX else digit
            else:
                self._current_input += digit.upper() if self._number_base == NumberBase.HEX else digit

        # Parse the full input string to update _int_value
        self._int_value = self._mask(
            int(self._current_input, self._number_base.value)
        )
        # Re-format in case masking changed the value
        reformatted = self._format_value_in_base(
            self._int_value, self._number_base
        )
        # Only replace current_input if masking actually truncated
        if int(self._current_input, self._number_base.value) != (
            self._int_value
            if self._int_value >= 0
            else self._int_value + (1 << self._word_size.value)
        ):
            self._current_input = reformatted

        return self.get_display_state()

    def input_decimal(self) -> DisplayState:
        """No-op in programmer mode (PM-3).

        Returns:
            Current display state unchanged.
        """
        return self.get_display_state()

    def input_sign_toggle(self) -> DisplayState:
        """Negate the current value and mask.

        Returns:
            Updated display state.
        """
        if self._error:
            return self.get_display_state()

        self._int_value = self._mask(-self._int_value)
        self._current_input = self._format_value_in_base(
            self._int_value, self._number_base
        )
        self._new_input = True
        return self.get_display_state()

    def input_backspace(self) -> DisplayState:
        """Remove the last character from current input and reparse.

        Returns:
            Updated display state.
        """
        if self._error or self._new_input:
            return self.get_display_state()

        self._current_input = self._current_input[:-1]
        if not self._current_input or self._current_input == "-":
            self._current_input = "0"
            self._int_value = 0
            self._new_input = True
        else:
            self._int_value = self._mask(
                int(self._current_input, self._number_base.value)
            )

        return self.get_display_state()

    # ── Arithmetic operators ────────────────────────────────────

    def _commit_pending(self) -> None:
        """Evaluate the pending operation if one exists.

        Stores result in _int_value and clears pending op.
        """
        if self._pending_op:
            result = self._apply_op(
                self._first_operand, self._pending_op, self._int_value
            )
            if result is None:
                self._error = True
                self._current_input = "Error"
                self._pending_op = ""
                self._expression = ""
                return
            self._int_value = self._mask(result)

    def input_operator(self, op: str) -> DisplayState:
        """Handle an arithmetic or bitwise binary operator.

        Supported operators: +, -, *, /, %

        Args:
            op: The operator string.

        Returns:
            Updated display state.
        """
        if self._error:
            return self.get_display_state()

        if not self._new_input:
            self._commit_pending()
            if self._error:
                return self.get_display_state()

        self._first_operand = self._int_value
        self._pending_op = op
        self._expression = (
            f"{self._format_value_in_base(self._int_value, self._number_base)}"
            f" {op} "
        )
        self._current_input = self._format_value_in_base(
            self._int_value, self._number_base
        )
        self._new_input = True
        return self.get_display_state()

    def _apply_op(self, a: int, op: str, b: int) -> "int | None":
        """Apply a binary operation.

        Args:
            a: Left operand.
            op: Operator string.
            b: Right operand.

        Returns:
            Result integer, or None on error (e.g. division by zero).
        """
        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            return a * b
        elif op == "/":
            if b == 0:
                return None
            return int(a / b)
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

    # ── Bitwise operations ──────────────────────────────────────

    def bitwise_and(self) -> DisplayState:
        """Set up bitwise AND as a binary operator.

        Returns:
            Updated display state.
        """
        return self.input_operator("AND")

    def bitwise_or(self) -> DisplayState:
        """Set up bitwise OR as a binary operator.

        Returns:
            Updated display state.
        """
        return self.input_operator("OR")

    def bitwise_xor(self) -> DisplayState:
        """Set up bitwise XOR as a binary operator.

        Returns:
            Updated display state.
        """
        return self.input_operator("XOR")

    def bitwise_not(self) -> DisplayState:
        """Apply bitwise NOT (complement) to the current value.

        Returns:
            Updated display state.
        """
        if self._error:
            return self.get_display_state()

        self._int_value = self._mask(~self._int_value)
        self._current_input = self._format_value_in_base(
            self._int_value, self._number_base
        )
        self._new_input = True
        return self.get_display_state()

    def left_shift(self) -> DisplayState:
        """Set up left shift as a binary operator.

        Returns:
            Updated display state.
        """
        return self.input_operator("LSH")

    def right_shift(self) -> DisplayState:
        """Set up right shift as a binary operator.

        Returns:
            Updated display state.
        """
        return self.input_operator("RSH")

    # ── Evaluation ──────────────────────────────────────────────

    def evaluate(self) -> DisplayState:
        """Apply the pending operation and return the result.

        Integer division truncates toward zero (uses int(a / b)).
        Division or modulo by zero produces an error.

        Returns:
            Updated display state.
        """
        if self._error:
            return self.get_display_state()

        if self._pending_op:
            result = self._apply_op(
                self._first_operand, self._pending_op, self._int_value
            )
            if result is None:
                self._error = True
                self._current_input = "Error"
                self._expression = ""
                self._pending_op = ""
                return self.get_display_state()

            self._int_value = self._mask(result)
            self._expression = ""
            self._pending_op = ""
            self._current_input = self._format_value_in_base(
                self._int_value, self._number_base
            )
            self._new_input = True

        return self.get_display_state()

    # ── Display ─────────────────────────────────────────────────

    def get_display_state(self) -> DisplayState:
        """Build and return the current DisplayState for the View.

        Includes all four base representations of the current value.

        Returns:
            A DisplayState snapshot.
        """
        main = self._current_input if not self._error else "Error"

        return DisplayState(
            main_display=main,
            expression_display=self._expression,
            error=self._error,
            memory_indicator=self.has_memory,
            number_base=self._number_base,
            word_size=self._word_size,
            hex_value=self._format_value_in_base(
                self._int_value, NumberBase.HEX
            ),
            dec_value=self._format_value_in_base(
                self._int_value, NumberBase.DEC
            ),
            oct_value=self._format_value_in_base(
                self._int_value, NumberBase.OCT
            ),
            bin_value=self._format_value_in_base(
                self._int_value, NumberBase.BIN
            ),
        )

    def get_button_enabled_state(self) -> Dict[str, bool]:
        """Return which digit and hex-digit buttons are valid for the current base.

        Returns:
            Dictionary mapping digit characters to enabled status.
        """
        valid = self._VALID_DIGITS[self._number_base]
        all_digits = "0123456789abcdef"
        return {d.upper(): d in valid for d in all_digits}

    # ── Clear ───────────────────────────────────────────────────

    def clear_all(self) -> DisplayState:
        """Reset all programmer-specific state except memory.

        Returns:
            Updated display state.
        """
        super().clear_all()
        self._int_value = 0
        self._pending_op = ""
        self._first_operand = 0
        self._expression = ""
        self._current_input = "0"
        return self.get_display_state()

    # ── Mode switching support ──────────────────────────────────

    def get_current_value(self) -> float:
        """Return the current integer value as a float for mode switching.

        Returns:
            The current integer value as a float.
        """
        return float(self._int_value)

    def set_current_value(self, value: float) -> DisplayState:
        """Set the current value from an external source (mode switch).

        Truncates the float to an integer and masks to word size.

        Args:
            value: The value to set (will be truncated to int).

        Returns:
            Updated display state.
        """
        self._int_value = self._mask(int(value))
        self._current_input = self._format_value_in_base(
            self._int_value, self._number_base
        )
        self._expression = ""
        self._error = False
        self._new_input = True
        self._pending_op = ""
        self._first_operand = 0
        return self.get_display_state()
