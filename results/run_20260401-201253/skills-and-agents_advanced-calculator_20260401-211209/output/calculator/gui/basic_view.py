"""Basic calculator view with standard arithmetic buttons."""

from __future__ import annotations

import tkinter as tk

from calculator.gui.base_view import BaseView

# -- colour constants --------------------------------------------------
_NUM_BG = "#E0E0E0"
_NUM_FG = "#000000"
_OP_BG = "#FF9500"
_OP_FG = "#FFFFFF"
_FUNC_BG = "#A5A5A5"
_FUNC_FG = "#000000"
_MEM_BG = "#D4D4D2"
_MEM_FG = "#333333"

_NUM_STYLE: dict = {"bg": _NUM_BG, "fg": _NUM_FG, "font": ("TkDefaultFont", 16)}
_OP_STYLE: dict = {"bg": _OP_BG, "fg": _OP_FG, "font": ("TkDefaultFont", 16, "bold")}
_FUNC_STYLE: dict = {"bg": _FUNC_BG, "fg": _FUNC_FG, "font": ("TkDefaultFont", 14)}
_MEM_STYLE: dict = {"bg": _MEM_BG, "fg": _MEM_FG, "font": ("TkDefaultFont", 11)}


class BasicView(BaseView):
    """Standard four-function calculator view.

    Layout (4 main columns, 5-column memory row):
        Row 0-1: Display (inherited from BaseView)
        Row 2:   MC | MR | M+ | M- | MS
        Row 3:   AC | +/- | % | div
        Row 4:   7 | 8 | 9 | mul
        Row 5:   4 | 5 | 6 | sub
        Row 6:   1 | 2 | 3 | add
        Row 7:   0 (colspan 2) | . | =
    """

    def __init__(self, parent: tk.Widget) -> None:
        """Initialize the basic calculator view.

        Args:
            parent: The parent Tkinter widget.
        """
        super().__init__(parent)
        self._buttons: dict[str, tk.Button] = {}
        self._create_buttons()

    # ------------------------------------------------------------------
    # Layout helpers
    # ------------------------------------------------------------------

    def _create_buttons(self) -> None:
        """Create and grid all buttons for the basic calculator."""
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=1, column=0, sticky="nsew")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Configure 4 main columns with equal weight
        for c in range(4):
            btn_frame.columnconfigure(c, weight=1)

        # Configure rows 0-5 (memory + 5 button rows) with equal weight
        for r in range(6):
            btn_frame.rowconfigure(r, weight=1)

        # -- Memory row (row 0) using a sub-frame for 5 columns -------
        mem_frame = tk.Frame(btn_frame)
        mem_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
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
            btn = self._make_button(
                mem_frame, text, bid, row=0, col=idx, style=_MEM_STYLE
            )
            self._buttons[bid] = btn

        # -- Row 1: AC, +/-, %, div ------------------------------------
        func_row = [
            ("AC", "all_clear", _FUNC_STYLE),
            ("\u207A/\u208B", "toggle_sign", _FUNC_STYLE),
            ("%", "percent", _FUNC_STYLE),
            ("\u00F7", "op_div", _OP_STYLE),
        ]
        for idx, (text, bid, style) in enumerate(func_row):
            btn = self._make_button(
                btn_frame, text, bid, row=1, col=idx, style=style
            )
            self._buttons[bid] = btn

        # -- Rows 2-4: digit grid + operators --------------------------
        digit_rows = [
            [("7", "digit_7"), ("8", "digit_8"), ("9", "digit_9"), ("\u00D7", "op_mul")],
            [("4", "digit_4"), ("5", "digit_5"), ("6", "digit_6"), ("\u2212", "op_sub")],
            [("1", "digit_1"), ("2", "digit_2"), ("3", "digit_3"), ("+", "op_add")],
        ]
        for row_offset, row_items in enumerate(digit_rows):
            grid_row = row_offset + 2
            for col_idx, (text, bid) in enumerate(row_items):
                is_op = bid.startswith("op_")
                style = _OP_STYLE if is_op else _NUM_STYLE
                btn = self._make_button(
                    btn_frame, text, bid, row=grid_row, col=col_idx, style=style
                )
                self._buttons[bid] = btn

        # -- Row 5: 0 (colspan 2), ., = --------------------------------
        btn = self._make_button(
            btn_frame, "0", "digit_0", row=5, col=0, colspan=2, style=_NUM_STYLE
        )
        self._buttons["digit_0"] = btn

        btn = self._make_button(
            btn_frame, ".", "decimal", row=5, col=2, style=_NUM_STYLE
        )
        self._buttons["decimal"] = btn

        btn = self._make_button(
            btn_frame, "=", "equals", row=5, col=3, style=_OP_STYLE
        )
        self._buttons["equals"] = btn
