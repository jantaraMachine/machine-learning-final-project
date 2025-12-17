import pygame
from sys import argv, exception
from random import randint
from copy import deepcopy

from snake import Snake
from food import Food

from agent import Agent

import matplotlib.pyplot as plt 

plt.ion()

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
ICON = 49
BOX_BL = 50
BOX_BR = 51
BOX_B = 52
INSTRUCTIONS_1 = 53
INSTRUCTIONS_2 = 54
INSTRUCTIONS_3 = 55
INSTRUCTIONS_4 = 56
INSTRUCTIONS_5 = 57
INSTRUCTIONS_6 = 58
ZERO = 59
ONE = 60
EIGHT = 61
NINE = 62
TWO = 63
THREE = 64
SCORE_1 = 65
SCORE_2 = 66
FOUR = 67
FIVE = 68
SCORE_3 = 69
# 70
SIX = 71
SEVEN = 72
# 73
# 74
GAME_OVER_1 = 75
GAME_OVER_2 = 76
YOU_WIN_1 = 77
YOU_WIN_2 = 78
HAPPY_N = 79
HAPPY_W = 80
HAPPY_S = 81
HAPPY_E = 82
BONK_NE = 83 # HEAD N, BODY from E
BONK_NW = 84 # HEAD N, BODY from W
BONK_WN = 85 # HEAD W, BODY from N
BONK_EN = 86 # HEAD E, BODY from N
BONK_ES = 87 # HEAD E, BODY from S
BONK_WS = 88 # HEAD W, BODY from S
BONK_SW = 89 # HEAD S, BODY from W
BONK_SE = 90 # HEAD S, BODY from E
# BONK_SW = 91 | repeat
DEAD_NE = 92
DEAD_NW = 93
DEAD_WN = 94
DEAD_EN = 95
DEAD_ES = 96
DEAD_WS = 97
DEAD_SW = 98
DEAD_SE = 99
# DEAD_SW = 100 | repeat
PAUSED_1 = 101
PAUSED_2 = 102

NORTH = 0
WEST = 1
SOUTH = 2
EAST = 3

HEAD = 0
BODY = 1
TAIL = 2
TINY = 3

GRASS = 0
SNAKE = 1 

# Loads all of the sprites in sprites.png
def load_sprites(scale):

    image = pygame.image.load("sprites.png").convert_alpha()

    sprites = []

    # Iterates through rows and columns of sprites.png
    for row in range (4):
        for col in range (10):

            sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
            sprite.blit(image, (0, 0), (col * 16, row * 16, 16, 16))
            
            if row == 2:

                if col < 6:
                    sprite = pygame.transform.scale_by(sprite, scale)
                    sprites.append(sprite)
                else:
                    for r in range(2):
                        for c in range(2):
                            small_sprite = pygame.Surface((8, 8), pygame.SRCALPHA)
                            small_sprite.blit(sprite, (0, 0), (c * 8, r * 8, 8, 8))
                            small_sprite = pygame.transform.scale_by(small_sprite, scale)
                            sprites.append(small_sprite)
            else:
                sprite = pygame.transform.scale_by(sprite, scale)
                sprites.append(sprite)

                if row < 2:
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
                        for i in range(1, 4):
                            sprites.append(pygame.transform.rotate(sprite, 90 * i))
                elif row == 3:
                    if col == 4:
                        # Unrotated = NORTH
                        for i in range(1, 4):
                            sprites.append(pygame.transform.rotate(sprite, 90 * i))
                    elif col > 4 and col < 7:

                        current_sprite = sprite

                        for i in range(1, 5):

                            sprites.append(pygame.transform.flip(current_sprite, True, False))
                            rotated = pygame.transform.rotate(current_sprite, 90 * i)
                            sprites.append(rotated)
                            current_sprite = rotated

    return sprites

