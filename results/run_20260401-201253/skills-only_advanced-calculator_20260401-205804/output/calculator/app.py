"""Calculator application controller — mode switching, event routing, keyboard support."""

import tkinter as tk
from typing import Optional

from calculator.logic.basic_logic import BasicLogic
from calculator.logic.scientific_logic import ScientificLogic
from calculator.logic.programmer_logic import ProgrammerLogic
from calculator.gui.basic_view import BasicView
from calculator.gui.scientific_view import ScientificView
from calculator.gui.programmer_view import ProgrammerView


MODE_BASIC = "Basic"
MODE_SCIENTIFIC = "Scientific"
MODE_PROGRAMMER = "Programmer"

WINDOW_SIZES = {
    MODE_BASIC: "320x480",
    MODE_SCIENTIFIC: "560x520",
    MODE_PROGRAMMER: "560x580",
}

# Button label to scientific function name mapping
SCIENTIFIC_FUNCTIONS = {
    "sin": "sin", "cos": "cos", "tan": "tan",
    "asin": "asin", "acos": "acos", "atan": "atan",
    "log": "log", "ln": "ln", "log\u2082": "log2",
    "x\u00b2": "x2", "x\u00b3": "x3",
    "10\u02e3": "10x", "e\u02e3": "ex",
    "\u221ax": "sqrt", "\u00b3\u221ax": "cbrt",
    "1/x": "recip", "n!": "fact", "|x|": "abs",
}


