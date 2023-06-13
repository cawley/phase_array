import time
import gymnasium as gym

env = gym.make("CartPole-v1", render_mode = "human")
env.reset()

obs, info = env.reset(seed=42)

for i in range(1500):
    # action = 1
    # action = 2
    # intelligent action is
    # action = my_intelligent_agent_fn(obs)
    # random is
    action = env.action_space.sample()

    # do action
    obs, reward, terminated, truncated, info = env.step(action)

    # render env
    env.render()

    # slow vid down
    # time.sleep(.001)

    if terminated or truncated:
       obs, info = env.reset()

env.close()