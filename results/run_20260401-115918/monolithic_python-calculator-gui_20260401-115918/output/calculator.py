"""Tkinter GUI calculator application."""

import tkinter as tk
from tkinter import ttk

from calculator_logic import CalculatorLogic

BUTTON_LAYOUT = [
    # (label, row, col, columnspan)
    ("C", 1, 0, 1),  ("(", 1, 1, 1),  (")", 1, 2, 1),  ("/", 1, 3, 1),
    ("7", 2, 0, 1),  ("8", 2, 1, 1),  ("9", 2, 2, 1),  ("*", 2, 3, 1),
    ("4", 3, 0, 1),  ("5", 3, 1, 1),  ("6", 3, 2, 1),  ("-", 3, 3, 1),
    ("1", 4, 0, 1),  ("2", 4, 1, 1),  ("3", 4, 2, 1),  ("+", 4, 3, 1),
    ("0", 5, 0, 2),  (".", 5, 2, 1),  ("=", 5, 3, 1),
]

KEY_MAP = {
    "Return": "=",
    "equal": "=",
    "Escape": "C",
    "c": "C",
    "C": "C",
    "BackSpace": "backspace",
}


class CalculatorApp(tk.Tk):
    """Tkinter GUI for the calculator."""

    def __init__(self) -> None:
        """Set up window, create widgets, bind events."""
        super().__init__()
        self.title("Calculator")
        self.geometry("300x400")
        self.resizable(False, False)

        self._logic = CalculatorLogic()
        self._display_var = tk.StringVar(value="0")

        self._create_widgets()
        self._bind_events()

    def _create_widgets(self) -> None:
        """Create the display and button grid."""
        main_frame = ttk.Frame(self, padding=5)
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Display
        display = ttk.Entry(
            main_frame,
            textvariable=self._display_var,
            font=("Courier", 20),
            justify="right",
            state="readonly",
        )
        display.grid(row=0, column=0, columnspan=4, sticky="ew", pady=(0, 5))

        # Configure grid weights
        for col in range(4):
            main_frame.columnconfigure(col, weight=1)
        for row in range(6):
            main_frame.rowconfigure(row, weight=1)

        # Buttons
        style = ttk.Style()
        style.configure("Calc.TButton", font=("Courier", 14))

        for label, row, col, colspan in BUTTON_LAYOUT:
            btn = ttk.Button(
                main_frame,
                text=label,
                style="Calc.TButton",
                command=lambda v=label: self._on_button_click(v),
            )
            btn.grid(
                row=row, column=col, columnspan=colspan,
                sticky="nsew", padx=2, pady=2,
            )

    def _bind_events(self) -> None:
        """Bind keyboard events to handler methods."""
        self.bind("<Key>", self._on_key_press)

    def _update_display(self, text: str) -> None:
        """Update the display widget with the given text."""
        self._display_var.set(text)

    def _on_button_click(self, value: str) -> None:
        """Handle a button press (digit, operator, =, C)."""
        if value == "C":
            result = self._logic.clear()
        elif value == "=":
            result = self._logic.evaluate()
        else:
            result = self._logic.add_character(value)
        self._update_display(result)

    def _on_key_press(self, event: tk.Event) -> None:
        """Handle keyboard input, delegating to _on_button_click."""
        key = event.keysym
        char = event.char

        if key in KEY_MAP:
            mapped = KEY_MAP[key]
            if mapped == "backspace":
                result = self._logic.backspace()
                self._update_display(result)
            else:
                self._on_button_click(mapped)
        elif char and char in "0123456789.+-*/()":
            self._on_button_click(char)


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
