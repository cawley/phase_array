import gym
import numpy as np

env = gym.make("MountainCar-v0")
env.reset()

# Learning Rate Hyperparameter
GAMMA = 0.1

# Weight of info learned later on
DISCOUNT = 0.95
# Iteration count
EPISODES = 25000

DISCRETE_OS_SIZE = [20, 20]
discrete_os_win_size = (env.observation_space.high - env.observation_space.low)/DISCRETE_OS_SIZE

# Exploration settings
epsilon = 1  # not a constant, going to be decayed
START_EPSILON_DECAYING = 1
END_EPSILON_DECAYING = EPISODES//2
epsilon_decay_value = epsilon/(END_EPSILON_DECAYING - START_EPSILON_DECAYING)

# Lookup table of Q-reward values
q_table = np.random.uniform(low=-2, high=0, size=(DISCRETE_OS_SIZE + [env.action_space.n]))

# Translating a continuous state to discrete one
def get_discrete_state(state):
    discrete_state = (state - env.observation_space.low)/discrete_os_win_size
    return tuple(discrete_state.astype(np.int))  # we use this tuple to look up the 3 Q values for the available actions in the q-table

for episode in range(EPISODES):
    discrete_state = get_discrete_state(env.reset())
    done = False

    # Render every couple episodes, sanity check
    if episode % SHOW_EVERY == 0:
        render = True
        print(episode)
    else:
        render = False
    while not done:

        if np.random.random() > epsilon:
            # Get action from Q table
            action = np.argmax(q_table[discrete_state])
        else:
            # Get random action
            action = np.random.randint(0, env.action_space.n)

        # Grab the max rated action
        # action = np.argmax(q_table[discrete_state])

        new_state, reward, done, _ = env.step(action)
        new_discrete_state = get_discrete_state(new_state)
        env.render()
        #new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

        # If simulation did not end after the previous step update the Q-reward table
        if not done:
            # Maximum possible Q value in next step (for new state)
            max_future_q = np.max(q_table[new_discrete_state])

            # Current Q value (for current state and performed action)
            current_q = q_table[discrete_state + (action,)]

            # NEW_Q calculated equation
            new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT * max_future_q)

            # Update Q table with new Q value
            q_table[discrete_state + (action,)] = new_q
            
        else:
            # If the simulation ends (i.e. goal position) update Q with reward directly
            if new_state[0] >= env.goal_position:
                #q_table[discrete_state + (action,)] = reward
                q_table[discrete_state + (action,)] = 0
            discrete_state = new_discrete_state

        # Decaying is being done every episode if episode number is within decaying range
        if END_EPSILON_DECAYING >= episode >= START_EPSILON_DECAYING:
            epsilon -= epsilon_decay_value

env.close()
