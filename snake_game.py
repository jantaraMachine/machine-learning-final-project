import pygame
from random import randint
from copy import deepcopy

from snake import Snake
from food import Food

# Scales the screen and sprites up by this constant so that it's easier for the user to see the game
SCALE = 3

HEAD_N = 0
HEAD_W = 1
HEAD_S = 2
HEAD_E = 3
BONK_N = 4
BONK_W = 5
BONK_S = 6
BONK_E = 7
DEAD_N = 8
DEAD_W = 9
DEAD_S = 10
DEAD_E = 11
EAT_N = 12
EAT_W = 13
EAT_S = 14
EAT_E = 15
TINY_BONK_N = 16
TINY_BONK_W = 17
TINY_BONK_S = 18
TINY_BONK_E = 19
BUSH = 20
GRASS_1 = 21
FOOD = 22
BOX_TL = 23
BOX_TR = 24
BOX_T = 25
BODY_NE = 26
BODY_NW = 27
BODY_SW = 28
BODY_SE = 29
BODY_NS = 30
BODY_WE = 31
TAIL_N = 32
TAIL_W = 33
TAIL_S = 34
TAIL_E = 35
TINY_N = 36
TINY_W = 37
TINY_S = 38
TINY_E = 39
TINY_EAT_N = 40
TINY_EAT_W = 41
TINY_EAT_S = 42
TINY_EAT_E = 43
TINY_DEAD_N = 44
TINY_DEAD_W = 45
TINY_DEAD_S = 46
TINY_DEAD_E = 47
GRASS_2 = 48
GRASS = 49 # Not actually a sprite but is a variable used in the tiles list
BOX_BL = 50
BOX_BR = 51
BOX_B = 52

NORTH = 0
WEST = 1
SOUTH = 2
EAST = 3

HEAD = 0
BODY = 1
TAIL = 2
TINY = 3

# Loads all of the sprites in sprites.png
def load_sprites():

    image = pygame.image.load("sprites.png").convert_alpha()

    sprites = []

    # Iterates through rows and columns of sprites.png
    for row in range (2):
        for col in range (10):

            sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
            sprite.blit(image, (0, 0), (col * 16, row * 16, 16, 16))
            sprite = pygame.transform.scale_by(sprite, SCALE)
            sprites.append(sprite)

            # Adds flipped versions of text box corners (BOX_TL, BOX_TR, BOX_BL, BOX_BR) to sprites list
            if (row == 0 and col == 8) or (row == 1 and col == 8):
                sprites.append(pygame.transform.flip(sprite, True, False))
            # Adds 90 degree rotated snake body (BODY_NS, BODY_WE) to sprites list
            elif row == 1 and col == 1:
                sprites.append(pygame.transform.rotate(sprite, 90))
            # Adds fully rotated parts of the snake (so they can face all four directions) to sprites list
            # Includes, HEAD, TINY, BODY (corners), BONK, DEAD, and TAIL
            elif (row == 0 and col < 5) or (row == 1 and col < 6):
                # Unrotated = NORTH
                sprites.append(pygame.transform.rotate(sprite, 90)) # WEST
                sprites.append(pygame.transform.rotate(sprite, 180)) # SOUTH
                sprites.append(pygame.transform.rotate(sprite, 270)) # EAST
    
    return sprites

# Converts a position on the grid (screen's grid is 17x19) to its appropriate xy-coordinates
# Each sprite is as big as a tile on the grid for reference
# EX: If SCALE = 3, (7, 8) on the screen's grid is (336, 384) in xy-coordinates
def grid(xy_pos):
    # Multiply number by 16 (width of unscaled sprite) times SCALE
    return xy_pos * 16 * SCALE

# A different conversion function that converts a position on the map's grid
# (the grid that the snake traverses on, a 17x17 grid) to its appropriate
# xy-coordinates
# EX: If SCALE = 3, (7, 8) on the map's grid is (336, 480) -- shifted down by 2
# tiles
def map(grid_pos):
    return [grid(grid_pos[0]), grid(2) + grid(grid_pos[1])]

