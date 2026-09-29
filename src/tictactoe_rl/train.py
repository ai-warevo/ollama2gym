import gymnasium as gym
from stable_baselines3 import DQN
from tictactoe_rl.env import TicTacToeEnv
import os

def train():
    print("Initializing environment...")
    env = TicTacToeEnv()
    
    # Using a simple MLP policy [128, 128] as requested
    model = DQN(
        "MlpPolicy", 
        env, 
        verbose=1, 
        learning_rate=1e-3, 
        buffer_size=50000, 
        batch_size=64,
        exploration_fraction=0.2,
        exploration_final_eps=0.05,
        policy_kwargs={'net_arch': [128, 128]}
    )
    
    print("Starting training (this may take a minute)...")
    model.learn(total_timesteps=40000)
    print("Training finished.")
    
    os.makedirs("models", exist_ok=True)
    model.save("models/tictactoe_dqn")
    print("Model saved to models/tictactoe_dqn")

if __name__ == "__main__":
    train()
