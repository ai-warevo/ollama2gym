# Tic-Tac-Toe Engine & GUI

This package contains the core logic and graphical interface for a Tic-Tac-Toe game. It is designed to be decoupled from any UI, making it easy to integrate into Reinforcement Learning (RL) environments like Gymnasium.

## Components

- **`TicTacToeEngine`**: The core game engine implemented in `engine.py`. It manages the board state, moves, and win/draw conditions without any dependency on a graphical interface.
- **`TicTacToeGUI`**: A desktop application using `DearPyGui` that provides a playable interface for humans to play against each other or an AI.

## Quick Start

### Playing the Game
To launch the graphical user interface:
```bash
uv run tictactoe
```

### For Developers

#### Running Tests
To ensure everything is working correctly, run the test suite:
```bash
uv run pytest
```

#### Code Quality Checks
To run all linters and type checkers (including `black`, `ruff`, `mypy`, and `pylint`), use the built-in check command:
```bash
uv run check
```
