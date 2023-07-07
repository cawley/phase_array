# tested on
# gym==0.26.2
# gym-notices==0.0.8

# gymnasium==0.27.0
# gymnasium-notices==0.0.1

# classical gym
import gym

# instead of gym, import gymnasium
# import gymnasium as gym
import numpy as np
import time


# create environment
env = gym.make("CartPole", render_mode="human")
# reset the environment,
# returns an initial state
(state, _) = env.reset()
# states are
# cart position, cart velocity
# pole angle, pole angular velocity


# simulate the environment
episodeNumber = 20
timeSteps = 3000


for episodeIndex in range(episodeNumber):
    initial_state = env.reset()
    print(episodeIndex)
    env.render()
    appendedObservations = []
    for timeIndex in range(timeSteps):
        print(timeIndex)
        random_action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(random_action)
        appendedObservations.append(observation)
        # time.sleep(0.1)
        if terminated:
            time.sleep(1)
            break
env.close()
