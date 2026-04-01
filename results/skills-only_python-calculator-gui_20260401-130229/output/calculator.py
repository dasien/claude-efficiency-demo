"""Tkinter GUI calculator application."""

import tkinter as tk

from calculator_logic import CalculatorLogic

# Color constants
COLOR_NUM_BG = "#f0f0f0"
COLOR_OP_BG = "#ff9500"
COLOR_OP_FG = "white"
COLOR_CLEAR_BG = "#ff3b30"
COLOR_CLEAR_FG = "white"
COLOR_EQUALS_BG = "#34c759"
COLOR_EQUALS_FG = "white"
COLOR_DISPLAY_BG = "white"
COLOR_PAREN_BG = "#d4d4d2"

FONT_DISPLAY = ("Helvetica", 24)
FONT_BUTTON = ("Helvetica", 18)

# Button layout: (text, row, col, colspan, bg, fg)
BUTTONS = [
    ("C", 1, 0, 1, COLOR_CLEAR_BG, COLOR_CLEAR_FG),
    ("(", 1, 1, 1, COLOR_PAREN_BG, "black"),
    (")", 1, 2, 1, COLOR_PAREN_BG, "black"),
    ("/", 1, 3, 1, COLOR_OP_BG, COLOR_OP_FG),
    ("7", 2, 0, 1, COLOR_NUM_BG, "black"),
    ("8", 2, 1, 1, COLOR_NUM_BG, "black"),
    ("9", 2, 2, 1, COLOR_NUM_BG, "black"),
    ("*", 2, 3, 1, COLOR_OP_BG, COLOR_OP_FG),
    ("4", 3, 0, 1, COLOR_NUM_BG, "black"),
    ("5", 3, 1, 1, COLOR_NUM_BG, "black"),
    ("6", 3, 2, 1, COLOR_NUM_BG, "black"),
    ("-", 3, 3, 1, COLOR_OP_BG, COLOR_OP_FG),
    ("1", 4, 0, 1, COLOR_NUM_BG, "black"),
    ("2", 4, 1, 1, COLOR_NUM_BG, "black"),
    ("3", 4, 2, 1, COLOR_NUM_BG, "black"),
    ("+", 4, 3, 1, COLOR_OP_BG, COLOR_OP_FG),
    ("0", 5, 0, 2, COLOR_NUM_BG, "black"),
    (".", 5, 2, 1, COLOR_NUM_BG, "black"),
    ("=", 5, 3, 1, COLOR_EQUALS_BG, COLOR_EQUALS_FG),
]

OPERATORS = {"+", "-", "*", "/"}


class CalculatorApp:
    """Tkinter GUI calculator."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.logic = CalculatorLogic()

        self.main_frame = tk.Frame(root, padx=5, pady=5)
        self.main_frame.pack()

        self._create_display()
        self._create_buttons()
        self._bind_keyboard()

    def _create_display(self) -> None:
        """Create the calculator display at the top."""
        self.display = tk.Entry(
            self.main_frame,
            font=FONT_DISPLAY,
            justify="right",
            bg=COLOR_DISPLAY_BG,
            relief="flat",
            borderwidth=2,
            state="readonly",
            readonlybackground=COLOR_DISPLAY_BG,
        )
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 5))
        self._update_display("0")

    def _create_buttons(self) -> None:
        """Create all calculator buttons in a grid."""
        for col in range(4):
            self.main_frame.columnconfigure(col, weight=1, uniform="btn", minsize=70)
        for row in range(1, 6):
            self.main_frame.rowconfigure(row, weight=1, uniform="btn", minsize=60)

        for text, row, col, colspan, bg, fg in BUTTONS:
            btn = tk.Button(
                self.main_frame,
                text=text,
                font=FONT_BUTTON,
                bg=bg,
                fg=fg,
                activebackground=bg,
                relief="flat",
                command=lambda v=text: self._on_button_click(v),
            )
            btn.grid(
                row=row, column=col, columnspan=colspan,
                sticky="nsew", padx=1, pady=1,
            )

    def _on_button_click(self, value: str) -> None:
        """Route a button press to the appropriate logic method."""
        if value.isdigit():
            result = self.logic.input_digit(value)
        elif value == ".":
            result = self.logic.input_decimal()
        elif value in OPERATORS:
            result = self.logic.input_operator(value)
        elif value == "=":
            result = self.logic.input_equals()
        elif value == "C":
            result = self.logic.input_clear()
        else:
            return
        self._update_display(result)

    def _update_display(self, text: str) -> None:
        """Update the display widget."""
        self.display.configure(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, text)
        self.display.configure(state="readonly")

    def _bind_keyboard(self) -> None:
        """Bind keyboard events to calculator actions."""
        self.root.bind("<Key>", self._on_key_press)

    def _on_key_press(self, event: tk.Event) -> None:
        """Handle keyboard input."""
        char = event.char
        keysym = event.keysym

        if char and char in "0123456789":
            self._on_button_click(char)
        elif char and char in "+-*/":
            self._on_button_click(char)
        elif char == ".":
            self._on_button_click(".")
        elif char == "=" or keysym == "Return":
            self._on_button_click("=")
        elif keysym == "Escape":
            self._on_button_click("C")
        elif keysym == "BackSpace":
            result = self.logic.input_backspace()
            self._update_display(result)


def main() -> None:
    """Launch the calculator application."""
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
