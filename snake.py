class Snake:

    # For direction: NORTH = 0 | WEST = 1 | SOUTH = 2 | EAST = 3
    # For body_part: HEAD = 0 | BODY = 1 | TAIL = 2 | TINY = 3

    def __init__(self, grid_pos, direction, body_part):

        self.grid_pos = grid_pos
        self.direction = direction
        self.body_part = body_part
    
    def get_grid_pos(self):
        return self.grid_pos
    
    def get_direction(self):
        return self.direction
    
    def get_body_part(self):
        return self.body_part
    
    def change_direction(self, direction):

        if direction is not None:

            prev = self.direction
            self.direction = direction

            return prev
        
        return self.direction

    def change_type(self, type):
        self.type = type
    
    def move(self):

        NORTH = 0
        WEST = 1
        SOUTH = 2

        grid_x = self.grid_pos[0]
        grid_y = self.grid_pos[1]

        if self.direction == NORTH:
            self.grid_pos = [grid_x, grid_y - 1]
        elif self.direction == WEST:
            self.grid_pos = [grid_x - 1, grid_y]
        elif self.direction == SOUTH:
            self.grid_pos = [grid_x, grid_y + 1]
        else:
            self.grid_pos = [grid_x + 1, grid_y]