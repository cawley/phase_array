import gym

env = gym.make("MountainCar-v0")
env.reset()

done = False

while not done:
    action = 2
    # this action means move right
    # we can probably just build the env in gym for calibration and go from there
    new_state, reward, done, truncated, info = env.step(action)

env.close()