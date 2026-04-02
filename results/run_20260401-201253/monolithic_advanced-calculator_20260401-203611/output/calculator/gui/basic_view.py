"""Basic mode GUI layout."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from calculator.gui.base_view import (
    DisplayFrame,
    MemoryButtonRow,
    create_button,
)


class BasicView(ttk.Frame):
    """Basic calculator mode view with digit and operator buttons."""

    def __init__(
        self,
        parent: tk.Widget,
        on_button: Callable[[str], None],
        **kwargs: object,
    ) -> None:
        super().__init__(parent, **kwargs)
        self._on_button = on_button

        self.display = DisplayFrame(self)
        self.display.pack(fill="x")

        self.memory_row = MemoryButtonRow(
            self, callback=on_button
        )
        self.memory_row.pack(fill="x", padx=5)

        self._button_frame = ttk.Frame(self)
        self._button_frame.pack(fill="both", expand=True)

        self._create_buttons()

    def _create_buttons(self) -> None:
        """Create the basic mode button grid."""
        bf = self._button_frame
        cb = self._on_button

        # Row 0: C, +/-, %, /
        for i, (text, action) in enumerate([
            ("C", "C"), ("\u00b1", "+/-"),
            ("%", "%"), ("\u00f7", "/"),
        ]):
            create_button(
                bf, text, 0, i,
                lambda a=action: cb(a)
            )

        # Row 1: 7, 8, 9, *
        for i, (text, action) in enumerate([
            ("7", "7"), ("8", "8"), ("9", "9"),
            ("\u00d7", "*"),
        ]):
            create_button(
                bf, text, 1, i,
                lambda a=action: cb(a)
            )

        # Row 2: 4, 5, 6, -
        for i, (text, action) in enumerate([
            ("4", "4"), ("5", "5"), ("6", "6"),
            ("\u2212", "-"),
        ]):
            create_button(
                bf, text, 2, i,
                lambda a=action: cb(a)
            )

        # Row 3: 1, 2, 3, +
        for i, (text, action) in enumerate([
            ("1", "1"), ("2", "2"), ("3", "3"),
            ("+", "+"),
        ]):
            create_button(
                bf, text, 3, i,
                lambda a=action: cb(a)
            )

        # Row 4: 0 (span 2), ., =
        create_button(
            bf, "0", 4, 0,
            lambda: cb("0"), colspan=2
        )
        create_button(
            bf, ".", 4, 2,
            lambda: cb(".")
        )
        create_button(
            bf, "=", 4, 3,
            lambda: cb("=")
        )

        # Backspace at top area (hidden keyboard-only)
        # AC button
        for col in range(4):
            bf.columnconfigure(col, weight=1)

    def update_display(
        self, result: str, expression: str = ""
    ) -> None:
        """Update the display with current values."""
        self.display.set_display(result, expression)
