import os, subprocess, time, signal
import gym
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import numpy as np

import logging

logger = logging.getLogger(__name__)


class DemoEnv(gym.Env):
    def __init__(self, dim, ep_length=100):
        """
        Identity environment for testing purposes
        :param dim: (int) the size of the dimensions you want to learn
        :param ep_length: (int) the length of each episodes in timesteps
        """
        self.action_space = spaces.Discrete(dim)
        self.observation_space = self.action_space
        self.ep_length = ep_length
        self.current_step = 0
        self.dim = dim
        self.reset()

    def reset(self):
        self.current_step = 0
        self._choose_next_state()
        return self.state

    def step(self, action):
        reward = self._get_reward(action)
        self._choose_next_state()
        self.current_step += 1
        done = self.current_step >= self.ep_length
        return self.state, reward, done, {}

    def _choose_next_state(self):
        self.state = self.action_space.sample()

    def _get_reward(self, action):
        return 1 if np.all(self.state == action) else 0

    def render(self, mode="human"):
        pass
