"""Basic mode GUI layout."""

import tkinter as tk
from typing import Callable
from .base_view import BaseView, COLORS


class BasicView(BaseView):
    """Basic calculator mode view."""

    def __init__(self, parent: tk.Widget, callback: Callable[[str], None]) -> None:
        """Initialize basic view with button grid."""
        super().__init__(parent, callback)
        self._build_buttons()

    def _build_buttons(self) -> None:
        """Build the button grid for basic mode."""
        btn_frame = tk.Frame(self.frame, bg=COLORS["bg"])
        btn_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configure grid weights
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1, uniform="btn")
        for i in range(7):
            btn_frame.rowconfigure(i, weight=1, uniform="btn")

        # Memory row
        mem_buttons = [
            ("MC", "memory_clear"),
            ("MR", "memory_recall"),
            ("M+", "memory_add"),
            ("M\u2212", "memory_subtract"),
            ("MS", "memory_store"),
        ]
        # Memory buttons span the top, but we have 4 columns so make MC-M- in cols 0-3, MS uses AC position
        mem_bg = COLORS["btn_memory"]
        mem_fg = COLORS["btn_memory_fg"]
        # Put 5 memory buttons across - we'll use 5 columns effectively
        # Actually let's keep 4 columns and put memory in a separate frame
        mem_frame = tk.Frame(btn_frame, bg=COLORS["bg"])
        mem_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
        for i in range(5):
            mem_frame.columnconfigure(i, weight=1, uniform="mem")
        mem_frame.rowconfigure(0, weight=1)
        for i, (text, action) in enumerate(mem_buttons):
            btn = tk.Button(
                mem_frame,
                text=text,
                font=("Helvetica", 13),
                bg=mem_bg,
                fg=mem_fg,
                activebackground=mem_bg,
                activeforeground=mem_fg,
                borderwidth=0,
                command=lambda a=action: self.callback(a),
            )
            btn.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        # Function row: C, +/-, %, /
        func_bg = COLORS["btn_func"]
        func_fg = COLORS["btn_func_fg"]
        op_bg = COLORS["btn_op"]
        op_fg = COLORS["btn_op_fg"]

        self._make_button(btn_frame, "C", "clear_entry", 1, 0, func_bg, func_fg)
        self._make_button(btn_frame, "+/\u2212", "toggle_sign", 1, 1, func_bg, func_fg)
        self._make_button(btn_frame, "%", "percent", 1, 2, func_bg, func_fg)
        self._make_button(btn_frame, "\u00F7", "op_/", 1, 3, op_bg, op_fg)

        # Digit rows
        digits = [
            [("7", "digit_7"), ("8", "digit_8"), ("9", "digit_9"), ("\u00D7", "op_*")],
            [("4", "digit_4"), ("5", "digit_5"), ("6", "digit_6"), ("\u2212", "op_-")],
            [("1", "digit_1"), ("2", "digit_2"), ("3", "digit_3"), ("+", "op_+")],
        ]
        for r, row_data in enumerate(digits):
            for c, (text, action) in enumerate(row_data):
                if c == 3:
                    self._make_button(btn_frame, text, action, r + 2, c, op_bg, op_fg)
                else:
                    self._make_button(btn_frame, text, action, r + 2, c)

        # Bottom row: 0 (double width), ., =
        self._make_button(btn_frame, "0", "digit_0", 5, 0, colspan=2)
        self._make_button(btn_frame, ".", "decimal", 5, 2)
        self._make_button(btn_frame, "=", "evaluate", 5, 3, op_bg, op_fg)
