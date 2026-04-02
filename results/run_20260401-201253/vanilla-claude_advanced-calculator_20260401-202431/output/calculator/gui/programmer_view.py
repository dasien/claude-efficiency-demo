"""Programmer mode GUI layout."""

import tkinter as tk
from typing import Callable, Dict, List
from .base_view import BaseView, COLORS


class ProgrammerView(BaseView):
    """Programmer calculator mode view."""

    def __init__(self, parent: tk.Widget, callback: Callable[[str], None]) -> None:
        """Initialize programmer view with base conversion panel and button grid."""
        super().__init__(parent, callback)
        self._word_label = None
        self._base_var = tk.StringVar(value="DEC")
        self._base_labels: Dict[str, tk.Label] = {}
        self._digit_buttons: Dict[str, tk.Button] = {}
        self._hex_buttons: List[tk.Button] = []
        self._build_word_size_indicator()
        self._build_base_panel()
        self._build_base_selector()
        self._build_buttons()

    def _build_word_size_indicator(self) -> None:
        """Build the word size indicator."""
        self._word_label = tk.Label(
            self.indicator_frame,
            text="64-bit",
            font=("Helvetica", 12),
            fg=COLORS["indicator"],
            bg=COLORS["display_bg"],
            anchor="e",
        )
        self._word_label.pack(side=tk.RIGHT)

    def update_word_size(self, bits: int) -> None:
        """Update the word size indicator."""
        if self._word_label:
            self._word_label.config(text=f"{bits}-bit")

    def _build_base_panel(self) -> None:
        """Build the panel showing all 4 base conversions."""
        panel = tk.Frame(self.frame, bg=COLORS["base_panel_bg"])
        panel.pack(fill=tk.X, padx=10, pady=(5, 0))

        for base in ["HEX", "DEC", "OCT", "BIN"]:
            row = tk.Frame(panel, bg=COLORS["base_panel_bg"])
            row.pack(fill=tk.X, pady=1)
            lbl_name = tk.Label(
                row,
                text=f"{base}:",
                font=("Helvetica Mono", 11),
                fg=COLORS["base_panel_fg"],
                bg=COLORS["base_panel_bg"],
                width=5,
                anchor="w",
            )
            lbl_name.pack(side=tk.LEFT)
            lbl_val = tk.Label(
                row,
                text="0",
                font=("Helvetica Mono", 11),
                fg=COLORS["display_fg"],
                bg=COLORS["base_panel_bg"],
                anchor="w",
            )
            lbl_val.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self._base_labels[base] = lbl_val

    def update_base_conversions(self, conversions: Dict[str, str]) -> None:
        """Update the base conversion panel."""
        for base, label in self._base_labels.items():
            label.config(text=conversions.get(base, "0"))

    def _build_base_selector(self) -> None:
        """Build the base selector radio buttons."""
        sel_frame = tk.Frame(self.frame, bg=COLORS["bg"])
        sel_frame.pack(fill=tk.X, padx=10, pady=5)

        for base in ["DEC", "HEX", "OCT", "BIN"]:
            rb = tk.Radiobutton(
                sel_frame,
                text=base,
                variable=self._base_var,
                value=base,
                font=("Helvetica", 12),
                fg=COLORS["display_fg"],
                bg=COLORS["bg"],
                selectcolor=COLORS["btn_sci"],
                activebackground=COLORS["bg"],
                activeforeground=COLORS["display_fg"],
                command=lambda b=base: self.callback(f"base_{b}"),
            )
            rb.pack(side=tk.LEFT, padx=10)

    def update_base_selector(self, base: str) -> None:
        """Update the base selector to reflect current base."""
        self._base_var.set(base)

    def _build_buttons(self) -> None:
        """Build the button grid for programmer mode."""
        btn_frame = tk.Frame(self.frame, bg=COLORS["bg"])
        btn_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        cols = 9
        rows = 6
        for i in range(cols):
            btn_frame.columnconfigure(i, weight=1, uniform="btn")
        for i in range(rows):
            btn_frame.rowconfigure(i, weight=1, uniform="btn")

        sci_bg = COLORS["btn_sci"]
        sci_fg = COLORS["btn_sci_fg"]
        func_bg = COLORS["btn_func"]
        func_fg = COLORS["btn_func_fg"]
        op_bg = COLORS["btn_op"]
        op_fg = COLORS["btn_op_fg"]

        # Row 0: A, B, C, D, E, F, AND, OR, AC
        hex_defs = [
            ("A", "digit_A", 0),
            ("B", "digit_B", 1),
            ("C", "digit_C", 2),
            ("D", "digit_D", 3),
            ("E", "digit_E", 4),
            ("F", "digit_F", 5),
        ]
        for text, action, c in hex_defs:
            btn = self._make_button(btn_frame, text, action, 0, c, sci_bg, sci_fg)
            self._hex_buttons.append(btn)
            self._digit_buttons[text] = btn

        self._make_button(btn_frame, "AND", "op_AND", 0, 6, sci_bg, sci_fg)
        self._make_button(btn_frame, "OR", "op_OR", 0, 7, sci_bg, sci_fg)
        self._make_button(btn_frame, "AC", "all_clear", 0, 8, func_bg, func_fg)

        # Row 1: NOT, XOR, LSH, RSH, MOD, C, +/-, word_size, /
        self._make_button(btn_frame, "NOT", "bitwise_not", 1, 0, sci_bg, sci_fg)
        self._make_button(btn_frame, "XOR", "op_XOR", 1, 1, sci_bg, sci_fg)
        self._make_button(btn_frame, "LSH", "op_LSH", 1, 2, sci_bg, sci_fg)
        self._make_button(btn_frame, "RSH", "op_RSH", 1, 3, sci_bg, sci_fg)
        self._make_button(btn_frame, "MOD", "op_%", 1, 4, sci_bg, sci_fg)
        self._make_button(btn_frame, "C", "clear_entry", 1, 5, func_bg, func_fg)
        self._make_button(btn_frame, "+/\u2212", "toggle_sign", 1, 6, func_bg, func_fg)

        # Word size cycle button
        self._make_button(btn_frame, "W:64", "cycle_word_size", 1, 7, sci_bg, sci_fg)

        self._make_button(btn_frame, "\u00F7", "op_/", 1, 8, op_bg, op_fg)

        # Row 2-4: digits 7-9/*, 4-6/-, 1-3/+
        digit_rows = [
            [("7", "digit_7"), ("8", "digit_8"), ("9", "digit_9"), ("\u00D7", "op_*")],
            [("4", "digit_4"), ("5", "digit_5"), ("6", "digit_6"), ("\u2212", "op_-")],
            [("1", "digit_1"), ("2", "digit_2"), ("3", "digit_3"), ("+", "op_+")],
        ]
        for r, row_data in enumerate(digit_rows):
            for c, (text, action) in enumerate(row_data):
                col = c + 5
                if c == 3:
                    self._make_button(btn_frame, text, action, r + 2, col, op_bg, op_fg)
                else:
                    btn = self._make_button(btn_frame, text, action, r + 2, col)
                    self._digit_buttons[text] = btn

        # Row 5: 0 (span 2), =, backspace
        btn = self._make_button(btn_frame, "0", "digit_0", 5, 5, colspan=2)
        self._digit_buttons["0"] = btn
        self._make_button(btn_frame, "=", "evaluate", 5, 7, op_bg, op_fg)
        self._make_button(btn_frame, "\u232B", "backspace", 5, 8, func_bg, func_fg)

    def update_digit_states(self, base: str) -> None:
        """Enable/disable digit buttons based on current base."""
        valid = {
            "DEC": set("0123456789"),
            "HEX": set("0123456789ABCDEF"),
            "OCT": set("01234567"),
            "BIN": set("01"),
        }.get(base, set())

        for digit, btn in self._digit_buttons.items():
            if digit in valid:
                btn.config(
                    state=tk.NORMAL,
                    bg=COLORS["btn_digit"] if digit.isdigit() else COLORS["btn_sci"],
                    fg=COLORS["btn_digit_fg"] if digit.isdigit() else COLORS["btn_sci_fg"],
                )
            else:
                btn.config(
                    state=tk.DISABLED,
                    bg=COLORS["btn_disabled"],
                    fg=COLORS["btn_disabled_fg"],
                )