# Converts a position on the grid (screen's grid is 17x19) to its appropriate xy-coordinates
# Each sprite is as big as a tile on the grid for reference
# EX: If scale = 3, (7, 8) on the screen's grid is (336, 384) in xy-coordinates
def grid(scale, grid_pos):
    # Multiply number by 16 (width of unscaled sprite) times scale
    return grid_pos * 16 * scale

def micro_grid(scale, micro_grid_pos):
    return micro_grid_pos * 8 * scale

# A different conversion function that converts a position on the map's grid
# (the grid that the snake traverses on, a 17x17 grid) to its appropriate
# xy-coordinates
# EX: If scale = 3, (7, 8) on the map's grid is (336, 480) -- shifted down by 2
# tiles
def map(scale, map_pos):
    return [grid(scale, map_pos[0]), grid(scale, 2) + grid(scale, map_pos[1])]

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
def update_snake(snake, food, tick, current_direction, tiles, alive, score, dead_head_direction):

    reward = 0

    # Moves and updates snake's segments' directions only after 12 ticks
    # (time units, can change ticks to make snake move faster or slower)
    if tick == 12:

        food.tick()

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
                # Get the direction that the head (and the player) is going
                head_direction = segment.get_direction()

                # If the head is in the same spot as the food, eat the food
                if head_map_pos == food.get_map_pos():

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
                        
                    food.eat(snake) # Food will be teleported somewhere else
                    score += 1

                    break
                # If the head is in the same spot as a BUSH (aka the wall), kill the snake and quit the loop
                elif tiles[head_map_pos[0]][head_map_pos[1]] == BUSH:
                    alive = False
                    dead_head_direction = head_direction
                    break
                # If the head is in the same spot as any of its other segments, kill the snake and quit the loop
                else:
                    for j, seg in enumerate(snake):
                        if j != 0:
                            if head_map_pos == seg.get_map_pos():
                                alive = False
                                dead_head_direction = head_direction
                                break
            # Otherwise, move all of the snake's segments according to how the previous segment has moved
            else:
                prev = segment.change_direction(prev)
                segment.move()
        # Return whether the snake is alive or not and reset ticks to 0 (the snake has moved)
        return alive, 0, score, dead_head_direction
    else:
        # Return that the snake is alive and add 1 tick (the snake has not moved)
        return alive, tick + 1, score, dead_head_direction

def get_digit_sprite(digit):

    if digit == 0:
        return ZERO
    elif digit == 1:
        return ONE
    elif digit == 2:
        return TWO
    elif digit == 3:
        return THREE
    elif digit == 4:
        return FOUR
    elif digit == 5:
        return FIVE
    elif digit == 6:
        return SIX
    elif digit == 7:
        return SEVEN
    elif digit == 8:
        return EIGHT
    return NINE

