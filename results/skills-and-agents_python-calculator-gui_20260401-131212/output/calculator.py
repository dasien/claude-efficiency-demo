"""Tkinter GUI for a calculator application."""

import tkinter as tk
from typing import Optional

from calculator_logic import CalculatorLogic

# Color constants
COLOR_BG = "#1C1C1C"
COLOR_DISPLAY_BG = "#1C1C1C"
COLOR_DISPLAY_FG = "#FFFFFF"
COLOR_NUMBER_BG = "#505050"
COLOR_NUMBER_FG = "#FFFFFF"
COLOR_OPERATOR_BG = "#FF9500"
COLOR_OPERATOR_FG = "#FFFFFF"
COLOR_SPECIAL_BG = "#A5A5A5"
COLOR_SPECIAL_FG = "#000000"


class CalculatorApp(tk.Tk):
    """A calculator GUI application using Tkinter."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Calculator")
        self.geometry("300x400")
        self.resizable(False, False)
        self.configure(bg=COLOR_BG)

        self.logic = CalculatorLogic()

        self._create_widgets()
        self._bind_events()

    def _create_widgets(self) -> None:
        """Create all GUI widgets."""
        # Configure grid weights for uniform sizing
        for col in range(4):
            self.columnconfigure(col, weight=1)
        for row in range(1, 6):
            self.rowconfigure(row, weight=1)
        self.rowconfigure(0, weight=1)

        # Display
        self.display = tk.Entry(
            self,
            font=("Helvetica", 28),
            justify=tk.RIGHT,
            readonlybackground=COLOR_DISPLAY_BG,
            fg=COLOR_DISPLAY_FG,
            bd=0,
            state="readonly",
            highlightthickness=0,
        )
        self.display.grid(
            row=0, column=0, columnspan=4,
            sticky="nsew", padx=5, pady=(10, 5),
        )

        # Row 1: C, +/-, %, /
        self._create_button("C", 1, 0, "special", self._on_clear)
        self._create_button("+/-", 1, 1, "special", self._on_toggle_sign)
        self._create_button("%", 1, 2, "special", self._on_percent)
        self._create_button("/", 1, 3, "operator", self._on_operator)

        # Row 2: 7, 8, 9, *
        self._create_button("7", 2, 0, "number", self._on_digit)
        self._create_button("8", 2, 1, "number", self._on_digit)
        self._create_button("9", 2, 2, "number", self._on_digit)
        self._create_button("*", 2, 3, "operator", self._on_operator)

        # Row 3: 4, 5, 6, -
        self._create_button("4", 3, 0, "number", self._on_digit)
        self._create_button("5", 3, 1, "number", self._on_digit)
        self._create_button("6", 3, 2, "number", self._on_digit)
        self._create_button("-", 3, 3, "operator", self._on_operator)

        # Row 4: 1, 2, 3, +
        self._create_button("1", 4, 0, "number", self._on_digit)
        self._create_button("2", 4, 1, "number", self._on_digit)
        self._create_button("3", 4, 2, "number", self._on_digit)
        self._create_button("+", 4, 3, "operator", self._on_operator)

        # Row 5: 0 (span 2), ., =
        self._create_button(
            "0", 5, 0, "number", self._on_digit, colspan=2,
        )
        self._create_button(".", 5, 2, "number", self._on_decimal)
        self._create_button("=", 5, 3, "operator", self._on_evaluate)

        self._update_display()

    def _create_button(
        self,
        text: str,
        row: int,
        col: int,
        style: str,
        command: Optional[object] = None,
        colspan: int = 1,
    ) -> tk.Button:
        """Create a styled button and place it on the grid.

        Args:
            text: The button label.
            row: Grid row.
            col: Grid column.
            style: One of 'number', 'operator', or 'special'.
            command: Callback function for the button.
            colspan: Number of columns to span.

        Returns:
            The created Button widget.
        """
        colors = {
            "number": (COLOR_NUMBER_BG, COLOR_NUMBER_FG),
            "operator": (COLOR_OPERATOR_BG, COLOR_OPERATOR_FG),
            "special": (COLOR_SPECIAL_BG, COLOR_SPECIAL_FG),
        }
        bg, fg = colors.get(style, (COLOR_NUMBER_BG, COLOR_NUMBER_FG))

        button = tk.Button(
            self,
            text=text,
            font=("Helvetica", 18),
            bg=bg,
            fg=fg,
            activebackground=bg,
            activeforeground=fg,
            bd=0,
            highlightthickness=0,
            command=lambda: command(text) if command else None,
        )
        button.grid(
            row=row, column=col, columnspan=colspan,
            sticky="nsew", padx=2, pady=2,
        )
        return button

    def _bind_events(self) -> None:
        """Bind keyboard events to calculator actions."""
        self.bind("<Key>", self._on_key_press)

    def _on_key_press(self, event: tk.Event) -> None:
        """Handle keyboard input."""
        key = event.char
        keysym = event.keysym

        if key in "0123456789":
            self._on_digit(key)
        elif key in "+-*/":
            self._on_operator(key)
        elif key == ".":
            self._on_decimal(key)
        elif keysym in ("Return", "KP_Enter"):
            self._on_evaluate("=")
        elif keysym == "Escape":
            self._on_clear("C")
        elif keysym == "BackSpace":
            self._on_backspace()

    def _on_digit(self, text: str) -> None:
        """Handle digit button press."""
        self.logic.add_digit(text)
        self._update_display()

    def _on_operator(self, text: str) -> None:
        """Handle operator button press."""
        if text == "=":
            self._on_evaluate(text)
            return
        self.logic.add_operator(text)
        self._update_display()

    def _on_decimal(self, text: str = ".") -> None:
        """Handle decimal button press."""
        self.logic.add_decimal()
        self._update_display()

    def _on_evaluate(self, text: str = "=") -> None:
        """Handle evaluate button press."""
        self.logic.evaluate()
        self._update_display()

    def _on_clear(self, text: str = "C") -> None:
        """Handle clear button press."""
        self.logic.clear()
        self._update_display()

    def _on_toggle_sign(self, text: str = "+/-") -> None:
        """Handle toggle sign button press."""
        self.logic.toggle_sign()
        self._update_display()

    def _on_percent(self, text: str = "%") -> None:
        """Handle percent button press."""
        self.logic.add_percent()
        self._update_display()

    def _on_backspace(self) -> None:
        """Handle backspace key press."""
        self.logic.backspace()
        self._update_display()

    def _update_display(self) -> None:
        """Update the display Entry with the current value."""
        self.display.configure(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, self.logic.get_display())
        self.display.configure(state="readonly")


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
