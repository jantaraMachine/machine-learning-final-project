from random import randint

class Food:

    def __init__(self, map_pos):
        self.map_pos = map_pos
        self.time_since_eaten = 0
    
    def get_map_pos(self):
        return self.map_pos
    
    def eat(self, snake):

        snake_positions = []

        for segment in snake:
            snake_positions.append(segment.get_map_pos())
        
        while True:

            food_pos = [randint(1, 15), randint(1, 15)]

            if not food_pos in snake_positions:
                self.map_pos = food_pos
                break
        
        self.time_since_eaten = 0
    
    def get_time_since_eaten(self):
        return self.time_since_eaten
    
    def tick(self):
        self.time_since_eaten += 1
    
    def reset_time_since_eaten(self):
        self.time_since_eaten = 0