import pygame

def load_sprites(SCALE):

    image = pygame.image.load("sprites.png").convert_alpha()

    sprites = []

    for row in range (2):
        for col in range (9):

            sprite = pygame.Surface((16, 16), pygame.SRCALPHA)
            sprite.blit(image, (0, 0), (col * 16, row * 16, 16, 16))
            sprite = pygame.transform.scale_by(sprite, SCALE)
            sprites.append(sprite)

            if row == 1 and col == 1:
                sprites.append(pygame.transform.rotate(sprite, 90))
            elif (row == 0 and col < 4) or (row == 1 and col < 5):

                sprites.append(pygame.transform.rotate(sprite, 90))
                sprites.append(pygame.transform.rotate(sprite, 180))
                sprites.append(pygame.transform.rotate(sprite, 270))
    
    return sprites

def main():

    SCALE = 3
    width = 160 * SCALE
    height = 144 * SCALE

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")

    sprites = load_sprites(SCALE)

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
    BOX_T = 20
    BODY_NE = 21
    BODY_NW = 22
    BODY_SW = 23
    BODY_SE = 24
    BODY_NS = 25
    BODY_EW = 26
    TAIL_N = 27
    TAIL_W = 28
    TAIL_S = 29
    TAIL_E = 30
    TINY_N = 31
    TINY_W = 32
    TINY_S = 33
    TINY_E = 34
    TINY_EAT_N = 35
    TINY_EAT_W = 36
    TINY_EAT_S = 37
    TINY_EAT_E = 38
    GRASS_2 = 39
    BOX_BL = 41


    screen.fill("black")
    screen.blit(sprites[42], (0, 0))

    running = True

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()