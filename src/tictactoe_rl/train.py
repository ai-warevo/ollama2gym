"""Module for training RL agents for Tic-Tac-Toe."""

import argparse
import os
from typing import Any

from stable_baselines3 import DQN

from core.logger import get_logger, setup_logging
from tictactoe_rl.env import TicTacToeEnv

logger = get_logger("tictactoe_rl.train")

# Configuration presets for different difficulty levels
DIFFICULTY_CONFIGS: dict[str, dict[str, Any]] = {
    "easy": {
        "net_arch": [64, 64],
        "total_timesteps": 50000,
        "learning_rate": 1e-3,
        "buffer_size": 50000,
        "batch_size": 64,
    },
    "medium": {
        "net_arch": [128, 128],
        "total_timesteps": 200000,
        "learning_rate": 5e-4,
        "buffer_size": 100000,
        "batch_size": 128,
    },
    "hard": {
        "net_arch": [256, 256],
        "total_timesteps": 500000,
        "learning_rate": 3e-4,
        "buffer_size": 100000,
        "batch_size": 128,
    },
    "expert": {
        "net_arch": [512, 512],
        "total_timesteps": 2000000,
        "learning_rate": 1e-4,
        "buffer_size": 200000,
        "batch_size": 256,
    },
}


def train(difficulty: str) -> None:
    """Trains a DQN model for the specified difficulty."""
    if difficulty not in DIFFICULTY_CONFIGS:
        raise ValueError(
            f"Invalid difficulty: {difficulty}. Choose from {list(DIFFICULTY_CONFIGS.keys())}"
        )

    config = DIFFICULTY_CONFIGS[difficulty]
    setup_logging()
    logger.info("Initializing environment for '%s' difficulty...", difficulty)
    env = TicTacToeEnv()

    logger.info(
        "Configuring DQN model (Difficulty: %s) with architecture %s",
        difficulty,
        config["net_arch"],
    )
    model = DQN(
        "MlpPolicy",
        env,
        verbose=1,
        learning_rate=config["learning_rate"],
        buffer_size=config["buffer_size"],
        batch_size=config["batch_size"],
        exploration_fraction=0.2,
        exploration_final_eps=0.05,
        policy_kwargs={"net_arch": config["net_arch"]},
    )

    logger.info(
        "Starting training for %s (%s timesteps)...",
        difficulty,
        config["total_timesteps"],
    )
    try:
        model.learn(total_timesteps=config["total_timesteps"])
        logger.info("Training finished successfully.")
    except Exception:  # pylint: disable=broad-exception-caught
        logger.exception("An error occurred during training")
        return

    os.makedirs("models", exist_ok=True)
    model_path = f"models/tictactoe_dqn_{difficulty}"
    model.save(model_path)
    logger.info("Model saved to %s", model_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train Tic-Tac-Toe RL agents with different difficulties."
    )
    parser.add_argument(
        "--difficulty",
        type=str,
        choices=list(DIFFICULTY_CONFIGS.keys()),
        default="medium",
        help="Difficulty preset to use for training (default: medium)",
    )
    args = parser.parse_args()
    train(args.difficulty)
