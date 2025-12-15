# Authored by Athena Osborne and Kali Bateman
from collections import deque
import torch
import random
import numpy as np
from model import DQN, QTrainer
import matplotlib.pyplot as plt

BUSH = 20 
GRASS = 0 
SNAKE = 1 
FOOD = 22

MAX_MEMORY = 100_000 # Controls the maximum amount of transitions we're allowed to store/act on
BATCH_SIZE = 1000
LR = 0.001 # Learning Rate

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # Epsilon value which controls randomness in action selection
        self.gamma = 0.9 # Gamma value which controls the importance which the model places on weighting certain outcomes in the near future versus possible outcomes in the far future
        self.memory = deque(maxlen=MAX_MEMORY)
        #create instance of model/trainer
        self.model = DQN(11)
        self.trainer = QTrainer(self.model, lr = LR, gamma=self.gamma) 

    
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
        direction = snake[0].get_direction() 
        dir_l = direction == 1
        dir_r = direction == 3
        dir_u = direction == 0 
        dir_d = direction == 2

        #collision if board_state[x][y] returns 1 or 20 
        state = [
            # danger straight 
            (dir_r and (board_state[point_r[1]][point_r[0]] == SNAKE or board_state[point_r[1]][point_r[0]] == BUSH)) or  
            (dir_l and (board_state[point_l[1]][point_l[0]] == SNAKE or board_state[point_l[1]][point_l[0]] == BUSH)) or
            (dir_u and (board_state[point_u[1]][point_u[0]] == SNAKE or board_state[point_u[1]][point_u[0]] == BUSH)) or
            (dir_d and (board_state[point_d[1]][point_d[0]] == SNAKE or board_state[point_d[1]][point_d[0]] == BUSH)),

            # danger right 
            (dir_u and (board_state[point_r[1]][point_r[0]] == SNAKE or board_state[point_r[1]][point_r[0]] == BUSH)) or 
            (dir_d and (board_state[point_l[1]][point_l[0]] == SNAKE or board_state[point_l[1]][point_l[0]] == BUSH)) or 
            (dir_l and (board_state[point_u[1]][point_u[0]] == SNAKE or board_state[point_u[1]][point_u[0]] == BUSH)) or 
            (dir_r and (board_state[point_d[1]][point_d[0]] == SNAKE or board_state[point_d[1]][point_d[0]] == BUSH)),

            # danger left 
            (dir_d and (board_state[point_r[1]][point_r[0]] == SNAKE or board_state[point_r[1]][point_r[0]] == BUSH)) or 
            (dir_u and (board_state[point_l[1]][point_l[0]] == SNAKE or board_state[point_l[1]][point_l[0]] == BUSH)) or 
            (dir_r and (board_state[point_u[1]][point_u[0]] == SNAKE or board_state[point_u[1]][point_u[0]] == BUSH)) or 
            (dir_l and (board_state[point_d[1]][point_d[0]] == SNAKE or board_state[point_d[1]][point_d[0]] == BUSH)),

            #move direction 
            dir_l, 
            dir_r, 
            dir_u, 
            dir_d, 

            #food location 
            food_x < head_x, # food left 
            food_x > head_x, # food right 
            food_y < head_y, # food up 
            food_y > head_y # food down 
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
        self.memory.append((state, action, reward, next_state, done)) # we want to return one tuple 

    def train_long_memory(self):
        #take variables from memory 
        #checking if we already have 1000 samples 
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) #returns list of tuples 
        else: 
            mini_sample = self.memory 
        
        #we want to put everything together and extracts it 
        states, actions, rewards, next_states, dones = zip(*mini_sample)

        #we have a list of tuples now 
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        


    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done) 

    def get_action(self):
        # we want to do some random moves, the better our model gets = less random moves 

        # the more games the smaller the epsilon gets then we dont use random move 
        self.epsilon = 100 - self.n_games # this doesn't have to be definitive just random val
        final_move = [0,0,0]

        if random.randint(0,200) < self.epsilon: 
            move = random.randint(0, 2) # gives us a random value
            final_move[move] = 1 
        else: 
            #if we dont have any random moves left
            # we want to make the state a tensor 
            state0 = torch.tensor(state, dtype = torch.float) 
            prediction = self.model(state0) 
            #take the raw value array and get max of the highest state in tuple to get the move 
            move = torch.argmax(prediction).item() 
            final_move[move] = 1

        return final_move 

    #define the training state 
    ## not sure if we have already done this 
    def train():
        # keep track of scores
        scores = [] 
        average_scores = [] 
        total_score = 0 
        record = 0 
        # we want to set up an agent 
        agent = Agent() 
        game = snake_game() 

        #create training loop, runs until we quit 
        while True: 
            # get current state 
            state_current = agent.get_state(game)

            #get move based on current state 
            final_move = agent.get_action(state_current)

            #perform move and get new state
            # not sure what is happening with reward but i'm just gonna keep this for now
            ## reward, done, score = game. ??? 
            state_new = agent.get_state(game)

            #we want to train short memory first 
            agent.train_short_memory(state_current, final_move, reward, state_new, done)

            # remeber 
            agent.remember(state_current, final_move, reward, state_new, done)

            if done: 
                #train long memory 
                #trains again on all previous moves 
                # helps with improvement 
                game.reset() # we want to reset the game
                agent.n_games += 1 
                agent.train_long_memory() 

                #check if we have a new high score 
                if score > record: 
                    record = score 
                    #agent.model.save() TODO 

                print('Game', agent.n_games, 'Score', score, 'Record:', record)

                #TODO plot 
                # plot the results from training, number of games and score in snake game when run 

def plot(scores, mean_scores):
    #allows us to plot and see results 
    plt.clf() 
    plt.title('Training Progress')
    plt.xlabel('Game Number')
    plt.ylabel('Score')
    plt.plot(scores, label='Score')
    plt.plot(mean_scores, label = 'Average Score')
    plt.legend() 
    plt.pause(0.1)



if __name__ == '__main__': 
    train() 
    











