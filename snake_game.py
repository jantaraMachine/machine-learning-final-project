import pygame
from random import randint
from copy import deepcopy
from time import sleep

from snake import Snake
from food import Food

SCALE = 3

def load_sprites():

    image = pygame.image.load("sprites.png").convert_alpha()

    sprites = []

    for row in range (2):
        for col in range (10):

            sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
            sprite.blit(image, (0, 0), (col * 16, row * 16, 16, 16))
            sprite = pygame.transform.scale_by(sprite, SCALE)
            sprites.append(sprite)

            if (row == 0 and col == 8) or (row == 1 and col == 8):
                sprites.append(pygame.transform.flip(sprite, True, False))
            elif row == 1 and col == 1:
                sprites.append(pygame.transform.rotate(sprite, 90))
            elif (row == 0 and col < 5) or (row == 1 and col < 6):
                sprites.append(pygame.transform.rotate(sprite, 90))
                sprites.append(pygame.transform.rotate(sprite, 180))
                sprites.append(pygame.transform.rotate(sprite, 270))
    
    return sprites

def grid(num):
    return num * 16 * SCALE

def translate(grid_pos):
    return [grid(grid_pos[0]), grid(2) + grid(grid_pos[1])]

def main():

    width = 272 * SCALE
    height = 304 * SCALE

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")

    sprites = load_sprites()

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
    GRASS = 49
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
    
    def init():

        snake = [Snake([8, 8], NORTH, TINY)]

        old_snake = deepcopy(snake)

        food_pos = None
        passed = True
        
        while(True):
            
            food_pos = [randint(1, 15), randint(1, 15)]
            for segment in snake:
                if food_pos == segment.get_grid_pos():
                    passed = False
            if passed == True:
                return snake, old_snake, Food(food_pos)

    def draw_background():

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

    def update_snake(tick, current_direction, tiles, alive):

        if tick == 12:
            prev = snake[0].change_direction(current_direction)
            for i, segment in enumerate(snake):
                if i == 0:
                    segment.move()
                    grid_pos = segment.get_grid_pos()
                    if grid_pos == food.get_grid_pos():
                        food.eat(snake)

                        head_direction = segment.get_direction()
                        head_grid_pos = segment.get_grid_pos()

                        if len(snake) == 1:

                            segment.change_body_part(HEAD)

                            if head_direction == NORTH:
                                snake.insert(1, Snake([head_grid_pos[0], head_grid_pos[1] + 1], prev, TAIL))
                            elif head_direction == WEST:
                                snake.insert(1, Snake([head_grid_pos[0] + 1, head_grid_pos[1]], prev, TAIL))
                            elif head_direction == SOUTH:
                                snake.insert(1, Snake([head_grid_pos[0], head_grid_pos[1] - 1], prev, TAIL))
                            else:
                                snake.insert(1, Snake([head_grid_pos[0] - 1, head_grid_pos[1]], prev, TAIL))
                        else:
                            if head_direction == NORTH:
                                snake.insert(1, Snake([head_grid_pos[0], head_grid_pos[1] + 1], prev, BODY))
                            elif head_direction == WEST:
                                snake.insert(1, Snake([head_grid_pos[0] + 1, head_grid_pos[1]], prev, BODY))
                            elif head_direction == SOUTH:
                                snake.insert(1, Snake([head_grid_pos[0], head_grid_pos[1] - 1], prev, BODY))
                            else:
                                snake.insert(1, Snake([head_grid_pos[0] - 1, head_grid_pos[1]], prev, BODY))
                        break
                    elif tiles[grid_pos[0]][grid_pos[1]] == BUSH:
                        alive = False
                        break
                    else:
                        for j, seg in enumerate(snake):
                            if j != 0:
                                if grid_pos == seg.get_grid_pos():
                                    alive = False
                                    break
                else:
                    prev = segment.change_direction(prev)
                    segment.move()
            return alive, 0
        else:
            return alive, tick + 1

    def draw_snake(a_snake, food):
        for i, segment in enumerate(a_snake):

            direction = segment.get_direction()
            body_part = segment.get_body_part()
            grid_pos = segment.get_grid_pos()
            position = translate(segment.get_grid_pos())

            ahead_direction = a_snake[i - 1].get_direction()
            food_pos = food.get_grid_pos()

            if direction == NORTH:
                if body_part == HEAD:
                    if food_pos[0] == grid_pos[0] and food_pos[1] == grid_pos[1] - 1:
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
                    if food_pos[0] == grid_pos[0] and food_pos[1] == grid_pos[1] - 1:
                        screen.blit(sprites[TINY_EAT_N], (position[0], position[1]))
                    else:
                        screen.blit(sprites[TINY_N], (position[0], position[1]))
            elif direction == WEST:
                if body_part == HEAD:
                    if food_pos[0] == grid_pos[0] - 1 and food_pos[1] == grid_pos[1]:
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
                    if food_pos[0] == grid_pos[0] - 1 and food_pos[1] == grid_pos[1]:
                        screen.blit(sprites[TINY_EAT_W], (position[0], position[1]))
                    else:
                        screen.blit(sprites[TINY_W], (position[0], position[1]))
            elif direction == SOUTH:
                if body_part == HEAD:
                    if food_pos[0] == grid_pos[0] and food_pos[1] == grid_pos[1] + 1:
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
                    if food_pos[0] == grid_pos[0] and food_pos[1] == grid_pos[1] + 1:
                        screen.blit(sprites[TINY_EAT_S], (position[0], position[1]))
                    else:
                        screen.blit(sprites[TINY_S], (position[0], position[1]))
            else:
                if body_part == HEAD:
                    if food_pos[0] == grid_pos[0] + 1 and food_pos[1] == grid_pos[1]:
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
                    if food_pos[0] == grid_pos[0] + 1 and food_pos[1] == grid_pos[1]:
                        screen.blit(sprites[TINY_EAT_E], (position[0], position[1]))
                    else:
                        screen.blit(sprites[TINY_E], (position[0], position[1]))

    def dead_1(a_snake):

        for i, segment in enumerate(a_snake):

            direction = segment.get_direction()
            body_part = segment.get_body_part()
            position = translate(segment.get_grid_pos())

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

    def dead_2(a_snake):
        for i, segment in enumerate(a_snake):

            direction = segment.get_direction()
            body_part = segment.get_body_part()
            position = translate(segment.get_grid_pos())

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

    def draw_food():
        position = translate(food.get_grid_pos())
        screen.blit(sprites[FOOD], (position[0], position[1]))

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

    while running:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    current_direction = NORTH
                if event.key == pygame.K_LEFT:
                    current_direction = WEST
                if event.key == pygame.K_DOWN:
                    current_direction = SOUTH
                if event.key == pygame.K_RIGHT:
                    current_direction = EAST
        if alive:
            alive, tick = update_snake(tick, current_direction, tiles, alive)

        draw_background()

        if alive:
            if tick == 0:
                draw_snake(snake, food)
                old_snake = deepcopy(snake)
            else:
                draw_snake(old_snake, food)
        else:
            if did_death_animation < 100:
                dead_1(old_snake)
                did_death_animation += 1
            else:
                dead_2(old_snake)
        draw_food()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()