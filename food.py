from random import randint


class Food:

    def __init__(self, grid_pos):
        self.grid_pos = grid_pos
    
    def get_grid_pos(self):
        return self.grid_pos
    
    def eat(self, snake):

        food_pos = None
        
        while(True):
            passed = True
            
            food_pos = [randint(1, 15), randint(1, 15)]
            for segment in snake:
                if food_pos == segment.get_grid_pos():
                    passed = False
                    break
            if passed == True:
                self.grid_pos = food_pos
                break