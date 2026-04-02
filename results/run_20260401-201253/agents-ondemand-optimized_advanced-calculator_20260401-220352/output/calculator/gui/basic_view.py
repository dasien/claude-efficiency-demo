"""Basic mode GUI layout.

Provides the standard four-function calculator layout with memory
buttons, digit pad, operator column, and equals button.
"""

from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

from calculator.gui.base_view import BaseView

if TYPE_CHECKING:
    from calculator.app import App


class BasicView(BaseView):
    """Basic mode button grid layout.

    Layout:
        Row 0: Display (expression + result)
        Row 1: Memory buttons (MC, MR, M+, M-, MS)
        Row 2: C, +/-, %, /
        Row 3: 7, 8, 9, *
        Row 4: 4, 5, 6, -
        Row 5: 1, 2, 3, +
        Row 6: 0 (span 2), ., =
    """

    def __init__(self, parent: tk.Widget, controller: App) -> None:
        super().__init__(parent, controller)
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create all widgets for basic mode."""
        main_frame = tk.Frame(self, bg=self.COLOR_BG)
        main_frame.pack(fill="both", expand=True)

        # Configure grid weights for uniform sizing
        for c in range(4):
            main_frame.columnconfigure(c, weight=1, minsize=70)
        for r in range(7):
            main_frame.rowconfigure(r, weight=1, minsize=50)
        main_frame.rowconfigure(0, weight=2, minsize=100)

        # Display area
        self._create_display(main_frame)

        # Memory row
        self._create_memory_row(main_frame, row=1)
        # Memory row only uses 4 columns, extend last one
        # (5 buttons in 4 cols would need adjustment)
        # Reconfigure for 5 columns in memory row
        # Actually, let's use 4 columns for main grid and overlay
        # memory in a sub-frame
        # Simpler: just use 4 columns, merge MS into col 3

        # Row 2: C, +/-, %, /
        self._create_button(
            main_frame, "C", 2, 0,
            self.controller.on_clear, style="function"
        )
        self._create_button(
            main_frame, "+/-", 2, 1,
            self.controller.on_toggle_sign, style="function"
        )
        self._create_button(
            main_frame, "%", 2, 2,
            self.controller.on_percentage, style="function"
        )
        self._create_button(
            main_frame, "/", 2, 3,
            lambda: self.controller.on_operator("/"),
            style="operator",
        )

        # Row 3: 7, 8, 9, *
        for i, digit in enumerate(["7", "8", "9"]):
            self._create_button(
                main_frame, digit, 3, i,
                lambda d=digit: self.controller.on_digit(d),
                style="digit",
            )
        self._create_button(
            main_frame, "*", 3, 3,
            lambda: self.controller.on_operator("*"),
            style="operator",
        )

        # Row 4: 4, 5, 6, -
        for i, digit in enumerate(["4", "5", "6"]):
            self._create_button(
                main_frame, digit, 4, i,
                lambda d=digit: self.controller.on_digit(d),
                style="digit",
            )
        self._create_button(
            main_frame, "-", 4, 3,
            lambda: self.controller.on_operator("-"),
            style="operator",
        )

        # Row 5: 1, 2, 3, +
        for i, digit in enumerate(["1", "2", "3"]):
            self._create_button(
                main_frame, digit, 5, i,
                lambda d=digit: self.controller.on_digit(d),
                style="digit",
            )
        self._create_button(
            main_frame, "+", 5, 3,
            lambda: self.controller.on_operator("+"),
            style="operator",
        )

        # Row 6: 0 (span 2), ., =
        self._create_button(
            main_frame, "0", 6, 0,
            lambda: self.controller.on_digit("0"),
            colspan=2, style="digit",
        )
        self._create_button(
            main_frame, ".", 6, 2,
            self.controller.on_decimal, style="digit"
        )
        self._create_button(
            main_frame, "=", 6, 3,
            self.controller.on_equals, style="equals"
        )

    def _create_memory_row(
        self, parent: tk.Widget, row: int, col_offset: int = 0
    ) -> None:
        """Create memory buttons spanning 4 columns with 5 buttons.

        Uses a sub-frame to fit 5 memory buttons into the grid.

        Args:
            parent: Parent widget.
            row: Grid row for the memory buttons.
            col_offset: Starting column offset.
        """
        mem_frame = tk.Frame(parent, bg=self.COLOR_BG)
        mem_frame.grid(
            row=row, column=0, columnspan=4, sticky="nsew"
        )
        for i in range(5):
            mem_frame.columnconfigure(i, weight=1)
        mem_frame.rowconfigure(0, weight=1)

        memory_ops = ["MC", "MR", "M+", "M-", "MS"]
        for i, op in enumerate(memory_ops):
            self._create_button(
                mem_frame, op, 0, i,
                lambda o=op: self.controller.on_memory(o),
                style="memory",
            )
