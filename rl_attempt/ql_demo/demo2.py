import time
import gym
from matplotlib import pyplot as plt

env = gym.make("MountainCar-v0")
env.render(mode = "human")

num_steps = 1500

obs = env.reset()

for i in range(num_steps):
    action = 2
    # intelligent action is
    # action = my_intelligent_agent_fn(obs)
    # random is
    # action = env.action_space.sample()

    # do action
    obs, reward, done, info = env.step(action)

    # render env
    env.render()

    # slow vid down
    time.sleep(.001)

    if done:
        env.reset()

env.close()