"""Entry point for the Advanced Calculator application.

Creates the Tk root window and launches the calculator app.
"""

from calculator.app import App


def main() -> None:
    """Create and run the calculator application."""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
