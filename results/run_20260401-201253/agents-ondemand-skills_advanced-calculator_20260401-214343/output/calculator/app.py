"""MVC Controller for the advanced calculator application.

Coordinates between logic objects and view objects, manages mode
switching, wires callbacks from view buttons to logic methods, and
registers keyboard bindings on the root window.
"""

import tkinter as tk
from typing import Callable, Dict, Optional

from calculator.logic.base_logic import (
    DisplayState,
    Mode,
    NumberBase,
    WordSize,
)
from calculator.logic.basic_logic import BasicLogic
from calculator.logic.scientific_logic import ScientificLogic
from calculator.logic.programmer_logic import ProgrammerLogic
from calculator.gui.basic_view import BasicView
from calculator.gui.scientific_view import ScientificView
from calculator.gui.programmer_view import ProgrammerView
from calculator.gui.base_view import BaseView

# Window dimensions per mode
_WINDOW_SIZES: Dict[Mode, str] = {
    Mode.BASIC: "320x500",
    Mode.SCIENTIFIC: "580x520",
    Mode.PROGRAMMER: "620x620",
}


class CalculatorApp:
    """Central controller that wires views to logic and manages modes.

    Instantiates all three logic objects and manages switching between
    Basic, Scientific, and Programmer modes while preserving numeric
    values and memory across transitions.
    """

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self._mode = Mode.BASIC
        self._basic_logic = BasicLogic()
        self._scientific_logic = ScientificLogic()
        self._programmer_logic = ProgrammerLogic()
        self._current_logic: BasicLogic = self._basic_logic
        self._current_view: Optional[BaseView] = None

        self._setup_menu()
        self._setup_keyboard_bindings()
        self._switch_mode(Mode.BASIC)

    # ── Menu bar ────────────────────────────────────────────────

    def _setup_menu(self) -> None:
        """Create the menu bar with mode switching entries."""
        self._menubar = tk.Menu(self._root)
        self._root.config(menu=self._menubar)

        self._mode_menu = tk.Menu(self._menubar, tearoff=0)
        self._menubar.add_cascade(label="Mode", menu=self._mode_menu)

        self._mode_var = tk.StringVar(value=Mode.BASIC.value)

        self._mode_menu.add_radiobutton(
            label="Basic",
            variable=self._mode_var,
            value=Mode.BASIC.value,
            command=lambda: self._switch_mode(Mode.BASIC),
            accelerator="Ctrl+1",
        )
        self._mode_menu.add_radiobutton(
            label="Scientific",
            variable=self._mode_var,
            value=Mode.SCIENTIFIC.value,
            command=lambda: self._switch_mode(Mode.SCIENTIFIC),
            accelerator="Ctrl+2",
        )
        self._mode_menu.add_radiobutton(
            label="Programmer",
            variable=self._mode_var,
            value=Mode.PROGRAMMER.value,
            command=lambda: self._switch_mode(Mode.PROGRAMMER),
            accelerator="Ctrl+3",
        )

    # ── Mode switching ──────────────────────────────────────────

    def _switch_mode(self, new_mode: Mode) -> None:
        """Switch to a new calculator mode.

        Transfers the current numeric value between logic objects,
        preserves memory across all instances, destroys the current
        view, creates the new one, and resizes the window.

        Args:
            new_mode: The mode to switch to.
        """
        old_mode = self._mode
        old_logic = self._current_logic

        # Determine the new logic object
        if new_mode == Mode.BASIC:
            new_logic = self._basic_logic
        elif new_mode == Mode.SCIENTIFIC:
            new_logic = self._scientific_logic
        else:
            new_logic = self._programmer_logic

        # Transfer value from old logic to new logic
        if old_logic is not new_logic:
            current_value = old_logic.get_current_value()

            # Preserve memory across all logic instances
            memory = old_logic._memory
            self._basic_logic._memory = memory
            self._scientific_logic._memory = memory
            self._programmer_logic._memory = memory

            new_logic.set_current_value(current_value)

        # Update state
        self._mode = new_mode
        self._current_logic = new_logic
        self._mode_var.set(new_mode.value)

        # Destroy old view
        if self._current_view is not None:
            self._current_view.destroy()
            self._current_view = None

        # Create new view
        if new_mode == Mode.BASIC:
            self._current_view = BasicView(self._root)
        elif new_mode == Mode.SCIENTIFIC:
            self._current_view = ScientificView(self._root)
        else:
            self._current_view = ProgrammerView(self._root)

        self._current_view.pack(fill=tk.BOTH, expand=True)

        # Wire callbacks
        self._wire_callbacks()

        # Resize window
        self._root.geometry(_WINDOW_SIZES[new_mode])

        # Update display with current state
        state = self._current_logic.get_display_state()
        self._current_view.update_display(state)

    # ── Callback wiring ─────────────────────────────────────────

    def _safe_call(
        self, fn: Callable[..., DisplayState], *args: object
    ) -> None:
        """Call a logic method wrapped in try/except, then update view.

        On unhandled exception, displays Error in the view to
        satisfy RC-3 (application must never crash).

        Args:
            fn: The logic method to call.
            *args: Arguments to pass to the logic method.
        """
        try:
            state = fn(*args)
        except Exception:
            # Fallback: show error state without crashing
            state = DisplayState(
                main_display="Error",
                expression_display="",
                error=True,
                memory_indicator=self._current_logic.has_memory,
            )
        if self._current_view is not None:
            self._current_view.update_display(state)

    def _wire_callbacks(self) -> None:
        """Wire all view button callbacks to the appropriate logic methods."""
        if self._current_view is None:
            return

        callbacks: Dict[str, Callable] = {}

        if self._mode == Mode.BASIC:
            callbacks = self._build_basic_callbacks()
        elif self._mode == Mode.SCIENTIFIC:
            callbacks = self._build_scientific_callbacks()
        elif self._mode == Mode.PROGRAMMER:
            callbacks = self._build_programmer_callbacks()

        self._current_view.set_callbacks(callbacks)

    def _build_common_callbacks(self) -> Dict[str, Callable]:
        """Build callbacks shared across all modes.

        Returns:
            Dictionary mapping button names to callables.
        """
        logic = self._current_logic
        callbacks: Dict[str, Callable] = {}

        # Digit buttons 0-9
        for d in "0123456789":
            digit = d
            callbacks[digit] = lambda d=digit: self._safe_call(
                logic.input_digit, d
            )

        # Decimal point
        callbacks["."] = lambda: self._safe_call(logic.input_decimal)

        # Arithmetic operators
        for op in ["+", "-", "*", "/"]:
            operator = op
            callbacks[operator] = lambda o=operator: self._safe_call(
                logic.input_operator, o
            )

        # Evaluate
        callbacks["="] = lambda: self._safe_call(logic.evaluate)

        # Clear
        callbacks["C"] = lambda: self._safe_call(logic.clear_entry)
        callbacks["AC"] = lambda: self._safe_call(logic.clear_all)

        # Backspace
        callbacks["Backspace"] = lambda: self._safe_call(
            logic.input_backspace
        )

        # Sign toggle
        callbacks["+/-"] = lambda: self._safe_call(
            logic.input_sign_toggle
        )

        return callbacks

    def _build_memory_callbacks(self) -> Dict[str, Callable]:
        """Build memory button callbacks.

        Returns:
            Dictionary mapping memory button names to callables.
        """
        logic = self._current_logic
        return {
            "MC": lambda: self._safe_call(logic.memory_clear),
            "MR": lambda: self._safe_call(logic.memory_recall),
            "M+": lambda: self._safe_call(logic.memory_add),
            "M-": lambda: self._safe_call(logic.memory_subtract),
            "MS": lambda: self._safe_call(logic.memory_store),
        }

    def _build_basic_callbacks(self) -> Dict[str, Callable]:
        """Build all callbacks for Basic mode.

        Returns:
            Dictionary mapping button names to callables.
        """
        logic = self._basic_logic
        callbacks = self._build_common_callbacks()
        callbacks.update(self._build_memory_callbacks())

        # Percent
        callbacks["%"] = lambda: self._safe_call(logic.input_percent)

        return callbacks

    def _build_scientific_callbacks(self) -> Dict[str, Callable]:
        """Build all callbacks for Scientific mode.

        Returns:
            Dictionary mapping button names to callables.
        """
        logic = self._scientific_logic
        callbacks = self._build_common_callbacks()
        callbacks.update(self._build_memory_callbacks())

        # Percent
        callbacks["%"] = lambda: self._safe_call(logic.input_percent)

        # Trig functions
        callbacks["sin"] = lambda: self._safe_call(logic.trig_sin)
        callbacks["cos"] = lambda: self._safe_call(logic.trig_cos)
        callbacks["tan"] = lambda: self._safe_call(logic.trig_tan)
        callbacks["asin"] = lambda: self._safe_call(logic.trig_asin)
        callbacks["acos"] = lambda: self._safe_call(logic.trig_acos)
        callbacks["atan"] = lambda: self._safe_call(logic.trig_atan)

        # Angle unit toggle
        callbacks["Deg/Rad"] = lambda: self._safe_call(
            logic.toggle_angle_unit
        )

        # Logarithmic functions
        callbacks["log"] = lambda: self._safe_call(logic.log_base10)
        callbacks["ln"] = lambda: self._safe_call(logic.log_natural)
        callbacks["log\u2082"] = lambda: self._safe_call(logic.log_base2)

        # Power and root functions
        callbacks["x\u00b2"] = lambda: self._safe_call(
            logic.power_square
        )
        callbacks["x\u00b3"] = lambda: self._safe_call(
            logic.power_cube
        )
        callbacks["x\u207f"] = lambda: self._safe_call(logic.power_n)
        callbacks["10\u02e3"] = lambda: self._safe_call(
            logic.power_10x
        )
        callbacks["e\u02e3"] = lambda: self._safe_call(logic.power_ex)
        callbacks["\u221ax"] = lambda: self._safe_call(
            logic.root_square
        )
        callbacks["\u00b3\u221ax"] = lambda: self._safe_call(
            logic.root_cube
        )
        callbacks["1/x"] = lambda: self._safe_call(logic.reciprocal)

        # Constants
        callbacks["\u03c0"] = lambda: self._safe_call(logic.insert_pi)
        callbacks["e"] = lambda: self._safe_call(logic.insert_e)

        # Factorial and absolute value
        callbacks["n!"] = lambda: self._safe_call(logic.factorial)
        callbacks["|x|"] = lambda: self._safe_call(
            logic.absolute_value
        )

        # Parentheses
        callbacks["("] = lambda: self._safe_call(logic.open_paren)
        callbacks[")"] = lambda: self._safe_call(logic.close_paren)

        return callbacks

    def _build_programmer_callbacks(self) -> Dict[str, Callable]:
        """Build all callbacks for Programmer mode.

        Returns:
            Dictionary mapping button names to callables.
        """
        logic = self._programmer_logic
        callbacks = self._build_common_callbacks()

        # Hex digit buttons A-F
        for hd in "ABCDEF":
            hex_digit = hd
            callbacks[hex_digit] = lambda d=hex_digit: self._safe_call(
                logic.input_digit, d
            )

        # Bitwise operations
        callbacks["AND"] = lambda: self._safe_call(logic.bitwise_and)
        callbacks["OR"] = lambda: self._safe_call(logic.bitwise_or)
        callbacks["XOR"] = lambda: self._safe_call(logic.bitwise_xor)
        callbacks["NOT"] = lambda: self._safe_call(logic.bitwise_not)
        callbacks["LSH"] = lambda: self._safe_call(logic.left_shift)
        callbacks["RSH"] = lambda: self._safe_call(logic.right_shift)

        # Modulo
        callbacks["MOD"] = lambda: self._safe_call(
            logic.input_operator, "%"
        )
        callbacks["%"] = lambda: self._safe_call(
            logic.input_operator, "%"
        )

        # Base selectors
        base_map = {
            "BASE_DEC": NumberBase.DEC,
            "BASE_HEX": NumberBase.HEX,
            "BASE_OCT": NumberBase.OCT,
            "BASE_BIN": NumberBase.BIN,
        }
        for name, base in base_map.items():
            callbacks[name] = lambda b=base: self._safe_call(
                logic.set_base, b
            )

        # Word size selectors
        word_map = {
            "WORD_8": WordSize.BITS_8,
            "WORD_16": WordSize.BITS_16,
            "WORD_32": WordSize.BITS_32,
            "WORD_64": WordSize.BITS_64,
        }
        for name, ws in word_map.items():
            callbacks[name] = lambda w=ws: self._safe_call(
                logic.set_word_size, w
            )

        return callbacks

    # ── Keyboard bindings ───────────────────────────────────────

    def _setup_keyboard_bindings(self) -> None:
        """Register keyboard bindings on the root window.

        Covers digits, operators, Enter, Escape, Backspace, Delete,
        parentheses, hex digits, bitwise operators, and Ctrl+1/2/3
        for mode switching.
        """
        root = self._root

        # Digits 0-9
        for d in "0123456789":
            digit = d
            root.bind(
                digit,
                lambda event, d=digit: self._handle_digit_key(d),
            )

        # Decimal point
        root.bind(".", lambda event: self._handle_decimal_key())

        # Arithmetic operators
        root.bind("+", lambda event: self._handle_operator_key("+"))
        root.bind("-", lambda event: self._handle_operator_key("-"))
        root.bind("*", lambda event: self._handle_operator_key("*"))
        root.bind("/", lambda event: self._handle_operator_key("/"))

        # Evaluate
        root.bind("<Return>", lambda event: self._handle_evaluate_key())
        root.bind(
            "<KP_Enter>", lambda event: self._handle_evaluate_key()
        )

        # All Clear
        root.bind("<Escape>", lambda event: self._handle_clear_all_key())

        # Backspace / Delete
        root.bind(
            "<BackSpace>",
            lambda event: self._handle_backspace_key(),
        )
        root.bind(
            "<Delete>", lambda event: self._handle_backspace_key()
        )

        # Parentheses (Scientific mode)
        root.bind(
            "(", lambda event: self._handle_paren_key("(")
        )
        root.bind(
            ")", lambda event: self._handle_paren_key(")")
        )

        # Hex digits a-f / A-F (Programmer mode)
        for ch in "abcdef":
            letter = ch
            root.bind(
                letter,
                lambda event, c=letter: self._handle_hex_key(
                    c.upper()
                ),
            )
            root.bind(
                letter.upper(),
                lambda event, c=letter: self._handle_hex_key(
                    c.upper()
                ),
            )

        # Bitwise operators (Programmer mode)
        root.bind(
            "&", lambda event: self._handle_bitwise_key("AND")
        )
        root.bind(
            "|", lambda event: self._handle_bitwise_key("OR")
        )
        root.bind(
            "^", lambda event: self._handle_bitwise_key("XOR")
        )
        root.bind(
            "~", lambda event: self._handle_bitwise_key("NOT")
        )
        root.bind(
            "<", lambda event: self._handle_bitwise_key("LSH")
        )
        root.bind(
            ">", lambda event: self._handle_bitwise_key("RSH")
        )

        # Percent key in programmer mode acts as modulo
        root.bind(
            "%", lambda event: self._handle_percent_key()
        )

        # Mode switching: Ctrl+1, Ctrl+2, Ctrl+3
        root.bind(
            "<Control-Key-1>",
            lambda event: self._switch_mode(Mode.BASIC),
        )
        root.bind(
            "<Control-Key-2>",
            lambda event: self._switch_mode(Mode.SCIENTIFIC),
        )
        root.bind(
            "<Control-Key-3>",
            lambda event: self._switch_mode(Mode.PROGRAMMER),
        )

    # ── Keyboard event handlers ─────────────────────────────────

    def _handle_digit_key(self, digit: str) -> None:
        """Handle a digit key press.

        Args:
            digit: The digit character '0'-'9'.
        """
        self._safe_call(self._current_logic.input_digit, digit)

    def _handle_decimal_key(self) -> None:
        """Handle the decimal point key press."""
        self._safe_call(self._current_logic.input_decimal)

    def _handle_operator_key(self, op: str) -> None:
        """Handle an arithmetic operator key press.

        Args:
            op: The operator character.
        """
        self._safe_call(self._current_logic.input_operator, op)

    def _handle_evaluate_key(self) -> None:
        """Handle the Enter/Return key press for evaluation."""
        self._safe_call(self._current_logic.evaluate)

    def _handle_clear_all_key(self) -> None:
        """Handle the Escape key press for All Clear."""
        self._safe_call(self._current_logic.clear_all)

    def _handle_backspace_key(self) -> None:
        """Handle the Backspace/Delete key press."""
        self._safe_call(self._current_logic.input_backspace)

    def _handle_paren_key(self, paren: str) -> None:
        """Handle parenthesis key press (Scientific mode only).

        Args:
            paren: Either '(' or ')'.
        """
        if self._mode != Mode.SCIENTIFIC:
            return

        logic = self._scientific_logic
        if paren == "(":
            self._safe_call(logic.open_paren)
        else:
            self._safe_call(logic.close_paren)

    def _handle_hex_key(self, hex_char: str) -> None:
        """Handle hex digit key press (Programmer mode, HEX base only).

        Args:
            hex_char: An uppercase hex digit 'A'-'F'.
        """
        if self._mode != Mode.PROGRAMMER:
            return

        self._safe_call(
            self._programmer_logic.input_digit, hex_char
        )

    def _handle_bitwise_key(self, op_name: str) -> None:
        """Handle bitwise operator key press (Programmer mode only).

        Args:
            op_name: The bitwise operation name (AND, OR, XOR,
                NOT, LSH, RSH).
        """
        if self._mode != Mode.PROGRAMMER:
            return

        logic = self._programmer_logic
        dispatch = {
            "AND": logic.bitwise_and,
            "OR": logic.bitwise_or,
            "XOR": logic.bitwise_xor,
            "NOT": logic.bitwise_not,
            "LSH": logic.left_shift,
            "RSH": logic.right_shift,
        }
        fn = dispatch.get(op_name)
        if fn is not None:
            self._safe_call(fn)

    def _handle_percent_key(self) -> None:
        """Handle the percent key press.

        In Programmer mode, acts as modulo. In other modes, acts
        as the percent function.
        """
        if self._mode == Mode.PROGRAMMER:
            self._safe_call(
                self._programmer_logic.input_operator, "%"
            )
        elif self._mode == Mode.SCIENTIFIC:
            self._safe_call(self._scientific_logic.input_percent)
        else:
            self._safe_call(self._basic_logic.input_percent)
