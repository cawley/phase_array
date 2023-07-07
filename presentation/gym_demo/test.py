import numpy as np
import gym

from stable_baselines3 import PPO
from stable_baselines3.ppo import MlpPolicy
from stable_baselines3.common.vec_env import DummyVecEnv

DIM = 10

# Create environment
env = gym.make("gym_demo:Demo-v0", dim=DIM)
vectEnv = DummyVecEnv([lambda: env])  # Usage of DummyVecEnv

# Create model
model = PPO(MlpPolicy, vectEnv, learning_rate=1.5e-3, gae_lambda=0.8)

# Learning...
model.learn(total_timesteps=10000)

# Inference
n_trials = 1000
reward_sum = 0
obs = env.reset()
for _ in range(n_trials):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, _, _ = env.step(action)
    reward_sum += reward

assert reward_sum > 0.9 * n_trials
print("Test OK!")
