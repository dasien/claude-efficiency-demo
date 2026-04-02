"""Abstract base view with shared display area and memory buttons."""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, Optional

from calculator.logic.base_logic import DisplayState


# ── Styling constants ────────────────────────────────────────────

BG_COLOR = "#1e1e1e"
DISPLAY_BG = "#1e1e1e"
EXPRESSION_FG = "#a0a0a0"
MAIN_DISPLAY_FG = "#ffffff"
ERROR_FG = "#ff4444"
MEMORY_INDICATOR_FG = "#888888"

BTN_BG = "#3c3c3c"
BTN_FG = "#ffffff"
BTN_ACTIVE_BG = "#505050"
OPERATOR_BG = "#ff9f0a"
OPERATOR_FG = "#ffffff"
OPERATOR_ACTIVE_BG = "#ffb840"
EQUALS_BG = "#ff9f0a"
MEMORY_BG = "#2a2a2a"
MEMORY_FG = "#a0a0a0"
SPECIAL_BG = "#505050"

FONT_FAMILY = "Helvetica"
MAIN_DISPLAY_FONT = (FONT_FAMILY, 36, "bold")
EXPRESSION_FONT = (FONT_FAMILY, 14)
BUTTON_FONT = (FONT_FAMILY, 16)
SMALL_BUTTON_FONT = (FONT_FAMILY, 13)
MEMORY_FONT = (FONT_FAMILY, 12)
INDICATOR_FONT = (FONT_FAMILY, 11)

BTN_PAD_X = 1
BTN_PAD_Y = 1
BTN_MIN_WIDTH = 60
BTN_MIN_HEIGHT = 45


class BaseView(ttk.Frame):
    """Abstract base view providing the common display area and memory row.

    Subclasses must implement _build_button_grid() to create
    mode-specific button layouts.
    """

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self._callbacks: Dict[str, Callable] = {}
        self._buttons: Dict[str, tk.Button] = {}

        self._build_display_area()
        self._build_memory_row()
        self._build_button_grid()

    # ── Display area ─────────────────────────────────────────────

    def _build_display_area(self) -> None:
        """Create the expression and main display labels."""
        self._display_frame = tk.Frame(self, bg=DISPLAY_BG)
        self._display_frame.pack(fill=tk.X, padx=5, pady=(5, 0))

        self._memory_indicator = tk.Label(
            self._display_frame,
            text="",
            font=INDICATOR_FONT,
            fg=MEMORY_INDICATOR_FG,
            bg=DISPLAY_BG,
            anchor=tk.W,
        )
        self._memory_indicator.pack(fill=tk.X, padx=5)

        self._expression_display = tk.Label(
            self._display_frame,
            text="",
            font=EXPRESSION_FONT,
            fg=EXPRESSION_FG,
            bg=DISPLAY_BG,
            anchor=tk.E,
        )
        self._expression_display.pack(fill=tk.X, padx=10)

        self._main_display = tk.Label(
            self._display_frame,
            text="0",
            font=MAIN_DISPLAY_FONT,
            fg=MAIN_DISPLAY_FG,
            bg=DISPLAY_BG,
            anchor=tk.E,
        )
        self._main_display.pack(fill=tk.X, padx=10, pady=(0, 5))

    # ── Memory button row ────────────────────────────────────────

    def _build_memory_row(self) -> None:
        """Create the shared MC, MR, M+, M-, MS button row."""
        self._memory_frame = tk.Frame(self, bg=BG_COLOR)
        self._memory_frame.pack(fill=tk.X, padx=5)

        memory_buttons = ["MC", "MR", "M+", "M-", "MS"]
        for name in memory_buttons:
            btn = tk.Button(
                self._memory_frame,
                text=name,
                font=MEMORY_FONT,
                fg=MEMORY_FG,
                bg=MEMORY_BG,
                activebackground=BTN_ACTIVE_BG,
                activeforeground=BTN_FG,
                bd=0,
                highlightthickness=0,
                command=lambda n=name: self._on_button_click(n),
            )
            btn.pack(side=tk.LEFT, expand=True, fill=tk.BOTH,
                     padx=BTN_PAD_X, pady=BTN_PAD_Y, ipady=2)
            self._buttons[name] = btn

    # ── Subclass hook ────────────────────────────────────────────

    def _build_button_grid(self) -> None:
        """Build the mode-specific button grid. Override in subclasses."""
        pass

    # ── Button helpers ───────────────────────────────────────────

    def _create_button(
        self,
        parent: tk.Widget,
        text: str,
        row: int,
        col: int,
        colspan: int = 1,
        rowspan: int = 1,
        bg: str = BTN_BG,
        fg: str = BTN_FG,
        active_bg: str = BTN_ACTIVE_BG,
        font: tuple = BUTTON_FONT,
        callback_name: Optional[str] = None,
    ) -> tk.Button:
        """Create a styled button and place it in a grid.

        Args:
            parent: The parent widget for the button.
            text: The button label text.
            row: Grid row index.
            col: Grid column index.
            colspan: Number of columns to span.
            rowspan: Number of rows to span.
            bg: Background color.
            fg: Foreground (text) color.
            active_bg: Background color when pressed.
            font: Font tuple for the button text.
            callback_name: The callback key name. Defaults to text.

        Returns:
            The created Button widget.
        """
        name = callback_name if callback_name is not None else text
        btn = tk.Button(
            parent,
            text=text,
            font=font,
            fg=fg,
            bg=bg,
            activebackground=active_bg,
            activeforeground=fg,
            bd=0,
            highlightthickness=0,
            command=lambda: self._on_button_click(name),
        )
        btn.grid(
            row=row,
            column=col,
            columnspan=colspan,
            rowspan=rowspan,
            sticky="nsew",
            padx=BTN_PAD_X,
            pady=BTN_PAD_Y,
        )
        self._buttons[name] = btn
        return btn

    def _on_button_click(self, name: str) -> None:
        """Dispatch a button press to the registered callback."""
        callback = self._callbacks.get(name)
        if callback is not None:
            callback()

    # ── Public interface ─────────────────────────────────────────

    def set_callbacks(self, callbacks: Dict[str, Callable]) -> None:
        """Register callbacks mapping button names to callables.

        Args:
            callbacks: A dict mapping button name strings to
                zero-argument callables.
        """
        self._callbacks = callbacks

    def update_display(self, state: DisplayState) -> None:
        """Update the display from a DisplayState snapshot.

        Args:
            state: The current display state from the logic layer.
        """
        fg = ERROR_FG if state.error else MAIN_DISPLAY_FG
        self._main_display.config(text=state.main_display, fg=fg)
        self._expression_display.config(text=state.expression_display)

        indicator_text = "M" if state.memory_indicator else ""
        self._memory_indicator.config(text=indicator_text)

    def get_button(self, name: str) -> Optional[tk.Button]:
        """Return a button widget by its callback name.

        Args:
            name: The callback name of the button.

        Returns:
            The Button widget, or None if not found.
        """
        return self._buttons.get(name)