# Draws the sprites for the background
def draw_background(scale, screen, sprites, score, alive, pause, won):

    screen.fill(color="black")

    screen.blit(sprites[INSTRUCTIONS_1], (0, 0))
    screen.blit(sprites[INSTRUCTIONS_2], (grid(scale, 1), 0))
    screen.blit(sprites[INSTRUCTIONS_3], (grid(scale, 2), 0))
    screen.blit(sprites[INSTRUCTIONS_4], (grid(scale, 3), 0))
    screen.blit(sprites[INSTRUCTIONS_5], (grid(scale, 2), grid(scale, 1)))
    screen.blit(sprites[INSTRUCTIONS_6], (grid(scale, 3), grid(scale, 1)))

    # Drawing box -- row 0 and 1
    screen.blit(sprites[BOX_TL], (grid(scale, 6), 0))

    for i in range (7, 10):
        screen.blit(sprites[BOX_T], (grid(scale, i), 0))

    screen.blit(sprites[BOX_TR], (grid(scale, 10), 0))

    screen.blit(sprites[BOX_BL], (grid(scale, 6), grid(scale, 1)))

    for i in range (7, 10):
        screen.blit(sprites[BOX_B], (grid(scale, i), grid(scale, 1)))

    screen.blit(sprites[BOX_BR], (grid(scale, 10), grid(scale, 1)))

    screen.blit(sprites[SCORE_1], (micro_grid(scale, 13), grid(scale, 1)))
    screen.blit(sprites[SCORE_2], (micro_grid(scale, 14), grid(scale, 1)))
    screen.blit(sprites[SCORE_3], (micro_grid(scale, 15), grid(scale, 1)))

    digits = [int(digit) for digit in str(score)]
    
    ones = None
    tens = None
    hundreds = None

    if score < 10:
        ones = digits[0]
    elif score < 100:
        ones = digits[1]
        tens = digits[0]
    else:
        ones = digits[2]
        tens = digits[1]
        hundreds = digits[0]
    
    screen.blit(sprites[get_digit_sprite(ones)], (micro_grid(scale, 18), grid(scale, 1)))
    
    if tens is not None:
        screen.blit(sprites[get_digit_sprite(tens)], (micro_grid(scale, 17), grid(scale, 1)))
    
    if hundreds is not None:
        screen.blit(sprites[get_digit_sprite(hundreds)], (micro_grid(scale, 16), grid(scale, 1)))
    
    if not alive:
        screen.blit(sprites[GAME_OVER_1], (micro_grid(scale, 15), 0))
        screen.blit(sprites[GAME_OVER_2], (micro_grid(scale, 17), 0))
    
    if pause:
        screen.blit(sprites[PAUSED_1], (micro_grid(scale, 15), 0))
        screen.blit(sprites[PAUSED_2], (micro_grid(scale, 17), 0))
    
    if won:
        screen.blit(sprites[YOU_WIN_1], (micro_grid(scale, 15), 0))
        screen.blit(sprites[YOU_WIN_2], (micro_grid(scale, 17), 0))
        
    # Drawing grass -- rows 2 through 18
    for row in range (2, 19):
        for col in range (17):
            if row == 2 or row == 18:
                screen.blit(sprites[BUSH], (grid(scale, col), grid(scale, row)))
            elif col == 0 or col == 16:
                screen.blit(sprites[BUSH], (grid(scale, col), grid(scale, row)))
            elif row % 2 == 1:
                if col % 2 == 1:
                    screen.blit(sprites[GRASS_1], (grid(scale, col), grid(scale, row)))
                else:
                    screen.blit(sprites[GRASS_2], (grid(scale, col), grid(scale, row)))
            else:
                if col % 2 == 1:
                    screen.blit(sprites[GRASS_2], (grid(scale, col), grid(scale, row)))
                else:
                    screen.blit(sprites[GRASS_1], (grid(scale, col), grid(scale, row)))

