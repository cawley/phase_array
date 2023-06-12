import keras
from functions_final import DeepQLearning
import gym
import numpy as np

loaded_model = keras.models.load_model("trained_model.h5",custom_objects={'my_loss_fn':DeepQLearning.my_loss_fn})
sumObtainedRewards=0
env = gym.make("CartPole-v1",render_mode='rgb_array')
(currentState,prob)=env.reset()

video_length=400

#env = gym.wrappers.RecordVideo(env, 'stored_video',step_trigger = lambda x: x == 1, video_length=video_length)
env = gym.wrappers.RecordVideo(env, 'stored_video', video_length=video_length)


terminalState=False
while not terminalState:
    # get the Q-value (1 by 2 vector)
    Qvalues=loaded_model.predict(currentState.reshape(1,4))
    # select the action that gives the max Qvalue
    action = np.random.choice(np.where(Qvalues[0,:]==np.max(Qvalues[0,:]))[0])
    action = env.action_space.sample()
    # apply the action
    (currentState, currentReward, terminalState,_,_) = env.step(action)
    # sum the rewards
    sumObtainedRewards+=currentReward

env.reset()
env.close()