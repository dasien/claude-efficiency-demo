"""Entry point for the Advanced Calculator application."""

from calculator.app import CalculatorApp


def main() -> None:
    """Launch the calculator."""
    app = CalculatorApp()
    app.run()


if __name__ == "__main__":
    main()
