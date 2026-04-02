"""Scientific mode GUI layout."""

import tkinter as tk
from typing import Callable
from .base_view import BaseView, COLORS


class ScientificView(BaseView):
    """Scientific calculator mode view."""

    def __init__(self, parent: tk.Widget, callback: Callable[[str], None]) -> None:
        """Initialize scientific view with extended button grid."""
        super().__init__(parent, callback)
        self._angle_label = None
        self._build_angle_indicator()
        self._build_buttons()

    def _build_angle_indicator(self) -> None:
        """Build the DEG/RAD indicator."""
        self._angle_label = tk.Label(
            self.indicator_frame,
            text="DEG",
            font=("Helvetica", 12),
            fg=COLORS["indicator"],
            bg=COLORS["display_bg"],
            anchor="e",
        )
        self._angle_label.pack(side=tk.RIGHT)

    def update_angle_mode(self, mode: str) -> None:
        """Update the angle mode indicator."""
        if self._angle_label:
            self._angle_label.config(text=mode)

    def _build_buttons(self) -> None:
        """Build the button grid for scientific mode."""
        btn_frame = tk.Frame(self.frame, bg=COLORS["bg"])
        btn_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        cols = 9
        rows = 7
        for i in range(cols):
            btn_frame.columnconfigure(i, weight=1, uniform="btn")
        for i in range(rows):
            btn_frame.rowconfigure(i, weight=1, uniform="btn")

        # Memory row
        mem_bg = COLORS["btn_memory"]
        mem_fg = COLORS["btn_memory_fg"]
        mem_frame = tk.Frame(btn_frame, bg=COLORS["bg"])
        mem_frame.grid(row=0, column=0, columnspan=cols, sticky="nsew")
        for i in range(5):
            mem_frame.columnconfigure(i, weight=1, uniform="mem")
        mem_frame.rowconfigure(0, weight=1)
        mem_buttons = [
            ("MC", "memory_clear"),
            ("MR", "memory_recall"),
            ("M+", "memory_add"),
            ("M\u2212", "memory_subtract"),
            ("MS", "memory_store"),
        ]
        for i, (text, action) in enumerate(mem_buttons):
            btn = tk.Button(
                mem_frame,
                text=text,
                font=("Helvetica", 12),
                bg=mem_bg,
                fg=mem_fg,
                activebackground=mem_bg,
                activeforeground=mem_fg,
                borderwidth=0,
                command=lambda a=action: self.callback(a),
            )
            btn.grid(row=0, column=i, sticky="nsew", padx=1, pady=1)

        sci_bg = COLORS["btn_sci"]
        sci_fg = COLORS["btn_sci_fg"]
        func_bg = COLORS["btn_func"]
        func_fg = COLORS["btn_func_fg"]
        op_bg = COLORS["btn_op"]
        op_fg = COLORS["btn_op_fg"]

        # Row 1: (, ), x², x³, xⁿ, C, +/-, %, /
        r = 1
        self._make_button(btn_frame, "(", "open_paren", r, 0, sci_bg, sci_fg)
        self._make_button(btn_frame, ")", "close_paren", r, 1, sci_bg, sci_fg)
        self._make_button(btn_frame, "x\u00B2", "square", r, 2, sci_bg, sci_fg)
        self._make_button(btn_frame, "x\u00B3", "cube", r, 3, sci_bg, sci_fg)
        self._make_button(btn_frame, "x\u207F", "power", r, 4, sci_bg, sci_fg)
        self._make_button(btn_frame, "C", "clear_entry", r, 5, func_bg, func_fg)
        self._make_button(btn_frame, "+/\u2212", "toggle_sign", r, 6, func_bg, func_fg)
        self._make_button(btn_frame, "%", "percent", r, 7, func_bg, func_fg)
        self._make_button(btn_frame, "\u00F7", "op_/", r, 8, op_bg, op_fg)

        # Row 2: sin, cos, tan, √x, ³√x, 7, 8, 9, *
        r = 2
        self._make_button(btn_frame, "sin", "sin", r, 0, sci_bg, sci_fg)
        self._make_button(btn_frame, "cos", "cos", r, 1, sci_bg, sci_fg)
        self._make_button(btn_frame, "tan", "tan", r, 2, sci_bg, sci_fg)
        self._make_button(btn_frame, "\u221Ax", "sqrt", r, 3, sci_bg, sci_fg)
        self._make_button(btn_frame, "\u00B3\u221Ax", "cbrt", r, 4, sci_bg, sci_fg)
        self._make_button(btn_frame, "7", "digit_7", r, 5)
        self._make_button(btn_frame, "8", "digit_8", r, 6)
        self._make_button(btn_frame, "9", "digit_9", r, 7)
        self._make_button(btn_frame, "\u00D7", "op_*", r, 8, op_bg, op_fg)

        # Row 3: asin, acos, atan, 10ˣ, eˣ, 4, 5, 6, -
        r = 3
        self._make_button(btn_frame, "asin", "asin", r, 0, sci_bg, sci_fg)
        self._make_button(btn_frame, "acos", "acos", r, 1, sci_bg, sci_fg)
        self._make_button(btn_frame, "atan", "atan", r, 2, sci_bg, sci_fg)
        self._make_button(btn_frame, "10\u02E3", "ten_power", r, 3, sci_bg, sci_fg)
        self._make_button(btn_frame, "e\u02E3", "e_power", r, 4, sci_bg, sci_fg)
        self._make_button(btn_frame, "4", "digit_4", r, 5)
        self._make_button(btn_frame, "5", "digit_5", r, 6)
        self._make_button(btn_frame, "6", "digit_6", r, 7)
        self._make_button(btn_frame, "\u2212", "op_-", r, 8, op_bg, op_fg)

        # Row 4: n!, |x|, log, ln, log₂, 1, 2, 3, +
        r = 4
        self._make_button(btn_frame, "n!", "factorial", r, 0, sci_bg, sci_fg)
        self._make_button(btn_frame, "|x|", "absolute", r, 1, sci_bg, sci_fg)
        self._make_button(btn_frame, "log", "log", r, 2, sci_bg, sci_fg)
        self._make_button(btn_frame, "ln", "ln", r, 3, sci_bg, sci_fg)
        self._make_button(btn_frame, "log\u2082", "log2", r, 4, sci_bg, sci_fg)
        self._make_button(btn_frame, "1", "digit_1", r, 5)
        self._make_button(btn_frame, "2", "digit_2", r, 6)
        self._make_button(btn_frame, "3", "digit_3", r, 7)
        self._make_button(btn_frame, "+", "op_+", r, 8, op_bg, op_fg)

        # Row 5: π, e, 1/x, Deg/Rad, AC, 0(span 2), ., =
        r = 5
        self._make_button(btn_frame, "\u03C0", "insert_pi", r, 0, sci_bg, sci_fg)
        self._make_button(btn_frame, "e", "insert_e", r, 1, sci_bg, sci_fg)
        self._make_button(btn_frame, "1/x", "reciprocal", r, 2, sci_bg, sci_fg)
        self._make_button(btn_frame, "Deg", "toggle_angle", r, 3, sci_bg, sci_fg)
        self._make_button(btn_frame, "AC", "all_clear", r, 4, func_bg, func_fg)
        self._make_button(btn_frame, "0", "digit_0", r, 5, colspan=2)
        self._make_button(btn_frame, ".", "decimal", r, 7)
        self._make_button(btn_frame, "=", "evaluate", r, 8, op_bg, op_fg)