# Draws the sprites for the snake
def draw_snake(scale, screen, sprites, snake, food):
    # Iterate through segments of the snake
    for i, segment in enumerate(snake):

        # Get all its data points (direction, body_part, grid_pos)
        direction = segment.get_direction()
        body_part = segment.get_body_part()
        map_pos = segment.get_map_pos()
        position = map(scale, map_pos) # Convert from map position

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
def dead_1(scale, screen, sprites, a_snake, dead_head_direction):
    for i, segment in enumerate(a_snake):

        direction = segment.get_direction()
        body_part = segment.get_body_part()
        position = map(scale, segment.get_map_pos())

        ahead_direction = a_snake[i - 1].get_direction()

        if body_part == TINY:
            if dead_head_direction == NORTH:
                screen.blit(sprites[TINY_BONK_N], (position[0], position[1]))
            elif dead_head_direction == WEST:
                screen.blit(sprites[TINY_BONK_W], (position[0], position[1]))
            elif dead_head_direction == SOUTH:
                screen.blit(sprites[TINY_BONK_S], (position[0], position[1]))
            else:
                screen.blit(sprites[TINY_BONK_E], (position[0], position[1]))
        else:
            if direction == NORTH:
                if body_part == HEAD:
                    if dead_head_direction == NORTH:
                        screen.blit(sprites[BONK_N], (position[0], position[1]))
                    elif dead_head_direction == WEST:
                        screen.blit(sprites[BONK_WS], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BONK_ES], (position[0], position[1]))
                elif body_part == BODY:
                    if ahead_direction == NORTH:
                        screen.blit(sprites[BODY_NS], (position[0], position[1]))
                    elif ahead_direction == WEST:
                        screen.blit(sprites[BODY_SW], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BODY_SE], (position[0], position[1]))
                else:
                    if ahead_direction == NORTH:
                        screen.blit(sprites[TAIL_N], (position[0], position[1]))
                    elif ahead_direction == WEST:
                        screen.blit(sprites[TAIL_W], (position[0], position[1]))
                    else:
                        screen.blit(sprites[TAIL_E], (position[0], position[1]))
            elif direction == WEST:
                if body_part == HEAD:
                    if dead_head_direction == NORTH:
                        screen.blit(sprites[BONK_NE], (position[0], position[1]))
                    elif dead_head_direction == WEST:
                        screen.blit(sprites[BONK_W], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BONK_SE], (position[0], position[1]))
                elif body_part == BODY:
                    if ahead_direction == NORTH:
                        screen.blit(sprites[BODY_NE], (position[0], position[1]))
                    elif ahead_direction == WEST:
                        screen.blit(sprites[BODY_WE], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BODY_SE], (position[0], position[1]))
                else:
                    if ahead_direction == NORTH:
                        screen.blit(sprites[TAIL_N], (position[0], position[1]))
                    elif ahead_direction == WEST:
                        screen.blit(sprites[TAIL_W], (position[0], position[1]))
                    else:
                        screen.blit(sprites[TAIL_S], (position[0], position[1]))
            elif direction == SOUTH:
                if body_part == HEAD:
                    if dead_head_direction == WEST:
                        screen.blit(sprites[BONK_WN], (position[0], position[1]))
                    elif dead_head_direction == SOUTH:
                        screen.blit(sprites[BONK_S], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BONK_EN], (position[0], position[1]))
                elif body_part == BODY:
                    if ahead_direction == WEST:
                        screen.blit(sprites[BODY_NW], (position[0], position[1]))
                    elif ahead_direction == SOUTH:
                        screen.blit(sprites[BODY_NS], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BODY_NE], (position[0], position[1]))
                else:
                    if ahead_direction == WEST:
                        screen.blit(sprites[TAIL_W], (position[0], position[1]))
                    elif ahead_direction == SOUTH:
                        screen.blit(sprites[TAIL_S], (position[0], position[1]))
                    else:
                        screen.blit(sprites[TAIL_E], (position[0], position[1]))
            else:
                if body_part == HEAD:
                    if dead_head_direction == NORTH:
                        screen.blit(sprites[BONK_NW], (position[0], position[1]))
                    elif dead_head_direction == SOUTH:
                        screen.blit(sprites[BONK_SW], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BONK_E], (position[0], position[1]))
                elif body_part == BODY:
                    if ahead_direction == NORTH:
                        screen.blit(sprites[BODY_NW], (position[0], position[1]))
                    elif ahead_direction == SOUTH:
                        screen.blit(sprites[BODY_SW], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BODY_WE], (position[0], position[1]))
                else:
                    if ahead_direction == NORTH:
                        screen.blit(sprites[TAIL_N], (position[0], position[1]))
                    elif ahead_direction == SOUTH:
                        screen.blit(sprites[TAIL_S], (position[0], position[1]))
                    else:
                        screen.blit(sprites[TAIL_E], (position[0], position[1]))

