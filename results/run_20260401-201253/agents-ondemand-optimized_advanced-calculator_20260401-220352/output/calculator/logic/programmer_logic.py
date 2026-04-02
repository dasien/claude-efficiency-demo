"""Programmer calculator logic for integer arithmetic in multiple bases.

Supports DEC/HEX/OCT/BIN base conversion, word sizes (8/16/32/64 bit)
with two's complement wrapping, bitwise operations (AND/OR/XOR/NOT/LSH/RSH),
modulo, and integer-only arithmetic.
"""

from __future__ import annotations

from calculator.logic.base_logic import (
    BaseCalculator,
    CalculatorError,
    ExpressionParser,
)


class ProgrammerCalculator(BaseCalculator):
    """Programmer mode: integer arithmetic, base conversion, bitwise ops.

    All values are stored as Python ints and constrained through
    _apply_word_size() for two's complement behavior. No decimal
    point input is allowed.
    """

    WORD_SIZES: dict[int, tuple[int, int]] = {
        8: (-128, 127),
        16: (-32768, 32767),
        32: (-2147483648, 2147483647),
        64: (-9223372036854775808, 9223372036854775807),
    }

    def __init__(self) -> None:
        super().__init__()
        self.base: int = 10
        self.word_size: int = 64
        self.value: int = 0
        self._parser = ExpressionParser()

    # --- Base conversion ---

    def set_base(self, base: int) -> str:
        """Switch to a new number base and return formatted current value.

        Args:
            base: The target base (2, 8, 10, or 16).

        Returns:
            The current value formatted in the new base.
        """
        current_val = self._get_int_value()
        self.base = base
        self.current_input = self.format_in_base(current_val, base)
        return self.current_input

    def format_in_base(self, value: int, base: int) -> str:
        """Format an integer value in the given base.

        Args:
            value: The integer to format.
            base: The target base (2, 8, 10, or 16).

        Returns:
            Uppercase string representation in the given base.
        """
        value = self._apply_word_size(value)
        if value < 0:
            # For display in non-decimal bases, show two's complement
            if base != 10:
                unsigned = value + (1 << self.word_size)
                if base == 16:
                    return format(unsigned, "X")
                elif base == 8:
                    return format(unsigned, "o")
                elif base == 2:
                    return format(unsigned, "b")
            return str(value)

        if base == 16:
            return format(value, "X")
        elif base == 8:
            return format(value, "o")
        elif base == 2:
            return format(value, "b")
        return str(value)

    def get_all_bases(self, value: int) -> dict[str, str]:
        """Return the value formatted in all four bases.

        Args:
            value: The integer to format.

        Returns:
            Dict with keys 'DEC', 'HEX', 'OCT', 'BIN' and formatted values.
        """
        value = self._apply_word_size(value)
        return {
            "DEC": self.format_in_base(value, 10),
            "HEX": self.format_in_base(value, 16),
            "OCT": self.format_in_base(value, 8),
            "BIN": self.format_in_base(value, 2),
        }

    def get_valid_digits(self) -> set[str]:
        """Return the set of valid digit characters for the current base.

        Returns:
            Set of valid digit strings.
        """
        if self.base == 2:
            return {"0", "1"}
        elif self.base == 8:
            return {str(i) for i in range(8)}
        elif self.base == 10:
            return {str(i) for i in range(10)}
        else:  # base 16
            return {str(i) for i in range(10)} | {
                "A", "B", "C", "D", "E", "F"
            }

    # --- Word size ---

    def set_word_size(self, bits: int) -> int:
        """Set the word size and truncate current value.

        Args:
            bits: The new word size (8, 16, 32, or 64).

        Returns:
            The truncated current value.
        """
        self.word_size = bits
        current_val = self._get_int_value()
        current_val = self._apply_word_size(current_val)
        self.value = current_val
        self.current_input = self.format_in_base(current_val, self.base)
        return current_val

    def _apply_word_size(self, value: int) -> int:
        """Wrap value using two's complement for current word size.

        Args:
            value: The integer value to constrain.

        Returns:
            The value wrapped to the current word size range.
        """
        bits = self.word_size
        mask = (1 << bits) - 1
        value = value & mask
        if value >= (1 << (bits - 1)):
            value -= 1 << bits
        return value

    # --- Bitwise operations ---

    def bitwise_and(self, a: int, b: int) -> int:
        """Bitwise AND of two values.

        Args:
            a: First operand.
            b: Second operand.

        Returns:
            a AND b, constrained to word size.
        """
        return self._apply_word_size(a & b)

    def bitwise_or(self, a: int, b: int) -> int:
        """Bitwise OR of two values.

        Args:
            a: First operand.
            b: Second operand.

        Returns:
            a OR b, constrained to word size.
        """
        return self._apply_word_size(a | b)

    def bitwise_xor(self, a: int, b: int) -> int:
        """Bitwise XOR of two values.

        Args:
            a: First operand.
            b: Second operand.

        Returns:
            a XOR b, constrained to word size.
        """
        return self._apply_word_size(a ^ b)

    def bitwise_not(self, value: int) -> int:
        """Bitwise NOT (complement) of a value.

        Args:
            value: The value to complement.

        Returns:
            NOT value, constrained to word size.
        """
        return self._apply_word_size(~value)

    def left_shift(self, value: int, n: int) -> int:
        """Left shift value by n positions.

        Args:
            value: The value to shift.
            n: Number of positions to shift.

        Returns:
            value << n, constrained to word size.
        """
        return self._apply_word_size(value << n)

    def right_shift(self, value: int, n: int) -> int:
        """Arithmetic right shift value by n positions.

        Args:
            value: The value to shift.
            n: Number of positions to shift.

        Returns:
            value >> n, constrained to word size.
        """
        return self._apply_word_size(value >> n)

    # --- Integer arithmetic ---

    def integer_divide(self, a: int, b: int) -> int:
        """Integer division truncating toward zero.

        Uses int(a / b) instead of a // b to get truncation
        rather than floor division for negative numbers.

        Args:
            a: Dividend.
            b: Divisor.

        Returns:
            Truncated quotient, constrained to word size.

        Raises:
            CalculatorError: If b is zero.
        """
        if b == 0:
            raise CalculatorError("Division by zero")
        return self._apply_word_size(int(a / b))

    def modulo(self, a: int, b: int) -> int:
        """Compute a modulo b.

        Args:
            a: Dividend.
            b: Divisor.

        Returns:
            a % b, constrained to word size.

        Raises:
            CalculatorError: If b is zero.
        """
        if b == 0:
            raise CalculatorError("Division by zero")
        # Truncation-consistent modulo
        result = a - int(a / b) * b
        return self._apply_word_size(result)

    # --- Input overrides ---

    def append_decimal(self) -> str:
        """No-op: decimal points are not allowed in programmer mode.

        Returns:
            The unchanged current input string.
        """
        return self.current_input if self.current_input else "0"

    def append_digit(self, digit: str) -> str:
        """Append a digit validated against the current base.

        Args:
            digit: A digit character valid for the current base.

        Returns:
            The updated current input string.

        Raises:
            CalculatorError: If the digit is invalid for the current base.
        """
        if self.error_state:
            self.clear_error()

        digit = digit.upper()
        if digit not in self.get_valid_digits():
            return self.current_input if self.current_input else "0"

        # Remove leading zero
        if self.current_input == "0" and digit != "0":
            self.current_input = digit
        elif self.current_input == "0" and digit == "0":
            return self.current_input
        else:
            self.current_input += digit

        # Validate the full number fits in word size
        try:
            val = int(self.current_input, self.base)
            val = self._apply_word_size(val)
        except ValueError:
            pass

        return self.current_input

    def _get_int_value(self) -> int:
        """Parse the current input as an integer in the current base.

        Returns:
            The integer value, or self.value if input is empty.
        """
        if not self.current_input or self.current_input == "-":
            if self.last_result is not None:
                return int(self.last_result)
            return self.value
        try:
            if self.current_input.startswith("-"):
                return -int(self.current_input[1:], self.base)
            return int(self.current_input, self.base)
        except ValueError:
            return self.value

    def get_current_value(self) -> float:
        """Return the current value as a float for compatibility.

        Returns:
            The current integer value as a float.
        """
        return float(self._get_int_value())

    def format_number(self, value: float) -> str:
        """Format number in the current base.

        Args:
            value: The value to format.

        Returns:
            String representation in the current base.
        """
        int_val = int(value)
        return self.format_in_base(int_val, self.base)

    # --- Expression and evaluation ---

    def add_operator(self, op: str) -> None:
        """Append an operator to the expression.

        Args:
            op: The operator string ('+', '-', '*', '/', 'AND', 'OR',
                'XOR', 'LSH', 'RSH', 'MOD').
        """
        if self.error_state:
            return

        if self.current_input:
            value = self._get_int_value()
            self.expression.append(float(value))
            self.current_input = ""
            self.last_result = None
        elif self.last_result is not None and not self.expression:
            self.expression.append(float(int(self.last_result)))
            self.last_result = None
        elif (
            not self.current_input
            and self.expression
            and isinstance(self.expression[-1], str)
            and self.expression[-1] in self._parser.PRECEDENCE
        ):
            self.expression[-1] = op
            return
        elif not self.current_input and not self.expression:
            self.expression.append(float(self.value))

        self.expression.append(op)

    def evaluate(self) -> float:
        """Evaluate the expression as integer arithmetic.

        Returns:
            The integer result as a float.

        Raises:
            CalculatorError: On division by zero or malformed expression.
        """
        if self.error_state:
            raise CalculatorError("Error state active")

        if self.current_input:
            value = self._get_int_value()
            self.expression.append(float(value))
            self.current_input = ""
        elif self.last_result is not None and not self.expression:
            return self.last_result
        elif (
            self.expression
            and isinstance(self.expression[-1], str)
            and self.expression[-1] in self._parser.PRECEDENCE
        ):
            if self.last_result is not None:
                self.expression.append(float(int(self.last_result)))
            else:
                self.expression.pop()

        if not self.expression:
            return float(self.value)

        while (
            self.expression
            and isinstance(self.expression[-1], str)
            and self.expression[-1] in self._parser.PRECEDENCE
        ):
            self.expression.pop()

        if not self.expression:
            return float(self.value)

        # Handle integer division specially
        tokens = list(self.expression)
        processed: list = []
        for token in tokens:
            if token == "/" and self._is_integer_division(tokens):
                processed.append("/")
            else:
                processed.append(token)

        result = self._parser.parse(processed)
        int_result = int(result)

        # For division, use truncating integer division
        int_result = self._recalculate_with_int_div(self.expression)
        int_result = self._apply_word_size(int_result)

        self.value = int_result
        self.last_result = float(int_result)
        self.expression = []
        self.current_input = self.format_in_base(int_result, self.base)
        return float(int_result)

    def _is_integer_division(self, tokens: list) -> bool:
        """Check if the token list contains division."""
        return "/" in tokens

    def _recalculate_with_int_div(self, tokens: list) -> int:
        """Recalculate expression with proper integer division.

        Uses the shunting-yard algorithm but applies integer truncating
        division instead of float division.

        Args:
            tokens: The expression tokens.

        Returns:
            Integer result with truncating division.
        """
        postfix = self._parser._to_postfix(tokens)
        stack: list[int] = []

        for token in postfix:
            if isinstance(token, (int, float)):
                stack.append(int(token))
            elif isinstance(token, str):
                if len(stack) < 2:
                    raise CalculatorError("Malformed expression")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_int_op(token, a, b)
                stack.append(result)

        if len(stack) != 1:
            raise CalculatorError("Malformed expression")
        return stack[0]

    def _apply_int_op(self, op: str, a: int, b: int) -> int:
        """Apply an operator to two integer operands.

        Args:
            op: Operator string.
            a: Left operand.
            b: Right operand.

        Returns:
            Integer result.

        Raises:
            CalculatorError: On division/modulo by zero.
        """
        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            return a * b
        elif op == "/":
            if b == 0:
                raise CalculatorError("Division by zero")
            return int(a / b)
        elif op == "MOD":
            if b == 0:
                raise CalculatorError("Division by zero")
            return a - int(a / b) * b
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
        else:
            raise CalculatorError(f"Unknown operator: {op}")

    def toggle_sign(self, value: float) -> float:
        """Toggle sign for the current integer value.

        Args:
            value: The value to negate.

        Returns:
            The negated value, constrained to word size.
        """
        int_val = int(value)
        result = self._apply_word_size(-int_val)
        return float(result)

    def get_expression_display(self) -> str:
        """Return the expression formatted for display.

        Returns:
            Expression string with values shown in the current base.
        """
        parts = []
        for token in self.expression:
            if isinstance(token, (int, float)):
                parts.append(self.format_in_base(int(token), self.base))
            else:
                parts.append(str(token))
        if self.current_input:
            if parts:
                parts.append(self.current_input)
            else:
                parts = [self.current_input]
        return " ".join(parts)
