"""Tkinter GUI calculator application."""

import tkinter as tk

from calculator_logic import CalculatorLogic


class CalculatorApp:
    """Tkinter GUI for the calculator."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Calculator")
        self.root.resizable(False, False)
        self.logic = CalculatorLogic()

        self._create_display()
        self._create_buttons()
        self.root.bind("<Key>", self._on_key_press)

    def _create_display(self) -> None:
        display_frame = tk.Frame(self.root, bg="#f0f0f0")
        display_frame.pack(fill=tk.X, padx=5, pady=5)

        self.expression_label = tk.Label(
            display_frame,
            text="",
            anchor=tk.E,
            font=("Arial", 14),
            fg="#666666",
            bg="#f0f0f0",
            padx=10,
        )
        self.expression_label.pack(fill=tk.X)

        self.result_label = tk.Label(
            display_frame,
            text="0",
            anchor=tk.E,
            font=("Arial", 28, "bold"),
            fg="#000000",
            bg="#f0f0f0",
            padx=10,
        )
        self.result_label.pack(fill=tk.X)

    def _create_buttons(self) -> None:
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configure grid weights for uniform sizing
        for i in range(4):
            button_frame.columnconfigure(i, weight=1)
        for i in range(5):
            button_frame.rowconfigure(i, weight=1)

        btn_config = {"font": ("Arial", 16), "relief": tk.RAISED, "bd": 1}

        # Layout: (text, row, col, colspan, rowspan, bg_color)
        buttons = [
            ("C", 0, 0, 3, 1, "#ff9999"),
            ("/", 0, 3, 1, 1, "#ffcc99"),
            ("7", 1, 0, 1, 1, "#ffffff"),
            ("8", 1, 1, 1, 1, "#ffffff"),
            ("9", 1, 2, 1, 1, "#ffffff"),
            ("*", 1, 3, 1, 1, "#ffcc99"),
            ("4", 2, 0, 1, 1, "#ffffff"),
            ("5", 2, 1, 1, 1, "#ffffff"),
            ("6", 2, 2, 1, 1, "#ffffff"),
            ("-", 2, 3, 1, 1, "#ffcc99"),
            ("1", 3, 0, 1, 1, "#ffffff"),
            ("2", 3, 1, 1, 1, "#ffffff"),
            ("3", 3, 2, 1, 1, "#ffffff"),
            ("+", 3, 3, 1, 1, "#ffcc99"),
            ("0", 4, 0, 2, 1, "#ffffff"),
            (".", 4, 2, 1, 1, "#ffffff"),
            ("=", 4, 3, 1, 1, "#99ccff"),
        ]

        for text, row, col, colspan, rowspan, bg in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                bg=bg,
                command=lambda v=text: self._on_button_click(v),
                **btn_config,
            )
            btn.grid(
                row=row,
                column=col,
                columnspan=colspan,
                rowspan=rowspan,
                sticky="nsew",
                padx=2,
                pady=2,
            )

    def _update_display(self) -> None:
        self.expression_label.config(text=self.logic.get_expression())
        self.result_label.config(text=self.logic.get_result())

    def _on_button_click(self, value: str) -> None:
        if value in "0123456789":
            self.logic.append_digit(value)
        elif value == ".":
            self.logic.append_decimal()
        elif value in "+-*/":
            self.logic.append_operator(value)
        elif value == "=":
            self.logic.evaluate()
        elif value == "C":
            self.logic.clear()

        self._update_display()

    def _on_key_press(self, event: tk.Event) -> None:
        key = event.char
        keysym = event.keysym

        if key in "0123456789":
            self._on_button_click(key)
        elif key == ".":
            self._on_button_click(".")
        elif key in "+-*/":
            self._on_button_click(key)
        elif keysym in ("Return", "KP_Enter", "equal"):
            self._on_button_click("=")
        elif key == "=":
            self._on_button_click("=")
        elif keysym == "Escape" or key in ("c", "C"):
            self._on_button_click("C")


def main() -> None:
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