# Draws the sprites for the second part of the death animation --
# replaces the HEAD with a DEAD sprite.
# Follows the same logic as dead_1()
def dead_2(scale, screen, sprites, a_snake, dead_head_direction):
    for i, segment in enumerate(a_snake):

        direction = segment.get_direction()
        body_part = segment.get_body_part()
        position = map(scale, segment.get_map_pos())

        ahead_direction = a_snake[i - 1].get_direction()

        if body_part == TINY:
            if dead_head_direction == NORTH:
                screen.blit(sprites[TINY_DEAD_N], (position[0], position[1]))
            elif dead_head_direction == WEST:
                screen.blit(sprites[TINY_DEAD_W], (position[0], position[1]))
            elif dead_head_direction == SOUTH:
                screen.blit(sprites[TINY_DEAD_S], (position[0], position[1]))
            else:
                screen.blit(sprites[TINY_DEAD_E], (position[0], position[1]))
        else:
            if direction == NORTH:
                if body_part == HEAD:
                    if dead_head_direction == NORTH:
                        screen.blit(sprites[DEAD_N], (position[0], position[1]))
                    elif dead_head_direction == WEST:
                        screen.blit(sprites[DEAD_WS], (position[0], position[1]))
                    else:
                        screen.blit(sprites[DEAD_ES], (position[0], position[1]))
                elif body_part == BODY:
                    if ahead_direction == NORTH:
                        screen.blit(sprites[BODY_NS], (position[0], position[1]))
                    elif ahead_direction == WEST:
                        screen.blit(sprites[BODY_SW], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BODY_SE], (position[0], position[1]))
                else:
                    if ahead_direction == NORTH:
                        screen.blit(sprites[TAIL_N], (position[0], position[1]))
                    elif ahead_direction == WEST:
                        screen.blit(sprites[TAIL_W], (position[0], position[1]))
                    else:
                        screen.blit(sprites[TAIL_E], (position[0], position[1]))
            elif direction == WEST:
                if body_part == HEAD:
                    if dead_head_direction == NORTH:
                        screen.blit(sprites[DEAD_NE], (position[0], position[1]))
                    elif dead_head_direction == WEST:
                        screen.blit(sprites[DEAD_W], (position[0], position[1]))
                    else:
                        screen.blit(sprites[DEAD_SE], (position[0], position[1]))
                elif body_part == BODY:
                    if ahead_direction == NORTH:
                        screen.blit(sprites[BODY_NE], (position[0], position[1]))
                    elif ahead_direction == WEST:
                        screen.blit(sprites[BODY_WE], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BODY_SE], (position[0], position[1]))
                else:
                    if ahead_direction == NORTH:
                        screen.blit(sprites[TAIL_N], (position[0], position[1]))
                    elif ahead_direction == WEST:
                        screen.blit(sprites[TAIL_W], (position[0], position[1]))
                    else:
                        screen.blit(sprites[TAIL_S], (position[0], position[1]))
            elif direction == SOUTH:
                if body_part == HEAD:
                    if dead_head_direction == WEST:
                        screen.blit(sprites[DEAD_WN], (position[0], position[1]))
                    elif dead_head_direction == SOUTH:
                        screen.blit(sprites[DEAD_S], (position[0], position[1]))
                    else:
                        screen.blit(sprites[DEAD_EN], (position[0], position[1]))
                elif body_part == BODY:
                    if ahead_direction == WEST:
                        screen.blit(sprites[BODY_NW], (position[0], position[1]))
                    elif ahead_direction == SOUTH:
                        screen.blit(sprites[BODY_NS], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BODY_NE], (position[0], position[1]))
                else:
                    if ahead_direction == WEST:
                        screen.blit(sprites[TAIL_W], (position[0], position[1]))
                    elif ahead_direction == SOUTH:
                        screen.blit(sprites[TAIL_S], (position[0], position[1]))
                    else:
                        screen.blit(sprites[TAIL_E], (position[0], position[1]))
            else:
                if body_part == HEAD:
                    if dead_head_direction == NORTH:
                        screen.blit(sprites[DEAD_NW], (position[0], position[1]))
                    elif dead_head_direction == SOUTH:
                        screen.blit(sprites[DEAD_SW], (position[0], position[1]))
                    else:
                        screen.blit(sprites[DEAD_E], (position[0], position[1]))
                elif body_part == BODY:
                    if ahead_direction == NORTH:
                        screen.blit(sprites[BODY_NW], (position[0], position[1]))
                    elif ahead_direction == SOUTH:
                        screen.blit(sprites[BODY_SW], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BODY_WE], (position[0], position[1]))
                else:
                    if ahead_direction == NORTH:
                        screen.blit(sprites[TAIL_N], (position[0], position[1]))
                    elif ahead_direction == SOUTH:
                        screen.blit(sprites[TAIL_S], (position[0], position[1]))
                    else:
                        screen.blit(sprites[TAIL_E], (position[0], position[1]))

