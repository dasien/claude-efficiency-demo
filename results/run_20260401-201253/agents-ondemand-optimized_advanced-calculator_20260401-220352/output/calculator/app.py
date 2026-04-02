"""Main application controller for the calculator.

Manages mode switching, event routing between view and logic layers,
keyboard bindings, and display updates. Follows MVC pattern.
"""

from __future__ import annotations

import tkinter as tk

from calculator.gui.basic_view import BasicView
from calculator.gui.programmer_view import ProgrammerView
from calculator.gui.scientific_view import ScientificView
from calculator.logic.base_logic import BaseCalculator, CalculatorError
from calculator.logic.basic_logic import BasicCalculator
from calculator.logic.programmer_logic import ProgrammerCalculator
from calculator.logic.scientific_logic import ScientificCalculator


class App(tk.Tk):
    """Main application controller.

    Manages mode switching and event routing between the GUI views
    and the logic models. Each mode has its own model and view instance.
    """

    MODE_BASIC = "basic"
    MODE_SCIENTIFIC = "scientific"
    MODE_PROGRAMMER = "programmer"

    SIZES = {
        "basic": "320x480",
        "scientific": "580x480",
        "programmer": "580x560",
    }

    def __init__(self) -> None:
        super().__init__()
        self.title("Calculator")
        self.configure(bg="#2D2D2D")
        self.resizable(True, True)

        # Models
        self.basic_calc = BasicCalculator()
        self.scientific_calc = ScientificCalculator()
        self.programmer_calc = ProgrammerCalculator()

        self.active_calc: BaseCalculator = self.basic_calc
        self.current_mode: str = self.MODE_BASIC

        # Views (created lazily, only one visible at a time)
        self._view_container = tk.Frame(self, bg="#2D2D2D")
        self._view_container.pack(fill="both", expand=True)

        self.basic_view: BasicView | None = None
        self.scientific_view: ScientificView | None = None
        self.programmer_view: ProgrammerView | None = None
        self.active_view: object | None = None

        self._create_menu()
        self._bind_keyboard()
        self._switch_mode(self.MODE_BASIC)

    # --- Menu ---

    def _create_menu(self) -> None:
        """Create the menu bar with mode selection."""
        menubar = tk.Menu(self)
        self.configure(menu=menubar)

        mode_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Mode", menu=mode_menu)

        self._mode_var = tk.StringVar(value=self.MODE_BASIC)

        mode_menu.add_radiobutton(
            label="Basic",
            variable=self._mode_var,
            value=self.MODE_BASIC,
            command=lambda: self._switch_mode(self.MODE_BASIC),
            accelerator="Ctrl+1",
        )
        mode_menu.add_radiobutton(
            label="Scientific",
            variable=self._mode_var,
            value=self.MODE_SCIENTIFIC,
            command=lambda: self._switch_mode(self.MODE_SCIENTIFIC),
            accelerator="Ctrl+2",
        )
        mode_menu.add_radiobutton(
            label="Programmer",
            variable=self._mode_var,
            value=self.MODE_PROGRAMMER,
            command=lambda: self._switch_mode(self.MODE_PROGRAMMER),
            accelerator="Ctrl+3",
        )

    # --- Mode switching ---

    def _switch_mode(self, mode: str) -> None:
        """Switch between calculator modes.

        Preserves the current value and memory when switching.
        Truncates to integer when entering programmer mode.

        Args:
            mode: Target mode ('basic', 'scientific', 'programmer').
        """
        # Get current value from active model
        try:
            current_value = self.active_calc.get_current_value()
        except Exception:
            current_value = 0.0

        old_memory = self.active_calc.memory
        old_has_memory = self.active_calc.has_memory

        # Hide current view
        if self.active_view is not None:
            self.active_view.pack_forget()

        # Select new model and transfer state
        if mode == self.MODE_BASIC:
            self.active_calc = self.basic_calc
            self.active_calc.all_clear()
            if self.current_mode == self.MODE_PROGRAMMER:
                current_value = float(int(current_value))
            self.active_calc.current_input = (
                self.active_calc.format_number(current_value)
            )
            self.active_calc.last_result = current_value
        elif mode == self.MODE_SCIENTIFIC:
            self.active_calc = self.scientific_calc
            self.active_calc.all_clear()
            if self.current_mode == self.MODE_PROGRAMMER:
                current_value = float(int(current_value))
            self.active_calc.current_input = (
                self.active_calc.format_number(current_value)
            )
            self.active_calc.last_result = current_value
        elif mode == self.MODE_PROGRAMMER:
            self.active_calc = self.programmer_calc
            self.active_calc.all_clear()
            int_value = int(current_value)
            self.programmer_calc.value = (
                self.programmer_calc._apply_word_size(int_value)
            )
            self.active_calc.current_input = (
                self.programmer_calc.format_in_base(
                    self.programmer_calc.value,
                    self.programmer_calc.base,
                )
            )
            self.active_calc.last_result = float(
                self.programmer_calc.value
            )

        # Transfer memory
        self.active_calc.memory = old_memory
        self.active_calc.has_memory = old_has_memory

        # Create or show view
        if mode == self.MODE_BASIC:
            if self.basic_view is None:
                self.basic_view = BasicView(
                    self._view_container, self
                )
            self.active_view = self.basic_view
        elif mode == self.MODE_SCIENTIFIC:
            if self.scientific_view is None:
                self.scientific_view = ScientificView(
                    self._view_container, self
                )
            self.active_view = self.scientific_view
        elif mode == self.MODE_PROGRAMMER:
            if self.programmer_view is None:
                self.programmer_view = ProgrammerView(
                    self._view_container, self
                )
            self.active_view = self.programmer_view

        self.active_view.pack(fill="both", expand=True)

        # Update mode tracking and menu
        self.current_mode = mode
        self._mode_var.set(mode)

        # Resize window
        self.geometry(self.SIZES.get(mode, self.SIZES["basic"]))

        # Update display
        self._update_display()

    # --- Event handlers ---

    def on_digit(self, digit: str) -> None:
        """Handle digit button press.

        Args:
            digit: The digit character.
        """
        if self.active_calc.error_state:
            self.active_calc.clear_error()

        # If we just evaluated, start fresh
        if (
            self.active_calc.last_result is not None
            and not self.active_calc.current_input
            and not self.active_calc.expression
        ):
            self.active_calc.last_result = None

        self.active_calc.append_digit(digit)
        self._update_display()

    def on_operator(self, op: str) -> None:
        """Handle operator button press.

        Args:
            op: The operator string.
        """
        if self.active_calc.error_state:
            return

        if self.current_mode == self.MODE_PROGRAMMER:
            self.programmer_calc.add_operator(op)
        elif self.current_mode == self.MODE_SCIENTIFIC:
            self.scientific_calc.add_operator(op)
        else:
            self.basic_calc.add_operator(op)
        self._update_display()

    def on_equals(self) -> None:
        """Handle equals button press."""
        try:
            if self.current_mode == self.MODE_PROGRAMMER:
                result = self.programmer_calc.evaluate()
            elif self.current_mode == self.MODE_SCIENTIFIC:
                result = self.scientific_calc.evaluate()
            else:
                result = self.basic_calc.evaluate()
            self._update_display()
        except CalculatorError:
            self._handle_error()

    def on_clear(self) -> None:
        """Handle C (clear entry) button press."""
        self.active_calc.clear_entry()
        self._update_display()

    def on_all_clear(self) -> None:
        """Handle AC (all clear) button press."""
        self.active_calc.all_clear()
        if self.current_mode == self.MODE_PROGRAMMER:
            self.programmer_calc.value = 0
        self._update_display()

    def on_backspace(self) -> None:
        """Handle backspace button press."""
        self.active_calc.backspace()
        self._update_display()

    def on_decimal(self) -> None:
        """Handle decimal point button press."""
        if self.current_mode == self.MODE_PROGRAMMER:
            return
        self.active_calc.append_decimal()
        self._update_display()

    def on_toggle_sign(self) -> None:
        """Handle +/- (sign toggle) button press."""
        if self.active_calc.error_state:
            return

        current = self.active_calc.get_current_value()
        result = self.active_calc.toggle_sign(current)

        if self.current_mode == self.MODE_PROGRAMMER:
            int_result = int(result)
            self.programmer_calc.value = int_result
            self.active_calc.current_input = (
                self.programmer_calc.format_in_base(
                    int_result, self.programmer_calc.base
                )
            )
        else:
            self.active_calc.current_input = (
                self.active_calc.format_number(result)
            )
        self.active_calc.last_result = result
        self._update_display()

    def on_percentage(self) -> None:
        """Handle % (percentage) button press."""
        if self.active_calc.error_state:
            return
        current = self.active_calc.get_current_value()
        result = self.active_calc.percentage(current)
        self.active_calc.current_input = (
            self.active_calc.format_number(result)
        )
        self.active_calc.last_result = result
        self._update_display()

    def on_memory(self, action: str) -> None:
        """Handle memory button press.

        Args:
            action: Memory operation ('MC', 'MR', 'M+', 'M-', 'MS').
        """
        current = self.active_calc.get_current_value()

        if action == "MC":
            self.active_calc.memory_clear()
        elif action == "MR":
            val = self.active_calc.memory_recall()
            if self.current_mode == self.MODE_PROGRAMMER:
                int_val = int(val)
                self.programmer_calc.value = int_val
                self.active_calc.current_input = (
                    self.programmer_calc.format_in_base(
                        int_val, self.programmer_calc.base
                    )
                )
            else:
                self.active_calc.current_input = (
                    self.active_calc.format_number(val)
                )
            self.active_calc.last_result = val
        elif action == "M+":
            self.active_calc.memory_add(current)
        elif action == "M-":
            self.active_calc.memory_subtract(current)
        elif action == "MS":
            self.active_calc.memory_store(current)

        self._update_display()

    def on_scientific(self, func: str) -> None:
        """Handle scientific function button press.

        Args:
            func: Function name (e.g., 'sin', 'sqrt', 'pi').
        """
        if self.current_mode != self.MODE_SCIENTIFIC:
            return

        calc = self.scientific_calc

        if func in ("open_paren", "close_paren"):
            try:
                if func == "open_paren":
                    calc.open_paren()
                else:
                    calc.close_paren()
                self._update_display()
                if self.scientific_view:
                    self.scientific_view.update_paren_depth(
                        calc.get_paren_depth()
                    )
            except CalculatorError:
                self._handle_error()
            return

        if func == "power":
            # Binary operation: x^n uses ** operator
            calc.add_operator("**")
            self._update_display()
            return

        # Unary operations
        try:
            current = calc.get_current_value()

            if func == "sin":
                result = calc.sin(current)
            elif func == "cos":
                result = calc.cos(current)
            elif func == "tan":
                result = calc.tan(current)
            elif func == "asin":
                result = calc.asin(current)
            elif func == "acos":
                result = calc.acos(current)
            elif func == "atan":
                result = calc.atan(current)
            elif func == "log10":
                result = calc.log10(current)
            elif func == "ln":
                result = calc.ln(current)
            elif func == "log2":
                result = calc.log2(current)
            elif func == "square":
                result = calc.square(current)
            elif func == "cube":
                result = calc.cube(current)
            elif func == "ten_to_x":
                result = calc.ten_to_x(current)
            elif func == "e_to_x":
                result = calc.e_to_x(current)
            elif func == "sqrt":
                result = calc.sqrt(current)
            elif func == "cbrt":
                result = calc.cbrt(current)
            elif func == "reciprocal":
                result = calc.reciprocal(current)
            elif func == "factorial":
                result = calc.factorial(current)
            elif func == "abs":
                result = calc.absolute_value(current)
            elif func == "pi":
                result = calc.get_pi()
            elif func == "e_const":
                result = calc.get_e()
            else:
                return

            calc.current_input = calc.format_number(result)
            calc.last_result = result
            self._update_display()

        except CalculatorError:
            self._handle_error()

    def on_toggle_angle(self) -> None:
        """Handle Deg/Rad toggle button press."""
        if self.current_mode != self.MODE_SCIENTIFIC:
            return
        mode = self.scientific_calc.toggle_angle_mode()
        if self.scientific_view:
            self.scientific_view.update_angle_display(mode)

    def on_programmer(self, func: str) -> None:
        """Handle programmer-mode specific operations.

        Args:
            func: Operation name ('AND', 'OR', 'XOR', 'NOT',
                  'LSH', 'RSH', 'MOD').
        """
        if self.current_mode != self.MODE_PROGRAMMER:
            return

        calc = self.programmer_calc

        if func == "NOT":
            # Unary operation
            try:
                current = int(calc.get_current_value())
                result = calc.bitwise_not(current)
                calc.value = result
                calc.current_input = calc.format_in_base(
                    result, calc.base
                )
                calc.last_result = float(result)
                self._update_display()
            except CalculatorError:
                self._handle_error()
            return

        # Binary operations go through the expression system
        calc.add_operator(func)
        self._update_display()

    def on_base_change(self, base: int) -> None:
        """Handle base selector change in programmer mode.

        Args:
            base: The new base (2, 8, 10, or 16).
        """
        if self.current_mode != self.MODE_PROGRAMMER:
            return

        self.programmer_calc.set_base(base)
        self._update_display()

        if self.programmer_view:
            valid = self.programmer_calc.get_valid_digits()
            self.programmer_view.update_button_states(valid)
            self.programmer_view.update_base_selector(base)

    def on_word_size_change(self, bits: int) -> None:
        """Handle word size selector change in programmer mode.

        Args:
            bits: The new word size (8, 16, 32, or 64).
        """
        if self.current_mode != self.MODE_PROGRAMMER:
            return

        self.programmer_calc.set_word_size(bits)
        self._update_display()

        if self.programmer_view:
            self.programmer_view.update_word_display(bits)

    # --- Keyboard handling ---

    def _bind_keyboard(self) -> None:
        """Bind all keyboard shortcuts per requirements section 6."""
        # Digits 0-9
        for i in range(10):
            self.bind_all(
                str(i),
                lambda e, d=str(i): self.on_digit(d),
            )

        # Operators
        self.bind_all("+", lambda e: self.on_operator("+"))
        self.bind_all("-", lambda e: self.on_operator("-"))
        self.bind_all("*", lambda e: self.on_operator("*"))
        self.bind_all("/", lambda e: self.on_operator("/"))

        # Decimal point
        self.bind_all(".", lambda e: self.on_decimal())

        # Enter/Return for equals
        self.bind_all("<Return>", lambda e: self.on_equals())
        self.bind_all("<KP_Enter>", lambda e: self.on_equals())

        # Escape for all clear
        self.bind_all("<Escape>", lambda e: self.on_all_clear())

        # Backspace
        self.bind_all("<BackSpace>", lambda e: self.on_backspace())
        self.bind_all("<Delete>", lambda e: self.on_backspace())

        # Parentheses (scientific mode)
        self.bind_all(
            "(", lambda e: self.on_scientific("open_paren")
        )
        self.bind_all(
            ")", lambda e: self.on_scientific("close_paren")
        )

        # Programmer mode hex digits
        for c in "abcdef":
            self.bind_all(
                c, lambda e, d=c.upper(): self._on_hex_key(d)
            )
            self.bind_all(
                c.upper(), lambda e, d=c.upper(): self._on_hex_key(d)
            )

        # Programmer mode bitwise shortcuts
        self.bind_all("&", lambda e: self.on_programmer("AND"))
        self.bind_all("|", lambda e: self.on_programmer("OR"))
        self.bind_all("^", lambda e: self.on_programmer("XOR"))
        self.bind_all("~", lambda e: self.on_programmer("NOT"))
        self.bind_all("<", lambda e: self.on_programmer("LSH"))
        self.bind_all(">", lambda e: self.on_programmer("RSH"))

        # Mode switching: Ctrl+1, Ctrl+2, Ctrl+3
        self.bind_all(
            "<Control-Key-1>",
            lambda e: self._switch_mode(self.MODE_BASIC),
        )
        self.bind_all(
            "<Control-Key-2>",
            lambda e: self._switch_mode(self.MODE_SCIENTIFIC),
        )
        self.bind_all(
            "<Control-Key-3>",
            lambda e: self._switch_mode(self.MODE_PROGRAMMER),
        )

    def _on_hex_key(self, digit: str) -> None:
        """Handle hex digit keyboard input (programmer mode only).

        Args:
            digit: Uppercase hex digit ('A'-'F').
        """
        if self.current_mode == self.MODE_PROGRAMMER:
            self.on_digit(digit)

    # --- Display update ---

    def _update_display(self) -> None:
        """Pull current state from the active model and update the view."""
        if self.active_view is None:
            return

        if self.active_calc.error_state:
            self.active_view.show_error("Error")
            self.active_view.show_memory_indicator(
                self.active_calc.has_memory
            )
            return

        # Get display value
        if self.active_calc.current_input:
            display_value = self.active_calc.current_input
        elif self.active_calc.last_result is not None:
            display_value = self.active_calc.format_number(
                self.active_calc.last_result
            )
        else:
            display_value = "0"

        # Get expression display
        expression = self.active_calc.get_expression_display()

        self.active_view.update_display(display_value, expression)
        self.active_view.show_memory_indicator(
            self.active_calc.has_memory
        )

        # Programmer mode extras
        if (
            self.current_mode == self.MODE_PROGRAMMER
            and self.programmer_view
        ):
            try:
                int_val = self.programmer_calc._get_int_value()
                int_val = self.programmer_calc._apply_word_size(int_val)
            except Exception:
                int_val = 0
            bases = self.programmer_calc.get_all_bases(int_val)
            self.programmer_view.update_base_panel(bases)

        # Scientific mode paren depth
        if (
            self.current_mode == self.MODE_SCIENTIFIC
            and self.scientific_view
        ):
            self.scientific_view.update_paren_depth(
                self.scientific_calc.get_paren_depth()
            )

    def _handle_error(self) -> None:
        """Display error state on the view."""
        self.active_calc.error_state = True
        if self.active_view:
            self.active_view.show_error("Error")
