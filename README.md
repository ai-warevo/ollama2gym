# Tic-Tac-Toe with RL Support

A Python implementation of the classic Tic-Tac-Toe game, featuring a standalone graphical user interface and integration with Reinforcement Learning (RL) frameworks like Gymnasium and Stable Baselines3.

## 🚀 Features

- **Core Engine**: A robust, decoupled game engine (`TicTacToeEngine`) that manages game state and logic.
- **Graphical Interface**: A desktop application built with `DearPyGui` for human players.
- **Reinforcement Learning**: A custom Gymnasium environment designed for training intelligent agents.
- **Training & Playback**: Built-in scripts to train models (e.g., DQN) and test them against human players via a UI.

## 🛠️ Installation

This project uses `uv` for package management. Ensure you have [uv installed](https://github.com/astral-sh/uv).

```bash
# Clone the repository
git clone <repository-url>
cd ollama2gym  # or your specific directory name

# Install dependencies
uv sync
```

## 🎮 Usage

### Playing the Game (GUI)

To launch the game and play manually:

```bash
uv run tictactoe
```

### Reinforcement Learning

#### Training an Agent

To start training a new RL agent from scratch:

```bash
PYTHONPATH=src uv run python -m tictactoe_rl.train
```

#### Playing Against AI

To test your trained model by playing against it through the GUI:

```bash
PYTHONPATH=src uv run python -m tictactoe_rl.play_vs_ai
```

## 🧪 Development & Testing

### Code Quality

Run all linters and type checkers (including `black`, `ruff`, `mypy`, and `pylint`):

```bash
uv run check
```

### Running Tests

To ensure everything is working correctly, execute the test suite:

```bash
uv run pytest
```

## 📂 Project Structure

Detailed documentation can be found within each sub-package:

- [`src/tictactoe`](src/tictactoe/README.md): Documentation for the core engine and GUI.
- [`src/tictactoe_rl`](src/tictactoe_rl/README.md): Documentation for Reinforcement Learning integration.
- [`src/core`](src/core/README.md): Shared utilities and common components.
