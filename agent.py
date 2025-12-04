# Authored by Athena Osborne and Kali Bateman
import snake_game.py 
import snake.py 
from collections import deque
import torch
import random
import numpy as np
from model import 

BUSH = 20 
GRASS = 0 
SNAKE = 1 
FOOD = 22

MAX_MEMORY = 100_100 # Controls the maximum amount of transitions we're allowed to store/act on
BATCH_SIZE = 1000
LR = 0.001 # Learning Rate

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # Epsilon value which controls randomness in action selection
        self.gamma - 0 # Gamma value which controls the importance which the model places on weighting certain outcomes in the near future versus possible outcomes in the far future
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = # TODO

    
    # For direction: NORTH = 0 | WEST = 1 | SOUTH = 2 | EAST = 3
    # get the position of the snake for the current state 
    def get_state(self, game, snake, board_state, food):
        #get food location 
        food_pos = food.get_map_pos() 
        food_x, food_y = food_pos

        #get head location of snake 
        head = snake[0].get_map_pos() # this returns the (x,y) position of snake
        head_x, head_y = head 
        point_l = (head_x-1, head_y)
        point_r = (head_x + 1, head_y)
        point_u = (head_x, head_y - 1)
        point_d = (head_x, head_y + 1)

        #get direction of snake 
        direction = snake.get_direction() 
        dir_l = direction == 1
        dir_r = direction == 3
        dir_u = direction == 0 
        dir_d = direction == 2

        #collision if board_state[x][y] returns 1 or 20 
        state = [
            # danger straight 
            (dir_r and (board_state(point_r) == (1 or 20))) or 
            (dir_l and (board_state(point_l) == (1 or 20))) or 
            (dir_u and (board_state(point_u) == (1 or 20))) or 
            (dir_d and (board_state(point_d) == (1 or 20))), 

            # danger right 
            (dir_u and (board_state(point_r) == (1 or 20))) or 
            (dir_d and (board_state(point_l) == (1 or 20))) or 
            (dir_l and (board_state(point_u) == (1 or 20))) or 
            (dir_r and (board_state(point_d) == (1 or 20))), 

            # danger left 
            (dir_d and (board_state(point_r) == (1 or 20))) or 
            (dir_u and (board_state(point_l) == (1 or 20))) or 
            (dir_r and (board_state(point_u) == (1 or 20))) or 
            (dir_l and (board_state(point_d) == (1 or 20))), 

            #move direction 
            dir_l, 
            dir_r, 
            dir_u, 
            dir_d, 

            #food location 
            food_x < head_x, # food left 
            food_x > head_x, # food right 
            food_y > head_y, # food up 
            food_y < head_y # food down 
        ]
        return np.array(state, dtype = int)

        ## Notes: 
        #board_state returns the whole grid 
        # board_state[x][y] this checks the x y position in a certain place on grid 
        # get points next to head of snake in all directions 
        # use Point(head.x - 16, head.y) to simulate the square to the left of the snakes head 
        # to get current direction have each dir_l = game.direction == Direction.LEFT to check current direction 
        # if we call the snake position we get the map positon and then we have to call the map function on it 

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self):
        pass

    