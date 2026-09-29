import os
import time
import threading
import numpy as np
import dearpygui.dearpygui as dpg
from stable_baselines3 import DQN
from tictactoe.engine import TicTacToeEngine
from tictactoe.gui import TicTacToeGUI

class AIPlayer:
    def __init__(self, model_path):
        print(f"Loading model from {model_path}...")
        self.model = DQN.load(model_path)
        print("Model loaded.")

    def predict(self, board):
        obs = np.array(board, dtype=np.float32).reshape(1, 9)
        action, _states = self.model.predict(obs, deterministic=True)
        return int(action[0])

class AIGameGUI(TicTacToeGUI):
    def __init__(self, engine: TicTacToeEngine, ai_player: AIPlayer):
        self.ai_player = ai_player
        super().__init__(engine)

    def _on_click(self, sender: int, app_data: int, user_data: int) -> None:
        # 1. Human Move (X)
        if self.engine.make_move(user_data):
            self._update_display()
            
            # Check if game ended after X move
            if self.engine.get_winner() is not None or self.engine.is_draw:
                return

            # 2. AI Move (O) - Run in a separate thread to avoid blocking DPG loop
            threading.Thread(target=self._ai_turn, daemon=True).start()

    def _ai_turn(self) -> None:
        time.sleep(0.5)
        board = self.engine.get_board()
        action = self.ai_player.predict(board)
        
        if not self.engine.make_move(action):
            import random
            possible_moves = [i for i, val in enumerate(board) if val == TicTacToeEngine.EMPTY]
            if possible_moves:
                action = random.choice(possible_moves)
                self.engine.make_move(action)

        self._update_display()

def main():
    model_path = "models/tictactoe_dqn"
    if not os.path.exists(model_path + ".zip"):
        print("Error: Trained model not found at", model_path)
        return

    ai = AIPlayer(model_path)
    engine = TicTacToeEngine()
    gui = AIGameGUI(engine, ai)
    gui.run()

if __name__ == "__main__":
    main()
