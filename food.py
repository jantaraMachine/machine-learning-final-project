from random import randint

class Food:

    def __init__(self, map_pos):
        self.map_pos = map_pos
    
    def get_map_pos(self):
        return self.map_pos
    
    def eat(self, snake):

        food_pos = None
        
        while(True):

            passed = True

            # Finds random coordinates on grass portion of map
            food_pos = [randint(1, 15), randint(1, 15)]
            # Iterates through all snake segments to verify that food_pos is not the same
            # as any snake's segments
            for segment in snake:
                if food_pos == segment.get_map_pos():
                    passed = False
                    break
            if passed == True:
                self.map_pos = food_pos
                break