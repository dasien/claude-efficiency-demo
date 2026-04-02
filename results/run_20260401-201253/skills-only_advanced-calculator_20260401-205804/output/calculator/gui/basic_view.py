"""Basic mode view — standard calculator button layout."""

import tkinter as tk
from typing import Callable
from calculator.gui.base_view import (
    BaseView, BTN_DIGIT, BTN_OP, BTN_FUNC, TEXT_COLOR, TEXT_OP_COLOR, BG_COLOR
)


class BasicView(BaseView):
    """Basic calculator mode GUI layout."""

    def __init__(self, parent: tk.Widget, on_button: Callable[[str], None]) -> None:
        super().__init__(parent, on_button)
        self._build_buttons()

    def _build_buttons(self) -> None:
        """Build the basic calculator button grid."""
        grid = tk.Frame(self.frame, bg=BG_COLOR)
        grid.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Configure grid weights
        for c in range(4):
            grid.columnconfigure(c, weight=1, uniform="btn")
        for r in range(5):
            grid.rowconfigure(r, weight=1, uniform="btn")

        # Row 0: C, +/-, %, /
        self.create_button(grid, "C", 0, 0, bg=BTN_FUNC)
        self.create_button(grid, "+/-", 0, 1, bg=BTN_FUNC)
        self.create_button(grid, "%", 0, 2, bg=BTN_FUNC)
        self.create_button(grid, "/", 0, 3, bg=BTN_OP, fg=TEXT_OP_COLOR)

        # Row 1: 7, 8, 9, *
        self.create_button(grid, "7", 1, 0)
        self.create_button(grid, "8", 1, 1)
        self.create_button(grid, "9", 1, 2)
        self.create_button(grid, "*", 1, 3, bg=BTN_OP, fg=TEXT_OP_COLOR)

        # Row 2: 4, 5, 6, -
        self.create_button(grid, "4", 2, 0)
        self.create_button(grid, "5", 2, 1)
        self.create_button(grid, "6", 2, 2)
        self.create_button(grid, "-", 2, 3, bg=BTN_OP, fg=TEXT_OP_COLOR)

        # Row 3: 1, 2, 3, +
        self.create_button(grid, "1", 3, 0)
        self.create_button(grid, "2", 3, 1)
        self.create_button(grid, "3", 3, 2)
        self.create_button(grid, "+", 3, 3, bg=BTN_OP, fg=TEXT_OP_COLOR)

        # Row 4: 0 (span 2), ., =
        self.create_button(grid, "0", 4, 0, colspan=2)
        self.create_button(grid, ".", 4, 2)
        self.create_button(grid, "=", 4, 3, bg=BTN_OP, fg=TEXT_OP_COLOR)
