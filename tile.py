class Tile:

    # For type: GRASS = 0 | BUSH = 1

    def __init__(self, type):
        self.type = type

    def get_type(self):
        return self.type