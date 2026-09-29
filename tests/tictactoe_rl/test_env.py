import pytest
import numpy as np
from tictactoe_rl.env import TicTacToeEnv
from tictactoe.engine import TicTacToeEngine

@pytest.fixture
def env():
    return TicTacToeEnv()

def test_env_reset(env):
    obs, info = env.reset()
    
    # Check observation shape and type
    assert obs.shape == (9,)
    assert obs.dtype == np.float32
    
    # Check that the engine is reset
    assert env.engine.get_winner() is None
    assert env.engine.is_draw is False
    
    # Because reset makes a random move for X, the board shouldn't be all zeros
    assert np.sum(obs) > 0

def test_env_step_invalid_move(env):
    env.reset()
    
    # Find an occupied spot (X moves first during reset)
    obs, _ = env.reset()
    occupied_indices = np.where(obs == 1)[0]
    assert len(occupied_indices) > 0
    occupied_spot = int(occupied_indices[0])
    
    obs, reward, terminated, truncated, info = env.step(occupied_spot)
    
    assert reward == -10.0
    assert terminated is True

def test_env_step_valid_move_reward(env):
    # Check that a normal move (that doesn't end the game) returns -0.1
    obs, _ = env.reset()
    empty_indices = np.where(obs == 0)[0]
    
    if len(empty_indices) > 0:
        first_empty = int(empty_indices[0])
        # We need to ensure this move doesn't end the game.
        # With only one X move at start, a single O move cannot win or draw.
        obs, reward, terminated, truncated, info = env.step(first_empty)
        assert reward == -0.1
        assert not terminated

def test_env_observation_space(env):
    obs, _ = env.reset()
    assert env.observation_space.contains(obs)
