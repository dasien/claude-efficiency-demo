"""Shared GUI components for all calculator modes."""

import tkinter as tk
from tkinter import font as tkfont
from typing import Callable, Optional


# Color scheme
COLORS = {
    "bg": "#1C1C1E",
    "display_bg": "#1C1C1E",
    "display_fg": "#FFFFFF",
    "expr_fg": "#8E8E93",
    "btn_digit": "#333333",
    "btn_digit_fg": "#FFFFFF",
    "btn_op": "#FF9F0A",
    "btn_op_fg": "#FFFFFF",
    "btn_func": "#505050",
    "btn_func_fg": "#FFFFFF",
    "btn_memory": "#3A3A3C",
    "btn_memory_fg": "#FFFFFF",
    "btn_sci": "#2C2C2E",
    "btn_sci_fg": "#FFFFFF",
    "btn_disabled": "#1C1C1E",
    "btn_disabled_fg": "#555555",
    "indicator": "#FF9F0A",
    "base_panel_bg": "#2C2C2E",
    "base_panel_fg": "#8E8E93",
}


class BaseView:
    """Base view with shared display components."""

    def __init__(self, parent: tk.Widget, callback: Callable[[str], None]) -> None:
        """Initialize the base view.

        Args:
            parent: Parent tkinter widget.
            callback: Function called with action string on any button press.
        """
        self.parent = parent
        self.callback = callback
        self.frame = tk.Frame(parent, bg=COLORS["bg"])

        # Display area
        self._build_display()

    def _build_display(self) -> None:
        """Build the expression and result display labels."""
        display_frame = tk.Frame(self.frame, bg=COLORS["display_bg"])
        display_frame.pack(fill=tk.X, padx=10, pady=(10, 0))

        # Expression line (secondary)
        self.expr_label = tk.Label(
            display_frame,
            text="",
            font=("Helvetica", 16),
            fg=COLORS["expr_fg"],
            bg=COLORS["display_bg"],
            anchor="e",
        )
        self.expr_label.pack(fill=tk.X)

        # Result line (primary)
        self.result_label = tk.Label(
            display_frame,
            text="0",
            font=("Helvetica", 36, "bold"),
            fg=COLORS["display_fg"],
            bg=COLORS["display_bg"],
            anchor="e",
        )
        self.result_label.pack(fill=tk.X)

        # Indicator row (memory indicator, angle mode, etc.)
        self.indicator_frame = tk.Frame(display_frame, bg=COLORS["display_bg"])
        self.indicator_frame.pack(fill=tk.X)

        self.memory_indicator = tk.Label(
            self.indicator_frame,
            text="",
            font=("Helvetica", 12),
            fg=COLORS["indicator"],
            bg=COLORS["display_bg"],
            anchor="w",
        )
        self.memory_indicator.pack(side=tk.LEFT)

    def update_display(self, value: str, expression: str = "") -> None:
        """Update the display labels."""
        self.result_label.config(text=value)
        self.expr_label.config(text=expression)

        # Auto-size font for long numbers
        length = len(value)
        if length > 20:
            size = 18
        elif length > 14:
            size = 24
        elif length > 10:
            size = 28
        else:
            size = 36
        self.result_label.config(font=("Helvetica", size, "bold"))

    def update_memory_indicator(self, has_memory: bool) -> None:
        """Show or hide the memory indicator."""
        self.memory_indicator.config(text="M" if has_memory else "")

    def show(self) -> None:
        """Show this view."""
        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self) -> None:
        """Hide this view."""
        self.frame.pack_forget()

    def _make_button(
        self,
        parent: tk.Widget,
        text: str,
        action: str,
        row: int,
        col: int,
        bg: str = "",
        fg: str = "",
        colspan: int = 1,
        rowspan: int = 1,
    ) -> tk.Button:
        """Create and grid a styled button."""
        if not bg:
            bg = COLORS["btn_digit"]
        if not fg:
            fg = COLORS["btn_digit_fg"]

        btn = tk.Button(
            parent,
            text=text,
            font=("Helvetica", 16),
            bg=bg,
            fg=fg,
            activebackground=bg,
            activeforeground=fg,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.callback(action),
        )
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
