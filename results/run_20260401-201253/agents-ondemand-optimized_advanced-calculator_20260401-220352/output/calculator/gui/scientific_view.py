"""Scientific mode GUI layout.

Extends the basic layout with additional columns for trigonometric,
logarithmic, power/root functions, constants, parentheses, and a
degree/radian mode toggle.
"""

from __future__ import annotations

import tkinter as tk
from typing import TYPE_CHECKING

from calculator.gui.base_view import BaseView

if TYPE_CHECKING:
    from calculator.app import App


class ScientificView(BaseView):
    """Scientific mode button grid layout.

    Adds 5 function columns to the left of the standard digit/operator
    grid. Includes Deg/Rad toggle and parenthesis depth indicator.
    """

    def __init__(self, parent: tk.Widget, controller: App) -> None:
        super().__init__(parent, controller)
        self.angle_label: tk.Label | None = None
        self.paren_label: tk.Label | None = None
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create all widgets for scientific mode."""
        main_frame = tk.Frame(self, bg=self.COLOR_BG)
        main_frame.pack(fill="both", expand=True)

        total_cols = 9  # 5 scientific + 4 basic
        for c in range(total_cols):
            main_frame.columnconfigure(c, weight=1, minsize=58)
        for r in range(8):
            main_frame.rowconfigure(r, weight=1, minsize=45)
        main_frame.rowconfigure(0, weight=2, minsize=100)

        # Display area spanning all columns
        self._create_display(main_frame)

        # Angle mode indicator
        angle_frame = tk.Frame(
            main_frame, bg=self.COLOR_DISPLAY_BG
        )
        angle_frame.grid(row=0, column=total_cols - 1, sticky="ne")
        self.angle_label = tk.Label(
            angle_frame,
            text="DEG",
            font=("Helvetica", 10, "bold"),
            fg="#FF9500",
            bg=self.COLOR_DISPLAY_BG,
            cursor="hand2",
        )
        self.angle_label.pack(padx=5, pady=5)
        self.angle_label.bind(
            "<Button-1>",
            lambda e: self.controller.on_toggle_angle(),
        )

        # Parenthesis depth indicator
        self.paren_label = tk.Label(
            main_frame,
            text="",
            font=("Helvetica", 9),
            fg="#AAAAAA",
            bg=self.COLOR_BG,
        )
        self.paren_label.grid(row=1, column=1, sticky="w")

        # Memory row
        mem_frame = tk.Frame(main_frame, bg=self.COLOR_BG)
        mem_frame.grid(
            row=1, column=0, columnspan=total_cols, sticky="nsew"
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

        # Row 2: (, ), x^2, x^3, x^n, C, +/-, %, /
        sci_row2 = [
            ("(", lambda: self.controller.on_scientific("open_paren")),
            (")", lambda: self.controller.on_scientific("close_paren")),
            ("x\u00b2", lambda: self.controller.on_scientific("square")),
            ("x\u00b3", lambda: self.controller.on_scientific("cube")),
            ("x\u207f", lambda: self.controller.on_scientific("power")),
            ("C", self.controller.on_clear),
            ("+/-", self.controller.on_toggle_sign),
            ("%", self.controller.on_percentage),
            ("/", lambda: self.controller.on_operator("/")),
        ]
        for i, (text, cmd) in enumerate(sci_row2):
            s = "operator" if text == "/" else "function"
            self._create_button(main_frame, text, 2, i, cmd, style=s)

        # Row 3: sin, cos, tan, sqrt, cbrt, 7, 8, 9, *
        sci_row3 = [
            ("sin", lambda: self.controller.on_scientific("sin")),
            ("cos", lambda: self.controller.on_scientific("cos")),
            ("tan", lambda: self.controller.on_scientific("tan")),
            ("\u221ax", lambda: self.controller.on_scientific("sqrt")),
            ("\u00b3\u221ax", lambda: self.controller.on_scientific("cbrt")),
            ("7", lambda: self.controller.on_digit("7")),
            ("8", lambda: self.controller.on_digit("8")),
            ("9", lambda: self.controller.on_digit("9")),
            ("*", lambda: self.controller.on_operator("*")),
        ]
        for i, (text, cmd) in enumerate(sci_row3):
            s = (
                "digit" if text.isdigit()
                else "operator" if text == "*"
                else "function"
            )
            self._create_button(main_frame, text, 3, i, cmd, style=s)

        # Row 4: asin, acos, atan, 10^x, e^x, 4, 5, 6, -
        sci_row4 = [
            ("asin", lambda: self.controller.on_scientific("asin")),
            ("acos", lambda: self.controller.on_scientific("acos")),
            ("atan", lambda: self.controller.on_scientific("atan")),
            ("10\u02e3", lambda: self.controller.on_scientific("ten_to_x")),
            ("e\u02e3", lambda: self.controller.on_scientific("e_to_x")),
            ("4", lambda: self.controller.on_digit("4")),
            ("5", lambda: self.controller.on_digit("5")),
            ("6", lambda: self.controller.on_digit("6")),
            ("-", lambda: self.controller.on_operator("-")),
        ]
        for i, (text, cmd) in enumerate(sci_row4):
            s = (
                "digit" if text.isdigit()
                else "operator" if text == "-"
                else "function"
            )
            self._create_button(main_frame, text, 4, i, cmd, style=s)

        # Row 5: n!, |x|, log, ln, log2, 1, 2, 3, +
        sci_row5 = [
            ("n!", lambda: self.controller.on_scientific("factorial")),
            ("|x|", lambda: self.controller.on_scientific("abs")),
            ("log", lambda: self.controller.on_scientific("log10")),
            ("ln", lambda: self.controller.on_scientific("ln")),
            ("log\u2082", lambda: self.controller.on_scientific("log2")),
            ("1", lambda: self.controller.on_digit("1")),
            ("2", lambda: self.controller.on_digit("2")),
            ("3", lambda: self.controller.on_digit("3")),
            ("+", lambda: self.controller.on_operator("+")),
        ]
        for i, (text, cmd) in enumerate(sci_row5):
            s = (
                "digit" if text.isdigit()
                else "operator" if text == "+"
                else "function"
            )
            self._create_button(main_frame, text, 5, i, cmd, style=s)

        # Row 6: pi, e, 1/x, [empty], [empty], 0 (span 2), ., =
        sci_row6_left = [
            ("\u03c0", lambda: self.controller.on_scientific("pi")),
            ("e", lambda: self.controller.on_scientific("e_const")),
            ("1/x", lambda: self.controller.on_scientific("reciprocal")),
        ]
        for i, (text, cmd) in enumerate(sci_row6_left):
            self._create_button(
                main_frame, text, 6, i, cmd, style="function"
            )

        # Empty spacer cells (columns 3, 4)
        for col in [3, 4]:
            spacer = tk.Frame(main_frame, bg=self.COLOR_BG)
            spacer.grid(row=6, column=col, sticky="nsew")

        # 0 button spanning 2 columns
        self._create_button(
            main_frame, "0", 6, 5,
            lambda: self.controller.on_digit("0"),
            colspan=2, style="digit",
        )
        self._create_button(
            main_frame, ".", 6, 7,
            self.controller.on_decimal, style="digit"
        )
        self._create_button(
            main_frame, "=", 6, 8,
            self.controller.on_equals, style="equals"
        )

    def update_angle_display(self, mode: str) -> None:
        """Update the angle mode indicator.

        Args:
            mode: 'DEG' or 'RAD'.
        """
        if self.angle_label:
            self.angle_label.configure(text=mode)

    def update_paren_depth(self, depth: int) -> None:
        """Update the parenthesis depth indicator.

        Args:
            depth: Current nesting depth.
        """
        if self.paren_label:
            if depth > 0:
                self.paren_label.configure(text=f"({depth}")
            else:
                self.paren_label.configure(text="")
