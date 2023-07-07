import numpy as np
import tensorflow as tf
from tensorflow import keras
import torch
import torch.nn.functional as F
import utils
import matplotlib.pyplot as plt

def test():
    max_eps = 20000
    max_dur = 100
    N = 16
    gamma = 0.999
    score = []

    model = torch.nn.Sequential(
        torch.nn.Conv2d(1, N, 2),
        torch.nn.ReLU(),
        torch.nn.MaxPool2d(2),
        torch.nn.Conv2d(N, 2 * N, 2),
        torch.nn.ReLU(),
        torch.nn.MaxPool2d(2),
        torch.nn.Conv2d(2 * N, 4 * N, 2),
        torch.nn.ReLU(),
        torch.nn.Flatten(),
        torch.nn.LazyLinear(2 * N**2)
        )
    
    learning_rate = 0.0009
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    # loop
    for ep in range(max_eps):
        curr_state = torch.ones((N, N)) / 2
        transitions = []
        max = 0

        for t in range(max_dur):
            curr_state_in = torch.reshape(curr_state, (1, 1, N, N))
            pred = torch.squeeze(model(curr_state_in))
            mu = pred[:N**2]
            sigma = torch.exp(pred[N**2:])
            #sigma = torch.ones((N**2)) / 1000
            action = torch.normal(mean=mu, std=sigma)
            prev_state = curr_state
            curr_state = prev_state + torch.reshape(action, (N, N))
            curr_state[curr_state > 1] = 1
            curr_state[curr_state < 0] = 0
            prev_score = utils.h_dec(prev_state.detach().numpy())
            current_score = utils.h_dec(curr_state.detach().numpy())
            reward = current_score - prev_score - 1
            transitions.append((prev_state, action, reward))
            if current_score > max:
                max = current_score
            if current_score > N * N - 1:
                break

        score.append(max)
        reward_batch = torch.Tensor([r for (s, a, r) in transitions]).flip(dims=(0,))
        disc_rewards = discount_rewards(reward_batch, gamma)
        state_batch = torch.stack([s for (s, a, r) in transitions])
        state_batch = state_batch[:, None, :, :]
        action_batch = torch.stack([a for (s, a, r) in transitions])
        pred_batch = model(state_batch)
        loss = loss_fn(action_batch, pred_batch, disc_rewards, N)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(ep, end='\r')

    plt.plot(score)
    plt.grid()
    plt.show()
    print('test works')
    return

def discount_rewards(rewards, gamma = 0.999):
    lenr = len(rewards)
    disc_return = torch.pow(gamma,torch.arange(lenr).float()) * rewards
    disc_return /= disc_return.max()
    return disc_return

def loss_fn(actions, preds, r, N):
    actions = torch.reshape(actions, (actions.size(dim=0), N**2))
    mu = preds[:, :pow(N, 2)]
    sigma = torch.exp(preds[:, pow(N, 2):])
    #sigma = torch.ones((N**2)) / 10
    r = r.unsqueeze(1).repeat(1, N**2)
    pdf_value = torch.exp(-0.5 *((actions - mu) / (sigma))**2) * 1 / (sigma * np.sqrt(2 * np.pi))
    return -1 * torch.sum(r * torch.log(pdf_value + 1e-5))

def main():
    test()
    print('main works')

if __name__=="__main__":
    main()