# Initializes snake, old_snake, and food variables
def init():

    # Snake object takes in starting position, starting direction it's going in, and the body type
    # that it is (in this case, snake's head start off as TINY but will change to HEAD as it gains
    # more segments, for now it is only one segment long)
    snake = [Snake([8, 8], NORTH, TINY)] # Length of snake list reflects number of segments

    # Creates a copy of the snake that is used to draw the snake's
    # state before it has moved -- used in particular for drawing
    # the snake during its death animation
    old_snake = deepcopy(snake)

    food_pos = None
    
    # Looks for a random starting position that doesn't intersect with the snake's position
    while(True):
        passed = True
        # Finds random coordinates on grass portion of map
        food_pos = [randint(1, 15), randint(1, 15)]
        # Iterates through all snake segments to verify that food_pos is not the same
        # as any snake's segments
        for segment in snake:
            if food_pos == segment.get_map_pos():
                passed = False
        if passed == True:
            return snake, old_snake, Food(food_pos)

# Updates the snake's and food's position depending on several factors
def update_snake(snake, food, tick, current_direction, tiles, alive):

    # Moves and updates snake's segments' directions only after 12 ticks
    # (time units, can change ticks to make snake move faster or slower)
    if tick == 12:
        # Iterate through all snake's segments
        for i, segment in enumerate(snake):
            # If i == 0, then we're looking at the head of the snake
            if i == 0:
                # Save the previous position -- to be used for creating a new snake segment
                # behind the head if the snake has eaten the food
                prev = snake[0].change_direction(current_direction)
                # Move the head in whatever direction the player is going
                segment.move()
                # Get the current map position of the snake's head
                head_map_pos = segment.get_map_pos()

                # If the head is in the same spot as the food, eat the food
                if head_map_pos == food.get_map_pos():

                    food.eat(snake) # Food will be teleported somewhere else

                    # Get the direction that the head (and the player) is going
                    head_direction = segment.get_direction()

                    # If the snake only has one segment, change the head from TINY to HEAD and add a TAIL behind the head
                    if len(snake) == 1:

                        segment.change_body_part(HEAD)

                        # Uses the direction and position of the HEAD to determine where to place the new TAIL
                        if head_direction == NORTH:
                            snake.insert(1, Snake([head_map_pos[0], head_map_pos[1] + 1], prev, TAIL))
                        elif head_direction == WEST:
                            snake.insert(1, Snake([head_map_pos[0] + 1, head_map_pos[1]], prev, TAIL))
                        elif head_direction == SOUTH:
                            snake.insert(1, Snake([head_map_pos[0], head_map_pos[1] - 1], prev, TAIL))
                        else:
                            snake.insert(1, Snake([head_map_pos[0] - 1, head_map_pos[1]], prev, TAIL))
                    else:
                        # Uses the direction and position of the HEAD to determine where to place the new BODY part
                        if head_direction == NORTH:
                            snake.insert(1, Snake([head_map_pos[0], head_map_pos[1] + 1], prev, BODY))
                        elif head_direction == WEST:
                            snake.insert(1, Snake([head_map_pos[0] + 1, head_map_pos[1]], prev, BODY))
                        elif head_direction == SOUTH:
                            snake.insert(1, Snake([head_map_pos[0], head_map_pos[1] - 1], prev, BODY))
                        else:
                            snake.insert(1, Snake([head_map_pos[0] - 1, head_map_pos[1]], prev, BODY))
                    break
                # If the head is in the same spot as a BUSH (aka the wall), kill the snake and quit the loop
                elif tiles[head_map_pos[0]][head_map_pos[1]] == BUSH:
                    alive = False
                    break
                # If the head is in the same spot as any of its other segments, kill the snake and quit the loop
                else:
                    for j, seg in enumerate(snake):
                        if j != 0:
                            if head_map_pos == seg.get_map_pos():
                                alive = False
                                break
            # Otherwise, move all of the snake's segments according to how the previous segment has moved
            else:
                prev = segment.change_direction(prev)
                segment.move()
        # Return whether the snake is alive or not and reset ticks to 0 (the snake has moved)
        return alive, 0
    else:
        # Return that the snake is alive and add 1 tick (the snake has not moved)
        return alive, tick + 1

