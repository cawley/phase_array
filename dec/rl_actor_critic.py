import torch
from torch import nn
from torch import optim
import numpy as np
from torch.nn import functional as F
import torch.multiprocessing as mp

class ActorCritic(nn.Module):
    def __init__(self):
        super(ActorCritic, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=(2, 2), stride=2, padding=1)
        self.conv2 = nn.Conv2d(16, 16, kernel_size=(2, 2), stride=2, padding=1)
        self.conv3 = nn.Conv2d(16, 16, kernel_size=(2, 2), stride=2, padding=1)
<<<<<<< HEAD
        self.linear1 = nn.LazyLinear(512)
        self.linear2 = nn.LazyLinear(1)
=======
        self.linear1 = nn.LazyLinear(256)
        self.linear2 = nn.LazyLinear(512)
        self.linear3 = nn.LazyLinear(1)
>>>>>>> 7c50ee401e4015af128216e9868dfe3eaa20f9ce

    def forward(self, x):
        x = F.normalize(x)
        y = F.elu(self.conv1(x))
        y = F.elu(self.conv2(y))
        y = F.elu(self.conv3(y))
        y = y.flatten(start_dim=1)
<<<<<<< HEAD
        actor = self.linear1(y)
        critic = self.linear2(y)
=======
        y = F.elu(self.linear1(y))
        actor = self.linear2(y)
        critic = self.linear3(y)
>>>>>>> 7c50ee401e4015af128216e9868dfe3eaa20f9ce

        return actor, critic
    
