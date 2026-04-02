"""Programmer mode view — base conversion, bitwise operations, hex digits."""

import tkinter as tk
from typing import Callable, Dict
from calculator.gui.base_view import (
    BaseView, BTN_DIGIT, BTN_OP, BTN_FUNC, BTN_MEMORY,
    TEXT_COLOR, TEXT_OP_COLOR, BG_COLOR, DISPLAY_BG, EXPR_COLOR
)


class ProgrammerView(BaseView):
    """Programmer calculator mode GUI layout."""

    def __init__(self, parent: tk.Widget, on_button: Callable[[str], None],
                 current_base: int = 10, word_size: int = 64) -> None:
        super().__init__(parent, on_button)
        self.current_base = current_base
        self._digit_buttons: Dict[str, tk.Button] = {}
        self._build_word_size_selector(word_size)
        self._build_base_panel()
        self._build_base_selector(current_base)
        self._build_buttons()
        self.update_digit_states(current_base)

    def _build_word_size_selector(self, word_size: int) -> None:
        """Build word size selector."""
        frame = tk.Frame(self.frame, bg=BG_COLOR)
        frame.pack(fill=tk.X, padx=5, pady=2)

        self.word_size_var = tk.IntVar(value=word_size)
        for bits in [8, 16, 32, 64]:
            rb = tk.Radiobutton(
                frame, text=f"{bits}-bit", variable=self.word_size_var,
                value=bits, font=("Helvetica", 10),
                fg=TEXT_COLOR, bg=BG_COLOR, selectcolor=BTN_FUNC,
                activebackground=BG_COLOR, activeforeground=TEXT_COLOR,
                command=lambda b=bits: self.on_button(f"WORD:{b}")
            )
            rb.pack(side=tk.LEFT, padx=4)

    def _build_base_panel(self) -> None:
        """Build the panel showing value in all four bases."""
        self.base_panel = tk.Frame(self.frame, bg=DISPLAY_BG, padx=5, pady=2)
        self.base_panel.pack(fill=tk.X)

        self.base_labels: Dict[str, tk.Label] = {}
        for name in ["HEX", "DEC", "OCT", "BIN"]:
            lbl = tk.Label(
                self.base_panel, text=f"{name}: 0", font=("Courier", 11),
                fg=EXPR_COLOR, bg=DISPLAY_BG, anchor="w"
            )
            lbl.pack(fill=tk.X)
            self.base_labels[name] = lbl

    def _build_base_selector(self, current_base: int) -> None:
        """Build base selector radio buttons."""
        frame = tk.Frame(self.frame, bg=BG_COLOR)
        frame.pack(fill=tk.X, padx=5, pady=2)

        base_map = {"DEC": 10, "HEX": 16, "OCT": 8, "BIN": 2}
        self.base_var = tk.IntVar(value=current_base)

        for name, val in base_map.items():
            rb = tk.Radiobutton(
                frame, text=name, variable=self.base_var,
                value=val, font=("Helvetica", 11, "bold"),
                fg=TEXT_COLOR, bg=BG_COLOR, selectcolor=BTN_FUNC,
                activebackground=BG_COLOR, activeforeground=TEXT_COLOR,
                command=lambda v=val: self.on_button(f"BASE:{v}")
            )
            rb.pack(side=tk.LEFT, padx=6)

    def update_base_panel(self, bases: Dict[str, str]) -> None:
        """Update the base conversion panel."""
        for name, value in bases.items():
            if name in self.base_labels:
                self.base_labels[name].config(text=f"{name}: {value}")

    def update_digit_states(self, base: int) -> None:
        """Enable/disable digit buttons based on current base."""
        self.current_base = base
        valid = set("0123456789ABCDEF"[:base]) if base <= 10 else set("0123456789ABCDEF"[:base])

        # Map base to valid chars
        if base == 2:
            valid = set("01")
        elif base == 8:
            valid = set("01234567")
        elif base == 10:
            valid = set("0123456789")
        elif base == 16:
            valid = set("0123456789ABCDEF")

        for digit, btn in self._digit_buttons.items():
            if digit.upper() in valid:
                btn.config(state=tk.NORMAL, fg=TEXT_COLOR)
            else:
                btn.config(state=tk.DISABLED, fg="#555555")

    def _build_buttons(self) -> None:
        """Build the programmer mode button grid."""
        grid = tk.Frame(self.frame, bg=BG_COLOR)
        grid.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        for c in range(9):
            grid.columnconfigure(c, weight=1, uniform="btn")
        for r in range(5):
            grid.rowconfigure(r, weight=1, uniform="btn")

        fs = 13

        # Row 0: A, B, C, D, E, F, AND, OR, AC
        for i, hex_d in enumerate("ABCDEF"):
            btn = self.create_button(grid, hex_d, 0, i, bg=BTN_FUNC, font_size=fs)
            self._digit_buttons[hex_d] = btn
        self.create_button(grid, "AND", 0, 6, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "OR", 0, 7, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "AC", 0, 8, bg=BTN_FUNC, font_size=fs)

        # Row 1: NOT, XOR, LSH, RSH, %, C, +/-, MOD, /
        self.create_button(grid, "NOT", 1, 0, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "XOR", 1, 1, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "LSH", 1, 2, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "RSH", 1, 3, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "C", 1, 5, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "+/-", 1, 6, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "MOD", 1, 7, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "/", 1, 8, bg=BTN_OP, fg=TEXT_OP_COLOR)

        # Row 2: [blanks], 7, 8, 9, *
        for c in range(5):
            tk.Frame(grid, bg=BG_COLOR).grid(row=2, column=c, sticky="nsew")
        btn7 = self.create_button(grid, "7", 2, 5)
        btn8 = self.create_button(grid, "8", 2, 6)
        btn9 = self.create_button(grid, "9", 2, 7)
        self.create_button(grid, "*", 2, 8, bg=BTN_OP, fg=TEXT_OP_COLOR)
        self._digit_buttons["7"] = btn7
        self._digit_buttons["8"] = btn8
        self._digit_buttons["9"] = btn9

        # Row 3: [blanks], 4, 5, 6, -
        for c in range(5):
            tk.Frame(grid, bg=BG_COLOR).grid(row=3, column=c, sticky="nsew")
        btn4 = self.create_button(grid, "4", 3, 5)
        btn5 = self.create_button(grid, "5", 3, 6)
        btn6 = self.create_button(grid, "6", 3, 7)
        self.create_button(grid, "-", 3, 8, bg=BTN_OP, fg=TEXT_OP_COLOR)
        self._digit_buttons["4"] = btn4
        self._digit_buttons["5"] = btn5
        self._digit_buttons["6"] = btn6

        # Row 4: [blanks], 1, 2, 3, +
        for c in range(5):
            tk.Frame(grid, bg=BG_COLOR).grid(row=4, column=c, sticky="nsew")
        btn1 = self.create_button(grid, "1", 4, 5)
        btn2 = self.create_button(grid, "2", 4, 6)
        btn3 = self.create_button(grid, "3", 4, 7)
        self.create_button(grid, "+", 4, 8, bg=BTN_OP, fg=TEXT_OP_COLOR)
        self._digit_buttons["1"] = btn1
        self._digit_buttons["2"] = btn2
        self._digit_buttons["3"] = btn3

        # Row 5: [blanks], 0(span2), =, backspace
        grid.rowconfigure(5, weight=1, uniform="btn")
        for c in range(5):
            tk.Frame(grid, bg=BG_COLOR).grid(row=5, column=c, sticky="nsew")
        btn0 = self.create_button(grid, "0", 5, 5, colspan=2)
        self.create_button(grid, "=", 5, 7, bg=BTN_OP, fg=TEXT_OP_COLOR)
        self.create_button(grid, "\u232b", 5, 8, bg=BTN_FUNC)
        self._digit_buttons["0"] = btn0
