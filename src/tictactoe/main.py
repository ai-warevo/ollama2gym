from .engine import TicTacToeEngine
from .gui import TicTacToeGUI

def main():
    engine = TicTacToeEngine()
    app = TicTacToeGUI(engine)
    app.run()

if __name__ == "__main__":
    main()
