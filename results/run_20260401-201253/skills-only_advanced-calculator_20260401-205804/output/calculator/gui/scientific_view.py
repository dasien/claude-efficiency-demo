"""Scientific mode view — extended button layout with math functions."""

import tkinter as tk
from typing import Callable
from calculator.gui.base_view import (
    BaseView, BTN_DIGIT, BTN_OP, BTN_FUNC, BTN_MEMORY,
    TEXT_COLOR, TEXT_OP_COLOR, BG_COLOR, DISPLAY_BG, EXPR_COLOR
)


class ScientificView(BaseView):
    """Scientific calculator mode GUI layout."""

    def __init__(self, parent: tk.Widget, on_button: Callable[[str], None],
                 angle_mode: str = "DEG") -> None:
        super().__init__(parent, on_button)
        self.angle_mode = angle_mode
        self._build_angle_indicator()
        self._build_buttons()

    def _build_angle_indicator(self) -> None:
        """Build the Deg/Rad toggle indicator."""
        frame = tk.Frame(self.frame, bg=BG_COLOR)
        frame.pack(fill=tk.X, padx=5)
        self.angle_btn = tk.Button(
            frame, text=self.angle_mode, font=("Helvetica", 11),
            fg=TEXT_COLOR, bg=BTN_MEMORY, relief=tk.FLAT,
            activebackground="#444444",
            command=lambda: self.on_button("DEG/RAD")
        )
        self.angle_btn.pack(side=tk.RIGHT, padx=2, pady=1)

        self.paren_label = tk.Label(
            frame, text="", font=("Helvetica", 11),
            fg=EXPR_COLOR, bg=BG_COLOR
        )
        self.paren_label.pack(side=tk.LEFT, padx=2)

    def update_angle_mode(self, mode: str) -> None:
        """Update the angle mode indicator."""
        self.angle_mode = mode
        self.angle_btn.config(text=mode)

    def update_paren_depth(self, depth: int) -> None:
        """Update parenthesis depth indicator."""
        if depth > 0:
            self.paren_label.config(text=f"({'(' * depth})")
        else:
            self.paren_label.config(text="")

    def _build_buttons(self) -> None:
        """Build the scientific calculator button grid."""
        grid = tk.Frame(self.frame, bg=BG_COLOR)
        grid.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # 9 columns: 5 scientific + 4 basic (3 digits + 1 operator)
        for c in range(9):
            grid.columnconfigure(c, weight=1, uniform="btn")
        for r in range(5):
            grid.rowconfigure(r, weight=1, uniform="btn")

        fs = 13  # smaller font for scientific buttons

        # Row 0: (, ), x², x³, xⁿ, C, +/-, %, /
        self.create_button(grid, "(", 0, 0, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, ")", 0, 1, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "x\u00b2", 0, 2, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "x\u00b3", 0, 3, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "x\u207f", 0, 4, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "C", 0, 5, bg=BTN_FUNC)
        self.create_button(grid, "+/-", 0, 6, bg=BTN_FUNC)
        self.create_button(grid, "%", 0, 7, bg=BTN_FUNC)
        self.create_button(grid, "/", 0, 8, bg=BTN_OP, fg=TEXT_OP_COLOR)

        # Row 1: sin, cos, tan, √x, ³√x, 7, 8, 9, *
        self.create_button(grid, "sin", 1, 0, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "cos", 1, 1, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "tan", 1, 2, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "\u221ax", 1, 3, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "\u00b3\u221ax", 1, 4, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "7", 1, 5)
        self.create_button(grid, "8", 1, 6)
        self.create_button(grid, "9", 1, 7)
        self.create_button(grid, "*", 1, 8, bg=BTN_OP, fg=TEXT_OP_COLOR)

        # Row 2: asin, acos, atan, 10ˣ, eˣ, 4, 5, 6, -
        self.create_button(grid, "asin", 2, 0, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "acos", 2, 1, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "atan", 2, 2, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "10\u02e3", 2, 3, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "e\u02e3", 2, 4, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "4", 2, 5)
        self.create_button(grid, "5", 2, 6)
        self.create_button(grid, "6", 2, 7)
        self.create_button(grid, "-", 2, 8, bg=BTN_OP, fg=TEXT_OP_COLOR)

        # Row 3: n!, |x|, log, ln, log₂, 1, 2, 3, +
        self.create_button(grid, "n!", 3, 0, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "|x|", 3, 1, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "log", 3, 2, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "ln", 3, 3, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "log\u2082", 3, 4, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "1", 3, 5)
        self.create_button(grid, "2", 3, 6)
        self.create_button(grid, "3", 3, 7)
        self.create_button(grid, "+", 3, 8, bg=BTN_OP, fg=TEXT_OP_COLOR)

        # Row 4: π, e, 1/x, [blank], [blank], 0(span2), ., =
        self.create_button(grid, "\u03c0", 4, 0, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "e", 4, 1, bg=BTN_FUNC, font_size=fs)
        self.create_button(grid, "1/x", 4, 2, bg=BTN_FUNC, font_size=fs)

        # Blank spacers
        tk.Frame(grid, bg=BG_COLOR).grid(row=4, column=3, sticky="nsew")
        tk.Frame(grid, bg=BG_COLOR).grid(row=4, column=4, sticky="nsew")

        self.create_button(grid, "0", 4, 5, colspan=2)
        self.create_button(grid, ".", 4, 7)
        self.create_button(grid, "=", 4, 8, bg=BTN_OP, fg=TEXT_OP_COLOR)
