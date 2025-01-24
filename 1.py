import os
import sys

import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    image.set_colorkey(colorkey)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


image = load_image("creature.png")


def main():
    pygame.init()
    size = 300, 300
    screen = pygame.display.set_mode(size)

    running = True
    clock = pygame.time.Clock()
    x, y = 0, 0

    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            y -= 10
        if keys[pygame.K_DOWN]:
            y += 10
        if keys[pygame.K_RIGHT]:
            x += 10
        if keys[pygame.K_LEFT]:
            x -= 10
        screen.blit(image, (x, y))
        pygame.display.flip()
        clock.tick(24)

    pygame.quit()


main()
