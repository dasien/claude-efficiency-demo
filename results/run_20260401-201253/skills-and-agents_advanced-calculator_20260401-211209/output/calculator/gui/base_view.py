"""Base view providing shared display area for all calculator modes."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable


class BaseView(ttk.Frame):
    """Shared display frame for all calculator modes.

    Provides the expression label, result display, memory indicator,
    and a callback dispatch mechanism for button presses.
    """

    def __init__(self, parent: tk.Widget) -> None:
        """Initialize the base view.

        Args:
            parent: The parent Tkinter widget.
        """
        super().__init__(parent)
        self._callbacks: dict[str, Callable[[], None]] = {}
        self._create_display()

    def _create_display(self) -> None:
        """Build the display area using grid layout.

        Row 0: expression label + memory indicator.
        Row 1: result display.
        """
        display_frame = ttk.Frame(self)
        display_frame.grid(row=0, column=0, columnspan=9, sticky="ew")
        display_frame.columnconfigure(1, weight=1)

        # Memory indicator (row 0, col 0) -- hidden by default
        self.memory_indicator = ttk.Label(
            display_frame,
            text="M",
            font=("TkDefaultFont", 10, "bold"),
            foreground="gray",
        )
        self.memory_indicator.grid(row=0, column=0, sticky="w", padx=(4, 0))
        self.memory_indicator.grid_remove()

        # Expression label (row 0, col 1) -- secondary display
        self.expression_label = ttk.Label(
            display_frame,
            text="",
            font=("TkDefaultFont", 12),
            anchor="e",
        )
        self.expression_label.grid(row=0, column=1, sticky="ew", padx=4, pady=(4, 0))

        # Result display (row 1, spanning full width)
        self.result_display = ttk.Label(
            display_frame,
            text="0",
            font=("TkDefaultFont", 24, "bold"),
            anchor="e",
        )
        self.result_display.grid(
            row=1, column=0, columnspan=2, sticky="ew", padx=4, pady=(0, 4)
        )

        # Configure the main frame so the display stretches
        self.columnconfigure(0, weight=1)

    def set_display(self, text: str) -> None:
        """Update the primary result display.

        Args:
            text: The text to show in the result display.
        """
        self.result_display.configure(text=text)

    def set_expression(self, text: str) -> None:
        """Update the secondary expression display.

        Args:
            text: The text to show in the expression label.
        """
        self.expression_label.configure(text=text)

    def show_memory_indicator(self, visible: bool) -> None:
        """Show or hide the memory indicator label.

        Args:
            visible: True to show the 'M' indicator, False to hide.
        """
        if visible:
            self.memory_indicator.grid()
        else:
            self.memory_indicator.grid_remove()

    def register_callback(self, button_id: str, callback: Callable[[], None]) -> None:
        """Register a callback for a button identifier.

        Args:
            button_id: The string identifier for the button.
            callback: The callable to invoke when the button is pressed.
        """
        self._callbacks[button_id] = callback

    def _fire_callback(self, button_id: str) -> None:
        """Look up and invoke the callback for the given button id.

        Args:
            button_id: The string identifier for the button.
        """
        callback = self._callbacks.get(button_id)
        if callback is not None:
            callback()

    def _make_button(
        self,
        parent: tk.Widget,
        text: str,
        button_id: str,
        row: int,
        col: int,
        colspan: int = 1,
        rowspan: int = 1,
        style: dict | None = None,
    ) -> tk.Button:
        """Create a tk.Button, place it with grid, and wire it to _fire_callback.

        Args:
            parent: The parent widget for the button.
            text: The button label text.
            button_id: Identifier used for callback dispatch.
            row: Grid row.
            col: Grid column.
            colspan: Number of columns to span.
            rowspan: Number of rows to span.
            style: Optional dict of tk.Button configure options
                   (e.g. bg, fg, font).

        Returns:
            The created tk.Button widget.
        """
        btn_kwargs: dict = {
            "text": text,
            "command": lambda bid=button_id: self._fire_callback(bid),
        }
        if style:
            btn_kwargs.update(style)

        btn = tk.Button(parent, **btn_kwargs)
        btn.grid(
            row=row,
            column=col,
            columnspan=colspan,
            rowspan=rowspan,
            sticky="nsew",
            padx=1,
            pady=1,
        )
        return btn
