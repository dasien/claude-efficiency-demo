"""Basic calculator view with standard arithmetic button grid."""

import tkinter as tk

from calculator.gui.base_view import (
    BG_COLOR,
    BTN_ACTIVE_BG,
    BTN_BG,
    BTN_FG,
    BUTTON_FONT,
    EQUALS_BG,
    OPERATOR_ACTIVE_BG,
    OPERATOR_BG,
    OPERATOR_FG,
    SPECIAL_BG,
    BaseView,
)


class BasicView(BaseView):
    """Basic calculator view with digits, operators, and memory buttons.

    Layout matches requirements section 3.6:
        Memory row: MC | MR | M+ | M- | MS
        Row 0:  C  | +/- |  %  |  /
        Row 1:  7  |  8  |  9  |  *
        Row 2:  4  |  5  |  6  |  -
        Row 3:  1  |  2  |  3  |  +
        Row 4:     0     |  .  |  =
    """

    def _build_button_grid(self) -> None:
        """Create the basic mode button grid."""
        self._grid_frame = tk.Frame(self, bg=BG_COLOR)
        self._grid_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        cols = 4
        rows = 5
        for c in range(cols):
            self._grid_frame.columnconfigure(c, weight=1, minsize=60)
        for r in range(rows):
            self._grid_frame.rowconfigure(r, weight=1, minsize=45)

        # Row 0: C, +/-, %, /
        self._create_button(
            self._grid_frame, "C", 0, 0,
            bg=SPECIAL_BG,
        )
        self._create_button(
            self._grid_frame, "\u00b1", 0, 1,
            bg=SPECIAL_BG, callback_name="+/-",
        )
        self._create_button(
            self._grid_frame, "%", 0, 2,
            bg=SPECIAL_BG,
        )
        self._create_button(
            self._grid_frame, "\u00f7", 0, 3,
            bg=OPERATOR_BG, fg=OPERATOR_FG,
            active_bg=OPERATOR_ACTIVE_BG, callback_name="/",
        )

        # Row 1: 7, 8, 9, *
        for i, digit in enumerate(["7", "8", "9"]):
            self._create_button(
                self._grid_frame, digit, 1, i,
            )
        self._create_button(
            self._grid_frame, "\u00d7", 1, 3,
            bg=OPERATOR_BG, fg=OPERATOR_FG,
            active_bg=OPERATOR_ACTIVE_BG, callback_name="*",
        )

        # Row 2: 4, 5, 6, -
        for i, digit in enumerate(["4", "5", "6"]):
            self._create_button(
                self._grid_frame, digit, 2, i,
            )
        self._create_button(
            self._grid_frame, "\u2212", 2, 3,
            bg=OPERATOR_BG, fg=OPERATOR_FG,
            active_bg=OPERATOR_ACTIVE_BG, callback_name="-",
        )

        # Row 3: 1, 2, 3, +
        for i, digit in enumerate(["1", "2", "3"]):
            self._create_button(
                self._grid_frame, digit, 3, i,
            )
        self._create_button(
            self._grid_frame, "+", 3, 3,
            bg=OPERATOR_BG, fg=OPERATOR_FG,
            active_bg=OPERATOR_ACTIVE_BG,
        )

        # Row 4: 0 (spanning 2 cols), ., =
        self._create_button(
            self._grid_frame, "0", 4, 0, colspan=2,
        )
        self._create_button(
            self._grid_frame, ".", 4, 2,
        )
        self._create_button(
            self._grid_frame, "=", 4, 3,
            bg=EQUALS_BG, fg=OPERATOR_FG,
            active_bg=OPERATOR_ACTIVE_BG,
        )
