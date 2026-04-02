"""Entry point for the advanced calculator application."""

import tkinter as tk

from calculator.app import CalculatorApp


def main() -> None:
    """Create the root window and start the calculator application."""
    root = tk.Tk()
    root.title("Calculator")
    root.resizable(True, True)
    app = CalculatorApp(root)  # noqa: F841
    root.mainloop()


if __name__ == "__main__":
    main()