# Draws the happy winning snake
def win(scale, screen, sprites, a_snake):
    for i, segment in enumerate(a_snake):

        # Get all its data points (direction, body_part, grid_pos)
        direction = segment.get_direction()
        body_part = segment.get_body_part()
        map_pos = segment.get_map_pos()
        position = map(scale, map_pos) # Convert from map position

        # Get the direction of the segment ahead of the current segment to use
        # for proper sprite drawing (specifically for corners)
        ahead_direction = a_snake[i - 1].get_direction()

        # Draw the correct sprite for each segment depending on what body type
        # it is, what direction it's going in, and if its body type is BODY,
        # whether to draw a corner sprite and if so, which one -- this depends
        # on the direction of the segment ahead of it.
        # Also draws the EAT sprite if the HEAD is one tile behind of the food in
        # each of the cardinal directions (no implemented sprite if food is diagonal
        # from HEAD).
        if direction == NORTH:
            if body_part == HEAD:
                screen.blit(sprites[HAPPY_N], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == NORTH:
                    screen.blit(sprites[BODY_NS], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[BODY_SW], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_SE], (position[0], position[1]))
            else:

                if ahead_direction == NORTH:
                    screen.blit(sprites[TAIL_N], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[TAIL_W], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_E], (position[0], position[1]))
        elif direction == WEST:
            if body_part == HEAD:
                screen.blit(sprites[HAPPY_W], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == NORTH:
                    screen.blit(sprites[BODY_NE], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[BODY_WE], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_SE], (position[0], position[1]))
            else:
                if ahead_direction == NORTH:
                    screen.blit(sprites[TAIL_N], (position[0], position[1]))
                elif ahead_direction == WEST:
                    screen.blit(sprites[TAIL_W], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_S], (position[0], position[1]))
        elif direction == SOUTH:
            if body_part == HEAD:
                screen.blit(sprites[HAPPY_S], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == WEST:
                    screen.blit(sprites[BODY_NW], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[BODY_NS], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_NE], (position[0], position[1]))
            else:
                if ahead_direction == WEST:
                    screen.blit(sprites[TAIL_W], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[TAIL_S], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_E], (position[0], position[1]))
        else:
            if body_part == HEAD:
                screen.blit(sprites[HAPPY_E], (position[0], position[1]))
            elif body_part == BODY:
                if ahead_direction == NORTH:
                    screen.blit(sprites[BODY_NW], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[BODY_SW], (position[0], position[1]))
                else:
                    screen.blit(sprites[BODY_WE], (position[0], position[1]))
            else:
                if ahead_direction == NORTH:
                    screen.blit(sprites[TAIL_N], (position[0], position[1]))
                elif ahead_direction == SOUTH:
                    screen.blit(sprites[TAIL_S], (position[0], position[1]))
                else:
                    screen.blit(sprites[TAIL_E], (position[0], position[1]))

# Draws the food depending on its position
def draw_food(scale, screen, sprites, food):
    position = map(scale, food.get_map_pos()) # Converts from map coordinates
    screen.blit(sprites[FOOD], (position[0], position[1]))

