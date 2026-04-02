"""Shared GUI components: display frame, button factory, memory row."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

BUTTON_WIDTH = 5
BUTTON_HEIGHT = 2
BUTTON_PADX = 2
BUTTON_PADY = 2


class DisplayFrame(ttk.Frame):
    """Expression line and result display."""

    def __init__(self, parent: tk.Widget, **kwargs: object) -> None:
        super().__init__(parent, **kwargs)
        self._expression_var = tk.StringVar(value="")
        self._result_var = tk.StringVar(value="0")

        self._expression_label = ttk.Label(
            self,
            textvariable=self._expression_var,
            anchor="e",
            font=("Courier", 12),
        )
        self._expression_label.pack(
            fill="x", padx=5, pady=(5, 0)
        )

        self._result_label = ttk.Label(
            self,
            textvariable=self._result_var,
            anchor="e",
            font=("Courier", 24, "bold"),
        )
        self._result_label.pack(fill="x", padx=5, pady=(0, 5))

    def set_display(
        self, result: str, expression: str = ""
    ) -> None:
        """Update both display lines."""
        self._result_var.set(result)
        self._expression_var.set(expression)

    def get_result_text(self) -> str:
        """Return the current result display text."""
        return self._result_var.get()


class MemoryButtonRow(ttk.Frame):
    """Row of memory buttons: MC, MR, M+, M-, MS."""

    def __init__(
        self,
        parent: tk.Widget,
        callback: Callable[[str], None],
        **kwargs: object,
    ) -> None:
        super().__init__(parent, **kwargs)
        self._indicator_var = tk.StringVar(value="")
        self._callback = callback

        for i, label in enumerate(
            ["MC", "MR", "M+", "M-", "MS"]
        ):
            btn = ttk.Button(
                self,
                text=label,
                width=BUTTON_WIDTH,
                command=lambda l=label: self._callback(l),
            )
            btn.grid(
                row=0, column=i,
                padx=BUTTON_PADX, pady=BUTTON_PADY
            )

        self._indicator_label = ttk.Label(
            self,
            textvariable=self._indicator_var,
            font=("Courier", 10),
        )
        self._indicator_label.grid(
            row=0, column=5, padx=5
        )

    def set_memory_indicator(self, has_value: bool) -> None:
        """Show or hide the memory indicator."""
        self._indicator_var.set("M" if has_value else "")


def create_button(
    parent: tk.Widget,
    text: str,
    row: int,
    col: int,
    callback: Callable[[], None],
    colspan: int = 1,
    rowspan: int = 1,
    width: int = BUTTON_WIDTH,
    style: str = "",
) -> ttk.Button:
    """Create a grid-placed button with consistent styling.

    Args:
        parent: Parent widget.
        text: Button label text.
        row: Grid row.
        col: Grid column.
        callback: Function to call on click.
        colspan: Column span.
        rowspan: Row span.
        width: Button width in characters.
        style: Optional ttk style name.

    Returns:
        The created button widget.
    """
    btn = ttk.Button(
        parent,
        text=text,
        width=width * colspan,
        command=callback,
    )
    btn.grid(
        row=row,
        column=col,
        columnspan=colspan,
        rowspan=rowspan,
        padx=BUTTON_PADX,
        pady=BUTTON_PADY,
        sticky="nsew",
    )
    return btn