# Draws the sprites for the background
def draw_background(screen, sprites):

    screen.fill(color="black")

    # Drawing box -- row 0 and 1
    screen.blit(sprites[BOX_TL], (grid(6), 0))

    for i in range (7, 10):
        screen.blit(sprites[BOX_T], (grid(i), 0))

    screen.blit(sprites[BOX_TR], (grid(10), 0))

    screen.blit(sprites[BOX_BL], (grid(6), grid(1)))

    for i in range (7, 10):
        screen.blit(sprites[BOX_B], (grid(i), grid(1)))

    screen.blit(sprites[BOX_BR], (grid(10), grid(1)))

    # Drawing grass -- rows 2 through 18
    for row in range (2, 19):
        for col in range (17):
            if row == 2 or row == 18:
                screen.blit(sprites[BUSH], (grid(col), grid(row)))
            elif col == 0 or col == 16:
                screen.blit(sprites[BUSH], (grid(col), grid(row)))
            elif row % 2 == 1:
                if col % 2 == 1:
                    screen.blit(sprites[GRASS_1], (grid(col), grid(row)))
                else:
                    screen.blit(sprites[GRASS_2], (grid(col), grid(row)))
            else:
                if col % 2 == 1:
                    screen.blit(sprites[GRASS_2], (grid(col), grid(row)))
                else:
                    screen.blit(sprites[GRASS_1], (grid(col), grid(row)))

# Draws the sprites for the snake
def draw_snake(screen, sprites, snake, food):
    # Iterate through segments of the snake
    for i, segment in enumerate(snake):

        # Get all its data points (direction, body_part, grid_pos)
        direction = segment.get_direction()
        body_part = segment.get_body_part()
        map_pos = segment.get_map_pos()
        position = map(map_pos) # Convert from map position

        # Get the direction of the segment ahead of the current segment to use
        # for proper sprite drawing (specifically for corners)
        ahead_direction = snake[i - 1].get_direction()
        # Get position of food so that we can draw the EAT sprite of the snake
        # when the snake is about to eat the food
        food_pos = food.get_map_pos()

        # Draw the correct sprite for each segment depending on what body type
        # it is, what direction it's going in, and if its body type is BODY,
        # whether to draw a corner sprite and if so, which one -- this depends
        # on the direction of the segment ahead of it.
        # Also draws the EAT sprite if the HEAD is one tile behind of the food in
        # each of the cardinal directions (no implemented sprite if food is diagonal
        # from HEAD).
        if direction == NORTH:
            if body_part == HEAD:
                if food_pos[0] == map_pos[0] and food_pos[1] == map_pos[1] - 1:
                    screen.blit(sprites[EAT_N], (position[0], position[1]))
                else:
                    screen.blit(sprites[HEAD_N], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == NORTH:
                    screen.blit(sprites[BODY_NS], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[BODY_SW], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_SE], (position[0], position[1]))
            elif body_part == TAIL:

                if ahead_direction == NORTH:
                    screen.blit(sprites[TAIL_N], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[TAIL_W], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_E], (position[0], position[1]))
            else:
                if food_pos[0] == map_pos[0] and food_pos[1] == map_pos[1] - 1:
                    screen.blit(sprites[TINY_EAT_N], (position[0], position[1]))
                else:
                    screen.blit(sprites[TINY_N], (position[0], position[1]))
        elif direction == WEST:
            if body_part == HEAD:
                if food_pos[0] == map_pos[0] - 1 and food_pos[1] == map_pos[1]:
                    screen.blit(sprites[EAT_W], (position[0], position[1]))
                else:
                    screen.blit(sprites[HEAD_W], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == NORTH:
                    screen.blit(sprites[BODY_NE], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[BODY_WE], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_SE], (position[0], position[1]))
            elif body_part == TAIL:
                if ahead_direction == NORTH:
                    screen.blit(sprites[TAIL_N], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[TAIL_W], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_S], (position[0], position[1]))
            else:
                if food_pos[0] == map_pos[0] - 1 and food_pos[1] == map_pos[1]:
                    screen.blit(sprites[TINY_EAT_W], (position[0], position[1]))
                else:
                    screen.blit(sprites[TINY_W], (position[0], position[1]))
        elif direction == SOUTH:
            if body_part == HEAD:
                if food_pos[0] == map_pos[0] and food_pos[1] == map_pos[1] + 1:
                    screen.blit(sprites[EAT_S], (position[0], position[1]))
                else:
                    screen.blit(sprites[HEAD_S], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == WEST:
                    screen.blit(sprites[BODY_NW], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[BODY_NS], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_NE], (position[0], position[1]))
            elif body_part == TAIL:
                if ahead_direction == WEST:
                    screen.blit(sprites[TAIL_W], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[TAIL_S], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_E], (position[0], position[1]))
            else:
                if food_pos[0] == map_pos[0] and food_pos[1] == map_pos[1] + 1:
                    screen.blit(sprites[TINY_EAT_S], (position[0], position[1]))
                else:
                    screen.blit(sprites[TINY_S], (position[0], position[1]))
        else:
            if body_part == HEAD:
                if food_pos[0] == map_pos[0] + 1 and food_pos[1] == map_pos[1]:
                    screen.blit(sprites[EAT_E], (position[0], position[1]))
                else:
                    screen.blit(sprites[HEAD_E], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == NORTH:
                    screen.blit(sprites[BODY_NW], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[BODY_SW], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_WE], (position[0], position[1]))
            elif body_part == TAIL:
                if ahead_direction == NORTH:
                    screen.blit(sprites[TAIL_N], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[TAIL_S], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_E], (position[0], position[1]))
            else:
                if food_pos[0] == map_pos[0] + 1 and food_pos[1] == map_pos[1]:
                    screen.blit(sprites[TINY_EAT_E], (position[0], position[1]))
                else:
                    screen.blit(sprites[TINY_E], (position[0], position[1]))

