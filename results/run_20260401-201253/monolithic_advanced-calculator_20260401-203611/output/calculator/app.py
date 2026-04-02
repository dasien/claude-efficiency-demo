"""Main application controller: mode switching, event routing, keyboard."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from calculator.logic.base_logic import Memory
from calculator.logic.basic_logic import BasicCalculator
from calculator.logic.scientific_logic import ScientificCalculator
from calculator.logic.programmer_logic import ProgrammerCalculator
from calculator.gui.basic_view import BasicView
from calculator.gui.scientific_view import ScientificView
from calculator.gui.programmer_view import ProgrammerView

MODE_BASIC = "basic"
MODE_SCIENTIFIC = "scientific"
MODE_PROGRAMMER = "programmer"

WINDOW_SIZES = {
    MODE_BASIC: "320x420",
    MODE_SCIENTIFIC: "580x450",
    MODE_PROGRAMMER: "620x520",
}


class CalculatorApp(tk.Tk):
    """Main calculator application with mode switching."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Calculator")
        self.resizable(False, False)

        self._memory = Memory()
        self._mode = MODE_BASIC

        # Logic engines
        self._basic_calc = BasicCalculator()
        self._sci_calc = ScientificCalculator()
        self._prog_calc = ProgrammerCalculator()

        # Views (created lazily on first switch)
        self._container = ttk.Frame(self)
        self._container.pack(fill="both", expand=True)

        self._basic_view: BasicView | None = None
        self._sci_view: ScientificView | None = None
        self._prog_view: ProgrammerView | None = None
        self._current_view: ttk.Frame | None = None

        self._create_menu()
        self._bind_keyboard()
        self._switch_mode(MODE_BASIC)

    # --- Menu ---

    def _create_menu(self) -> None:
        """Create the mode-switching menu bar."""
        menubar = tk.Menu(self)
        mode_menu = tk.Menu(menubar, tearoff=0)
        mode_menu.add_radiobutton(
            label="Basic",
            command=lambda: self._switch_mode(MODE_BASIC),
        )
        mode_menu.add_radiobutton(
            label="Scientific",
            command=lambda: self._switch_mode(
                MODE_SCIENTIFIC
            ),
        )
        mode_menu.add_radiobutton(
            label="Programmer",
            command=lambda: self._switch_mode(
                MODE_PROGRAMMER
            ),
        )
        menubar.add_cascade(label="Mode", menu=mode_menu)
        self.config(menu=menubar)

    # --- Mode switching ---

    def _switch_mode(self, new_mode: str) -> None:
        """Switch to a different calculator mode."""
        # Get current value from active logic engine
        current_value = self._get_current_value()

        # Hide current view
        if self._current_view is not None:
            self._current_view.pack_forget()

        old_mode = self._mode
        self._mode = new_mode

        # Transfer value to new mode's logic engine
        self._set_value_for_mode(new_mode, current_value)

        # Show appropriate view
        if new_mode == MODE_BASIC:
            if self._basic_view is None:
                self._basic_view = BasicView(
                    self._container,
                    on_button=self._on_button,
                )
            self._current_view = self._basic_view
        elif new_mode == MODE_SCIENTIFIC:
            if self._sci_view is None:
                self._sci_view = ScientificView(
                    self._container,
                    on_button=self._on_button,
                )
            self._current_view = self._sci_view
        elif new_mode == MODE_PROGRAMMER:
            if self._prog_view is None:
                self._prog_view = ProgrammerView(
                    self._container,
                    on_button=self._on_button,
                )
            self._current_view = self._prog_view

        self._current_view.pack(fill="both", expand=True)
        self.geometry(WINDOW_SIZES[new_mode])
        self._update_display()

    def _get_current_value(self) -> float:
        """Get the numeric value from the active logic engine."""
        if self._mode == MODE_BASIC:
            return self._basic_calc.get_value()
        elif self._mode == MODE_SCIENTIFIC:
            return self._sci_calc.get_value()
        elif self._mode == MODE_PROGRAMMER:
            return float(self._prog_calc.get_value())
        return 0.0

    def _set_value_for_mode(
        self, mode: str, value: float
    ) -> None:
        """Set value on the target mode's logic engine."""
        if mode == MODE_BASIC:
            self._basic_calc.set_value(value)
        elif mode == MODE_SCIENTIFIC:
            self._sci_calc.set_value(value)
        elif mode == MODE_PROGRAMMER:
            self._prog_calc.set_value(int(value))

    # --- Button dispatch ---

    def _on_button(self, action: str) -> None:
        """Central button dispatcher."""
        try:
            if self._mode == MODE_PROGRAMMER:
                self._handle_programmer_action(action)
            elif self._mode == MODE_SCIENTIFIC:
                self._handle_scientific_action(action)
            else:
                self._handle_basic_action(action)
        except Exception:
            pass  # Never crash (RC-3)
        self._update_display()

    def _handle_basic_action(self, action: str) -> None:
        """Route actions to BasicCalculator."""
        calc = self._basic_calc
        if action.isdigit():
            calc.input_digit(action)
        elif action == ".":
            calc.input_decimal()
        elif action in ("+", "-", "*", "/"):
            calc.input_operator(action)
        elif action == "=":
            calc.input_equals()
        elif action == "C":
            calc.input_clear()
        elif action == "AC":
            calc.input_all_clear()
        elif action == "BACKSPACE":
            calc.input_backspace()
        elif action == "%":
            calc.input_percent()
        elif action == "+/-":
            calc.input_negate()
        else:
            self._handle_memory_action(action, calc)

    def _handle_scientific_action(self, action: str) -> None:
        """Route actions to ScientificCalculator."""
        calc = self._sci_calc
        # Scientific-specific actions
        sci_actions = {
            "sin": calc.apply_sin,
            "cos": calc.apply_cos,
            "tan": calc.apply_tan,
            "asin": calc.apply_asin,
            "acos": calc.apply_acos,
            "atan": calc.apply_atan,
            "log": calc.apply_log,
            "ln": calc.apply_ln,
            "log₂": calc.apply_log2,
            "x²": calc.apply_square,
            "x³": calc.apply_cube,
            "xⁿ": calc.input_power,
            "10ˣ": calc.apply_ten_power,
            "eˣ": calc.apply_e_power,
            "√x": calc.apply_sqrt,
            "³√x": calc.apply_cbrt,
            "1/x": calc.apply_reciprocal,
            "π": calc.input_pi,
            "e": calc.input_e,
            "n!": calc.apply_factorial,
            "|x|": calc.apply_abs,
            "(": calc.input_open_paren,
            ")": calc.input_close_paren,
            "DEG/RAD": calc.toggle_angle_mode,
        }
        if action in sci_actions:
            sci_actions[action]()
        elif action.isdigit():
            calc.input_digit(action)
        elif action == ".":
            calc.input_decimal()
        elif action in ("+", "-", "*", "/"):
            calc.input_operator(action)
        elif action == "=":
            calc.input_equals()
        elif action == "C":
            calc.input_clear()
        elif action == "AC":
            calc.input_all_clear()
        elif action == "BACKSPACE":
            calc.input_backspace()
        elif action == "%":
            calc.input_percent()
        elif action == "+/-":
            calc.input_negate()
        else:
            self._handle_memory_action(action, calc)

    def _handle_programmer_action(self, action: str) -> None:
        """Route actions to ProgrammerCalculator."""
        calc = self._prog_calc
        if action.startswith("BASE_"):
            calc.set_base(action[5:])
        elif action.startswith("WORD_"):
            calc.set_word_size(int(action[5:]))
        elif action in "0123456789ABCDEF" and len(action) == 1:
            calc.input_digit(action)
        elif action in ("+", "-", "*", "/"):
            calc.input_operator(action)
        elif action == "=":
            calc.input_equals()
        elif action == "C":
            calc.input_clear()
        elif action == "AC":
            calc.input_all_clear()
        elif action == "BACKSPACE":
            calc.input_backspace()
        elif action == "+/-":
            calc.input_negate()
        elif action == "MOD":
            calc.input_operator("%")
        elif action == "AND":
            calc.input_operator("AND")
        elif action == "OR":
            calc.input_operator("OR")
        elif action == "XOR":
            calc.input_operator("XOR")
        elif action == "NOT":
            calc.apply_not()
        elif action == "LSH":
            calc.input_operator("LSH")
        elif action == "RSH":
            calc.input_operator("RSH")
        else:
            self._handle_memory_action_prog(action)

    def _handle_memory_action(
        self,
        action: str,
        calc: BasicCalculator,
    ) -> None:
        """Handle memory button actions for basic/scientific modes."""
        if action == "MC":
            self._memory.clear()
        elif action == "MR":
            val = self._memory.recall()
            calc.set_value(val)
        elif action == "M+":
            self._memory.add(calc.get_value())
        elif action == "M-":
            self._memory.subtract(calc.get_value())
        elif action == "MS":
            self._memory.store(calc.get_value())

    def _handle_memory_action_prog(self, action: str) -> None:
        """Handle memory button actions for programmer mode."""
        calc = self._prog_calc
        if action == "MC":
            self._memory.clear()
        elif action == "MR":
            val = self._memory.recall()
            calc.set_value(int(val))
        elif action == "M+":
            self._memory.add(float(calc.get_value()))
        elif action == "M-":
            self._memory.subtract(float(calc.get_value()))
        elif action == "MS":
            self._memory.store(float(calc.get_value()))

    # --- Display update ---

    def _update_display(self) -> None:
        """Update the current view's display from the active engine."""
        if self._mode == MODE_BASIC and self._basic_view:
            calc = self._basic_calc
            self._basic_view.update_display(
                calc.get_display(), calc.get_expression()
            )
            self._basic_view.memory_row.set_memory_indicator(
                self._memory.has_value
            )
        elif self._mode == MODE_SCIENTIFIC and self._sci_view:
            calc = self._sci_calc
            self._sci_view.update_display(
                calc.get_display(), calc.get_expression()
            )
            self._sci_view.set_angle_mode(
                calc.get_angle_mode()
            )
            self._sci_view.set_paren_depth(
                calc.get_paren_depth()
            )
            self._sci_view.memory_row.set_memory_indicator(
                self._memory.has_value
            )
        elif self._mode == MODE_PROGRAMMER and self._prog_view:
            calc = self._prog_calc
            self._prog_view.update_display(
                calc.get_display(), calc.get_expression()
            )
            self._prog_view.set_base_panel(
                calc.get_all_bases()
            )
            self._prog_view.set_word_size_display(
                calc.get_word_size()
            )
            self._prog_view.set_base_mode(calc.get_base())

    # --- Keyboard bindings ---

    def _bind_keyboard(self) -> None:
        """Bind keyboard shortcuts."""
        # Digits
        for d in "0123456789":
            self.bind(
                d,
                lambda e, digit=d: self._on_button(digit),
            )
        # Operators
        self.bind(
            "+", lambda e: self._on_button("+")
        )
        self.bind(
            "-", lambda e: self._on_button("-")
        )
        self.bind(
            "*", lambda e: self._on_button("*")
        )
        self.bind(
            "/", lambda e: self._on_button("/")
        )
        # Decimal
        self.bind(
            ".", lambda e: self._on_button(".")
        )
        # Enter/Return = equals
        self.bind(
            "<Return>", lambda e: self._on_button("=")
        )
        self.bind(
            "<KP_Enter>", lambda e: self._on_button("=")
        )
        # Escape = All Clear
        self.bind(
            "<Escape>", lambda e: self._on_button("AC")
        )
        # Backspace
        self.bind(
            "<BackSpace>",
            lambda e: self._on_button("BACKSPACE"),
        )
        self.bind(
            "<Delete>",
            lambda e: self._on_button("BACKSPACE"),
        )
        # Parentheses (scientific only, but harmless in other)
        self.bind(
            "(", lambda e: self._on_button("(")
        )
        self.bind(
            ")", lambda e: self._on_button(")")
        )
        # Hex digits
        for h in "abcdef":
            self.bind(
                h,
                lambda e, c=h.upper(): self._on_button(c),
            )
            self.bind(
                h.upper(),
                lambda e, c=h.upper(): self._on_button(c),
            )
        # Programmer bitwise shortcuts
        self.bind(
            "&", lambda e: self._on_button("AND")
        )
        self.bind(
            "|", lambda e: self._on_button("OR")
        )
        self.bind(
            "^", lambda e: self._on_button("XOR")
        )
        self.bind(
            "~", lambda e: self._on_button("NOT")
        )
        self.bind(
            "<", lambda e: self._on_button("LSH")
        )
        self.bind(
            ">", lambda e: self._on_button("RSH")
        )
        self.bind(
            "%", lambda e: self._on_button("MOD")
        )
        # Mode switching: Ctrl+1/2/3
        self.bind(
            "<Control-Key-1>",
            lambda e: self._switch_mode(MODE_BASIC),
        )
        self.bind(
            "<Control-Key-2>",
            lambda e: self._switch_mode(MODE_SCIENTIFIC),
        )
        self.bind(
            "<Control-Key-3>",
            lambda e: self._switch_mode(MODE_PROGRAMMER),
        )
