import pygame

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
    BODY_EW = 27
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

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_background()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()