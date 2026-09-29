# Tic-Tac-Toe Reinforcement Learning (RL)

This package provides a Reinforcement Learning wrapper around the `tictactoe` core engine, making it compatible with the Gymnasium interface and enabling training using libraries like `stable-baselines3`.

## Features

- **Gymnasium Environment**: A standard RL environment based on the `TicTacToeEngine`.
- **Training Scripts**: Tools to train agents (e.g., DQN) from scratch.
- **Play vs AI**: An interactive way to play against a trained agent.

## Components

- **`env.py`**: The Gymnasium implementation of the Tic-Tac-Toe game.
- **`train.py`**: Script to initiate the training process for an RL agent.
- **`play_vs_ai.py`**: Scenario where you can play against a trained model.

## Requirements

This package requires the core `tictactoe` engine and several RL dependencies (e.g., `gymnasium`, `stable-baselines3`, `torch`). Ensure the project is installed in your environment or use `uv`.

## Usage

### Training an Agent
To start training a reinforcement learning agent:
```bash
PYTHONPATH=src uv run python -m tictactoe_rl.train
```

### Playing Against AI
To test your trained model by playing against it through a UI:
```bash
PYTHONPATH=src uv run python -m tictactoe_rl.play_vs_ai
```
