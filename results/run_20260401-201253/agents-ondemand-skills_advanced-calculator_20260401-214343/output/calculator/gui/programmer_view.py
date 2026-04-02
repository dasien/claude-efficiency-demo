"""Programmer calculator view with base conversion and bitwise operations."""

import tkinter as tk
from typing import Dict, Callable, List

from calculator.gui.base_view import (
    BG_COLOR,
    BTN_ACTIVE_BG,
    BTN_BG,
    BTN_FG,
    BUTTON_FONT,
    DISPLAY_BG,
    EQUALS_BG,
    EXPRESSION_FG,
    INDICATOR_FONT,
    MAIN_DISPLAY_FG,
    MEMORY_BG,
    MEMORY_FG,
    OPERATOR_ACTIVE_BG,
    OPERATOR_BG,
    OPERATOR_FG,
    SMALL_BUTTON_FONT,
    SPECIAL_BG,
    BaseView,
)
from calculator.logic.base_logic import DisplayState, NumberBase, WordSize

# Disabled button styling
DISABLED_BG = "#2a2a2a"
DISABLED_FG = "#555555"

# Base conversion panel styling
CONVERSION_FONT = ("Courier", 11)
CONVERSION_FG = "#b0b0b0"
CONVERSION_ACTIVE_FG = "#ffffff"


