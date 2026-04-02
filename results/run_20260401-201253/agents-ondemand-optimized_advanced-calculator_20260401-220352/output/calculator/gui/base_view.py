"""Base view with shared GUI components for all calculator modes.

Provides the display area (expression line and result), button creation
helpers, memory indicator, and keyboard binding framework.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from calculator.app import App


class BaseView(ttk.Frame):
    """Shared GUI components: display widget, memory row, layout helpers.

    All calculator mode views inherit from this class to get
    consistent display area and button styling.
    """

    # Color constants
    COLOR_BG = "#2D2D2D"
    COLOR_DISPLAY_BG = "#1E1E1E"
    COLOR_DIGIT = "#505050"
    COLOR_DIGIT_FG = "#FFFFFF"
    COLOR_OP = "#FF9500"
    COLOR_OP_FG = "#FFFFFF"
    COLOR_FUNC = "#3A3A3A"
    COLOR_FUNC_FG = "#FFFFFF"
    COLOR_EQUALS = "#FF9500"
    COLOR_MEMORY = "#2D2D2D"
    COLOR_MEMORY_FG = "#AAAAAA"
    COLOR_EXPR_FG = "#AAAAAA"
    COLOR_RESULT_FG = "#FFFFFF"

    def __init__(self, parent: tk.Widget, controller: App) -> None:
        super().__init__(parent)
        self.controller = controller
        self.expression_label: tk.Label | None = None
        self.result_label: tk.Label | None = None
        self.memory_indicator: tk.Label | None = None
        self._buttons: dict[str, tk.Button] = {}

    def _create_display(self, parent: tk.Widget) -> None:
        """Create the expression line and result display at the top.

        Args:
            parent: The parent widget to place the display in.
        """
        display_frame = tk.Frame(parent, bg=self.COLOR_DISPLAY_BG)
        display_frame.grid(
            row=0, column=0, columnspan=20, sticky="nsew", padx=1, pady=1
        )
        display_frame.columnconfigure(0, weight=1)

        # Memory indicator
        self.memory_indicator = tk.Label(
            display_frame,
            text="M",
            font=("Helvetica", 10),
            fg="#AAAAAA",
            bg=self.COLOR_DISPLAY_BG,
            anchor="w",
        )
        self.memory_indicator.grid(row=0, column=0, sticky="w", padx=5)
        self.memory_indicator.grid_remove()

        # Expression (secondary) display
        self.expression_label = tk.Label(
            display_frame,
            text="",
            font=("Helvetica", 14),
            fg=self.COLOR_EXPR_FG,
            bg=self.COLOR_DISPLAY_BG,
            anchor="e",
        )
        self.expression_label.grid(
            row=1, column=0, sticky="ew", padx=10, pady=(5, 0)
        )

        # Result (primary) display
        self.result_label = tk.Label(
            display_frame,
            text="0",
            font=("Helvetica", 32, "bold"),
            fg=self.COLOR_RESULT_FG,
            bg=self.COLOR_DISPLAY_BG,
            anchor="e",
        )
        self.result_label.grid(
            row=2, column=0, sticky="ew", padx=10, pady=(0, 10)
        )

    def update_display(self, value: str, expression: str = "") -> None:
        """Update both the result and expression displays.

        Args:
            value: Text for the primary (result) display.
            expression: Text for the secondary (expression) display.
        """
        if self.result_label:
            self.result_label.configure(text=value)
        if self.expression_label:
            self.expression_label.configure(text=expression)

    def show_error(self, message: str = "Error") -> None:
        """Display an error message on the result display.

        Args:
            message: The error message to show.
        """
        if self.result_label:
            self.result_label.configure(text=message)
        if self.expression_label:
            self.expression_label.configure(text="")

    def show_memory_indicator(self, visible: bool) -> None:
        """Show or hide the memory indicator.

        Args:
            visible: Whether to show the indicator.
        """
        if self.memory_indicator:
            if visible:
                self.memory_indicator.grid()
            else:
                self.memory_indicator.grid_remove()

    def _create_button(
        self,
        parent: tk.Widget,
        text: str,
        row: int,
        col: int,
        command: object,
        colspan: int = 1,
        rowspan: int = 1,
        style: str = "default",
    ) -> tk.Button:
        """Create a grid-placed button with consistent styling.

        Args:
            parent: Parent widget.
            text: Button label text.
            row: Grid row.
            col: Grid column.
            command: Callback function.
            colspan: Number of columns to span.
            rowspan: Number of rows to span.
            style: Style name ('digit', 'operator', 'function',
                   'equals', 'memory', 'default').

        Returns:
            The created Button widget.
        """
        styles = {
            "digit": {
                "bg": self.COLOR_DIGIT,
                "fg": self.COLOR_DIGIT_FG,
                "font": ("Helvetica", 16),
            },
            "operator": {
                "bg": self.COLOR_OP,
                "fg": self.COLOR_OP_FG,
                "font": ("Helvetica", 16, "bold"),
            },
            "function": {
                "bg": self.COLOR_FUNC,
                "fg": self.COLOR_FUNC_FG,
                "font": ("Helvetica", 13),
            },
            "equals": {
                "bg": self.COLOR_EQUALS,
                "fg": self.COLOR_OP_FG,
                "font": ("Helvetica", 16, "bold"),
            },
            "memory": {
                "bg": self.COLOR_MEMORY,
                "fg": self.COLOR_MEMORY_FG,
                "font": ("Helvetica", 11),
            },
            "default": {
                "bg": self.COLOR_FUNC,
                "fg": self.COLOR_FUNC_FG,
                "font": ("Helvetica", 13),
            },
        }

        s = styles.get(style, styles["default"])
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=s["bg"],
            fg=s["fg"],
            font=s["font"],
            relief="flat",
            borderwidth=0,
            highlightthickness=0,
            activebackground=s["bg"],
            activeforeground=s["fg"],
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

        self._buttons[text] = btn
        return btn

    def _create_memory_row(
        self, parent: tk.Widget, row: int, col_offset: int = 0
    ) -> None:
        """Create the MC, MR, M+, M-, MS button row.

        Args:
            parent: Parent widget.
            row: Grid row for the memory buttons.
            col_offset: Starting column offset.
        """
        memory_ops = ["MC", "MR", "M+", "M-", "MS"]
        for i, op in enumerate(memory_ops):
            self._create_button(
                parent,
                op,
                row,
                col_offset + i,
                lambda o=op: self.controller.on_memory(o),
                style="memory",
            )

    def get_button(self, text: str) -> tk.Button | None:
        """Get a button reference by its text label.

        Args:
            text: The button's label text.

        Returns:
            The Button widget, or None if not found.
        """
        return self._buttons.get(text)
