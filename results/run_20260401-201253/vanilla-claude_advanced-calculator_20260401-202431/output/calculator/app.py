"""Main application controller coordinating views and logic."""

import tkinter as tk
from typing import Optional

from .logic.basic_logic import BasicCalculator
from .logic.scientific_logic import ScientificCalculator
from .logic.programmer_logic import ProgrammerCalculator
from .gui.basic_view import BasicView
from .gui.scientific_view import ScientificView
from .gui.programmer_view import ProgrammerView


class CalculatorApp:
    """Main calculator application controller."""

    MODES = ("Basic", "Scientific", "Programmer")
    MODE_SIZES = {
        "Basic": (320, 500),
        "Scientific": (580, 540),
        "Programmer": (580, 600),
    }

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the calculator application."""
        self.root = root
        self.root.title("Calculator")
        self.root.configure(bg="#1C1C1E")
        self.root.resizable(True, True)

        self._current_mode: str = "Basic"

        # Initialize logic engines
        self.basic_logic = BasicCalculator()
        self.scientific_logic = ScientificCalculator()
        self.programmer_logic = ProgrammerCalculator()

        # Build menu
        self._build_menu()

        # Initialize views
        self.basic_view = BasicView(self.root, self.handle_input)
        self.scientific_view = ScientificView(self.root, self.handle_input)
        self.programmer_view = ProgrammerView(self.root, self.handle_input)

        # Bind keyboard
        self._bind_keyboard()

        # Show initial mode
        self.switch_mode("Basic")

    def _build_menu(self) -> None:
        """Build the mode-switching menu bar."""
        menubar = tk.Menu(self.root)
        mode_menu = tk.Menu(menubar, tearoff=0)
        for mode in self.MODES:
            mode_menu.add_radiobutton(
                label=mode,
                command=lambda m=mode: self.switch_mode(m),
            )
        menubar.add_cascade(label="Mode", menu=mode_menu)
        self.root.config(menu=menubar)

    def _bind_keyboard(self) -> None:
        """Bind keyboard shortcuts."""
        root = self.root

        # Digits 0-9
        for d in range(10):
            root.bind(str(d), lambda e, digit=str(d): self.handle_input(f"digit_{digit}"))

        # Operators
        root.bind("+", lambda e: self.handle_input("op_+"))
        root.bind("-", lambda e: self.handle_input("op_-"))
        root.bind("*", lambda e: self.handle_input("op_*"))
        root.bind("/", lambda e: self.handle_input("op_/"))

        # Decimal
        root.bind(".", lambda e: self.handle_input("decimal"))

        # Enter/Return = evaluate
        root.bind("<Return>", lambda e: self.handle_input("evaluate"))
        root.bind("<KP_Enter>", lambda e: self.handle_input("evaluate"))

        # Escape = all clear
        root.bind("<Escape>", lambda e: self.handle_input("all_clear"))

        # Backspace
        root.bind("<BackSpace>", lambda e: self.handle_input("backspace"))
        root.bind("<Delete>", lambda e: self.handle_input("backspace"))

        # Parentheses (scientific mode)
        root.bind("(", lambda e: self.handle_input("open_paren"))
        root.bind(")", lambda e: self.handle_input("close_paren"))

        # Programmer mode hex digits
        for c in "abcdef":
            root.bind(c, lambda e, ch=c.upper(): self.handle_input(f"digit_{ch}"))
            root.bind(c.upper(), lambda e, ch=c.upper(): self.handle_input(f"digit_{ch}"))

        # Programmer mode bitwise
        root.bind("&", lambda e: self.handle_input("op_AND"))
        root.bind("|", lambda e: self.handle_input("op_OR"))
        root.bind("^", lambda e: self.handle_input("op_XOR"))
        root.bind("~", lambda e: self.handle_input("bitwise_not"))
        root.bind("<", lambda e: self.handle_input("op_LSH"))
        root.bind(">", lambda e: self.handle_input("op_RSH"))
        root.bind("%", lambda e: self._handle_percent_or_mod())

        # Mode switching: Ctrl+1/2/3
        root.bind("<Control-Key-1>", lambda e: self.switch_mode("Basic"))
        root.bind("<Control-Key-2>", lambda e: self.switch_mode("Scientific"))
        root.bind("<Control-Key-3>", lambda e: self.switch_mode("Programmer"))

    def _handle_percent_or_mod(self) -> None:
        """Handle % key - percent in basic/scientific, modulo in programmer."""
        if self._current_mode == "Programmer":
            self.handle_input("op_%")
        else:
            self.handle_input("percent")

    @property
    def _active_logic(self):
        """Return the logic engine for the current mode."""
        if self._current_mode == "Basic":
            return self.basic_logic
        elif self._current_mode == "Scientific":
            return self.scientific_logic
        return self.programmer_logic

    @property
    def _active_view(self):
        """Return the view for the current mode."""
        if self._current_mode == "Basic":
            return self.basic_view
        elif self._current_mode == "Scientific":
            return self.scientific_view
        return self.programmer_view

    def switch_mode(self, mode: str) -> None:
        """Switch calculator mode, preserving value and memory."""
        if mode not in self.MODES:
            return

        # Get current value before switching
        old_mode = self._current_mode
        if old_mode == "Programmer":
            current_value = float(self.programmer_logic.get_current_int_value())
            mem = self.programmer_logic.memory
            has_mem = self.programmer_logic.has_memory
        else:
            logic = self.basic_logic if old_mode == "Basic" else self.scientific_logic
            current_value = logic.get_current_value()
            mem = logic.memory
            has_mem = logic.has_memory

        # Hide current view
        self.basic_view.hide()
        self.scientific_view.hide()
        self.programmer_view.hide()

        self._current_mode = mode

        # Transfer memory to new logic engine
        if mode == "Programmer":
            self.programmer_logic.memory = mem
            self.programmer_logic.has_memory = has_mem
            # Truncate to integer
            int_val = int(current_value)
            self.programmer_logic.set_value(int_val)
        else:
            logic = self.basic_logic if mode == "Basic" else self.scientific_logic
            logic.memory = mem
            logic.has_memory = has_mem
            if old_mode == "Programmer":
                logic.set_value(current_value)
            else:
                logic.set_value(current_value)

        # Show new view and resize
        w, h = self.MODE_SIZES[mode]
        self.root.geometry(f"{w}x{h}")
        self._active_view.show()
        self._update_display()

    def handle_input(self, action: str) -> None:
        """Route user input to the appropriate logic engine."""
        logic = self._active_logic

        if self._current_mode == "Programmer":
            self._handle_programmer_input(action)
        elif self._current_mode == "Scientific":
            self._handle_scientific_input(action)
        else:
            self._handle_basic_input(action)

        self._update_display()

    def _handle_basic_input(self, action: str) -> None:
        """Handle input for basic mode."""
        logic = self.basic_logic
        if action.startswith("digit_"):
            logic.input_digit(action[6:])
        elif action == "decimal":
            logic.input_decimal()
        elif action.startswith("op_"):
            logic.input_operator(action[3:])
        elif action == "evaluate":
            logic.evaluate()
        elif action == "clear_entry":
            logic.clear_entry()
        elif action == "all_clear":
            logic.all_clear()
        elif action == "backspace":
            logic.backspace()
        elif action == "toggle_sign":
            logic.toggle_sign()
        elif action == "percent":
            logic.percent()
        elif action == "memory_clear":
            logic.memory_clear()
        elif action == "memory_recall":
            logic.memory_recall()
        elif action == "memory_add":
            logic.memory_add()
        elif action == "memory_subtract":
            logic.memory_subtract()
        elif action == "memory_store":
            logic.memory_store()

    def _handle_scientific_input(self, action: str) -> None:
        """Handle input for scientific mode."""
        logic = self.scientific_logic

        # Basic actions
        if action.startswith("digit_"):
            logic.input_digit(action[6:])
        elif action == "decimal":
            logic.input_decimal()
        elif action.startswith("op_"):
            logic.input_operator(action[3:])
        elif action == "evaluate":
            logic.evaluate()
        elif action == "clear_entry":
            logic.clear_entry()
        elif action == "all_clear":
            logic.all_clear()
        elif action == "backspace":
            logic.backspace()
        elif action == "toggle_sign":
            logic.toggle_sign()
        elif action == "percent":
            logic.percent()
        # Memory
        elif action == "memory_clear":
            logic.memory_clear()
        elif action == "memory_recall":
            logic.memory_recall()
        elif action == "memory_add":
            logic.memory_add()
        elif action == "memory_subtract":
            logic.memory_subtract()
        elif action == "memory_store":
            logic.memory_store()
        # Scientific functions
        elif action == "sin":
            logic.sin()
        elif action == "cos":
            logic.cos()
        elif action == "tan":
            logic.tan()
        elif action == "asin":
            logic.asin()
        elif action == "acos":
            logic.acos()
        elif action == "atan":
            logic.atan()
        elif action == "log":
            logic.log()
        elif action == "ln":
            logic.ln()
        elif action == "log2":
            logic.log2()
        elif action == "square":
            logic.square()
        elif action == "cube":
            logic.cube()
        elif action == "power":
            logic.power()
        elif action == "ten_power":
            logic.ten_power()
        elif action == "e_power":
            logic.e_power()
        elif action == "sqrt":
            logic.sqrt()
        elif action == "cbrt":
            logic.cbrt()
        elif action == "reciprocal":
            logic.reciprocal()
        elif action == "factorial":
            logic.factorial()
        elif action == "absolute":
            logic.absolute()
        elif action == "insert_pi":
            logic.insert_pi()
        elif action == "insert_e":
            logic.insert_e()
        elif action == "open_paren":
            logic.open_paren()
        elif action == "close_paren":
            logic.close_paren()
        elif action == "toggle_angle":
            logic.toggle_angle_mode()

    def _handle_programmer_input(self, action: str) -> None:
        """Handle input for programmer mode."""
        logic = self.programmer_logic

        if action.startswith("digit_"):
            logic.input_digit(action[6:])
        elif action.startswith("op_"):
            logic.input_operator(action[3:])
        elif action == "evaluate":
            logic.evaluate()
        elif action == "clear_entry":
            logic.clear_entry()
        elif action == "all_clear":
            logic.all_clear()
        elif action == "backspace":
            logic.backspace()
        elif action == "toggle_sign":
            logic.toggle_sign()
        elif action == "bitwise_not":
            logic.bitwise_not()
        elif action.startswith("base_"):
            logic.set_base(action[5:])
        elif action == "cycle_word_size":
            sizes = [8, 16, 32, 64]
            current = logic.word_size
            idx = sizes.index(current) if current in sizes else 3
            logic.set_word_size(sizes[(idx + 1) % len(sizes)])
        # Memory
        elif action == "memory_clear":
            logic.memory_clear()
        elif action == "memory_recall":
            logic.memory_recall()
        elif action == "memory_add":
            logic.memory_add()
        elif action == "memory_subtract":
            logic.memory_subtract()
        elif action == "memory_store":
            logic.memory_store()

    def _update_display(self) -> None:
        """Update the active view's display from the active logic state."""
        view = self._active_view
        logic = self._active_logic

        display = logic.get_display_value()
        expression = logic.get_expression()
        view.update_display(display, expression)
        view.update_memory_indicator(logic.has_memory)

        if self._current_mode == "Scientific":
            self.scientific_view.update_angle_mode(self.scientific_logic.angle_mode)
        elif self._current_mode == "Programmer":
            self.programmer_view.update_base_conversions(
                self.programmer_logic.get_base_conversions()
            )
            self.programmer_view.update_digit_states(self.programmer_logic.base)
            self.programmer_view.update_base_selector(self.programmer_logic.base)
            self.programmer_view.update_word_size(self.programmer_logic.word_size)
