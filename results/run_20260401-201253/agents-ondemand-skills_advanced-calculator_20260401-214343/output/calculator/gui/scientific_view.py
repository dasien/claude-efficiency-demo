"""Scientific calculator view extending basic mode with advanced functions."""

import tkinter as tk
from typing import Dict, Callable

from calculator.gui.base_view import (
    BG_COLOR,
    BTN_ACTIVE_BG,
    BTN_BG,
    BTN_FG,
    BUTTON_FONT,
    DISPLAY_BG,
    EQUALS_BG,
    INDICATOR_FONT,
    MAIN_DISPLAY_FG,
    OPERATOR_ACTIVE_BG,
    OPERATOR_BG,
    OPERATOR_FG,
    SMALL_BUTTON_FONT,
    SPECIAL_BG,
    BaseView,
)
from calculator.logic.base_logic import AngleUnit, DisplayState


class ScientificView(BaseView):
    """Scientific calculator view with trig, log, power, and constant buttons.

    Layout matches requirements section 4.7:
        Memory row: MC | MR | M+ | M- | MS
        Left panel (5 cols): scientific functions
        Right panel (4 cols): basic digit/operator grid
        Deg/Rad indicator toggle in display area
    """

    def _build_display_area(self) -> None:
        """Override to add a Deg/Rad toggle button beside the display."""
        super()._build_display_area()

        self._angle_btn = tk.Button(
            self._display_frame,
            text="DEG",
            font=INDICATOR_FONT,
            fg=MAIN_DISPLAY_FG,
            bg=SPECIAL_BG,
            activebackground=BTN_ACTIVE_BG,
            activeforeground=BTN_FG,
            bd=0,
            highlightthickness=0,
            width=5,
            command=lambda: self._on_button_click("Deg/Rad"),
        )
        self._angle_btn.place(relx=1.0, rely=0.5, anchor=tk.E, x=-10)
        self._buttons["Deg/Rad"] = self._angle_btn

    def _build_button_grid(self) -> None:
        """Create the scientific mode button grid."""
        self._grid_frame = tk.Frame(self, bg=BG_COLOR)
        self._grid_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        total_cols = 9
        total_rows = 5
        for c in range(total_cols):
            self._grid_frame.columnconfigure(c, weight=1, minsize=55)
        for r in range(total_rows):
            self._grid_frame.rowconfigure(r, weight=1, minsize=45)

        sci_font = SMALL_BUTTON_FONT
        sci_bg = SPECIAL_BG

        # ── Row 0: ( ) x^2 x^3 x^n | C +/- % / ────────────
        sci_row0 = [
            ("(", "("),
            (")", ")"),
            ("x\u00b2", "x\u00b2"),
            ("x\u00b3", "x\u00b3"),
            ("x\u207f", "x\u207f"),
        ]
        for i, (text, name) in enumerate(sci_row0):
            self._create_button(
                self._grid_frame, text, 0, i,
                bg=sci_bg, font=sci_font, callback_name=name,
            )

        self._create_button(
            self._grid_frame, "C", 0, 5, bg=SPECIAL_BG,
        )
        self._create_button(
            self._grid_frame, "\u00b1", 0, 6,
            bg=SPECIAL_BG, callback_name="+/-",
        )
        self._create_button(
            self._grid_frame, "%", 0, 7, bg=SPECIAL_BG,
        )
        self._create_button(
            self._grid_frame, "\u00f7", 0, 8,
            bg=OPERATOR_BG, fg=OPERATOR_FG,
            active_bg=OPERATOR_ACTIVE_BG, callback_name="/",
        )

        # ── Row 1: sin cos tan sqrt cbrt | 7 8 9 * ─────────
        sci_row1 = [
            ("sin", "sin"),
            ("cos", "cos"),
            ("tan", "tan"),
            ("\u221ax", "\u221ax"),
            ("\u00b3\u221ax", "\u00b3\u221ax"),
        ]
        for i, (text, name) in enumerate(sci_row1):
            self._create_button(
                self._grid_frame, text, 1, i,
                bg=sci_bg, font=sci_font, callback_name=name,
            )

        for j, digit in enumerate(["7", "8", "9"]):
            self._create_button(
                self._grid_frame, digit, 1, 5 + j,
            )
        self._create_button(
            self._grid_frame, "\u00d7", 1, 8,
            bg=OPERATOR_BG, fg=OPERATOR_FG,
            active_bg=OPERATOR_ACTIVE_BG, callback_name="*",
        )

        # ── Row 2: asin acos atan 10^x e^x | 4 5 6 - ──────
        sci_row2 = [
            ("asin", "asin"),
            ("acos", "acos"),
            ("atan", "atan"),
            ("10\u02e3", "10\u02e3"),
            ("e\u02e3", "e\u02e3"),
        ]
        for i, (text, name) in enumerate(sci_row2):
            self._create_button(
                self._grid_frame, text, 2, i,
                bg=sci_bg, font=sci_font, callback_name=name,
            )

        for j, digit in enumerate(["4", "5", "6"]):
            self._create_button(
                self._grid_frame, digit, 2, 5 + j,
            )
        self._create_button(
            self._grid_frame, "\u2212", 2, 8,
            bg=OPERATOR_BG, fg=OPERATOR_FG,
            active_bg=OPERATOR_ACTIVE_BG, callback_name="-",
        )

        # ── Row 3: n! |x| log ln log2 | 1 2 3 + ───────────
        sci_row3 = [
            ("n!", "n!"),
            ("|x|", "|x|"),
            ("log", "log"),
            ("ln", "ln"),
            ("log\u2082", "log\u2082"),
        ]
        for i, (text, name) in enumerate(sci_row3):
            self._create_button(
                self._grid_frame, text, 3, i,
                bg=sci_bg, font=sci_font, callback_name=name,
            )

        for j, digit in enumerate(["1", "2", "3"]):
            self._create_button(
                self._grid_frame, digit, 3, 5 + j,
            )
        self._create_button(
            self._grid_frame, "+", 3, 8,
            bg=OPERATOR_BG, fg=OPERATOR_FG,
            active_bg=OPERATOR_ACTIVE_BG,
        )

        # ── Row 4: pi e 1/x [blank] [blank] | 0(x2) . = ───
        sci_row4 = [
            ("\u03c0", "\u03c0"),
            ("e", "e"),
            ("1/x", "1/x"),
        ]
        for i, (text, name) in enumerate(sci_row4):
            self._create_button(
                self._grid_frame, text, 4, i,
                bg=sci_bg, font=sci_font, callback_name=name,
            )

        # Blank spacer buttons for columns 3 and 4
        for col in (3, 4):
            spacer = tk.Frame(
                self._grid_frame, bg=BG_COLOR,
            )
            spacer.grid(
                row=4, column=col, sticky="nsew",
                padx=1, pady=1,
            )

        self._create_button(
            self._grid_frame, "0", 4, 5, colspan=2,
        )
        self._create_button(
            self._grid_frame, ".", 4, 7,
        )
        self._create_button(
            self._grid_frame, "=", 4, 8,
            bg=EQUALS_BG, fg=OPERATOR_FG,
            active_bg=OPERATOR_ACTIVE_BG,
        )

    def update_display(self, state: DisplayState) -> None:
        """Update the display including the angle unit indicator.

        Args:
            state: The current display state from the logic layer.
        """
        super().update_display(state)
        angle_text = (
            "DEG" if state.angle_unit == AngleUnit.DEG else "RAD"
        )
        self._angle_btn.config(text=angle_text)

        # Show paren depth if nonzero
        if state.paren_depth > 0:
            expr = state.expression_display
            depth_hint = f"  ({state.paren_depth} open)"
            self._expression_display.config(text=expr + depth_hint)
