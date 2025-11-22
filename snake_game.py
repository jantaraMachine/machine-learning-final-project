import pygame
from random import choice

from snake import Snake
from food import Food

SCALE = 3

def load_sprites():

    image = pygame.image.load("sprites.png").convert_alpha()

    sprites = []

    for row in range (2):
        for col in range (9):

            sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
            sprite.blit(image, (0, 0), (col * 16, row * 16, 16, 16))
            sprite = pygame.transform.scale_by(sprite, SCALE)
            sprites.append(sprite)

            if (row == 0 and col == 7) or (row == 1 and col == 7):
                sprites.append(pygame.transform.flip(sprite, True, False))
            elif row == 1 and col == 1:
                sprites.append(pygame.transform.rotate(sprite, 90))
            elif (row == 0 and col < 4) or (row == 1 and col < 5):
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

    snake = None
    old_snake = None
    food = None

    HEAD_N = 0
    HEAD_W = 1
    HEAD_S = 2
    HEAD_E = 3
    BUMP_N = 4
    BUMP_W = 5
    BUMP_S = 6
    BUMP_E = 7
    DEAD_N = 8
    DEAD_W = 9
    DEAD_S = 10
    DEAD_E = 11
    EAT_N = 12
    EAT_W = 13
    EAT_S = 14
    EAT_E = 15
    BUSH = 16
    GRASS_1 = 17
    FOOD = 18
    BOX_TL = 19
    BOX_TR = 20
    BOX_T = 21
    BODY_NE = 22
    BODY_NW = 23
    BODY_SW = 24
    BODY_SE = 25
    BODY_NS = 26
    BODY_WE = 27
    TAIL_N = 28
    TAIL_W = 29
    TAIL_S = 30
    TAIL_E = 31
    TINY_N = 32
    TINY_W = 33
    TINY_S = 34
    TINY_E = 35
    TINY_EAT_N = 36
    TINY_EAT_W = 37
    TINY_EAT_S = 38
    TINY_EAT_E = 39
    GRASS_2 = 40
    # EMPTY = 41
    BOX_BL = 42
    BOX_BR = 43
    BOX_B = 44

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

        old_snake = [Snake([8, 8], NORTH, TINY)]

        snake_xs = []
        snake_ys = []
        for segment in snake:

            grid_pos = segment.get_grid_pos()

            snake_xs.append(grid_pos[0])
            snake_ys.append(grid_pos[1])
        
        food_x = choice([i for i in range (0, 14) if i not in snake_xs])
        food_y = choice([i for i in range (0, 14) if i not in snake_ys])

        food = Food([food_x, food_y])

    init()

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

    def update_snake(tick, direction):
        if tick == 1000:
            for segment in snake:
                direction = segment.change_direction(direction)
                segment.move()
            return 0
        else:
            for segment in snake:
                direction = segment.change_direction(direction)
            return tick + 1

    def draw_snake(a_snake):
        for i, segment in enumerate(a_snake):

            direction = segment.get_direction()
            body_part = segment.get_body_part()
            position = translate(segment.get_grid_pos())

            if direction == NORTH:
                if body_part == HEAD:
                    screen.blit(sprites[HEAD_N], (position[0], position[1]))
                elif body_part == BODY:

                    behind_direction = a_snake[i + 1].get_direction()

                    if behind_direction == NORTH:
                        screen.blit(sprites[BODY_NS], (position[0], position[1]))
                    elif behind_direction == WEST:
                        screen.blit(sprites[BODY_NW], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BODY_NE], (position[0], position[1]))
                elif body_part == TAIL:
                    screen.blit(sprites[TAIL_N], (position[0], position[1]))
                else:
                    screen.blit(sprites[TINY_N], (position[0], position[1]))
            elif direction == WEST:
                if body_part == HEAD:
                    screen.blit(sprites[HEAD_W], (position[0], position[1]))
                elif body_part == BODY:

                    behind_direction = a_snake[i + 1].get_direction()

                    if behind_direction == NORTH:
                        screen.blit(sprites[BODY_SW], (position[0], position[1]))
                    elif behind_direction == WEST:
                        screen.blit(sprites[BODY_WE], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BODY_NW], (position[0], position[1]))
                elif body_part == TAIL:
                    screen.blit(sprites[TAIL_W], (position[0], position[1]))
                else:
                    screen.blit(sprites[TINY_W], (position[0], position[1]))
            elif direction == SOUTH:
                if body_part == HEAD:
                    screen.blit(sprites[HEAD_S], (position[0], position[1]))
                elif body_part == BODY:

                    behind_direction = a_snake[i + 1].get_direction()

                    if behind_direction == WEST:
                        screen.blit(sprites[BODY_SE], (position[0], position[1]))
                    elif behind_direction == SOUTH:
                        screen.blit(sprites[BODY_NS], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BODY_SW], (position[0], position[1]))
                elif body_part == TAIL:
                    screen.blit(sprites[TAIL_S], (position[0], position[1]))
                else:
                    screen.blit(sprites[TINY_S], (position[0], position[1]))
            else:
                if body_part == HEAD:
                    screen.blit(sprites[HEAD_E], (position[0], position[1]))
                elif body_part == BODY:

                    behind_direction = a_snake[i + 1].get_direction()

                    if behind_direction == NORTH:
                        screen.blit(sprites[BODY_SE], (position[0], position[1]))
                    elif behind_direction == SOUTH:
                        screen.blit(sprites[BODY_NE], (position[0], position[1]))
                    else:
                        screen.blit(sprites[BODY_WE], (position[0], position[1]))
                elif body_part == TAIL:
                    screen.blit(sprites[TAIL_E], (position[0], position[1]))
                else:
                    screen.blit(sprites[TINY_E], (position[0], position[1]))

    running = True
    tick = 0

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    tick = update_snake(tick, NORTH)
                if event.key == pygame.K_LEFT:
                    tick = update_snake(tick, WEST)
                if event.key == pygame.K_DOWN:
                    tick = update_snake(tick, SOUTH)
                if event.key == pygame.K_RIGHT:
                    tick = update_snake(tick, EAST)
        tick = update_snake(tick, None)

        draw_background()

        if tick == 0:
            draw_snake(snake)
            old_snake = []
            for segment in snake:
                old_snake.append(Snake(segment.get_grid_pos(), segment.get_direction(), segment.get_body_part()))
        else:
            draw_snake(old_snake)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()