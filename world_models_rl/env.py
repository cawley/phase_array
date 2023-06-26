import numpy as np
import json
import os
import tensorflow as tf
import gc
import utils

from gym.spaces.box import Box

class PhaseArray():
    def __init__(self, full_episode=False):
        self.full_episode = full_episode
        self.observation_space = np.ones((16, 16, 1)) # dtype=np.uint8

    def _process_frame(self, frame):
        obs = np.array(frame)
        return obs
        
    def _step(self, action):
        action = np.reshape(action, (16, 16, 1))

        prev = utils.h_dec(np.squeeze(self.observation_space))
        self.observation_space += action
        self.observation_space[self.observation_space < 0] = 0
        self.observation_space[self.observation_space > 1] = 1
        next = utils.h_dec(np.squeeze(self.observation_space))
        reward = next - prev - 0.1

        if next >= 255:
            reward = 1000
            done = True

        return self.observation_space, reward, done