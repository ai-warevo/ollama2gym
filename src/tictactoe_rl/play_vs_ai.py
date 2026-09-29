import os
import time
import threading
import numpy as np
import dearpygui.dearpygui as dpg
from stable_baselines3 import DQN
from tictactoe.engine import TicTacToeEngine
from tictactoe.gui import TicTacToeGUI
from core.logger import setup_logging, get_logger

logger = get_logger("tictactoe_rl.play")

class AIPlayer:
    def __init__(self, model_path):
        logger.info(f"Loading model from {model_path}...")
        try:
            self.model = DQN.load(model_path)
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model from {model_path}: {e}")
            raise

    def predict(self, board):
        obs = np.array(board, dtype=np.float32).reshape(1, 9)
        action, _states = self.model.predict(obs, deterministic=True)
        return int(action[0])

class AIGameGUI(TicTacToeGUI):
    def __init__(self, engine: TicTacToeEngine, ai_player: AIPlayer):
        logger.debug("Initializing AIGameGUI")
        self.ai_player = ai_player
        super().__init__(engine)

    def _on_click(self, sender: int, app_data: int, user_data: int) -> None:
        # 1. Human Move (X)
        if self.engine.make_move(user_data):
            logger.debug(f"Human move made at position {user_data}")
            self._update_display()
            
            # Check if game ended after X move
            if self.engine.get_winner() is not None or self.engine.is_draw:
                logger.info("Game ended after human move")
                return

            # 2. AI Move (O) - Run in a separate thread to avoid blocking DPG loop
            logger.debug("Starting AI turn thread")
            threading.Thread(target=self._ai_turn, daemon=True).start()
        else:
            logger.warning(f"Invalid human move attempt at position {user_data}")

    def _ai_turn(self) -> None:
        time.sleep(0.5)
        board = self.engine.get_board()
        action = self.ai_player.predict(board)
        logger.debug(f"AI predicts action: {action}")
        
        if not self.engine.make_move(action):
            import random
            logger.warning(f"AI move to {action} was invalid, attempting fallback")
            possible_moves = [i for i, val in enumerate(board) if val == TicTacToeEngine.EMPTY]
            if possible_moves:
                action = random.choice(possible_moves)
                logger.debug(f"AI using fallback move: {action}")
                self.engine.make_move(action)

        self._update_display()

def main():
    setup_logging()
    model_path = "models/tictactoe_dqn"
    if not os.path.exists(model_path + ".zip"):
        logger.error(f"Trained model not found at {model_path}")
        return

    try:
        ai = AIPlayer(model_path)
        engine = TicTacToeEngine()
        gui = AIGameGUI(engine, ai)
        logger.info("Starting Play vs AI GUI")
        gui.run()
    except Exception as e:
        logger.error(f"Error in main loop: {e}", exc_info=True)

if __name__ == "__main__":
    main()
