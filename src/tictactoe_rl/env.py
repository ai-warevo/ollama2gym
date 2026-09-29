import gymnasium as gym
import numpy as np
from gymnasium import spaces
from tictactoe.engine import TicTacToeEngine
import random

class TicTacToeEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.engine = TicTacToeEngine()
        # Observation space: 9 cells, each can be 0 (empty), 1 (X), or 2 (O)
        self.observation_space = spaces.Box(low=0, high=2, shape=(9,), dtype=np.float32)
        # Action space: 9 positions
        self.action_space = spaces.Discrete(9)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.engine.reset()
        return self._get_obs(), {}

    def _get_obs(self):
        return np.array(self.engine.get_board(), dtype=np.float32)

    def step(self, action):
        # Agent is playing as PLAYER_O (Player 2).
        # The engine starts with PLAYER_X.
        # We assume the turn has reached O by this call.

        success = self.engine.make_move(action)
        
        if not success:
            return self._get_obs(), -10.0, True, False, {}
        
        # Check if agent (O) won
        if self.engine.get_winner() == TicTacToeEngine.PLAYER_O:
            return self._get_obs(), 10.0, True, False, {}
        
        if self.engine.is_draw:
            return self._get_obs(), 0.0, True, False, {}

        # Now it is X's turn (Random Player)
        possible_moves = [i for i, val in enumerate(self.engine.get_board()) if val == TicTacToeEngine.EMPTY]
        if possible_moves:
            random_move = random.choice(possible_moves)
            self.engine.make_move(random_move)
            
            # Check if X won after their random move
            if self.engine.get_winner() == TicTacToeEngine.PLAYER_X:
                return self._get_obs(), -10.0, True, False, {}
            elif self.engine.is_draw:
                return self._get_obs(), 0.0, True, False, {}

        return self._get_obs(), 0.0, False, False, {}
