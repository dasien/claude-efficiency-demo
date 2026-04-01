"""Tkinter GUI for the calculator application."""

import tkinter as tk

from calculator_logic import CalculatorLogic


class CalculatorApp(tk.Tk):
    """Main calculator window built with Tkinter.

    Provides a display and button grid for basic arithmetic
    operations, delegating all computation to CalculatorLogic.
    """

    def __init__(self) -> None:
        super().__init__()
        self.title("Calculator")
        self.geometry("300x400")
        self.minsize(250, 350)
        self.resizable(True, True)

        self.logic = CalculatorLogic()

        self._create_widgets()
        self._bind_events()

    def _create_widgets(self) -> None:
        """Build the display entry and button grid."""
        # Display
        self.display = tk.Entry(
            self,
            justify="right",
            font=("Courier", 20),
            state="readonly",
            readonlybackground="white",
        )
        self.display.grid(
            row=0, column=0, columnspan=4, sticky="nsew", padx=4, pady=4
        )
        self._update_display("0")

        # Button layout: (text, row, col, rowspan, colspan)
        buttons: list[tuple[str, int, int, int, int]] = [
            ("C", 1, 0, 1, 1),
            ("/", 1, 1, 1, 1),
            ("*", 1, 2, 1, 1),
            ("-", 1, 3, 1, 1),
            ("7", 2, 0, 1, 1),
            ("8", 2, 1, 1, 1),
            ("9", 2, 2, 1, 1),
            ("+", 2, 3, 2, 1),
            ("4", 3, 0, 1, 1),
            ("5", 3, 1, 1, 1),
            ("6", 3, 2, 1, 1),
            ("1", 4, 0, 1, 1),
            ("2", 4, 1, 1, 1),
            ("3", 4, 2, 1, 1),
            ("=", 4, 3, 2, 1),
            ("0", 5, 0, 1, 2),
            (".", 5, 2, 1, 1),
        ]

        for text, row, col, rowspan, colspan in buttons:
            btn = tk.Button(
                self,
                text=text,
                command=lambda t=text: self._on_button_click(t),
            )
            btn.grid(
                row=row,
                column=col,
                rowspan=rowspan,
                columnspan=colspan,
                sticky="nsew",
                padx=2,
                pady=2,
            )

        # Configure row/column weights for proportional resizing
        for col in range(4):
            self.columnconfigure(col, weight=1)
        for row in range(6):
            self.rowconfigure(row, weight=1)

    def _bind_events(self) -> None:
        """Bind keyboard events to calculator actions."""
        for digit in "0123456789":
            self.bind(
                digit,
                lambda event, d=digit: self._on_digit(d),
            )

        self.bind(".", lambda event: self._on_decimal())

        operator_keys = {
            "plus": "+",
            "minus": "-",
            "asterisk": "*",
            "slash": "/",
        }
        for char in "+-*/":
            self.bind(
                char,
                lambda event, op=char: self._on_operator(op),
            )
        for key_name, op in operator_keys.items():
            self.bind(
                f"<{key_name}>",
                lambda event, o=op: self._on_operator(o),
            )

        self.bind("<Return>", lambda event: self._on_equals())
        self.bind("=", lambda event: self._on_equals())
        self.bind("<Escape>", lambda event: self._on_clear())
        self.bind("c", lambda event: self._on_clear())
        self.bind("C", lambda event: self._on_clear())

    def _on_button_click(self, text: str) -> None:
        """Route a button click to the appropriate handler.

        Args:
            text: The label of the button that was clicked.
        """
        if text.isdigit():
            self._on_digit(text)
        elif text in "+-*/":
            self._on_operator(text)
        elif text == ".":
            self._on_decimal()
        elif text == "=":
            self._on_equals()
        elif text == "C":
            self._on_clear()

    def _on_digit(self, digit: str) -> None:
        """Handle a digit input.

        Args:
            digit: A single character '0' through '9'.
        """
        result = self.logic.append_digit(digit)
        self._update_display(result)

    def _on_operator(self, op: str) -> None:
        """Handle an operator input.

        Args:
            op: One of '+', '-', '*', '/'.
        """
        result = self.logic.append_operator(op)
        self._update_display(result)

    def _on_decimal(self) -> None:
        """Handle a decimal point input."""
        result = self.logic.append_decimal()
        self._update_display(result)

    def _on_equals(self) -> None:
        """Handle the equals / evaluate action."""
        result = self.logic.evaluate()
        self._update_display(result)

    def _on_clear(self) -> None:
        """Handle the clear action, resetting the calculator."""
        result = self.logic.clear()
        self._update_display(result)

    def _update_display(self, text: str) -> None:
        """Update the display entry with the given text.

        Temporarily sets the entry to normal state to modify its
        contents, then restores it to readonly.

        Args:
            text: The string to show in the display.
        """
        self.display.configure(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, text)
        self.display.configure(state="readonly")


def main() -> None:
    """Create and run the calculator application."""
    app = CalculatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
