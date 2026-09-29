import gymnasium as gym
from stable_baselines3 import DQN
from tictactoe_rl.env import TicTacToeEnv
from core.logger import setup_logging, get_logger
import os

logger = get_logger("tictactoe_rl.train")

def train():
    setup_logging()
    logger.info("Initializing environment...")
    env = TicTacToeEnv()
    
    # Using a more robust MLP policy [256, 256]
    logger.info("Configuring DQN model with MlpPolicy and architecture [256, 256]")
    model = DQN(
        "MlpPolicy", 
        env, 
        verbose=1, 
        learning_rate=3e-4, 
        buffer_size=100000, 
        batch_size=128,
        exploration_fraction=0.2,
        exploration_final_eps=0.05,
        policy_kwargs={'net_arch': [256, 256]}
    )
    
    logger.info("Starting training (this may take a few minutes)...")
    try:
        model.learn(total_timesteps=500000)
        logger.info("Training finished successfully.")
    except Exception as e:
        logger.error(f"An error occurred during training: {e}", exc_info=True)
        return
    
    os.makedirs("models", exist_ok=True)
    model_name = "models/tictactoe_dqn"
    model.save(model_name)
    logger.info(f"Model saved to {model_name}")

if __name__ == "__main__":
    train()
