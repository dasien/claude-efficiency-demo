"""Tkinter GUI calculator application using MVC pattern."""

import tkinter as tk
from tkinter import ttk

from calculator_logic import CalculatorLogic

BUTTON_LAYOUT = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
]


class CalculatorApp(tk.Tk):
    """Tkinter GUI calculator application.

    Uses CalculatorLogic for all computation. Handles layout,
    button creation, and event binding.

    Attributes:
        logic: The calculator business logic instance.
        display_var: Variable bound to the display widget.
    """

    def __init__(self) -> None:
        """Initialize the calculator window, widgets, and event bindings."""
        super().__init__()
        self.title("Calculator")
        self.geometry("300x400")
        self.resizable(False, False)

        self.logic = CalculatorLogic()
        self.display_var = tk.StringVar(value="")

        self._create_widgets()
        self._bind_events()

    def _create_widgets(self) -> None:
        """Create the display and all calculator buttons using grid layout."""
        # Configure column weights
        for col in range(4):
            self.columnconfigure(col, weight=1)

        # Display row has fixed height
        self.rowconfigure(0, weight=0)

        # Button rows expand equally
        for row in range(1, 6):
            self.rowconfigure(row, weight=1)

        # Display entry
        display = ttk.Entry(
            self,
            textvariable=self.display_var,
            font=("Courier", 18),
            justify="right",
            state="readonly",
        )
        display.grid(
            row=0, column=0, columnspan=4, sticky="ew", padx=2, pady=2
        )

        # Button grid
        for row_idx, row_buttons in enumerate(BUTTON_LAYOUT):
            for col_idx, label in enumerate(row_buttons):
                btn = ttk.Button(
                    self,
                    text=label,
                    command=lambda v=label: self._on_button_click(v),
                )
                btn.grid(
                    row=row_idx + 1,
                    column=col_idx,
                    sticky="nsew",
                    padx=1,
                    pady=1,
                )

        # Clear button spanning all columns
        clear_btn = ttk.Button(
            self,
            text="C",
            command=lambda: self._on_button_click("C"),
        )
        clear_btn.grid(
            row=5, column=0, columnspan=4, sticky="nsew", padx=1, pady=1
        )

    def _bind_events(self) -> None:
        """Bind keyboard events to calculator actions."""
        self.bind("<Key>", self._on_key_press)

    def _on_key_press(self, event: tk.Event) -> None:
        """Map keyboard characters and keysyms to button click actions.

        Args:
            event: The keyboard event.
        """
        if event.char in "0123456789.+-*/":
            self._on_button_click(event.char)
        elif event.keysym == "Return":
            self._on_button_click("=")
        elif event.keysym in ("Escape", "BackSpace", "Delete"):
            self._on_button_click("C")

    def _on_button_click(self, value: str) -> None:
        """Handle a button click or keyboard input.

        Routes to the appropriate CalculatorLogic method based on
        the value, then updates the display.

        Args:
            value: The button label or key character that was pressed.
        """
        if value == "C":
            result = self.logic.clear()
        elif value == "=":
            result = self.logic.evaluate()
        elif value in "+-*/":
            self.logic.append_operator(value)
            result = self.logic.get_display_text()
        else:
            self.logic.append_number(value)
            result = self.logic.get_display_text()

        self._update_display(result)

    def _update_display(self, text: str) -> None:
        """Update the display widget with the given text.

        Args:
            text: The string to show in the display.
        """
        self.display_var.set(text)


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
