class Snake:

    # For direction: NORTH = 0 | WEST = 1 | SOUTH = 2 | EAST = 3
    # For body_part: HEAD = 0 | BODY = 1 | TAIL = 2 | TINY = 3

    def __init__(self, map_pos, direction, body_part):

        self.map_pos = map_pos
        self.direction = direction
        self.body_part = body_part
    
    def get_map_pos(self):
        return self.map_pos
    
    def get_direction(self):
        return self.direction
    
    def get_body_part(self):
        return self.body_part
    
    def change_direction(self, direction):

        NORTH = 0
        WEST = 1
        SOUTH = 2
        EAST = 3

        if direction is not None:

            # If self.direction and diretion are completely opposite, don't update direction
            if (self.direction == NORTH and direction == SOUTH) or \
                (self.direction == SOUTH and direction == NORTH) or \
                (self.direction == WEST and direction == EAST) or \
                (self.direction == EAST and direction == WEST):
                return self.direction

            # If all is well, save the inputted direction as the current direction and return
            # the previous direction
            prev = self.direction
            self.direction = direction

            return prev
        
        # If direction = None, don't update direction
        return self.direction

    def change_body_part(self, body_part):
        self.body_part = body_part
    
    def move(self):

        NORTH = 0
        WEST = 1
        SOUTH = 2

        grid_x = self.map_pos[0]
        grid_y = self.map_pos[1]

        if self.direction == NORTH: # Moves segment up 1 unit
            self.map_pos = [grid_x, grid_y - 1]
        elif self.direction == WEST: # Moves segment left 1 unit
            self.map_pos = [grid_x - 1, grid_y]
        elif self.direction == SOUTH: # Moves segment down 1 unit
            self.map_pos = [grid_x, grid_y + 1]
        else: # Moves segment right 1 unit
            self.map_pos = [grid_x + 1, grid_y]