# Returns board state
def get_board_state(tiles, snake, food):
    from copy import deepcopy
    board_state = deepcopy(tiles)

    for segment in snake:
        snake_pos = segment.get_map_pos()
        board_state[snake_pos[1]][snake_pos[0]] = SNAKE
    
    food_pos = food.get_map_pos()

    board_state[food_pos[1]][food_pos[0]] = FOOD

    return board_state

def player_mode(scale):

    # Initializing variables -----------------------------------
    width = 272 * scale
    height = 304 * scale

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")

    sprites = load_sprites(scale)

    pygame.display.set_icon(sprites[ICON])

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
    score = 0
    pause = False
    dead_head_direction = None
    won = False
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
                elif event.key == pygame.K_SPACE:
                    if not alive or won:
                        alive = True
                        snake, old_snake, food = init()
                        did_death_animation = 0
                        current_direction = NORTH
                        won = False
                        score = 0
                    elif pause:
                        pause = False
                    else:
                        pause = True
        # Updates the snake's current condition + living status + tick count if alive
        if alive and not pause and not won:
            alive, tick, score, dead_head_direction = update_snake(snake, food, tick, current_direction, tiles, alive, score, dead_head_direction)

        draw_background(scale, screen, sprites, score, alive, pause, won)

        if score == 225:
            won = True

        if not won:
            # Draws snake normally if alive
            if alive:
                draw_snake(scale, screen, sprites, snake, food)
                if tick == 0: # Updates old_snake to be current snake after it moves
                    old_snake = deepcopy(snake)
            # Draws death animation if snake is dead
            else:
                
                # dead_1 for 100 frames
                if did_death_animation < 100:
                    dead_1(scale, screen, sprites, old_snake, dead_head_direction)
                    did_death_animation += 1
                # dead_2 for remainder
                else:
                    dead_2(scale, screen, sprites, old_snake, dead_head_direction)
            
            draw_food(scale, screen, sprites, food)
        else:
            win(scale, screen, sprites, snake)

        # Updates screen with drawn sprites
        pygame.display.flip()

    # Quits if running = False
    pygame.quit()

