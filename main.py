import os
import random
import sys

import pygame

white = (255, 255, 255)
black = (0, 0, 0)
size = width, height = 1000, 700
FPS = 24

pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Ship(pygame.sprite.Sprite):
    ship_size = 65, 100
    image = load_image("ship1.png", -1)
    image = pygame.transform.rotate(image, -90)
    image1 = load_image("ship.png", -1)
    image1 = pygame.transform.rotate(image1, -90)
    image2 = load_image("ship2.png", -1)
    image2 = pygame.transform.rotate(image2, -90)
    images = [image, image1, image2]

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Ship.image
        self.rect = self.image.get_rect()
        self.rect.x = width // 10
        self.rect.y = height // 2 - Ship.ship_size[0] // 2
        self.speed = 10
        self.cur_frame = 0
        self.count = 0

    def update(self, *args):
        self.count += 1
        if self.count > 4:
            self.cur_frame = (self.cur_frame + 1) % 3
            self.image = Ship.images[self.cur_frame]
            self.count = 0

    def move(self, direction):
        c = self.speed * direction
        y = self.rect.y
        if not ((y <= 0 and direction < 0) or (y >= height - Ship.ship_size[0] and direction > 0)):
            self.rect.y += c


class Asteroid(pygame.sprite.Sprite):
    image = load_image("asteroid.png", -1)
    a_size = a_width, a_height = 100, 100
    image = pygame.transform.scale(image, a_size)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Asteroid.image
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(width, 2 * width)
        self.rect.y = random.randrange(0, height - Asteroid.a_height)
        self.speed = random.randrange(5, 10)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        if self.rect.x <= -50:
            self.rect.x = random.randrange(width, 2 * width)
        self.rect = self.rect.move(-self.speed, 0)


class Star(pygame.sprite.Sprite):
    image = load_image("star.png", -1)
    a_size = a_width, a_height = 50, 50
    image = pygame.transform.scale(image, a_size)

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Star.image
        self.rect = self.image.get_rect()

        self.rect.x = random.randrange(width, 2 * width)
        self.rect.y = random.randrange(Star.a_height, height - Star.a_height)
        self.speed = 10
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        if self.rect.x <= -50:
            self.rect.x = random.randrange(width, 2 * width)
        self.rect = self.rect.move(-self.speed, 0)

    def on_collect(self):
        self.rect.x = random.randrange(width, 2 * width)
        self.rect.y = random.randrange(Star.a_height, height - Star.a_height)


def terminate():
    pygame.quit()
    sys.exit()


def start_menu():
    options = menu_options
    pygame.init()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)

    font = pygame.font.Font(None, 60)

    screen_width, screen_height = screen.get_size()

    button_width, button_height = 300, 60

    running = True
    while running:
        screen.fill(WHITE)

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for index, (text, action) in enumerate(options):
            button_x = (screen_width - button_width) // 2
            button_y = 200 + index * (button_height + 20)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

            color = GRAY if button_rect.collidepoint(mouse_pos) else BLACK

            pygame.draw.rect(screen, color, button_rect, border_radius=10)

            text_surface = font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)

            if button_rect.collidepoint(mouse_pos) and mouse_click[0]:
                action()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()


def main():
    all_sprites = pygame.sprite.Group()
    asteroids_group = pygame.sprite.Group()
    ship = Ship(all_sprites)
    asteroids = []
    for _ in range(10):
        asteroids.append(Asteroid([all_sprites, asteroids_group]))
    star = Star(all_sprites)

    TIMER_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER_EVENT, 500)

    running = True
    background = pygame.transform.scale(load_image('background.jpg'), (width, height))
    score = 0

    while running:
        screen.fill(black)
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == TIMER_EVENT:
                score += 1
        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            ship.move(1)
        if keys[pygame.K_UP]:
            ship.move(-1)
        if keys[pygame.K_p]:
            pause_menu()

        for asteroid in asteroids:
            if pygame.sprite.collide_mask(asteroid, ship):
                start_menu(menu_options)

        if pygame.sprite.collide_mask(star, ship):
            score += 100
            star.on_collect()

        all_sprites.draw(screen)
        all_sprites.update()

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, white)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    terminate()


def pause_menu():
    pygame.init()
    font = pygame.font.Font(None, 60)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    resume_text = font.render('Resume', True, WHITE)
    quit_text = font.render('Quit', True, WHITE)
    menu_text = font.render('Menu', True, WHITE)

    screen_width, screen_height = screen.get_size()
    button_width, button_height = 300, 60

    paused = True
    while paused:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        resume_button = pygame.Rect((screen_width - button_width) // 2, 100, button_width, button_height)
        menu_button = pygame.Rect((screen_width - button_width) // 2, 200, button_width, button_height)
        quit_button = pygame.Rect((screen_width - button_width) // 2, 300, button_width, button_height)

        pygame.draw.rect(screen, BLACK, resume_button, border_radius=10)
        pygame.draw.rect(screen, BLACK, menu_button, border_radius=10)
        pygame.draw.rect(screen, BLACK, quit_button, border_radius=10)

        screen.blit(resume_text, resume_text.get_rect(center=resume_button.center))
        screen.blit(menu_text, menu_text.get_rect(center=menu_button.center))
        screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if resume_button.collidepoint(mouse_pos) and mouse_click[0]:
            paused = False
        if quit_button.collidepoint(mouse_pos) and mouse_click[0]:
            pygame.quit()
            sys.exit()
        if menu_button.collidepoint(mouse_pos) and mouse_click[0]:
            start_menu()

        pygame.display.flip()


def leaderboard():
    print('leaderboard')


def settings():
    print('settings')


menu_options = [
    ("Start Game", main),
    ("Leaderboard", leaderboard),
    ("Quit", terminate)
]

if __name__ == '__main__':
    start_menu()
