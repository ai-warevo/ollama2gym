# pylint: disable=duplicate-code
"""Module for playing Tic-Tac-Toe against an AI agent."""

import argparse
import os
import random
import threading
import time

import numpy as np
from stable_baselines3 import DQN

from core.logger import get_logger, setup_logging
from tictactoe.engine import TicTacToeEngine
from tictactoe.gui import TicTacToeGUI

logger = get_logger("tictactoe_rl.play")


class AIPlayer:
    """Represents an AI player using either a trained DQN model or Minimax."""

    def __init__(self, model_path: str, difficulty: str = "hard") -> None:
        """Initializes the AI player with a model or minimax strategy."""
        self.difficulty = difficulty
        self.model: DQN | None = None
        if self.difficulty != "expert":
            logger.info("Loading model from %s...", model_path)
            try:
                self.model = DQN.load(model_path)
                logger.info("Model loaded successfully.")
            except Exception as e:
                logger.error("Failed to load model from %s: %s", model_path, e)
                raise
        else:
            logger.info("Using minimax for expert difficulty")

    def get_difficulty(self) -> str:
        """Returns the current difficulty level."""
        return self.difficulty

    def predict(self, board: list[int]) -> int:
        """Predicts the next move based on the current board state."""
        if self.difficulty == "expert":
            return self._minimax_move(board)

        obs = np.array(board, dtype=np.float32).reshape(1, 9)
        assert self.model is not None
        action, _states = self.model.predict(obs, deterministic=True)
        return int(action[0])

    def _minimax_move(self, board: list[int]) -> int:
        """Calculates the minimax move."""
        best_score = -float("inf")
        move = -1
        # AI is Player 2 (O), Human is Player 1 (X)
        ai_player = 2
        human_player = 1

        for i in range(9):
            if board[i] == 0:  # EMPTY
                board[i] = ai_player
                score = self._minimax(board, 0, False, ai_player, human_player)
                board[i] = 0
                if score > best_score:
                    best_score = score
                    move = i
        return move

    def _minimax(
        self,
        board: list[int],
        depth: int,
        is_maximizing: bool,
        ai_player: int,
        human_player: int,
    ) -> float:
        """Performs minimax algorithm."""
        winner = self._get_winner(board)
        if winner == ai_player:
            return 10 - depth
        if winner == human_player:
            return depth - 10
        if 0 not in board:
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for i in range(9):
                if board[i] == 0:
                    board[i] = ai_player
                    score = self._minimax(
                        board, depth + 1, False, ai_player, human_player
                    )
                    board[i] = 0
                    best_score = max(score, best_score)
            return best_score

        best_score = float("inf")
        for i in range(9):
            if board[i] == 0:
                board[i] = human_player
                score = self._minimax(board, depth + 1, True, ai_player, human_player)
                board[i] = 0
                best_score = min(score, best_score)
        return best_score

    def _get_winner(self, board: list[int]) -> int | None:
        """Returns the winner if there is one."""
        win_combinations = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),  # Rows
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),  # Cols
            (0, 4, 8),
            (2, 4, 6),  # Diagonals
        ]
        for combo in win_combinations:
            if (
                board[combo[0]] != 0
                and board[combo[0]] == board[combo[1]] == board[combo[2]]
            ):
                return board[combo[0]]
        return None


class AIGameGUI(TicTacToeGUI):
    """A GUI for playing against the AI."""

    def __init__(self, engine: TicTacToeEngine, ai_player: AIPlayer) -> None:
        """Initializes the AIGameGUI."""
        logger.debug("Initializing AIGameGUI")
        self.ai_player = ai_player
        super().__init__(engine)

    def get_info(self) -> str:
        """Returns information about the GUI."""
        return "AIGameGUI is active"

    def _on_click(self, _sender: int, _app_data: int, user_data: int) -> None:
        # 1. Human Move (X)
        if self.engine.make_move(user_data):
            logger.debug("Human move made at position %s", user_data)
            self._update_display()

            # Check if game ended after X move
            if self.engine.get_winner() is not None or self.engine.is_draw:
                logger.info("Game ended after human move")
                return

            # 2. AI Move (O) - Run in a separate thread to avoid blocking DPG loop
            logger.debug("Starting AI turn thread")
            threading.Thread(target=self._ai_turn, daemon=True).start()
        else:
            logger.warning("Invalid human move attempt at position %s", user_data)

    def _ai_turn(self) -> None:
        """Executes the AI's turn."""
        time.sleep(0.5)
        board = self.engine.get_board()
        action = self.ai_player.predict(board)
        logger.debug("AI predicts action: %s", action)

        if not self.engine.make_move(action):
            logger.warning("AI move to %s was invalid, attempting fallback", action)
            possible_moves = [
                i for i, val in enumerate(board) if val == TicTacToeEngine.EMPTY
            ]
            if possible_moves:
                action = random.choice(possible_moves)
                logger.debug("AI using fallback move: %s", action)
                self.engine.make_move(action)

        self._update_display()


def main() -> None:
    """Main entry point for the play-vs-ai script."""
    setup_logging()

    parser = argparse.ArgumentParser(description="Play Tic-Tac-Toe against an AI.")
    parser.add_argument(
        "--difficulty",
        type=str,
        choices=["easy", "medium", "hard", "expert"],
        help="Difficulty level (loads models/tictactoe_dqn_{difficulty}.zip)",
    )
    args = parser.parse_args()
    difficulty = args.difficulty or "hard"
    model_path = f"models/tictactoe_dqn_{difficulty}"

    if not os.path.exists(model_path + ".zip"):
        msg = (
            f"Trained model not found at {model_path}. Please train it first using "
            "'python -m tictactoe_rl.train --difficulty <level>'."
        )
        logger.error(msg)
        return

    try:
        ai = AIPlayer(model_path, difficulty=difficulty)
        engine = TicTacToeEngine()
        gui = AIGameGUI(engine, ai)
        logger.info("Starting Play vs AI GUI")
        gui.run()
    except Exception:  # pylint: disable=broad-exception-caught
        logger.exception("Error in main loop")


if __name__ == "__main__":
    main()
