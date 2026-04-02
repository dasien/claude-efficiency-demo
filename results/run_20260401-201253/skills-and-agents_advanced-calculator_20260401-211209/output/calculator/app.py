"""Calculator controller connecting logic engines and GUI views."""

import tkinter as tk

from calculator.logic.basic_logic import BasicCalculator
from calculator.logic.scientific_logic import ScientificCalculator
from calculator.logic.programmer_logic import ProgrammerCalculator
from calculator.gui.basic_view import BasicView
from calculator.gui.scientific_view import ScientificView
from calculator.gui.programmer_view import ProgrammerView

# Window dimensions per mode
WINDOW_SIZES: dict[str, str] = {
    "basic": "320x450",
    "scientific": "580x450",
    "programmer": "600x520",
}


class App(tk.Tk):
    """Main calculator application controller.

    Coordinates between logic engines and GUI views following the
    MVC pattern. Manages mode switching, keyboard shortcuts, and
    the menu bar.
    """

    def __init__(self) -> None:
        """Initialize the calculator application."""
        super().__init__()
        self.title("Calculator")

        # Create logic instances for each mode
        self.logic_instances: dict[str, BasicCalculator] = {
            "basic": BasicCalculator(),
            "scientific": ScientificCalculator(),
            "programmer": ProgrammerCalculator(),
        }

        # Create a container frame for all views
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Create view instances for each mode
        self.views: dict[str, BasicView] = {
            "basic": BasicView(self.container),
            "scientific": ScientificView(self.container),
            "programmer": ProgrammerView(self.container),
        }

        self.current_mode: str = "basic"

        # Register callbacks for all views
        self._register_callbacks("basic")
        self._register_callbacks("scientific")
        self._register_callbacks("programmer")

        # Show the basic view, hide others
        self.views["basic"].pack(fill="both", expand=True)

        # Bind keyboard shortcuts
        self.bind("<Key>", self._on_key_press)
        self.bind("<Control-Key-1>", lambda e: self.switch_mode("basic"))
        self.bind("<Control-Key-2>", lambda e: self.switch_mode("scientific"))
        self.bind("<Control-Key-3>", lambda e: self.switch_mode("programmer"))

        # Create menu bar
        self._create_menu_bar()

        # Set initial window size
        self.geometry(WINDOW_SIZES["basic"])

        # Initial display update
        self._update_display()

    def _create_menu_bar(self) -> None:
        """Build the menu bar with mode selection options."""
        menubar = tk.Menu(self)
        mode_menu = tk.Menu(menubar, tearoff=0)

        self._mode_var = tk.StringVar(value="basic")
        mode_menu.add_radiobutton(
            label="Basic",
            variable=self._mode_var,
            value="basic",
            accelerator="Ctrl+1",
            command=lambda: self.switch_mode("basic"),
        )
        mode_menu.add_radiobutton(
            label="Scientific",
            variable=self._mode_var,
            value="scientific",
            accelerator="Ctrl+2",
            command=lambda: self.switch_mode("scientific"),
        )
        mode_menu.add_radiobutton(
            label="Programmer",
            variable=self._mode_var,
            value="programmer",
            accelerator="Ctrl+3",
            command=lambda: self.switch_mode("programmer"),
        )

        menubar.add_cascade(label="Mode", menu=mode_menu)
        self.config(menu=menubar)

    def switch_mode(self, new_mode: str) -> None:
        """Switch between calculator modes, transferring state.

        Transfers the current numeric value and memory between the
        old and new logic engines, swaps the visible view, and
        resizes the window.

        Args:
            new_mode: The target mode ('basic', 'scientific',
                or 'programmer').
        """
        if new_mode == self.current_mode:
            return

        old_logic = self.logic_instances[self.current_mode]
        new_logic = self.logic_instances[new_mode]

        # Transfer value with appropriate conversion
        value = old_logic.current_value
        if new_mode == "programmer":
            int_value = int(value)
            new_logic.current_value = new_logic.mask_value(int_value)
        elif self.current_mode == "programmer":
            new_logic.current_value = float(old_logic.current_value)
        else:
            new_logic.current_value = value

        # Transfer memory
        new_logic.memory = old_logic.memory
        new_logic.has_memory = old_logic.has_memory

        # Swap views
        self.views[self.current_mode].pack_forget()
        self.views[new_mode].pack(fill="both", expand=True)

        # Update state
        self.current_mode = new_mode
        self._mode_var.set(new_mode)

        # Resize window
        self.geometry(WINDOW_SIZES[new_mode])

        self._update_display()

    def _register_callbacks(self, mode: str) -> None:
        """Register all button callbacks for a given mode's view.

        Wires each button identifier to the appropriate controller
        handler method.

        Args:
            mode: The mode whose view should be configured.
        """
        view = self.views[mode]

        # Digit buttons 0-9
        for digit in range(10):
            d = str(digit)
            view._callbacks[f"digit_{d}"] = (
                lambda d=d: self._on_digit(d)
            )

        # Basic arithmetic operators
        view._callbacks["op_add"] = lambda: self._on_operator("+")
        view._callbacks["op_sub"] = lambda: self._on_operator("-")
        view._callbacks["op_mul"] = lambda: self._on_operator("*")
        view._callbacks["op_div"] = lambda: self._on_operator("/")

        # Standard operations
        view._callbacks["equals"] = self._on_equals
        view._callbacks["all_clear"] = self._on_all_clear
        view._callbacks["clear_entry"] = self._on_clear_entry
        view._callbacks["decimal"] = self._on_decimal
        view._callbacks["toggle_sign"] = self._on_toggle_sign
        view._callbacks["percent"] = self._on_percent
        view._callbacks["backspace"] = self._on_backspace

        # Memory operations
        view._callbacks["mc"] = self._on_mc
        view._callbacks["mr"] = self._on_mr
        view._callbacks["m_plus"] = self._on_m_plus
        view._callbacks["m_minus"] = self._on_m_minus
        view._callbacks["ms"] = self._on_ms

        # Scientific-specific callbacks
        if mode == "scientific":
            # Unary scientific functions
            unary_funcs = [
                "sin", "cos", "tan", "asin", "acos", "atan",
                "log", "ln", "log2",
                "square", "cube", "ten_power", "e_power",
                "square_root", "cube_root",
                "reciprocal", "factorial", "absolute",
            ]
            for func in unary_funcs:
                view._callbacks[func] = (
                    lambda f=func: self._on_scientific_unary(f)
                )

            # Two-operand and structural scientific functions
            view._callbacks["power"] = (
                lambda: self._on_scientific_func("power")
            )
            view._callbacks["open_paren"] = (
                lambda: self._on_scientific_func("open_paren")
            )
            view._callbacks["close_paren"] = (
                lambda: self._on_scientific_func("close_paren")
            )
            view._callbacks["pi"] = (
                lambda: self._on_scientific_func("insert_pi")
            )
            view._callbacks["euler"] = (
                lambda: self._on_scientific_func("insert_e")
            )
            view._callbacks["toggle_angle"] = self._on_toggle_angle

        # Programmer-specific callbacks
        if mode == "programmer":
            # Hex digit buttons A-F
            for hex_digit in "ABCDEF":
                view._callbacks[f"hex_{hex_digit.lower()}"] = (
                    lambda d=hex_digit: self._on_hex_digit(d)
                )

            # Base selection
            for base in ("DEC", "HEX", "OCT", "BIN"):
                view._callbacks[f"base_{base.lower()}"] = (
                    lambda b=base: self._on_base_change(b)
                )

            # Word size selection
            for bits in (8, 16, 32, 64):
                view._callbacks[f"word_{bits}"] = (
                    lambda b=bits: self._on_word_size(b)
                )

            # Bitwise operators
            view._callbacks["op_and"] = (
                lambda: self._on_operator("AND")
            )
            view._callbacks["op_or"] = (
                lambda: self._on_operator("OR")
            )
            view._callbacks["op_xor"] = (
                lambda: self._on_operator("XOR")
            )
            view._callbacks["op_lsh"] = (
                lambda: self._on_operator("LSH")
            )
            view._callbacks["op_rsh"] = (
                lambda: self._on_operator("RSH")
            )
            view._callbacks["op_not"] = self._on_bitwise_not
            view._callbacks["op_mod"] = (
                lambda: self._on_operator("%")
            )

    # ------------------------------------------------------------------
    # Handler methods
    # ------------------------------------------------------------------

    def _on_digit(self, digit: str) -> None:
        """Handle a digit button press.

        Args:
            digit: The digit character ('0'-'9').
        """
        try:
            logic = self.logic_instances[self.current_mode]
            logic.append_digit(digit)
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_operator(self, op: str) -> None:
        """Handle an operator button press.

        Args:
            op: The operator string ('+', '-', '*', '/', etc.).
        """
        try:
            logic = self.logic_instances[self.current_mode]
            logic.add_operator(op)
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_equals(self) -> None:
        """Handle the equals button press."""
        try:
            logic = self.logic_instances[self.current_mode]
            logic.evaluate()
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_all_clear(self) -> None:
        """Handle the all-clear (AC) button press."""
        try:
            logic = self.logic_instances[self.current_mode]
            logic.clear_all()
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_clear_entry(self) -> None:
        """Handle the clear-entry (CE) button press."""
        try:
            logic = self.logic_instances[self.current_mode]
            logic.clear_entry()
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_decimal(self) -> None:
        """Handle the decimal point button press."""
        try:
            logic = self.logic_instances[self.current_mode]
            logic.append_decimal()
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_toggle_sign(self) -> None:
        """Handle the toggle-sign (+/-) button press."""
        try:
            logic = self.logic_instances[self.current_mode]
            logic.toggle_sign()
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_percent(self) -> None:
        """Handle the percent button press."""
        try:
            logic = self.logic_instances[self.current_mode]
            logic.percentage()
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_backspace(self) -> None:
        """Handle the backspace button press."""
        try:
            logic = self.logic_instances[self.current_mode]
            logic.backspace()
            self._update_display()
        except Exception:
            self._handle_error()

    # Memory handlers

    def _on_mc(self) -> None:
        """Handle the memory-clear (MC) button press."""
        try:
            logic = self.logic_instances[self.current_mode]
            logic.mc()
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_mr(self) -> None:
        """Handle the memory-recall (MR) button press."""
        try:
            logic = self.logic_instances[self.current_mode]
            logic.mr()
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_m_plus(self) -> None:
        """Handle the memory-add (M+) button press."""
        try:
            logic = self.logic_instances[self.current_mode]
            logic.m_plus()
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_m_minus(self) -> None:
        """Handle the memory-subtract (M-) button press."""
        try:
            logic = self.logic_instances[self.current_mode]
            logic.m_minus()
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_ms(self) -> None:
        """Handle the memory-store (MS) button press."""
        try:
            logic = self.logic_instances[self.current_mode]
            logic.ms()
            self._update_display()
        except Exception:
            self._handle_error()

    # Scientific handlers

    def _on_scientific_unary(self, func_name: str) -> None:
        """Handle a unary scientific function button press.

        Args:
            func_name: The name of the method on ScientificCalculator
                to invoke (e.g. 'sin', 'cos', 'square_root').
        """
        try:
            logic = self.logic_instances[self.current_mode]
            func = getattr(logic, func_name)
            func()
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_scientific_func(self, func_name: str) -> None:
        """Handle a structural scientific function button press.

        Covers two-operand operations (power), parentheses, and
        constant insertion.

        Args:
            func_name: The name of the method on ScientificCalculator
                to invoke (e.g. 'power', 'open_paren', 'insert_pi').
        """
        try:
            logic = self.logic_instances[self.current_mode]
            func = getattr(logic, func_name)
            func()
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_toggle_angle(self) -> None:
        """Handle the angle mode toggle (DEG/RAD) button press."""
        try:
            logic = self.logic_instances[self.current_mode]
            logic.toggle_angle_mode()
            view = self.views[self.current_mode]
            if hasattr(view, "set_angle_mode"):
                view.set_angle_mode(logic.angle_mode)
            self._update_display()
        except Exception:
            self._handle_error()

    # Programmer handlers

    def _on_hex_digit(self, digit: str) -> None:
        """Handle a hex digit (A-F) button press.

        Args:
            digit: The hex digit character ('A'-'F').
        """
        try:
            logic = self.logic_instances[self.current_mode]
            logic.append_hex_digit(digit)
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_base_change(self, base: str) -> None:
        """Handle a base-selection button press.

        Args:
            base: The target base ('DEC', 'HEX', 'OCT', 'BIN').
        """
        try:
            logic = self.logic_instances[self.current_mode]
            logic.set_base(base)
            view = self.views[self.current_mode]
            if hasattr(view, "set_base_panel"):
                view.set_base_panel(logic.get_all_bases())
            if hasattr(view, "enable_digits"):
                view.enable_digits(logic.get_valid_digits())
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_word_size(self, bits: int) -> None:
        """Handle a word-size selection button press.

        Args:
            bits: The word size in bits (8, 16, 32, or 64).
        """
        try:
            logic = self.logic_instances[self.current_mode]
            logic.set_word_size(bits)
            self._update_display()
        except Exception:
            self._handle_error()

    def _on_bitwise_not(self) -> None:
        """Handle the bitwise NOT button press."""
        try:
            logic = self.logic_instances[self.current_mode]
            logic.bitwise_not()
            self._update_display()
        except Exception:
            self._handle_error()

    # ------------------------------------------------------------------
    # Display update
    # ------------------------------------------------------------------

    def _update_display(self) -> None:
        """Push current logic state to the active view.

        Reads display value, expression, memory indicator, and
        mode-specific state from the logic engine and updates
        the corresponding view widgets.
        """
        try:
            logic = self.logic_instances[self.current_mode]
            view = self.views[self.current_mode]

            if logic.error:
                view.set_display(logic.error_message)
                view.set_expression("")
            else:
                view.set_display(logic.get_display_value())
                view.set_expression(logic.get_expression_display())

            view.show_memory_indicator(logic.has_memory)

            if self.current_mode == "programmer":
                if hasattr(view, "set_base_panel"):
                    view.set_base_panel(logic.get_all_bases())
                if hasattr(view, "enable_digits"):
                    view.enable_digits(logic.get_valid_digits())
                if hasattr(view, "set_word_size_display"):
                    view.set_word_size_display(logic.word_size)

            if self.current_mode == "scientific":
                if hasattr(view, "set_angle_mode"):
                    view.set_angle_mode(logic.angle_mode)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Keyboard handling
    # ------------------------------------------------------------------

    def _on_key_press(self, event: tk.Event) -> None:
        """Route keyboard events to the appropriate handler.

        Args:
            event: The Tkinter key event.
        """
        char = event.char
        keysym = event.keysym

        # Digit keys 0-9
        if char in "0123456789":
            self._on_digit(char)
            return

        # Basic arithmetic operators
        if char == "+":
            self._on_operator("+")
            return
        if char == "-":
            self._on_operator("-")
            return
        if char == "*":
            self._on_operator("*")
            return
        if char == "/":
            self._on_operator("/")
            return

        # Enter / Return
        if keysym in ("Return", "KP_Enter"):
            self._on_equals()
            return

        # Escape -> all clear
        if keysym == "Escape":
            self._on_all_clear()
            return

        # Backspace
        if keysym == "BackSpace":
            self._on_backspace()
            return

        # Decimal point (not in programmer mode)
        if char == "." and self.current_mode != "programmer":
            self._on_decimal()
            return

        # Parentheses (scientific mode only)
        if self.current_mode == "scientific":
            if char == "(":
                self._on_scientific_func("open_paren")
                return
            if char == ")":
                self._on_scientific_func("close_paren")
                return

        # Programmer mode special keys
        if self.current_mode == "programmer":
            logic = self.logic_instances["programmer"]

            # Hex digits A-F when in HEX base
            if hasattr(logic, "base") and logic.base == "HEX":
                if char.upper() in "ABCDEF":
                    self._on_hex_digit(char.upper())
                    return

            # Bitwise operator shortcuts
            if char == "&":
                self._on_operator("AND")
                return
            if char == "|":
                self._on_operator("OR")
                return
            if char == "^":
                self._on_operator("XOR")
                return
            if char == "~":
                self._on_bitwise_not()
                return
            if char == "<":
                self._on_operator("LSH")
                return
            if char == ">":
                self._on_operator("RSH")
                return
            if char == "%":
                self._on_operator("%")
                return

    def _handle_error(self) -> None:
        """Set error state on the current logic engine after an exception."""
        try:
            logic = self.logic_instances[self.current_mode]
            logic.set_error("Error")
            self._update_display()
        except Exception:
            pass
