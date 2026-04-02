"""Programmer mode GUI layout.

Provides integer arithmetic interface with base conversion panel,
base selector, word size selector, hex digit buttons, and bitwise
operation buttons.
"""

from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

from calculator.gui.base_view import BaseView

if TYPE_CHECKING:
    from calculator.app import App


class ProgrammerView(BaseView):
    """Programmer mode button grid layout.

    Includes base conversion panel showing all four bases, base
    selector radio buttons, word size selector, hex digits A-F,
    and bitwise operations.
    """

    def __init__(self, parent: tk.Widget, controller: App) -> None:
        super().__init__(parent, controller)
        self.base_labels: dict[str, tk.Label] = {}
        self.base_var: tk.StringVar = tk.StringVar(value="DEC")
        self.word_var: tk.StringVar = tk.StringVar(value="64")
        self.word_label: tk.Label | None = None
        self.digit_buttons: dict[str, tk.Button] = {}
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create all widgets for programmer mode."""
        main_frame = tk.Frame(self, bg=self.COLOR_BG)
        main_frame.pack(fill="both", expand=True)

        total_cols = 9
        for c in range(total_cols):
            main_frame.columnconfigure(c, weight=1, minsize=58)
        for r in range(10):
            main_frame.rowconfigure(r, weight=1, minsize=40)
        main_frame.rowconfigure(0, weight=2, minsize=100)

        # Display area
        self._create_display(main_frame)

        # Word size indicator in display area
        self.word_label = tk.Label(
            main_frame,
            text="QWORD",
            font=("Helvetica", 10, "bold"),
            fg="#FF9500",
            bg=self.COLOR_DISPLAY_BG,
        )
        self.word_label.grid(
            row=0, column=total_cols - 1, sticky="ne", padx=5, pady=5
        )

        # Base conversion panel (row 1)
        panel_frame = tk.Frame(main_frame, bg="#1A1A1A")
        panel_frame.grid(
            row=1, column=0, columnspan=total_cols,
            sticky="nsew", padx=1, pady=1,
        )
        for i in range(4):
            panel_frame.columnconfigure(i, weight=1)
        panel_frame.rowconfigure(0, weight=1)

        for i, (label, key) in enumerate([
            ("HEX", "HEX"), ("DEC", "DEC"),
            ("OCT", "OCT"), ("BIN", "BIN"),
        ]):
            lbl = tk.Label(
                panel_frame,
                text=f"{label}: 0",
                font=("Courier", 10),
                fg="#CCCCCC",
                bg="#1A1A1A",
                anchor="w",
            )
            lbl.grid(row=0, column=i, sticky="ew", padx=5, pady=2)
            self.base_labels[key] = lbl

        # Base selector (row 2)
        base_frame = tk.Frame(main_frame, bg=self.COLOR_BG)
        base_frame.grid(
            row=2, column=0, columnspan=total_cols, sticky="nsew"
        )
        for i in range(4):
            base_frame.columnconfigure(i, weight=1)

        bases = [("DEC", "10"), ("HEX", "16"), ("OCT", "8"), ("BIN", "2")]
        for i, (label, val) in enumerate(bases):
            rb = tk.Radiobutton(
                base_frame,
                text=label,
                variable=self.base_var,
                value=label,
                command=lambda v=val: self.controller.on_base_change(
                    int(v)
                ),
                font=("Helvetica", 11),
                fg="#FFFFFF",
                bg=self.COLOR_BG,
                selectcolor="#505050",
                activebackground=self.COLOR_BG,
                activeforeground="#FFFFFF",
                indicatoron=True,
            )
            rb.grid(row=0, column=i, padx=5, pady=2)

        # Word size selector
        word_sizes = [("8", "BYTE"), ("16", "WORD"),
                      ("32", "DWORD"), ("64", "QWORD")]
        word_frame = tk.Frame(main_frame, bg=self.COLOR_BG)
        word_frame.grid(
            row=2, column=5, columnspan=4, sticky="nsew"
        )
        for i in range(4):
            word_frame.columnconfigure(i, weight=1)

        for i, (bits, label) in enumerate(word_sizes):
            rb = tk.Radiobutton(
                word_frame,
                text=label,
                variable=self.word_var,
                value=bits,
                command=lambda b=bits: self.controller.on_word_size_change(
                    int(b)
                ),
                font=("Helvetica", 9),
                fg="#AAAAAA",
                bg=self.COLOR_BG,
                selectcolor="#505050",
                activebackground=self.COLOR_BG,
                activeforeground="#FFFFFF",
                indicatoron=True,
            )
            rb.grid(row=0, column=i, padx=2, pady=2)

        # Row 3: A, B, C, D, E, F, AND, OR, AC
        hex_row = [
            ("A", lambda: self.controller.on_digit("A")),
            ("B", lambda: self.controller.on_digit("B")),
            ("C", lambda: self.controller.on_digit("C")),
            ("D", lambda: self.controller.on_digit("D")),
            ("E", lambda: self.controller.on_digit("E")),
            ("F", lambda: self.controller.on_digit("F")),
            ("AND", lambda: self.controller.on_programmer("AND")),
            ("OR", lambda: self.controller.on_programmer("OR")),
            ("AC", self.controller.on_all_clear),
        ]
        for i, (text, cmd) in enumerate(hex_row):
            s = "function"
            btn = self._create_button(
                main_frame, text, 3, i, cmd, style=s
            )
            if text in "ABCDEF":
                self.digit_buttons[text] = btn

        # Row 4: NOT, XOR, LSH, RSH, %, C, +/-, MOD, /
        row4 = [
            ("NOT", lambda: self.controller.on_programmer("NOT")),
            ("XOR", lambda: self.controller.on_programmer("XOR")),
            ("LSH", lambda: self.controller.on_programmer("LSH")),
            ("RSH", lambda: self.controller.on_programmer("RSH")),
            ("%", lambda: self.controller.on_programmer("MOD")),
            ("C", self.controller.on_clear),
            ("+/-", self.controller.on_toggle_sign),
            ("MOD", lambda: self.controller.on_programmer("MOD")),
            ("/", lambda: self.controller.on_operator("/")),
        ]
        for i, (text, cmd) in enumerate(row4):
            s = "operator" if text == "/" else "function"
            self._create_button(main_frame, text, 4, i, cmd, style=s)

        # Row 5: [empty x5], 7, 8, 9, *
        for col in range(5):
            spacer = tk.Frame(main_frame, bg=self.COLOR_BG)
            spacer.grid(row=5, column=col, sticky="nsew")
        for i, digit in enumerate(["7", "8", "9"]):
            btn = self._create_button(
                main_frame, digit, 5, 5 + i,
                lambda d=digit: self.controller.on_digit(d),
                style="digit",
            )
            self.digit_buttons[digit] = btn
        self._create_button(
            main_frame, "*", 5, 8,
            lambda: self.controller.on_operator("*"),
            style="operator",
        )

        # Row 6: [empty x5], 4, 5, 6, -
        for col in range(5):
            spacer = tk.Frame(main_frame, bg=self.COLOR_BG)
            spacer.grid(row=6, column=col, sticky="nsew")
        for i, digit in enumerate(["4", "5", "6"]):
            btn = self._create_button(
                main_frame, digit, 6, 5 + i,
                lambda d=digit: self.controller.on_digit(d),
                style="digit",
            )
            self.digit_buttons[digit] = btn
        self._create_button(
            main_frame, "-", 6, 8,
            lambda: self.controller.on_operator("-"),
            style="operator",
        )

        # Row 7: [empty x5], 1, 2, 3, +
        for col in range(5):
            spacer = tk.Frame(main_frame, bg=self.COLOR_BG)
            spacer.grid(row=7, column=col, sticky="nsew")
        for i, digit in enumerate(["1", "2", "3"]):
            btn = self._create_button(
                main_frame, digit, 7, 5 + i,
                lambda d=digit: self.controller.on_digit(d),
                style="digit",
            )
            self.digit_buttons[digit] = btn
        self._create_button(
            main_frame, "+", 7, 8,
            lambda: self.controller.on_operator("+"),
            style="operator",
        )

        # Row 8: [empty x5], 0 (span 2), =, backspace
        for col in range(5):
            spacer = tk.Frame(main_frame, bg=self.COLOR_BG)
            spacer.grid(row=8, column=col, sticky="nsew")
        btn = self._create_button(
            main_frame, "0", 8, 5,
            lambda: self.controller.on_digit("0"),
            colspan=2, style="digit",
        )
        self.digit_buttons["0"] = btn
        self._create_button(
            main_frame, "=", 8, 7,
            self.controller.on_equals, style="equals"
        )
        self._create_button(
            main_frame, "\u232b", 8, 8,
            self.controller.on_backspace, style="function"
        )

    def update_base_panel(self, values: dict[str, str]) -> None:
        """Update the base conversion panel with current values.

        Args:
            values: Dict with keys 'DEC', 'HEX', 'OCT', 'BIN'.
        """
        for key, label in self.base_labels.items():
            val = values.get(key, "0")
            label.configure(text=f"{key}: {val}")

    def update_button_states(self, valid_digits: set[str]) -> None:
        """Enable/disable digit and hex buttons based on current base.

        Args:
            valid_digits: Set of valid digit characters.
        """
        for digit_text, btn in self.digit_buttons.items():
            if digit_text.upper() in valid_digits:
                btn.configure(state="normal")
            else:
                btn.configure(state="disabled")

    def update_word_display(self, bits: int) -> None:
        """Update the word size display indicator.

        Args:
            bits: Current word size (8, 16, 32, or 64).
        """
        labels = {8: "BYTE", 16: "WORD", 32: "DWORD", 64: "QWORD"}
        if self.word_label:
            self.word_label.configure(text=labels.get(bits, str(bits)))
        self.word_var.set(str(bits))

    def update_base_selector(self, base: int) -> None:
        """Update the base selector to reflect the current base.

        Args:
            base: Current base (2, 8, 10, or 16).
        """
        base_names = {10: "DEC", 16: "HEX", 8: "OCT", 2: "BIN"}
        self.base_var.set(base_names.get(base, "DEC"))
