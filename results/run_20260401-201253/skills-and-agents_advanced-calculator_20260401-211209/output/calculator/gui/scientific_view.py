"""Scientific calculator view with trigonometric and other advanced functions."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from calculator.gui.base_view import BaseView

# -- colour constants --------------------------------------------------
_NUM_BG = "#E0E0E0"
_NUM_FG = "#000000"
_OP_BG = "#FF9500"
_OP_FG = "#FFFFFF"
_FUNC_BG = "#A5A5A5"
_FUNC_FG = "#000000"
_SCI_BG = "#505050"
_SCI_FG = "#FFFFFF"
_MEM_BG = "#D4D4D2"
_MEM_FG = "#333333"

_NUM_STYLE: dict = {"bg": _NUM_BG, "fg": _NUM_FG, "font": ("TkDefaultFont", 14)}
_OP_STYLE: dict = {"bg": _OP_BG, "fg": _OP_FG, "font": ("TkDefaultFont", 14, "bold")}
_FUNC_STYLE: dict = {"bg": _FUNC_BG, "fg": _FUNC_FG, "font": ("TkDefaultFont", 12)}
_SCI_STYLE: dict = {"bg": _SCI_BG, "fg": _SCI_FG, "font": ("TkDefaultFont", 11)}
_MEM_STYLE: dict = {"bg": _MEM_BG, "fg": _MEM_FG, "font": ("TkDefaultFont", 10)}


class ScientificView(BaseView):
    """Scientific calculator view with trig, log, and power functions.

    Layout uses 9 columns:
        Cols 0-4: scientific function buttons
        Cols 5-8: standard digit/operator buttons
    """

    def __init__(self, parent: tk.Widget) -> None:
        """Initialize the scientific calculator view.

        Args:
            parent: The parent Tkinter widget.
        """
        super().__init__(parent)
        self._buttons: dict[str, tk.Button] = {}
        self._create_angle_indicator()
        self._create_buttons()

    # ------------------------------------------------------------------
    # Display additions
    # ------------------------------------------------------------------

    def _create_angle_indicator(self) -> None:
        """Add an angle-mode indicator next to the display."""
        self.angle_indicator = ttk.Label(
            self,
            text="DEG",
            font=("TkDefaultFont", 10),
        )
        self.angle_indicator.grid(row=0, column=1, sticky="ne", padx=4)

        self.paren_indicator = ttk.Label(
            self,
            text="",
            font=("TkDefaultFont", 10),
        )
        self.paren_indicator.grid(row=0, column=2, sticky="ne", padx=4)

    def set_angle_mode(self, mode: str) -> None:
        """Update the angle-mode indicator text.

        Args:
            mode: 'DEG' or 'RAD'.
        """
        self.angle_indicator.configure(text=mode)

    def set_paren_depth(self, depth: int) -> None:
        """Show a parenthesis-depth indicator.

        Args:
            depth: The current open-paren nesting depth.
        """
        if depth > 0:
            self.paren_indicator.configure(text=f"( \u00d7 {depth}")
        else:
            self.paren_indicator.configure(text="")

    # ------------------------------------------------------------------
    # Button layout
    # ------------------------------------------------------------------

    def _create_buttons(self) -> None:
        """Create and grid all buttons for the scientific calculator."""
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=1, column=0, columnspan=9, sticky="nsew")
        self.rowconfigure(1, weight=1)
        for c in range(9):
            self.columnconfigure(c, weight=1)

        for c in range(9):
            btn_frame.columnconfigure(c, weight=1)
        for r in range(6):
            btn_frame.rowconfigure(r, weight=1)

        # -- Memory row (row 0) spanning full width --------------------
        mem_frame = tk.Frame(btn_frame)
        mem_frame.grid(row=0, column=0, columnspan=9, sticky="nsew")
        for c in range(5):
            mem_frame.columnconfigure(c, weight=1)
        mem_frame.rowconfigure(0, weight=1)

        mem_buttons = [
            ("MC", "mc"),
            ("MR", "mr"),
            ("M+", "m_plus"),
            ("M\u2212", "m_minus"),
            ("MS", "ms"),
        ]
        for idx, (text, bid) in enumerate(mem_buttons):
            self._buttons[bid] = self._make_button(
                mem_frame, text, bid, row=0, col=idx, style=_MEM_STYLE
            )

        # -- Row 1: parens + powers + function row ---------------------
        row1 = [
            ("(", "open_paren", _SCI_STYLE),
            (")", "close_paren", _SCI_STYLE),
            ("x\u00B2", "square", _SCI_STYLE),
            ("x\u00B3", "cube", _SCI_STYLE),
            ("x\u207F", "power", _SCI_STYLE),
            ("AC", "all_clear", _FUNC_STYLE),
            ("\u207A/\u208B", "toggle_sign", _FUNC_STYLE),
            ("%", "percent", _FUNC_STYLE),
            ("\u00F7", "op_div", _OP_STYLE),
        ]
        for idx, (text, bid, style) in enumerate(row1):
            self._buttons[bid] = self._make_button(
                btn_frame, text, bid, row=1, col=idx, style=style
            )

        # -- Rows 2-4: scientific left + digit/op right ----------------
        sci_rows = [
            # (sci cols 0-4, standard cols 5-8)
            [
                ("sin", "sin", _SCI_STYLE),
                ("cos", "cos", _SCI_STYLE),
                ("tan", "tan", _SCI_STYLE),
                ("\u221Ax", "sqrt", _SCI_STYLE),
                ("\u00B3\u221Ax", "cbrt", _SCI_STYLE),
                ("7", "digit_7", _NUM_STYLE),
                ("8", "digit_8", _NUM_STYLE),
                ("9", "digit_9", _NUM_STYLE),
                ("\u00D7", "op_mul", _OP_STYLE),
            ],
            [
                ("asin", "asin", _SCI_STYLE),
                ("acos", "acos", _SCI_STYLE),
                ("atan", "atan", _SCI_STYLE),
                ("10\u02E3", "ten_power", _SCI_STYLE),
                ("e\u02E3", "e_power", _SCI_STYLE),
                ("4", "digit_4", _NUM_STYLE),
                ("5", "digit_5", _NUM_STYLE),
                ("6", "digit_6", _NUM_STYLE),
                ("\u2212", "op_sub", _OP_STYLE),
            ],
            [
                ("n!", "factorial", _SCI_STYLE),
                ("|x|", "absolute", _SCI_STYLE),
                ("log", "log", _SCI_STYLE),
                ("ln", "ln", _SCI_STYLE),
                ("log\u2082", "log2", _SCI_STYLE),
                ("1", "digit_1", _NUM_STYLE),
                ("2", "digit_2", _NUM_STYLE),
                ("3", "digit_3", _NUM_STYLE),
                ("+", "op_add", _OP_STYLE),
            ],
        ]
        for row_offset, items in enumerate(sci_rows):
            grid_row = row_offset + 2
            for col_idx, (text, bid, style) in enumerate(items):
                self._buttons[bid] = self._make_button(
                    btn_frame, text, bid, row=grid_row, col=col_idx, style=style
                )

        # -- Row 5: constants + bottom standard row --------------------
        bottom_sci = [
            ("\u03C0", "pi", _SCI_STYLE),
            ("e", "euler", _SCI_STYLE),
            ("1/x", "reciprocal", _SCI_STYLE),
            ("DEG", "toggle_angle", _SCI_STYLE),
        ]
        for idx, (text, bid, style) in enumerate(bottom_sci):
            self._buttons[bid] = self._make_button(
                btn_frame, text, bid, row=5, col=idx, style=style
            )

        # col 4 intentionally empty

        self._buttons["digit_0"] = self._make_button(
            btn_frame, "0", "digit_0", row=5, col=5, colspan=2, style=_NUM_STYLE
        )
        self._buttons["decimal"] = self._make_button(
            btn_frame, ".", "decimal", row=5, col=7, style=_NUM_STYLE
        )
        self._buttons["equals"] = self._make_button(
            btn_frame, "=", "equals", row=5, col=8, style=_OP_STYLE
        )
