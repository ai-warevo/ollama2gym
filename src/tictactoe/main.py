"""Main entry point for the Tic-Tac-Toe application."""

from core.logger import get_logger, setup_logging

from .engine import TicTacToeEngine
from .gui import TicTacToeGUI

logger = get_logger("tictactoe.main")


def main() -> None:
    """Starts the Tic-Tac-Toe app."""
    setup_logging()
    logger.info("App started")

    try:
        engine = TicTacToeEngine()
        app = TicTacToeGUI(engine)
        app.run()
    except Exception:  # pylint: disable=broad-exception-caught
        logger.exception("An error occurred")


if __name__ == "__main__":
    main()