class ProgrammerView(BaseView):
    """Programmer calculator view with base conversion and bitwise ops.

    Layout matches requirements section 5.6:
        Display area with word size indicator
        Base conversion panel (HEX, DEC, OCT, BIN values)
        Base selector radio buttons
        Hex digit buttons A-F
        Bitwise operation buttons
        Standard digit/operator grid
    """

    def __init__(self, parent: tk.Widget) -> None:
        self._base_var = tk.StringVar(value="DEC")
        self._word_var = tk.StringVar(value="64")
        self._conversion_labels: Dict[str, tk.Label] = {}
        self._hex_buttons: List[str] = ["A", "B", "C", "D", "E", "F"]
        self._digit_buttons: List[str] = [
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        ]
        super().__init__(parent)

    def _build_display_area(self) -> None:
        """Override to add word size indicator beside the display."""
        super()._build_display_area()

        self._word_label = tk.Label(
            self._display_frame,
            text="Word: 64",
            font=INDICATOR_FONT,
            fg=MAIN_DISPLAY_FG,
            bg=SPECIAL_BG,
        )
        self._word_label.place(relx=1.0, rely=0.5, anchor=tk.E, x=-10)

    def _build_memory_row(self) -> None:
        """Override: programmer mode has no memory row.

        Memory row is replaced by the base conversion panel and
        base selector.
        """
        self._build_conversion_panel()
        self._build_base_selector()
        self._build_word_size_selector()

    def _build_conversion_panel(self) -> None:
        """Create the panel showing values in all four bases."""
        self._conv_frame = tk.Frame(self, bg=BG_COLOR)
        self._conv_frame.pack(fill=tk.X, padx=5, pady=(2, 0))

        bases = ["HEX", "DEC", "OCT", "BIN"]
        for base_name in bases:
            row = tk.Frame(self._conv_frame, bg=BG_COLOR)
            row.pack(fill=tk.X, padx=2, pady=1)

            label = tk.Label(
                row,
                text=f"{base_name}:",
                font=CONVERSION_FONT,
                fg=CONVERSION_FG,
                bg=BG_COLOR,
                width=4,
                anchor=tk.W,
            )
            label.pack(side=tk.LEFT, padx=(5, 2))

            value_label = tk.Label(
                row,
                text="0",
                font=CONVERSION_FONT,
                fg=CONVERSION_FG,
                bg=BG_COLOR,
                anchor=tk.W,
            )
            value_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self._conversion_labels[base_name] = value_label

    def _build_base_selector(self) -> None:
        """Create the DEC/HEX/OCT/BIN radio button selector."""
        self._base_frame = tk.Frame(self, bg=BG_COLOR)
        self._base_frame.pack(fill=tk.X, padx=5, pady=2)

        bases = ["DEC", "HEX", "OCT", "BIN"]
        for base_name in bases:
            rb = tk.Radiobutton(
                self._base_frame,
                text=base_name,
                variable=self._base_var,
                value=base_name,
                font=SMALL_BUTTON_FONT,
                fg=BTN_FG,
                bg=BG_COLOR,
                selectcolor=SPECIAL_BG,
                activebackground=BG_COLOR,
                activeforeground=BTN_FG,
                highlightthickness=0,
                bd=0,
                command=lambda b=base_name: self._on_base_selected(b),
            )
            rb.pack(side=tk.LEFT, expand=True, padx=5)

    def _build_word_size_selector(self) -> None:
        """Create the word size selector buttons."""
        self._word_frame = tk.Frame(self, bg=BG_COLOR)
        self._word_frame.pack(fill=tk.X, padx=5, pady=2)

        word_sizes = ["8", "16", "32", "64"]
        for ws in word_sizes:
            rb = tk.Radiobutton(
                self._word_frame,
                text=f"{ws}-bit",
                variable=self._word_var,
                value=ws,
                font=SMALL_BUTTON_FONT,
                fg=BTN_FG,
                bg=BG_COLOR,
                selectcolor=SPECIAL_BG,
                activebackground=BG_COLOR,
                activeforeground=BTN_FG,
                highlightthickness=0,
                bd=0,
                command=lambda w=ws: self._on_word_size_selected(w),
            )
            rb.pack(side=tk.LEFT, expand=True, padx=5)

    def _on_base_selected(self, base_name: str) -> None:
        """Handle base radio button selection."""
        self._on_button_click(f"BASE_{base_name}")

    def _on_word_size_selected(self, word_size: str) -> None:
        """Handle word size radio button selection."""
        self._on_button_click(f"WORD_{word_size}")

    def _build_button_grid(self) -> None:
        """Create the programmer mode button grid."""
        self._grid_frame = tk.Frame(self, bg=BG_COLOR)
        self._grid_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        total_cols = 9
        total_rows = 6
        for c in range(total_cols):
            self._grid_frame.columnconfigure(c, weight=1, minsize=50)
        for r in range(total_rows):
            self._grid_frame.rowconfigure(r, weight=1, minsize=40)

        btn_font = SMALL_BUTTON_FONT

        # ── Row 0: A B C D E F AND OR AC ────────────────────
        hex_digits = ["A", "B", "C", "D", "E", "F"]
        for i, hd in enumerate(hex_digits):
            self._create_button(
                self._grid_frame, hd, 0, i,
                bg=SPECIAL_BG, font=btn_font,
            )

        self._create_button(
            self._grid_frame, "AND", 0, 6,
            bg=SPECIAL_BG, font=btn_font,
        )
        self._create_button(
            self._grid_frame, "OR", 0, 7,
            bg=SPECIAL_BG, font=btn_font,
        )
        self._create_button(
            self._grid_frame, "AC", 0, 8,
            bg=SPECIAL_BG, font=btn_font,
        )

        # ── Row 1: NOT XOR LSH RSH % C +/- MOD / ───────────
        row1_left = [
            ("NOT", "NOT"),
            ("XOR", "XOR"),
            ("LSH", "LSH"),
            ("RSH", "RSH"),
            ("%", "%"),
        ]
        for i, (text, name) in enumerate(row1_left):
            self._create_button(
                self._grid_frame, text, 1, i,
                bg=SPECIAL_BG, font=btn_font, callback_name=name,
            )

        self._create_button(
            self._grid_frame, "C", 1, 5,
            bg=SPECIAL_BG, font=btn_font,
        )
        self._create_button(
            self._grid_frame, "\u00b1", 1, 6,
            bg=SPECIAL_BG, font=btn_font, callback_name="+/-",
        )
        self._create_button(
            self._grid_frame, "MOD", 1, 7,
            bg=SPECIAL_BG, font=btn_font,
        )
        self._create_button(
            self._grid_frame, "\u00f7", 1, 8,
            bg=OPERATOR_BG, fg=OPERATOR_FG,
            active_bg=OPERATOR_ACTIVE_BG,
            font=btn_font, callback_name="/",
        )

        # ── Row 2: [blank x5] 7 8 9 * ──────────────────────
        for col in range(5):
            spacer = tk.Frame(self._grid_frame, bg=BG_COLOR)
            spacer.grid(row=2, column=col, sticky="nsew", padx=1, pady=1)

        for j, digit in enumerate(["7", "8", "9"]):
            self._create_button(
                self._grid_frame, digit, 2, 5 + j, font=btn_font,
            )
        self._create_button(
            self._grid_frame, "\u00d7", 2, 8,
            bg=OPERATOR_BG, fg=OPERATOR_FG,
            active_bg=OPERATOR_ACTIVE_BG,
            font=btn_font, callback_name="*",
        )

        # ── Row 3: [blank x5] 4 5 6 - ──────────────────────
        for col in range(5):
            spacer = tk.Frame(self._grid_frame, bg=BG_COLOR)
            spacer.grid(row=3, column=col, sticky="nsew", padx=1, pady=1)

        for j, digit in enumerate(["4", "5", "6"]):
            self._create_button(
                self._grid_frame, digit, 3, 5 + j, font=btn_font,
            )
        self._create_button(
            self._grid_frame, "\u2212", 3, 8,
            bg=OPERATOR_BG, fg=OPERATOR_FG,
            active_bg=OPERATOR_ACTIVE_BG,
            font=btn_font, callback_name="-",
        )

        # ── Row 4: [blank x5] 1 2 3 + ──────────────────────
        for col in range(5):
            spacer = tk.Frame(self._grid_frame, bg=BG_COLOR)
            spacer.grid(row=4, column=col, sticky="nsew", padx=1, pady=1)

        for j, digit in enumerate(["1", "2", "3"]):
            self._create_button(
                self._grid_frame, digit, 4, 5 + j, font=btn_font,
            )
        self._create_button(
            self._grid_frame, "+", 4, 8,
            bg=OPERATOR_BG, fg=OPERATOR_FG,
            active_bg=OPERATOR_ACTIVE_BG, font=btn_font,
        )

        # ── Row 5: [blank x5] 0(x2) = backspace ────────────
        for col in range(5):
            spacer = tk.Frame(self._grid_frame, bg=BG_COLOR)
            spacer.grid(row=5, column=col, sticky="nsew", padx=1, pady=1)

        self._create_button(
            self._grid_frame, "0", 5, 5, colspan=2, font=btn_font,
        )
        self._create_button(
            self._grid_frame, "=", 5, 7,
            bg=EQUALS_BG, fg=OPERATOR_FG,
            active_bg=OPERATOR_ACTIVE_BG, font=btn_font,
        )
        self._create_button(
            self._grid_frame, "\u232b", 5, 8,
            bg=SPECIAL_BG, font=btn_font, callback_name="Backspace",
        )

    # ── Display update ───────────────────────────────────────────

    def update_display(self, state: DisplayState) -> None:
        """Update display including base conversions and word size.

        Args:
            state: The current display state from the logic layer.
        """
        super().update_display(state)

        # Update word size indicator
        self._word_label.config(
            text=f"Word: {state.word_size.value}"
        )
        self._word_var.set(str(state.word_size.value))

        # Update base selector
        self._base_var.set(state.number_base.name)

        # Update conversion panel
        conversion_map = {
            "HEX": state.hex_value,
            "DEC": state.dec_value,
            "OCT": state.oct_value,
            "BIN": state.bin_value,
        }
        for base_name, value in conversion_map.items():
            label = self._conversion_labels.get(base_name)
            if label is not None:
                fg = (
                    CONVERSION_ACTIVE_FG
                    if base_name == state.number_base.name
                    else CONVERSION_FG
                )
                label.config(text=value or "0", fg=fg)

        # Enable/disable buttons based on current base
        self._update_button_states(state.number_base)

    def _update_button_states(self, base: NumberBase) -> None:
        """Enable or disable digit and hex buttons for the current base.

        In BIN mode, only 0-1 are enabled.
        In OCT mode, only 0-7 are enabled.
        In DEC mode, only 0-9 are enabled.
        In HEX mode, all digits 0-9 and A-F are enabled.

        Args:
            base: The currently selected number base.
        """
        base_value = base.value

        # Handle digit buttons 0-9
        for digit_str in self._digit_buttons:
            digit_val = int(digit_str)
            btn = self._buttons.get(digit_str)
            if btn is not None:
                if digit_val < base_value:
                    btn.config(
                        state=tk.NORMAL,
                        bg=BTN_BG,
                        fg=BTN_FG,
                    )
                else:
                    btn.config(
                        state=tk.DISABLED,
                        bg=DISABLED_BG,
                        fg=DISABLED_FG,
                        disabledforeground=DISABLED_FG,
                    )

        # Handle hex buttons A-F
        hex_enabled = base == NumberBase.HEX
        for hd in self._hex_buttons:
            btn = self._buttons.get(hd)
            if btn is not None:
                if hex_enabled:
                    btn.config(
                        state=tk.NORMAL,
                        bg=SPECIAL_BG,
                        fg=BTN_FG,
                    )
                else:
                    btn.config(
                        state=tk.DISABLED,
                        bg=DISABLED_BG,
                        fg=DISABLED_FG,
                        disabledforeground=DISABLED_FG,
                    )
