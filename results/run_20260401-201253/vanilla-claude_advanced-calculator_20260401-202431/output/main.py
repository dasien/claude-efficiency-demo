"""Entry point for the Advanced Calculator application."""

import tkinter as tk
from calculator.app import CalculatorApp


def main() -> None:
    """Launch the calculator application."""
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
