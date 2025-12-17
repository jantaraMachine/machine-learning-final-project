import math
import random
from collections import deque, namedtuple
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import os 


class DQN(nn.Module):

    def __init__(self, n_observations, state_dict=0):
        ## call super initalizer 
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, 3)

        if state_dict != 0:
            self.load_state_dict(state_dict)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)
    
    def save(self):
        torch.save(self.state_dict(), "model.pt")
    
class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state_old, action, reward, next_state, done):
        state = torch.tensor(state_old, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # Predict Q values given current state
        pred = self.model(state)

        target = pred.clone()
        for i in range(len(done)):
            Q_new = reward[i]
            if not done[i]:
                Q_new = reward[i] + self.gamma * torch.max(self.model(next_state[i]))
            target[i][torch.argmax(action[i]).item()] = Q_new
       
        # Predict Q values for a given action, then maximize
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()
 
        self.optimizer.step()

        