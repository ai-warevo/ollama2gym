from .engine import TicTacToeEngine
from .gui import TicTacToeGUI
from core.logger import setup_logging, get_logger

logger = get_logger("tictactoe.main")

def main():
    setup_logging()
    logger.info("App started")
    
    try:
        engine = TicTacToeEngine()
        app = TicTacToeGUI(engine)
        app.run()
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
