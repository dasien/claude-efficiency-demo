"""Entry point for the calculator application."""

from calculator.app import App


def main() -> None:
    """Create and run the calculator application."""
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
