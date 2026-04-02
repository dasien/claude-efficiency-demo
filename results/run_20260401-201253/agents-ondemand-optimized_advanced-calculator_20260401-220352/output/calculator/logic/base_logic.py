"""Base calculator logic with memory, display formatting, and expression parsing.

Provides the shared foundation for all calculator modes including the
shunting-yard expression parser, memory operations, and input management.
"""

from __future__ import annotations


class CalculatorError(Exception):
    """Raised for all user-facing calculator errors."""

    pass


class ExpressionParser:
    """Parses and evaluates mathematical expressions with operator precedence.

    Uses the shunting-yard algorithm to convert infix to postfix notation,
    then evaluates the postfix expression. Does NOT use Python's eval().

    Supported operators (in precedence order, low to high):
      - OR (bitwise, precedence 1)
      - XOR (bitwise, precedence 2)
      - AND (bitwise, precedence 3)
      - Addition (+), Subtraction (-) (precedence 4)
      - Multiplication (*), Division (/), Modulo (MOD/%) (precedence 5)
      - Left Shift (LSH), Right Shift (RSH) (precedence 6)
      - Power (**) (precedence 7, right-associative)
      - Parentheses override precedence
    """

    PRECEDENCE: dict[str, int] = {
        "OR": 1,
        "XOR": 2,
        "AND": 3,
        "+": 4,
        "-": 4,
        "*": 5,
        "/": 5,
        "MOD": 5,
        "LSH": 6,
        "RSH": 6,
        "**": 7,
    }

    RIGHT_ASSOCIATIVE: set[str] = {"**"}

    def _is_operator(self, token: object) -> bool:
        """Check if a token is a known operator string."""
        return isinstance(token, str) and token in self.PRECEDENCE

    def _to_postfix(self, tokens: list) -> list:
        """Convert infix token list to postfix using shunting-yard algorithm.

        Args:
            tokens: List of numbers (int/float) and operator/paren strings.

        Returns:
            List of tokens in postfix (RPN) order.

        Raises:
            CalculatorError: On mismatched parentheses.
        """
        output: list = []
        operator_stack: list[str] = []

        for token in tokens:
            if isinstance(token, (int, float)):
                output.append(token)
            elif token == "(":
                operator_stack.append(token)
            elif token == ")":
                while operator_stack and operator_stack[-1] != "(":
                    output.append(operator_stack.pop())
                if not operator_stack:
                    raise CalculatorError("Mismatched parentheses")
                operator_stack.pop()  # Remove the '('
            elif self._is_operator(token):
                while (
                    operator_stack
                    and operator_stack[-1] != "("
                    and self._is_operator(operator_stack[-1])
                    and (
                        (
                            token not in self.RIGHT_ASSOCIATIVE
                            and self.PRECEDENCE[token]
                            <= self.PRECEDENCE[operator_stack[-1]]
                        )
                        or (
                            token in self.RIGHT_ASSOCIATIVE
                            and self.PRECEDENCE[token]
                            < self.PRECEDENCE[operator_stack[-1]]
                        )
                    )
                ):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
            else:
                raise CalculatorError(f"Unknown token: {token}")

        while operator_stack:
            op = operator_stack.pop()
            if op == "(":
                raise CalculatorError("Mismatched parentheses")
            output.append(op)

        return output

    def _evaluate_postfix(self, postfix: list) -> float:
        """Evaluate a postfix (RPN) token list.

        Args:
            postfix: Tokens in postfix order.

        Returns:
            The computed result.

        Raises:
            CalculatorError: On division by zero or malformed expression.
        """
        stack: list[float] = []

        for token in postfix:
            if isinstance(token, (int, float)):
                stack.append(float(token))
            elif self._is_operator(token):
                if len(stack) < 2:
                    raise CalculatorError("Malformed expression")
                b = stack.pop()
                a = stack.pop()
                result = self._apply_operator(token, a, b)
                stack.append(result)
            else:
                raise CalculatorError(f"Unknown token in postfix: {token}")

        if len(stack) != 1:
            raise CalculatorError("Malformed expression")

        return stack[0]

    def _apply_operator(
        self, op: str, a: float, b: float
    ) -> float:
        """Apply a binary operator to two operands.

        Args:
            op: The operator string.
            a: Left operand.
            b: Right operand.

        Returns:
            The result of the operation.

        Raises:
            CalculatorError: On division by zero or modulo by zero.
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
            return a / b
        elif op == "MOD":
            if b == 0:
                raise CalculatorError("Division by zero")
            return a % b
        elif op == "**":
            return a ** b
        elif op == "AND":
            return float(int(a) & int(b))
        elif op == "OR":
            return float(int(a) | int(b))
        elif op == "XOR":
            return float(int(a) ^ int(b))
        elif op == "LSH":
            return float(int(a) << int(b))
        elif op == "RSH":
            return float(int(a) >> int(b))
        else:
            raise CalculatorError(f"Unknown operator: {op}")

    def parse(self, tokens: list) -> float:
        """Evaluate a list of infix tokens.

        Args:
            tokens: e.g. [2.0, "+", 3.0, "*", 4.0]

        Returns:
            The evaluated result.

        Raises:
            CalculatorError: On division by zero, mismatched parens,
                or malformed input.
        """
        if not tokens:
            raise CalculatorError("Empty expression")
        postfix = self._to_postfix(tokens)
        return self._evaluate_postfix(postfix)


class BaseCalculator:
    """Shared state and operations for all calculator modes.

    Provides memory functions, display formatting, input management,
    and error state handling. Subclassed by each calculator mode.
    """

    def __init__(self) -> None:
        self.current_input: str = ""
        self.expression: list = []
        self.memory: float = 0.0
        self.has_memory: bool = False
        self.error_state: bool = False
        self.last_result: float | None = None

    # --- Display formatting ---

    def format_number(self, value: float) -> str:
        """Format a number for display.

        Integer results display without decimal point (5 not 5.0).
        Float results use max 10 significant digits.
        Very large/small numbers use scientific notation.

        Args:
            value: The number to format.

        Returns:
            Formatted string representation.
        """
        if isinstance(value, float) and (
            value != value  # NaN check
            or value == float("inf")
            or value == float("-inf")
        ):
            raise CalculatorError("Undefined result")

        try:
            if value == int(value) and abs(value) < 1e15:
                return str(int(value))
        except (OverflowError, ValueError):
            pass

        formatted = f"{value:.10g}"
        return formatted

    # --- Memory operations ---

    def memory_clear(self) -> None:
        """Clear the stored memory value to zero (MC)."""
        self.memory = 0.0
        self.has_memory = False

    def memory_recall(self) -> float:
        """Return the stored memory value (MR).

        Returns:
            The current memory value.
        """
        return self.memory

    def memory_add(self, value: float) -> None:
        """Add the given value to stored memory (M+).

        Args:
            value: The value to add to memory.
        """
        self.memory += value
        self.has_memory = True

    def memory_subtract(self, value: float) -> None:
        """Subtract the given value from stored memory (M-).

        Args:
            value: The value to subtract from memory.
        """
        self.memory -= value
        self.has_memory = True

    def memory_store(self, value: float) -> None:
        """Store the given value in memory, replacing any previous value (MS).

        Args:
            value: The value to store.
        """
        self.memory = value
        self.has_memory = True

    # --- Input management ---

    def append_digit(self, digit: str) -> str:
        """Append a digit to the current input.

        Handles leading-zero prevention: '007' becomes '7'.

        Args:
            digit: A single digit character ('0'-'9').

        Returns:
            The updated current input string.
        """
        if self.error_state:
            self.clear_error()

        if self.current_input == "0" and digit != "0":
            self.current_input = digit
        elif self.current_input == "0" and digit == "0":
            pass  # Prevent leading zeros
        elif self.current_input == "-0" and digit != "0":
            self.current_input = f"-{digit}"
        elif self.current_input == "-0" and digit == "0":
            pass
        else:
            self.current_input += digit

        return self.current_input

    def append_decimal(self) -> str:
        """Add a decimal point to the current input.

        Only one decimal point per number is allowed.
        If current input is empty, starts with '0.'.

        Returns:
            The updated current input string.
        """
        if self.error_state:
            self.clear_error()

        if "." in self.current_input:
            return self.current_input

        if self.current_input == "" or self.current_input == "-":
            prefix = self.current_input if self.current_input == "-" else ""
            self.current_input = f"{prefix}0."
        else:
            self.current_input += "."

        return self.current_input

    def toggle_sign(self, value: float) -> float:
        """Toggle the sign of a value.

        Args:
            value: The value to negate.

        Returns:
            The negated value.
        """
        return -value

    def percentage(self, value: float) -> float:
        """Divide the value by 100.

        Args:
            value: The value to convert to percentage.

        Returns:
            value / 100.
        """
        return value / 100.0

    def backspace(self) -> str:
        """Delete the last character from current input.

        Returns:
            The updated current input string.
        """
        if self.error_state:
            self.clear_error()
            return "0"

        if self.current_input:
            self.current_input = self.current_input[:-1]

        if self.current_input in ("", "-"):
            self.current_input = ""

        return self.current_input if self.current_input else "0"

    def clear_entry(self) -> None:
        """Reset the current entry to '0' without clearing pending operation (C)."""
        self.current_input = ""
        self.error_state = False

    def all_clear(self) -> None:
        """Reset all state: display, pending operation, expression (AC)."""
        self.current_input = ""
        self.expression = []
        self.error_state = False
        self.last_result = None

    # --- Error recovery ---

    def clear_error(self) -> None:
        """Clear the error state and reset calculator."""
        self.error_state = False
        self.all_clear()

    def get_current_value(self) -> float:
        """Parse and return the current input as a float.

        Returns:
            The current input value, or 0.0 if empty.
        """
        if not self.current_input:
            if self.last_result is not None:
                return self.last_result
            return 0.0
        try:
            return float(self.current_input)
        except ValueError:
            return 0.0

    def get_expression_display(self) -> str:
        """Return the current expression as a string for the secondary display.

        Returns:
            The expression formatted as a human-readable string.
        """
        parts = []
        for token in self.expression:
            if isinstance(token, float):
                parts.append(self.format_number(token))
            elif isinstance(token, int):
                parts.append(str(token))
            else:
                parts.append(str(token))
        return " ".join(parts)
