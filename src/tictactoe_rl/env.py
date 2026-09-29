"""Module containing the reinforcement learning environment for Tic-Tac-Toe."""

import random

import gymnasium as gym
import numpy as np
from gymnasium import spaces

from core.logger import get_logger
from tictactoe.engine import TicTacToeEngine

logger = get_logger("tictactoe_rl.env")


class TicTacToeEnv(gym.Env):
    """Gymnasium environment for playing Tic-Tac-Toe."""

    def __init__(self):
        super().__init__()
        self.engine = TicTacToeEngine()
        # Observation space: 9 cells, each can be 0 (empty), 1 (X), or 2 (O)
        self.observation_space = spaces.Box(low=0, high=2, shape=(9,), dtype=np.float32)
        # Action space: 9 positions
        self.action_space = spaces.Discrete(9)

    def reset(self, *, seed=None, options=None):
        """Resets the environment to an initial state."""
        logger.info("Resetting environment")
        super().reset(seed=seed)
        self.engine.reset()

        # Agent is playing as PLAYER_O (Player 2).
        # The engine starts with PLAYER_X. We make a random move for X
        # so that it's the agent's turn when step() is first called.
        possible_moves = [
            i
            for i, val in enumerate(self.engine.get_board())
            if val == TicTacToeEngine.EMPTY
        ]
        if possible_moves:
            random_move = random.choice(possible_moves)
            logger.debug("X (Random Player) makes first move: %s", random_move)
            self.engine.make_move(random_move)

        return self._get_obs(), {}

    def render(self):
        """Renders the environment state."""

    def _get_obs(self):
        """Returns current board observation."""
        return np.array(self.engine.get_board(), dtype=np.float32)

    def step(self, action):
        """Executes one step in the environment."""
        # Agent is playing as PLAYER_O (Player 2).
        # The engine starts with PLAYER_X.
        # We assume the turn has reached O by this call.
        logger.debug("Step: Action taken = %s", action)

        success = self.engine.make_move(action)

        if not success:
            logger.warning("Invalid action attempted: %s", action)
            return self._get_obs(), -10.0, True, False, {}

        # Check if agent (O) won
        if self.engine.get_winner() == TicTacToeEngine.PLAYER_O:
            logger.info("Agent (O) won!")
            return self._get_obs(), 10.0, True, False, {}

        if self.engine.is_draw:
            logger.info("Game drawn!")
            return self._get_obs(), 0.0, True, False, {}

        # Now it is X's turn (Random Player)
        possible_moves = [
            i
            for i, val in enumerate(self.engine.get_board())
            if val == TicTacToeEngine.EMPTY
        ]
        if possible_moves:
            random_move = random.choice(possible_moves)
            logger.debug("X (Random Player) chooses move: %s", random_move)
            self.engine.make_move(random_move)

            # Check if X won after their random move
            if self.engine.get_winner() == TicTacToeEngine.PLAYER_X:
                logger.info("X (Random Player) won!")
                return self._get_obs(), -10.0, True, False, {}

            if self.engine.is_draw:
                logger.info("Game drawn after X move!")
                return self._get_obs(), 0.0, True, False, {}

        return self._get_obs(), -0.1, False, False, {}
