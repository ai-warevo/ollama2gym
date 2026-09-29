import pytest
from tictactoe.engine import TicTacToeEngine

@pytest.fixture
def engine():
    return TicTacToeEngine()

def test_initial_state(engine):
    assert engine.get_board() == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert engine.get_winner() is None
    assert engine.is_draw is False

def test_make_move_valid(engine):
    assert engine.make_move(4) is True
    assert engine.get_board()[4] == TicTacToeEngine.PLAYER_X
    assert engine.get_current_player() == TicTacToeEngine.PLAYER_O

def test_make_move_invalid(engine):
    engine.make_move(0) # X moves at 0
    assert engine.make_move(0) is False # X tries to move at 0 again
    assert engine.make_move(10) is False # Out of bounds

def test_win_condition(engine):
    # X wins by completing top row (0, 1, 2)
    engine.make_move(0) # X
    engine.make_move(3) # O
    engine.make_move(1) # X
    engine.make_move(4) # O
    engine.make_move(2) # X (Wins!)
    assert engine.get_winner() == TicTacToeEngine.PLAYER_X

def test_draw_condition(engine):
    # Draw board configuration
    # X O X
    # X X O
    # O X O
    moves = [0, 1, 2, 5, 3, 6, 7, 8, 4]
    for move in moves:
        engine.make_move(move)
    
    assert engine.is_draw is True
    assert engine.get_winner() is None

def test_reset(engine):
    engine.make_move(0)
    engine.reset()
    assert engine.get_board() == [0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert engine.get_current_player() == TicTacToeEngine.PLAYER_X
