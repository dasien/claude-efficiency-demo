"""Scientific mode GUI layout."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from calculator.gui.base_view import (
    DisplayFrame,
    MemoryButtonRow,
    create_button,
)


class ScientificView(ttk.Frame):
    """Scientific calculator mode view with extended functions."""

    def __init__(
        self,
        parent: tk.Widget,
        on_button: Callable[[str], None],
        **kwargs: object,
    ) -> None:
        super().__init__(parent, **kwargs)
        self._on_button = on_button

        # Display
        self.display = DisplayFrame(self)
        self.display.pack(fill="x")

        # Angle mode indicator
        self._angle_var = tk.StringVar(value="DEG")
        angle_frame = ttk.Frame(self)
        angle_frame.pack(fill="x", padx=5)
        self._angle_label = ttk.Label(
            angle_frame,
            textvariable=self._angle_var,
            font=("Courier", 10, "bold"),
        )
        self._angle_label.pack(side="right")
        self._angle_btn = ttk.Button(
            angle_frame,
            text="Deg/Rad",
            command=lambda: on_button("DEG/RAD"),
            width=8,
        )
        self._angle_btn.pack(side="right", padx=5)

        # Paren depth indicator
        self._paren_var = tk.StringVar(value="")
        ttk.Label(
            angle_frame,
            textvariable=self._paren_var,
            font=("Courier", 10),
        ).pack(side="left")

        # Memory row
        self.memory_row = MemoryButtonRow(
            self, callback=on_button
        )
        self.memory_row.pack(fill="x", padx=5)

        # Button grid
        self._button_frame = ttk.Frame(self)
        self._button_frame.pack(fill="both", expand=True)
        self._create_buttons()

    def _create_buttons(self) -> None:
        """Create the scientific mode button grid (5 sci + 4 basic cols)."""
        bf = self._button_frame
        cb = self._on_button

        # Define rows: each row is list of (display_text, action)
        rows = [
            # Row 0
            [("(", "("), (")", ")"), ("x\u00b2", "x²"),
             ("x\u00b3", "x³"), ("x\u207f", "xⁿ"),
             ("C", "C"), ("\u00b1", "+/-"),
             ("%", "%"), ("\u00f7", "/")],
            # Row 1
            [("sin", "sin"), ("cos", "cos"), ("tan", "tan"),
             ("\u221ax", "√x"), ("\u00b3\u221ax", "³√x"),
             ("7", "7"), ("8", "8"), ("9", "9"),
             ("\u00d7", "*")],
            # Row 2
            [("asin", "asin"), ("acos", "acos"),
             ("atan", "atan"),
             ("10\u02e3", "10ˣ"), ("e\u02e3", "eˣ"),
             ("4", "4"), ("5", "5"), ("6", "6"),
             ("\u2212", "-")],
            # Row 3
            [("n!", "n!"), ("|x|", "|x|"),
             ("log", "log"), ("ln", "ln"),
             ("log\u2082", "log₂"),
             ("1", "1"), ("2", "2"), ("3", "3"),
             ("+", "+")],
            # Row 4
            [("\u03c0", "π"), ("e", "e"), ("1/x", "1/x"),
             ("", ""), ("", ""),
             None, (".", "."), ("=", "=")],
        ]

        for row_idx, row in enumerate(rows):
            col = 0
            for item in row:
                if item is None:
                    # Span-2 zero button
                    create_button(
                        bf, "0", row_idx, col,
                        lambda: cb("0"), colspan=2
                    )
                    col += 2
                    continue
                text, action = item
                if text == "":
                    col += 1
                    continue
                create_button(
                    bf, text, row_idx, col,
                    lambda a=action: cb(a)
                )
                col += 1

        for col in range(9):
            bf.columnconfigure(col, weight=1)

    def set_angle_mode(self, mode: str) -> None:
        """Update the angle mode indicator."""
        self._angle_var.set(mode)

    def set_paren_depth(self, depth: int) -> None:
        """Update the parenthesis depth indicator."""
        if depth > 0:
            self._paren_var.set(f"({depth})")
        else:
            self._paren_var.set("")

    def update_display(
        self, result: str, expression: str = ""
    ) -> None:
        """Update the display with current values."""
        self.display.set_display(result, expression)
