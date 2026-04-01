"""Calculator business logic — pure Python, no GUI dependencies."""

import ast
import operator
from typing import Union

OPERATORS = {"+", "-", "*", "/"}


def safe_eval(expression: str) -> Union[int, float]:
    """Safely evaluate a mathematical expression.

    Only allows numbers, basic arithmetic operators (+, -, *, /),
    and parentheses. Uses AST parsing to prevent code injection.

    Args:
        expression: A string containing a mathematical expression.

    Returns:
        The numeric result of the expression.

    Raises:
        ValueError: If the expression contains disallowed operations.
        ZeroDivisionError: If division by zero occurs.
    """
    if not expression or expression.isspace():
        raise ValueError("Empty expression")

    allowed_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    def _eval_node(node: ast.AST) -> Union[int, float]:
        if isinstance(node, ast.Expression):
            return _eval_node(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp):
            op_func = allowed_ops.get(type(node.op))
            if op_func is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            left = _eval_node(node.left)
            right = _eval_node(node.right)
            return op_func(left, right)
        if isinstance(node, ast.UnaryOp):
            op_func = allowed_ops.get(type(node.op))
            if op_func is None:
                raise ValueError(f"Unsupported operator: {type(node.op).__name__}")
            return op_func(_eval_node(node.operand))
        raise ValueError(f"Unsupported expression element: {type(node).__name__}")

    tree = ast.parse(expression, mode="eval")
    return _eval_node(tree)


def format_result(value: Union[int, float]) -> str:
    """Format a numeric result for display.

    Removes unnecessary trailing zeros from floats.
    Returns integer format when the value is a whole number.

    Args:
        value: The numeric result to format.

    Returns:
        A clean string representation.
    """
    if isinstance(value, float) and value == int(value) and abs(value) < 1e15:
        return str(int(value))
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


class CalculatorLogic:
    """Pure business logic for the calculator.

    Manages expression building, validation, evaluation, and state.
    All methods return the current display string.
    """

    def __init__(self) -> None:
        """Initialize with empty expression."""
        self._expression: str = ""
        self._last_was_eval: bool = False

    @property
    def display_text(self) -> str:
        """Return the current display string."""
        return self._expression if self._expression else "0"

    def add_character(self, char: str) -> str:
        """Append a digit, decimal point, operator, or parenthesis.

        Handles validation:
        - After evaluation, a digit starts a new expression.
        - After evaluation, an operator continues from the result.
        - Consecutive operators replace the previous one.
        - Multiple decimal points in one number are prevented.

        Args:
            char: A single character to append.

        Returns:
            Updated display string.
        """
        if char in OPERATORS:
            return self._add_operator(char)
        if char == ".":
            return self._add_decimal()
        if char in ("(", ")"):
            return self._add_parenthesis(char)
        if char.isdigit():
            return self._add_digit(char)
        return self.display_text

    def _add_digit(self, digit: str) -> str:
        if self._last_was_eval:
            self._expression = digit
            self._last_was_eval = False
        else:
            self._expression += digit
        return self.display_text

    def _add_operator(self, op: str) -> str:
        if self._last_was_eval:
            self._last_was_eval = False

        if not self._expression:
            if op == "-":
                self._expression = "-"
            return self.display_text

        if self._expression[-1] in OPERATORS:
            self._expression = self._expression[:-1] + op
        else:
            self._expression += op
        return self.display_text

    def _add_decimal(self) -> str:
        if self._last_was_eval:
            self._expression = "0."
            self._last_was_eval = False
            return self.display_text

        current_number = self._get_current_number()
        if "." in current_number:
            return self.display_text

        if not self._expression or self._expression[-1] in OPERATORS:
            self._expression += "0."
        else:
            self._expression += "."
        return self.display_text

    def _add_parenthesis(self, paren: str) -> str:
        if self._last_was_eval:
            if paren == "(":
                self._expression = "("
                self._last_was_eval = False
            return self.display_text

        self._expression += paren
        return self.display_text

    def _get_current_number(self) -> str:
        """Extract the current (rightmost) number being typed."""
        result = []
        for char in reversed(self._expression):
            if char.isdigit() or char == ".":
                result.append(char)
            else:
                break
        return "".join(reversed(result))

    def evaluate(self) -> str:
        """Evaluate the current expression.

        Returns:
            Result as a formatted string, or "Error" on failure.
        """
        if not self._expression:
            self._last_was_eval = True
            return "0"

        expr = self._expression.rstrip("+-*/")
        if not expr:
            self._expression = ""
            self._last_was_eval = True
            return "0"

        try:
            result = safe_eval(expr)
            self._expression = format_result(result)
            self._last_was_eval = True
            return self._expression
        except (ValueError, ZeroDivisionError, SyntaxError, TypeError):
            self._expression = ""
            self._last_was_eval = True
            return "Error"

    def clear(self) -> str:
        """Reset to initial state.

        Returns:
            "0"
        """
        self._expression = ""
        self._last_was_eval = False
        return "0"

    def backspace(self) -> str:
        """Remove the last character from the expression.

        Returns:
            Updated display string.
        """
        if self._last_was_eval:
            self._expression = ""
            self._last_was_eval = False
        elif self._expression:
            self._expression = self._expression[:-1]
        return self.display_text
