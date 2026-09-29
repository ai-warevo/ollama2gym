import pytest
import dearpygui.dearpygui as dpg
from tictactoe.engine import TicTacToeEngine
from tictactoe.gui import TicTacToeGUI

@pytest.fixture(scope="module", autouse=True)
def dpg_context():
    """Fixture to initialize and destroy DPG context for the whole test module."""
    dpg.create_context()
    yield
    dpg.destroy_context()

@pytest.fixture(scope="module")
def engine():
    return TicTacToeEngine()

@pytest.fixture(scope="module")
def gui(engine):
    return TicTacToeGUI(engine)

@pytest.fixture(autouse=True)
def reset_game_state(engine, gui):
    engine.reset()
    gui._update_display()

def test_gui_integration_flow(engine, gui):
    # Simulate first move (X at 0)
    assert engine.make_move(0) is True
    gui._update_display()
    assert engine.get_board() == [1, 0, 0, 0, 0, 0, 0, 0, 0]
    
    # Simulate second move (O at 1)
    assert engine.make_move(1) is True
    gui._update_display()
    assert engine.get_board() == [1, 2, 0, 0, 0, 0, 0, 0, 0]

def test_gui_reset_button(engine, gui):
    # Moves to setup a non-empty board
    engine.make_move(0)
    engine.make_move(1)
    gui._update_display()
    
    # Should be able to reset via engine (tested indirectly via GUI refresh)
    engine.reset()
    gui._update_display()
    assert engine.get_board() == [0, 0, 0, 0, 0, 0, 0, 0, 0]

def test_gui_win_condition(engine, gui):
    # X wins by completing top row (0, 1, 2)
    engine.make_move(0) # X
    engine.make_move(3) # O
    engine.make_move(1) # X
    engine.make_move(4) # O
    engine.make_move(2) # X (Wins!)
    gui._update_display()
    assert engine.get_winner() == TicTacToeEngine.PLAYER_X