def ai_mode(scale, epochs, num_subtract, punish_time, death_time):

    # Initializing variables -----------------------------------
    width = 272 * scale
    height = 304 * scale

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")

    sprites = load_sprites(scale)

    pygame.display.set_icon(sprites[ICON])

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

    # Initialize clock
    clock = pygame.time.Clock()

    # Initialize plots for scores
    plot_scores = []
    plot_mean_scores = []

    # Initialize high score metric
    record = 0

    # ----------------------------------------------------------

    for i in range(epochs):

        print(f"Epoch: {i}")

        snake, _, food = init()

        alive = True

        tick = 0
        current_direction = None
        score = 0

        learning_score = 0

        total_score = 0
        
        agent = Agent()

        rewardSum = 0
    

        while(alive):

            reward = 1 # Set the default reward to be 1. This provides the snake a short and long term incentive to stay alive.

            board_state = get_board_state(tiles, snake, food)

            #clock.tick(60) # Keeps game running at 60 fps -- otherwise timing is way off

            # Set the old state as the current state for access next loop
            state_old = agent.get_state(None, snake, board_state, food)

            pygame.event.pump() # Prevents window from becoming unresponsive
            
            # TODO on getting AI's directional input -- setting current_direction to NORTH for now

            final_move = agent.get_action(state_old) # Get the AI's move based on its state

            # Set the current direction based on this move
            #changed to make the snake actually move and not go the same direction 
            clockwise = [NORTH, EAST, SOUTH, WEST]
            idx = clockwise.index(snake[0].get_direction())

            #right turn 
            if final_move[1] == 1: 
                current_direction = clockwise[(idx + 1)%4]
            elif final_move[2] == 1: 
                current_direction = clockwise[(idx - 1)%4]
            else: 
                current_direction = snake[0].get_direction() 

            time_to_eat = food.get_time_since_eaten()

            # Updates the snake's current condition
            alive, tick, score, _ = update_snake(snake, food, tick, current_direction, tiles, alive, score, None)

            #get new board state after it has moved 
            board_state = get_board_state(tiles, snake, food)

            time_since_eaten = food.get_time_since_eaten()

            if time_since_eaten == 0: # If the snake ate the food this turn, give it a higher reward. This incentivises the snake to go for the food
                reward = 100
            elif time_since_eaten == punish_time: # If the snake exceeds a certain number of hyperparametrized steps without eating the apple, punish the snake on this turn.
                reward = -num_subtract
                food.reset_time_since_eaten()
            elif time_since_eaten == death_time: # Straight up just kill the snake if it exceeds a certain hyperparametrized turn count without eating
                alive = False

            if not alive:
                reward = -10000 # Dying should always be an overriding punishment
            
            state_new = agent.get_state(None, snake, board_state, food) # Get the new state after moving and score update

            agent.train_short_memory(state_old, final_move, reward, state_new, alive) # train the short term memory based on what happened this turn

            rewardSum += reward

            draw_background(scale, screen, sprites, score, alive, False, False)

            draw_snake(scale, screen, sprites, snake, food)
            draw_food(scale, screen, sprites, food)

            # This version does not bother drawing the death animation when dying, so snake will intersect with the wall
            # briefly before dying in this version.

            pygame.display.flip()
        
        # Once the epoch is over, print the rewardsum
        print("rewardSum: " + str(rewardSum))

        # What are we doing with learning_score? Might be obsolete
        learning_score += score

        # If dead, update long term memory
        agent.n_games += 1
        agent.train_long_memory()

        # Update the high score if necessary
        if score > record:
            record = score
            # agent.model.save()
        
        plot_scores.append(rewardSum)
        total_score = sum(plot_scores)
        mean_score = total_score / agent.n_games
        plot_mean_scores.append(mean_score)
        plot2(plot_scores, plot_mean_scores) 
    
    print("High score: " + str(record))

    pygame.quit()

def plot(scores, mean_scores):
    '''
    Function to display a live plot 
    '''

    plt.style.use('_mpl-gallery')

    #allows us to plot and see results 
    plt.subplot()
    plt.clf() 
    plt.title('Training Progress')
    plt.xlabel('Game Number')
    plt.ylabel('Reward Score')
    plt.plot(scores, label='Score')
    plt.plot(mean_scores, label = 'Average Score')
    plt.legend() 
    plt.pause(0.1)

    plt.draw()


# Derived from https://stackoverflow.com/questions/16446443/live-updating-with-matplotlib
def plot2(scores, mean_scores):

    # Create list with numbers for the game
    Y = [x+1 for x in range(len(scores))]

    plt.ion()
    graph = plt.plot(Y, scores)[0]

    graph.set_ydata(scores)
    plt.draw()
    plt.pause(0.01)





# Main function
def main():

    # Command line format: python snake_game scale num_epochs num_subtract punish_time

    scale = None
    epochs = None
    num_subtract = None
    punish_time = None
    death_time = None

    num_args = len(argv)

    if num_args > 1:

        scale = argv[1]

        if num_args == 6:
            epochs = argv[2]
            num_subtract = argv[3]
            punish_time = argv[4]
            death_time = argv[5]

            try:
                epochs = int(epochs)
            except TypeError:
                print("All command line arguments must be integers.")
            try:
                num_subtract = int(num_subtract)
            except TypeError:
                print("All command line arguments must be integers.")
            try:
                punish_time = int(punish_time)
            except TypeError:
                print("All command line arguments must be integers.")
            try:
                death_time = int(death_time)
            except TypeError:
                print("All command line arguments must be integers.")
        try:
            scale = int(scale)
        except TypeError:
            print("All command line arguments must be integers.")

    else:
        scale = 3

    if num_args < 6:
        player_mode(scale)
    else:
        ai_mode(scale, epochs, num_subtract, punish_time, death_time)

if __name__ == "__main__":
    main()