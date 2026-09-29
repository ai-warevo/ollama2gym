import pytest
from unittest.mock import MagicMock
from tictactoe_rl.play_vs_ai import AIPlayer

@pytest.fixture
def expert_ai():
    # "expert" difficulty avoids loading a DQN model
    return AIPlayer(model_path="non_existent_path", difficulty="expert")

def test_minimax_immediate_win(expert_ai):
    # AI is Player 2 (O). Human is Player 1 (X).
    # Board:
    # X O .
    # X . .
    # . . O (Wait, let's make a real win)
    # If O has (3, 4), and position 5 is empty.
    board = [
        0, 0, 0,
        2, 2, 0, # O at 3 and 4
        0, 0, 0
    ]
    # The AI should pick 5 to win.
    move = expert_ai.predict(board)
    assert move == 5

def test_minimax_block_opponent(expert_ai):
    # Human (X/1) has (0, 1) and position 2 is empty.
    # AI (O/2) must block at 2.
    board = [
        1, 1, 0,
        2, 0, 0,
        0, 0, 0
    ]
    move = expert_ai.predict(board)
    assert move == 2

def test_minimax_draw_scenario(expert_ai):
    # A board that is one move away from a draw or win.
    # X O X
    # X X O
    # O . O  <- O can take 7 to make it a draw (or if 7 was the last move)
    board = [
        1, 2, 1,
        1, 1, 2,
        2, 0, 2
    ]
    # Positions filled: 0(X), 1(O), 2(X), 3(X), 4(X) -- wait this is a win for X.
    # Let's use the draw from earlier:
    # X O X
    # X X O
    # O X O  -> No, that's full.
    
    # Empty board with some moves that leads to forced draw if played optimally.
    # For simplicity, just ensuring it returns a valid move on a nearly full board.
    board = [
        1, 2, 1,
        1, 2, 1,
        2, 1, 0 
    ]
    move = expert_ai.predict(board)
    assert move == 8

def test_minimax_empty_board(expert_ai):
    # On an empty board, it should return a valid move (usually first available or similar).
    board = [0] * 9
    move = expert_ai.predict(board)
    assert 0 <= move < 9

def test_get_difficulty(expert_ai):
    assert expert_ai.get_difficulty() == "expert"