# Draws the sprites for the first part of the death animation --
# replaces the HEAD with a BONK sprite.
# Follows the same logic as draw_snake() without food logic
def dead_1(screen, sprites, a_snake):

    for i, segment in enumerate(a_snake):

        direction = segment.get_direction()
        body_part = segment.get_body_part()
        position = map(segment.get_map_pos())

        ahead_direction = a_snake[i - 1].get_direction()

        if direction == NORTH:
            if body_part == HEAD:
                screen.blit(sprites[BONK_N], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == NORTH:
                    screen.blit(sprites[BODY_NS], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[BODY_SW], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_SE], (position[0], position[1]))
            elif body_part == TAIL:

                if ahead_direction == NORTH:
                    screen.blit(sprites[TAIL_N], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[TAIL_W], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_E], (position[0], position[1]))
            else:
                screen.blit(sprites[TINY_BONK_N], (position[0], position[1]))
        elif direction == WEST:
            if body_part == HEAD:
                screen.blit(sprites[BONK_W], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == NORTH:
                    screen.blit(sprites[BODY_NE], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[BODY_WE], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_SE], (position[0], position[1]))
            elif body_part == TAIL:
                if ahead_direction == NORTH:
                    screen.blit(sprites[TAIL_N], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[TAIL_W], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_S], (position[0], position[1]))
            else:
                screen.blit(sprites[TINY_BONK_W], (position[0], position[1]))
        elif direction == SOUTH:
            if body_part == HEAD:
                screen.blit(sprites[BONK_S], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == WEST:
                    screen.blit(sprites[BODY_NW], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[BODY_NS], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_NE], (position[0], position[1]))
            elif body_part == TAIL:
                if ahead_direction == WEST:
                    screen.blit(sprites[TAIL_W], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[TAIL_S], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_E], (position[0], position[1]))
            else:
                screen.blit(sprites[TINY_BONK_S], (position[0], position[1]))
        else:
            if body_part == HEAD:
                screen.blit(sprites[BONK_E], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == NORTH:
                    screen.blit(sprites[BODY_NW], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[BODY_SW], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_WE], (position[0], position[1]))
            elif body_part == TAIL:
                if ahead_direction == NORTH:
                    screen.blit(sprites[TAIL_N], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[TAIL_S], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_E], (position[0], position[1]))
            else:
                screen.blit(sprites[TINY_BONK_E], (position[0], position[1]))

