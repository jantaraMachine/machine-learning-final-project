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
        # Create input layer which connects to hidden layer
        self.layer1 = nn.Linear(n_observations, 128)
        #self.layer2 = nn.Linear(128, 128)

        # Create output layer which takes from hidden layer
        self.layer3 = nn.Linear(128, 3)

        if str(state_dict) != "0":
            # If we were given a pytorch file to load from, use it to load weights into the neural network
            self.load_state_dict(torch.load(state_dict))

    def forward(self, x):
        x = F.relu(self.layer1(x))
        #x = F.relu(self.layer2(x))
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


        # Torch architecture implementation derived from https://www.youtube.com/watch?v=L8ypSXwyBds
        if len(state.shape) == 1:
            # We unsqueeze the tensors so that they can be passed into the network as batches, not datapoints.
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # Predict Q values given current state
        pred = self.model(state)

        # Clone this data structure so that we can assign the target value easily
        target = pred.clone()
        for i in range(len(done)):

            # Grab the q value assuming that this is the last turn.
            Q_new = reward[i]

            if not done[i]:
                # However, if this isn't the final turn, then we want to change the q value based on the Bellman equation
                Q_new = reward[i] + self.gamma * torch.max(self.model(next_state[i]))
            # Given the resulting Q value from the bellman eq (or not), assign the target.
            target[i][torch.argmax(action[i]).item()] = Q_new

            # Debug: print Q values
            print("Q: " + str(Q_new))
       
        # With q values updated...

        # Clear previous gradients from optimizer so as to not interfere with current optimization
        self.optimizer.zero_grad()

        # Calculate the loss function as MSE between the target and predicted Q values
        loss = self.criterion(target, pred)

        # Use the loss value to backpropogate the nn.
        loss.backward()
        self.optimizer.step()

        