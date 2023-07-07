import numpy as np
import gym

from stable_baselines import A2C, ACER, ACKTR, DQN, DDPG, SAC, PPO1, PPO2, TD3, TRPO
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common import set_global_seeds
from stable_baselines.common.policies import MlpPolicy

DIM = 10

# Create environment
env = gym.make("gym_demo:Demo-v0", dim=DIM)
vectEnv = DummyVecEnv([lambda: env])


# Create model
model = PPO2(MlpPolicy, env=vectEnv, learning_rate=1.5e-3, lam=0.8)
# model = TRPO(MlpPolicy, env=vectEnv, max_kl=0.05, lam=0.7)


# Learning...
model.learn(total_timesteps=10000, seed=0)


# Inference
n_trials = 1000
reward_sum = 0
set_global_seeds(0)
obs = env.reset()
for _ in range(n_trials):
    action, _ = model.predict(obs)
    obs, reward, _, _ = env.step(action)
    reward_sum += reward


# Testing
assert model.action_probability(obs).shape == (
    DIM,
), "Error: action_probability not returning correct shape"
action = env.action_space.sample()
action_prob = model.action_probability(obs, actions=action)
assert np.prod(action_prob.shape) == 1, "Error: not scalar probability"
action_logprob = model.action_probability(obs, actions=action, logp=True)
assert np.allclose(action_prob, np.exp(action_logprob)), (action_prob, action_logprob)

assert reward_sum > 0.9 * n_trials
print("Test OK!")