class CalculatorApp:
    """Main calculator application controller."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Calculator")
        self.root.configure(bg="#1C1C1E")
        self.root.resizable(False, False)

        self.mode: str = MODE_BASIC
        self.logic: Optional[object] = None
        self.view: Optional[object] = None

        # Shared state across modes
        self._memory: float = 0.0
        self._has_memory: bool = False

        self._build_menu()
        self._switch_mode(MODE_BASIC)
        self._bind_keyboard()

    def _build_menu(self) -> None:
        """Build the mode-switching menu bar."""
        menubar = tk.Menu(self.root)
        mode_menu = tk.Menu(menubar, tearoff=0)

        self._mode_var = tk.StringVar(value=self.mode)
        for mode in [MODE_BASIC, MODE_SCIENTIFIC, MODE_PROGRAMMER]:
            mode_menu.add_radiobutton(
                label=mode, variable=self._mode_var,
                command=lambda m=mode: self._switch_mode(m)
            )

        menubar.add_cascade(label="Mode", menu=mode_menu)
        self.root.config(menu=menubar)

    def _switch_mode(self, new_mode: str) -> None:
        """Switch calculator mode, preserving value and memory."""
        # Get current value before destroying
        current_value = 0.0
        if self.logic:
            current_value = self.logic.get_current_value()
            self._memory = self.logic.memory
            self._has_memory = self.logic.has_memory

        # Destroy current view
        if self.view:
            self.view.destroy()

        self.mode = new_mode
        self._mode_var.set(new_mode)
        self.root.geometry(WINDOW_SIZES[new_mode])

        # Create new logic and view
        if new_mode == MODE_BASIC:
            self.logic = BasicLogic()
            self.view = BasicView(self.root, self._on_button)
        elif new_mode == MODE_SCIENTIFIC:
            self.logic = ScientificLogic()
            self.view = ScientificView(self.root, self._on_button,
                                        angle_mode=getattr(self, '_angle_mode', 'DEG'))
            self.logic.angle_mode = getattr(self, '_angle_mode', 'DEG')
        elif new_mode == MODE_PROGRAMMER:
            self.logic = ProgrammerLogic()
            self.view = ProgrammerView(self.root, self._on_button)
            # Truncate to integer for programmer mode
            current_value = float(int(current_value))

        # Restore state
        self.logic.memory = self._memory
        self.logic.has_memory = self._has_memory
        if current_value != 0.0:
            self.logic.set_current_value(current_value)

        self._update_display()

    def _on_button(self, label: str) -> None:
        """Route button presses to appropriate logic methods."""
        try:
            self._dispatch_button(label)
        except Exception:
            # Safety net: never crash
            if self.logic:
                self.logic._set_error()
        self._update_display()

    def _dispatch_button(self, label: str) -> None:
        """Dispatch a button label to the correct logic method."""
        # Digits
        if label in "0123456789":
            self.logic.input_digit(label)
            return

        # Hex digits (programmer mode)
        if label.upper() in "ABCDEF" and len(label) == 1:
            self.logic.input_digit(label)
            return

        # Decimal point
        if label == ".":
            self.logic.input_decimal()
            return

        # Operators (basic arithmetic)
        if label in ("+", "-", "*", "/"):
            self.logic.input_operator(label)
            return

        # Equals
        if label == "=":
            self.logic.evaluate()
            return

        # Clear
        if label == "C":
            self.logic.clear_entry()
            return
        if label == "AC":
            self.logic.all_clear()
            return

        # Backspace
        if label in ("\u232b", "Backspace"):
            self.logic.backspace()
            return

        # Sign toggle
        if label == "+/-":
            self.logic.toggle_sign()
            return

        # Percent
        if label == "%":
            self.logic.percent()
            return

        # Memory operations
        if label == "MC":
            self.logic.memory_clear()
            return
        if label == "MR":
            self.logic.memory_recall()
            return
        if label == "M+":
            self.logic.memory_add()
            return
        if label == "M-":
            self.logic.memory_subtract()
            return
        if label == "MS":
            self.logic.memory_store()
            return

        # Scientific mode functions
        if self.mode == MODE_SCIENTIFIC and isinstance(self.logic, ScientificLogic):
            if label in SCIENTIFIC_FUNCTIONS:
                self.logic.apply_function(SCIENTIFIC_FUNCTIONS[label])
                return
            if label == "x\u207f":  # xⁿ
                self.logic.input_power()
                return
            if label == "\u03c0":  # π
                self.logic.insert_constant("pi")
                return
            if label == "e" and self.mode == MODE_SCIENTIFIC:
                self.logic.insert_constant("e")
                return
            if label == "DEG/RAD":
                self.logic.toggle_angle_mode()
                self._angle_mode = self.logic.angle_mode
                if hasattr(self.view, 'update_angle_mode'):
                    self.view.update_angle_mode(self.logic.angle_mode)
                return
            if label == "(":
                self.logic.open_paren()
                return
            if label == ")":
                self.logic.close_paren()
                return

        # Programmer mode operations
        if self.mode == MODE_PROGRAMMER and isinstance(self.logic, ProgrammerLogic):
            if label.startswith("BASE:"):
                base = int(label.split(":")[1])
                self.logic.set_base(base)
                if hasattr(self.view, 'update_digit_states'):
                    self.view.update_digit_states(base)
                    self.view.base_var.set(base)
                return
            if label.startswith("WORD:"):
                bits = int(label.split(":")[1])
                self.logic.set_word_size(bits)
                return
            if label in ("AND", "OR", "XOR", "LSH", "RSH", "MOD"):
                self.logic.input_operator(label)
                return
            if label == "NOT":
                self.logic.bitwise_not()
                return

    def _update_display(self) -> None:
        """Update the view's display from the logic state."""
        if not self.view or not self.logic:
            return

        self.view.update_display(
            self.logic.display_value,
            self.logic.expression_display,
            self.logic.has_memory
        )

        # Update programmer mode specific displays
        if self.mode == MODE_PROGRAMMER and isinstance(self.logic, ProgrammerLogic):
            if hasattr(self.view, 'update_base_panel'):
                self.view.update_base_panel(self.logic.get_all_bases())

        # Update scientific mode specific displays
        if self.mode == MODE_SCIENTIFIC and isinstance(self.logic, ScientificLogic):
            if hasattr(self.view, 'update_paren_depth'):
                self.view.update_paren_depth(self.logic.paren_depth)

    def _bind_keyboard(self) -> None:
        """Set up keyboard shortcuts."""
        # Digits
        for d in "0123456789":
            self.root.bind(d, lambda e, digit=d: self._on_button(digit))

        # Decimal
        self.root.bind(".", lambda e: self._on_button("."))

        # Operators
        self.root.bind("+", lambda e: self._on_button("+"))
        self.root.bind("-", lambda e: self._on_button("-"))
        self.root.bind("*", lambda e: self._on_button("*"))
        self.root.bind("/", lambda e: self._on_button("/"))

        # Equals
        self.root.bind("<Return>", lambda e: self._on_button("="))
        self.root.bind("<KP_Enter>", lambda e: self._on_button("="))

        # Clear
        self.root.bind("<Escape>", lambda e: self._on_button("AC"))

        # Backspace
        self.root.bind("<BackSpace>", lambda e: self._on_button("Backspace"))
        self.root.bind("<Delete>", lambda e: self._on_button("Backspace"))

        # Parentheses (scientific)
        self.root.bind("(", lambda e: self._on_button("("))
        self.root.bind(")", lambda e: self._on_button(")"))

        # Programmer mode keys
        for c in "abcdefABCDEF":
            self.root.bind(c, lambda e, ch=c: self._on_button(ch.upper()))
        self.root.bind("&", lambda e: self._on_button("AND"))
        self.root.bind("|", lambda e: self._on_button("OR"))
        self.root.bind("^", lambda e: self._on_button("XOR"))
        self.root.bind("~", lambda e: self._on_button("NOT"))
        self.root.bind("<", lambda e: self._on_button("LSH"))
        self.root.bind(">", lambda e: self._on_button("RSH"))
        self.root.bind("%", lambda e: self._on_button("%"))

        # Mode switching
        self.root.bind("<Control-Key-1>", lambda e: self._switch_mode(MODE_BASIC))
        self.root.bind("<Control-Key-2>", lambda e: self._switch_mode(MODE_SCIENTIFIC))
        self.root.bind("<Control-Key-3>", lambda e: self._switch_mode(MODE_PROGRAMMER))

    def run(self) -> None:
        """Start the application main loop."""
        self.root.mainloop()
