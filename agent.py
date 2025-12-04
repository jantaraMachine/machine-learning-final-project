# Authored by Athena Osborne and Kali Bateman

from collections import deque
import torch
import random
import numpy as np
from model import 

MAX_MEMORY = 100_100 # Controls the maximum amount of transitions we're allowed to store/act on
BATCH_SIZE = 1000
LR = 0.001 # Learning Rate

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # Epsilon value which controls randomness in action selection
        self.gamma - 0 # Gamma value which controls the importance which the model places on weighting certain outcomes in the near future versus possible outcomes in the far future
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = 

    def get_state(self, game):
        pass

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self):
        pass

    