# Draws the sprites for the second part of the death animation --
# replaces the HEAD with a DEAD sprite.
# Follows the same logic as dead_1()
def dead_2(screen, sprites, a_snake):
    for i, segment in enumerate(a_snake):

        direction = segment.get_direction()
        body_part = segment.get_body_part()
        position = map(segment.get_map_pos())

        ahead_direction = a_snake[i - 1].get_direction()

        if direction == NORTH:
            if body_part == HEAD:
                screen.blit(sprites[DEAD_N], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == NORTH:
                    screen.blit(sprites[BODY_NS], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[BODY_SW], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_SE], (position[0], position[1]))
            elif body_part == TAIL:

                if ahead_direction == NORTH:
                    screen.blit(sprites[TAIL_N], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[TAIL_W], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_E], (position[0], position[1]))
            else:
                screen.blit(sprites[TINY_DEAD_N], (position[0], position[1]))
        elif direction == WEST:
            if body_part == HEAD:
                screen.blit(sprites[DEAD_W], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == NORTH:
                    screen.blit(sprites[BODY_NE], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[BODY_WE], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_SE], (position[0], position[1]))
            elif body_part == TAIL:
                if ahead_direction == NORTH:
                    screen.blit(sprites[TAIL_N], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[TAIL_W], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_S], (position[0], position[1]))
            else:
                screen.blit(sprites[TINY_DEAD_W], (position[0], position[1]))
        elif direction == SOUTH:
            if body_part == HEAD:
                screen.blit(sprites[DEAD_S], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == WEST:
                    screen.blit(sprites[BODY_NW], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[BODY_NS], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_NE], (position[0], position[1]))
            elif body_part == TAIL:
                if ahead_direction == WEST:
                    screen.blit(sprites[TAIL_W], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[TAIL_S], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_E], (position[0], position[1]))
            else:
                screen.blit(sprites[TINY_DEAD_S], (position[0], position[1]))
        else:
            if body_part == HEAD:
                screen.blit(sprites[DEAD_E], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == NORTH:
                    screen.blit(sprites[BODY_NW], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[BODY_SW], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_WE], (position[0], position[1]))
            elif body_part == TAIL:
                if ahead_direction == NORTH:
                    screen.blit(sprites[TAIL_N], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[TAIL_S], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_E], (position[0], position[1]))
            else:
                screen.blit(sprites[TINY_DEAD_E], (position[0], position[1]))

# Draws the food depending on its position
def draw_food(screen, sprites, food):
    position = map(food.get_map_pos()) # Converts from map coordinates
    screen.blit(sprites[FOOD], (position[0], position[1]))

# Main function
def main():

    # Initializing variables -----------------------------------
    width = 272 * SCALE
    height = 304 * SCALE

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")

    sprites = load_sprites()

    # Specifies what kind of tile each map tile is -- used for collision
    tiles = [
        [BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH],
        [BUSH, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BUSH],
        [BUSH, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BUSH],
        [BUSH, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BUSH],
        [BUSH, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BUSH],
        [BUSH, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BUSH],
        [BUSH, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BUSH],
        [BUSH, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BUSH],
        [BUSH, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BUSH],
        [BUSH, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BUSH],
        [BUSH, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BUSH],
        [BUSH, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BUSH],
        [BUSH, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BUSH],
        [BUSH, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BUSH],
        [BUSH, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BUSH],
        [BUSH, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, GRASS, BUSH],
        [BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH, BUSH]
    ]

    snake, old_snake, food = init()

    alive = True

    running = True
    tick = 0
    current_direction = None
    clock = pygame.time.Clock()
    did_death_animation = 0
    # ----------------------------------------------------------

    # Game loop
    while running:
        clock.tick(60) # Keeps game running at 60 fps -- otherwise timing is way off

        # Finds keyboard input
        for event in pygame.event.get():

            # Sets running to false if player quits game
            if event.type == pygame.QUIT:
                running = False
            # Else looks for directional input using arrow keys -- changes direction variable
            # to that of corresponding arrow key
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_direction = NORTH
                elif event.key == pygame.K_LEFT:
                    current_direction = WEST
                elif event.key == pygame.K_DOWN:
                    current_direction = SOUTH
                elif event.key == pygame.K_RIGHT:
                    current_direction = EAST
        # Updates the snake's current condition + living status + tick count if alive
        if alive:
            alive, tick = update_snake(snake, food, tick, current_direction, tiles, alive)

        draw_background(screen, sprites)

        # Draws snake normally if alive
        if alive:
            draw_snake(screen, sprites, snake, food)
            if tick == 0: # Updates old_snake to be current snake after it moves
                old_snake = deepcopy(snake)
        # Draws death animation if snake is dead
        else:
            # dead_1 for 100 frames
            if did_death_animation < 100:
                dead_1(screen, sprites, old_snake)
                did_death_animation += 1
            # dead_2 for remainder
            else:
                dead_2(screen, sprites, old_snake)
        
        draw_food(screen, sprites, food)

        # Updates screen with drawn sprites
        pygame.display.flip()

    # Quits if running = False
    pygame.quit()

if __name__ == "__main__":
    main()