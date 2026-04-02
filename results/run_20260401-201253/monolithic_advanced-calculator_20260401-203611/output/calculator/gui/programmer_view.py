"""Programmer mode GUI layout."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from calculator.gui.base_view import (
    DisplayFrame,
    create_button,
)


class ProgrammerView(ttk.Frame):
    """Programmer calculator mode view with base conversion and bitwise ops."""

    def __init__(
        self,
        parent: tk.Widget,
        on_button: Callable[[str], None],
        **kwargs: object,
    ) -> None:
        super().__init__(parent, **kwargs)
        self._on_button = on_button
        self._digit_buttons: dict[str, ttk.Button] = {}
        self._hex_buttons: dict[str, ttk.Button] = {}

        # Display
        self.display = DisplayFrame(self)
        self.display.pack(fill="x")

        # Word size indicator
        self._word_size_var = tk.StringVar(value="64-bit")
        ws_frame = ttk.Frame(self)
        ws_frame.pack(fill="x", padx=5)
        ttk.Label(
            ws_frame, text="Word Size:",
            font=("Courier", 10),
        ).pack(side="left")
        for bits in [8, 16, 32, 64]:
            ttk.Button(
                ws_frame,
                text=f"{bits}",
                width=4,
                command=lambda b=bits: on_button(
                    f"WORD_{b}"
                ),
            ).pack(side="left", padx=2)
        ttk.Label(
            ws_frame,
            textvariable=self._word_size_var,
            font=("Courier", 10, "bold"),
        ).pack(side="right")

        # Base conversion panel
        self._base_panel_var = tk.StringVar(value="")
        base_panel = ttk.Label(
            self,
            textvariable=self._base_panel_var,
            font=("Courier", 10),
            anchor="w",
        )
        base_panel.pack(fill="x", padx=5, pady=2)

        # Base selector
        base_frame = ttk.Frame(self)
        base_frame.pack(fill="x", padx=5)
        self._base_var = tk.StringVar(value="DEC")
        for base in ["DEC", "HEX", "OCT", "BIN"]:
            ttk.Radiobutton(
                base_frame,
                text=base,
                variable=self._base_var,
                value=base,
                command=lambda b=base: on_button(
                    f"BASE_{b}"
                ),
            ).pack(side="left", padx=5)

        # Button grid
        self._button_frame = ttk.Frame(self)
        self._button_frame.pack(fill="both", expand=True)
        self._create_buttons()

    def _create_buttons(self) -> None:
        """Create the programmer mode button grid."""
        bf = self._button_frame
        cb = self._on_button

        # Row 0: A B C D E F AND OR AC
        hex_labels = ["A", "B", "C", "D", "E", "F"]
        for i, h in enumerate(hex_labels):
            btn = create_button(
                bf, h, 0, i,
                lambda a=h: cb(a)
            )
            self._hex_buttons[h] = btn
        create_button(bf, "AND", 0, 6, lambda: cb("AND"))
        create_button(bf, "OR", 0, 7, lambda: cb("OR"))
        create_button(bf, "AC", 0, 8, lambda: cb("AC"))

        # Row 1: NOT XOR LSH RSH % C +/- MOD /
        row1 = [
            ("NOT", "NOT"), ("XOR", "XOR"),
            ("LSH", "LSH"), ("RSH", "RSH"),
            ("%", "MOD"), ("C", "C"),
            ("\u00b1", "+/-"), ("MOD", "MOD"),
            ("\u00f7", "/"),
        ]
        for i, (text, action) in enumerate(row1):
            create_button(
                bf, text, 1, i,
                lambda a=action: cb(a)
            )

        # Rows 2-4: digits 7-1 in right columns
        digit_rows = [
            [("7", "7"), ("8", "8"), ("9", "9"),
             ("\u00d7", "*")],
            [("4", "4"), ("5", "5"), ("6", "6"),
             ("\u2212", "-")],
            [("1", "1"), ("2", "2"), ("3", "3"),
             ("+", "+")],
        ]
        for row_idx, row in enumerate(digit_rows):
            for i, (text, action) in enumerate(row):
                col = i + 5
                btn = create_button(
                    bf, text, row_idx + 2, col,
                    lambda a=action: cb(a)
                )
                if action.isdigit():
                    self._digit_buttons[action] = btn

        # Row 5: 0 (span 2), =, backspace
        btn0 = create_button(
            bf, "0", 5, 5,
            lambda: cb("0"), colspan=2
        )
        self._digit_buttons["0"] = btn0
        create_button(
            bf, "=", 5, 7, lambda: cb("=")
        )
        create_button(
            bf, "\u232b", 5, 8, lambda: cb("BACKSPACE")
        )

        for col in range(9):
            bf.columnconfigure(col, weight=1)

    def set_base_panel(self, bases: dict[str, str]) -> None:
        """Update the base conversion panel display.

        Args:
            bases: Dict with DEC, HEX, OCT, BIN string values.
        """
        text = (
            f"DEC: {bases.get('DEC', '0')}  "
            f"HEX: {bases.get('HEX', '0')}  "
            f"OCT: {bases.get('OCT', '0')}  "
            f"BIN: {bases.get('BIN', '0')}"
        )
        self._base_panel_var.set(text)

    def set_word_size_display(self, bits: int) -> None:
        """Update the word size indicator."""
        self._word_size_var.set(f"{bits}-bit")

    def set_base_mode(self, base: str) -> None:
        """Update base selector and enable/disable buttons."""
        self._base_var.set(base)
        self._update_button_states(base)

    def _update_button_states(self, base: str) -> None:
        """Enable/disable digit and hex buttons based on base."""
        from calculator.logic.programmer_logic import (
            VALID_DIGITS,
        )
        valid = VALID_DIGITS[base]
        for digit, btn in self._digit_buttons.items():
            btn.state(
                ["!disabled"]
                if digit in valid
                else ["disabled"]
            )
        for hex_char, btn in self._hex_buttons.items():
            btn.state(
                ["!disabled"]
                if hex_char in valid
                else ["disabled"]
            )

    def update_display(
        self, result: str, expression: str = ""
    ) -> None:
        """Update the display with current values."""
        self.display.set_display(result, expression)
