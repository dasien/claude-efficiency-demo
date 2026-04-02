"""Programmer calculator view with base conversion and bitwise operations."""

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
_BIT_BG = "#505050"
_BIT_FG = "#FFFFFF"
_MEM_BG = "#D4D4D2"
_MEM_FG = "#333333"
_HEX_BG = "#606060"
_HEX_FG = "#FFFFFF"

_NUM_STYLE: dict = {"bg": _NUM_BG, "fg": _NUM_FG, "font": ("TkDefaultFont", 14)}
_OP_STYLE: dict = {"bg": _OP_BG, "fg": _OP_FG, "font": ("TkDefaultFont", 14, "bold")}
_FUNC_STYLE: dict = {"bg": _FUNC_BG, "fg": _FUNC_FG, "font": ("TkDefaultFont", 12)}
_BIT_STYLE: dict = {"bg": _BIT_BG, "fg": _BIT_FG, "font": ("TkDefaultFont", 11)}
_HEX_STYLE: dict = {"bg": _HEX_BG, "fg": _HEX_FG, "font": ("TkDefaultFont", 12)}


class ProgrammerView(BaseView):
    """Programmer calculator view with base conversion and bitwise ops.

    Shows HEX/DEC/OCT/BIN representations simultaneously and provides
    buttons for hex digits, bitwise operations, and base/word-size selection.
    """

    def __init__(self, parent: tk.Widget) -> None:
        """Initialize the programmer calculator view.

        Args:
            parent: The parent Tkinter widget.
        """
        super().__init__(parent)
        self._buttons: dict[str, tk.Button] = {}
        self._digit_buttons: dict[str, tk.Button] = {}
        self._hex_buttons: dict[str, tk.Button] = {}
        self.base_var = tk.StringVar(value="DEC")
        self._create_base_panel()
        self._create_base_radio_row()
        self._create_buttons()

    # ------------------------------------------------------------------
    # Base conversion panel
    # ------------------------------------------------------------------

    def _create_base_panel(self) -> None:
        """Build the multi-base display panel."""
        self.base_panel = ttk.Frame(self)
        self.base_panel.grid(row=1, column=0, columnspan=9, sticky="ew", padx=4)
        self.base_panel.columnconfigure(1, weight=1)

        self._base_labels: dict[str, ttk.Label] = {}
        bases = ["HEX", "DEC", "OCT", "BIN"]
        for idx, base in enumerate(bases):
            tag = ttk.Label(
                self.base_panel,
                text=base,
                font=("TkDefaultFont", 9),
                width=4,
            )
            tag.grid(row=idx, column=0, sticky="w", padx=(2, 4))

            value_label = ttk.Label(
                self.base_panel,
                text="0",
                font=("Courier", 10),
                anchor="e",
            )
            value_label.grid(row=idx, column=1, sticky="ew")
            self._base_labels[base] = value_label

    def _create_base_radio_row(self) -> None:
        """Build the base-selection radio buttons and word-size controls."""
        ctrl_frame = ttk.Frame(self)
        ctrl_frame.grid(row=2, column=0, columnspan=9, sticky="ew", padx=4)

        for base in ["DEC", "HEX", "OCT", "BIN"]:
            bid = f"base_{base.lower()}"
            rb = ttk.Radiobutton(
                ctrl_frame,
                text=base,
                variable=self.base_var,
                value=base,
                command=lambda b=bid: self._fire_callback(b),
            )
            rb.pack(side=tk.LEFT, padx=4)

        # Word size buttons
        self.word_size_label = ttk.Label(
            ctrl_frame,
            text="64-bit",
            font=("TkDefaultFont", 9),
        )
        self.word_size_label.pack(side=tk.RIGHT, padx=4)

        for bits in [64, 32, 16, 8]:
            bid = f"word_{bits}"
            btn = ttk.Button(
                ctrl_frame,
                text=str(bits),
                width=3,
                command=lambda b=bid: self._fire_callback(b),
            )
            btn.pack(side=tk.RIGHT, padx=1)

    # ------------------------------------------------------------------
    # Button grid
    # ------------------------------------------------------------------

    def _create_buttons(self) -> None:
        """Create and grid all programmer-mode buttons."""
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=3, column=0, columnspan=9, sticky="nsew")
        self.rowconfigure(3, weight=1)
        for c in range(9):
            self.columnconfigure(c, weight=1)
            btn_frame.columnconfigure(c, weight=1)
        for r in range(6):
            btn_frame.rowconfigure(r, weight=1)

        # -- Row 0: hex digits + bitwise ops + AC ----------------------
        row0 = [
            ("A", "hex_a", _HEX_STYLE),
            ("B", "hex_b", _HEX_STYLE),
            ("C", "hex_c", _HEX_STYLE),
            ("D", "hex_d", _HEX_STYLE),
            ("E", "hex_e", _HEX_STYLE),
            ("F", "hex_f", _HEX_STYLE),
            ("AND", "op_and", _BIT_STYLE),
            ("OR", "op_or", _BIT_STYLE),
            ("AC", "all_clear", _FUNC_STYLE),
        ]
        for idx, (text, bid, style) in enumerate(row0):
            btn = self._make_button(
                btn_frame, text, bid, row=0, col=idx, style=style
            )
            self._buttons[bid] = btn
            if bid.startswith("hex_"):
                self._hex_buttons[bid] = btn

        # -- Row 1: bitwise extras + function keys ---------------------
        row1 = [
            ("NOT", "op_not", _BIT_STYLE),
            ("XOR", "op_xor", _BIT_STYLE),
            ("LSH", "op_lsh", _BIT_STYLE),
            ("RSH", "op_rsh", _BIT_STYLE),
            ("%", "percent", _BIT_STYLE),
            ("C", "clear_entry", _FUNC_STYLE),
            ("\u207A/\u208B", "toggle_sign", _FUNC_STYLE),
            ("MOD", "op_mod", _BIT_STYLE),
            ("\u00F7", "op_div", _OP_STYLE),
        ]
        for idx, (text, bid, style) in enumerate(row1):
            btn = self._make_button(
                btn_frame, text, bid, row=1, col=idx, style=style
            )
            self._buttons[bid] = btn

        # -- Rows 2-4: empty left side + digit grid + operators --------
        digit_rows = [
            [("7", "digit_7"), ("8", "digit_8"), ("9", "digit_9"), ("\u00D7", "op_mul")],
            [("4", "digit_4"), ("5", "digit_5"), ("6", "digit_6"), ("\u2212", "op_sub")],
            [("1", "digit_1"), ("2", "digit_2"), ("3", "digit_3"), ("+", "op_add")],
        ]
        for row_off, items in enumerate(digit_rows):
            grid_row = row_off + 2
            for col_off, (text, bid) in enumerate(items):
                col = col_off + 5  # cols 5-8
                is_op = bid.startswith("op_")
                style = _OP_STYLE if is_op else _NUM_STYLE
                btn = self._make_button(
                    btn_frame, text, bid, row=grid_row, col=col, style=style
                )
                self._buttons[bid] = btn
                if bid.startswith("digit_"):
                    self._digit_buttons[bid] = btn

        # -- Row 5: 0 (colspan 2), =, backspace -----------------------
        btn = self._make_button(
            btn_frame, "0", "digit_0", row=5, col=5, colspan=2, style=_NUM_STYLE
        )
        self._buttons["digit_0"] = btn
        self._digit_buttons["digit_0"] = btn

        btn = self._make_button(
            btn_frame, "=", "equals", row=5, col=7, style=_OP_STYLE
        )
        self._buttons["equals"] = btn

        btn = self._make_button(
            btn_frame, "\u232B", "backspace", row=5, col=8, style=_FUNC_STYLE
        )
        self._buttons["backspace"] = btn

    # ------------------------------------------------------------------
    # Public interface for controller
    # ------------------------------------------------------------------

    def set_base_panel(self, values: dict[str, str]) -> None:
        """Update the simultaneous base-conversion display.

        Args:
            values: Mapping of base name ('HEX', 'DEC', 'OCT', 'BIN')
                    to display string.
        """
        for base, text in values.items():
            label = self._base_labels.get(base)
            if label is not None:
                label.configure(text=text)

    def set_active_base(self, base: str) -> None:
        """Set the active base radio selection.

        Args:
            base: One of 'HEX', 'DEC', 'OCT', 'BIN'.
        """
        self.base_var.set(base)

    def enable_digits(self, valid_digits: set[str]) -> None:
        """Enable or disable digit and hex buttons based on the current base.

        Args:
            valid_digits: Set of button IDs that should be enabled
                          (e.g. {'digit_0', 'digit_1', ..., 'hex_a', ...}).
        """
        for bid, btn in self._digit_buttons.items():
            state = tk.NORMAL if bid in valid_digits else tk.DISABLED
            btn.configure(state=state)
        for bid, btn in self._hex_buttons.items():
            state = tk.NORMAL if bid in valid_digits else tk.DISABLED
            btn.configure(state=state)

    def set_word_size_display(self, bits: int) -> None:
        """Update the word-size indicator label.

        Args:
            bits: The current word size (8, 16, 32, or 64).
        """
        self.word_size_label.configure(text=f"{bits}-bit")
