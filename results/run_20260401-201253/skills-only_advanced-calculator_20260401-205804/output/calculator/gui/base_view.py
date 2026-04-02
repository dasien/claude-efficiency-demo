"""Base view — shared GUI components for all calculator modes."""

import tkinter as tk
from typing import Callable, Optional


# Color scheme
BG_COLOR = "#1C1C1E"
DISPLAY_BG = "#1C1C1E"
BTN_DIGIT = "#505050"
BTN_OP = "#FF9F0A"
BTN_FUNC = "#333333"
BTN_MEMORY = "#2C2C2E"
TEXT_COLOR = "#FFFFFF"
TEXT_OP_COLOR = "#FFFFFF"
DISPLAY_COLOR = "#FFFFFF"
EXPR_COLOR = "#8E8E93"
MEMORY_IND_COLOR = "#FF9F0A"


class BaseView:
    """Base view with display and memory row shared by all modes."""

    def __init__(self, parent: tk.Widget, on_button: Callable[[str], None]) -> None:
        self.parent = parent
        self.on_button = on_button
        self.frame = tk.Frame(parent, bg=BG_COLOR)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self._build_display()
        self._build_memory_row()

    def _build_display(self) -> None:
        """Build the expression and result display area."""
        display_frame = tk.Frame(self.frame, bg=DISPLAY_BG, padx=10, pady=5)
        display_frame.pack(fill=tk.X)

        self.expr_label = tk.Label(
            display_frame, text="", font=("Helvetica", 14),
            fg=EXPR_COLOR, bg=DISPLAY_BG, anchor="e"
        )
        self.expr_label.pack(fill=tk.X)

        result_frame = tk.Frame(display_frame, bg=DISPLAY_BG)
        result_frame.pack(fill=tk.X)

        self.memory_indicator = tk.Label(
            result_frame, text="", font=("Helvetica", 10),
            fg=MEMORY_IND_COLOR, bg=DISPLAY_BG, width=2, anchor="w"
        )
        self.memory_indicator.pack(side=tk.LEFT)

        self.result_label = tk.Label(
            result_frame, text="0", font=("Helvetica", 36, "bold"),
            fg=DISPLAY_COLOR, bg=DISPLAY_BG, anchor="e"
        )
        self.result_label.pack(fill=tk.X, expand=True)

    def _build_memory_row(self) -> None:
        """Build the memory function button row."""
        row_frame = tk.Frame(self.frame, bg=BG_COLOR)
        row_frame.pack(fill=tk.X, padx=2)

        for label in ["MC", "MR", "M+", "M-", "MS"]:
            btn = tk.Button(
                row_frame, text=label, font=("Helvetica", 12),
                fg=TEXT_COLOR, bg=BTN_MEMORY, relief=tk.FLAT,
                activebackground="#444444", activeforeground=TEXT_COLOR,
                command=lambda l=label: self.on_button(l)
            )
            btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1, pady=1)

    def update_display(self, value: str, expression: str = "",
                       has_memory: bool = False) -> None:
        """Update the display labels."""
        self.result_label.config(text=value)
        self.expr_label.config(text=expression)
        self.memory_indicator.config(text="M" if has_memory else "")

    def create_button(self, parent: tk.Widget, text: str,
                      row: int, col: int,
                      colspan: int = 1, rowspan: int = 1,
                      bg: str = BTN_DIGIT,
                      fg: str = TEXT_COLOR,
                      font_size: int = 16) -> tk.Button:
        """Create a styled button in a grid layout."""
        btn = tk.Button(
            parent, text=text, font=("Helvetica", font_size),
            fg=fg, bg=bg, relief=tk.FLAT,
            activebackground="#666666", activeforeground=fg,
            command=lambda: self.on_button(text)
        )
        btn.grid(
            row=row, column=col,
            columnspan=colspan, rowspan=rowspan,
            sticky="nsew", padx=1, pady=1
        )
        return btn

    def destroy(self) -> None:
        """Remove this view."""
        self.frame.destroy()
