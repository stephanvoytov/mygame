import os
import random
import sys
import pygame

# Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

SCREEN_SIZE = WIDTH, HEIGHT = 1000, 700
FPS = 24
BUTTON_WIDTH, BUTTON_HEIGHT = 300, 60
BUTTON_MARGIN = 20
FONT_SIZE = 60

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)

records_file = 'records.txt'


def load_recods():
    if os.path.exists(records_file):
        with open(records_file, 'r') as file:
            records = file.readline().split()
            file.close()
            return records
    return []


def save_record(record):
    with open(records_file, 'w') as file:
        file.write(f', {record}')
        file.close()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Image file '{fullname}' not found")
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


class BaseSprite(pygame.sprite.Sprite):
    """Base class for common sprite functionality."""

    def __init__(self, image, size, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Ship(BaseSprite):
    ship_images = [
        pygame.transform.rotate(load_image(f"ship{i}.png", -1), -90) for i in range(3)
    ]
    ship_size = (65, 100)

    def __init__(self, *groups):
        super().__init__(Ship.ship_images[0], Ship.ship_size, *groups)
        self.rect.x = WIDTH // 10
        self.rect.y = HEIGHT // 2 - Ship.ship_size[0] // 2
        self.speed = 10
        self.cur_frame = 0
        self.frame_count = 0

    def update(self):
        self.frame_count += 1
        if self.frame_count > 4:
            self.cur_frame = (self.cur_frame + 1) % len(Ship.ship_images)
            self.image = Ship.ship_images[self.cur_frame]
            self.frame_count = 0

    def move(self, direction):
        if 0 <= self.rect.y + self.speed * direction <= HEIGHT - self.rect.height:
            self.rect.y += self.speed * direction


class Asteroid(BaseSprite):
    asteroid_image = load_image("asteroid.png", -1)
    asteroid_size = (100, 100)

    def __init__(self, *groups):
        super().__init__(Asteroid.asteroid_image, Asteroid.asteroid_size, *groups)
        self.reset()

    def reset(self):
        self.rect.x = random.randint(WIDTH, 2 * WIDTH)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.randint(5, 10)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.reset()


class Star(BaseSprite):
    star_image = load_image("star.png", -1)
    star_size = (50, 50)

    def __init__(self, *groups):
        super().__init__(Star.star_image, Star.star_size, *groups)
        self.reset()

    def reset(self):
        self.rect.x = random.randint(WIDTH, 2 * WIDTH)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

    def on_collect(self):
        self.reset()


def terminate():
    pygame.quit()
    sys.exit()


def leaderboard():
    button_width, button_height = 300, 60
    running = True
    while running:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        button_x = WIDTH - button_width - 10
        button_y = 10
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        color = GRAY if button_rect.collidepoint(mouse_pos) else BLACK
        pygame.draw.rect(screen, color, button_rect, border_radius=10)

        text_surface = font.render('Main Menu', True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

        if button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            start_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()


def draw_button(rect, text, color):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def start_menu():
    options = [
        ("Start Game", main),
        ("Leaderboard", leaderboard),
        ("Quit", terminate)
    ]

    running = True
    while running:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for index, (text, action) in enumerate(options):
            button_x = (WIDTH - BUTTON_WIDTH) // 2
            button_y = 200 + index * (BUTTON_HEIGHT + BUTTON_MARGIN)
            button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

            color = GRAY if button_rect.collidepoint(mouse_pos) else BLACK
            draw_button(button_rect, text, color)

            if button_rect.collidepoint(mouse_pos) and mouse_click[0]:
                action()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()


def main():
    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()

    ship = Ship(all_sprites)
    [Asteroid(all_sprites, asteroids) for _ in range(10)]
    star = Star(all_sprites)

    background = pygame.transform.scale(load_image('background.jpg'), SCREEN_SIZE)
    score = 0
    pause_rect = pygame.Rect(WIDTH - 160, 10, 150, 40)

    running = True
    while running:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN and pause_rect.collidepoint(event.pos):
                pause_menu()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            ship.move(1)
        if keys[pygame.K_UP]:
            ship.move(-1)

        if pygame.sprite.spritecollide(ship, asteroids, False, pygame.sprite.collide_mask):
            start_menu()

        if pygame.sprite.collide_mask(ship, star):
            score += 100
            star.on_collect()

        all_sprites.update()
        all_sprites.draw(screen)

        draw_button(pause_rect, "Pause", GRAY)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)


def pause_menu():
    options = [
        ("Resume", lambda: None),
        ("Menu", start_menu),
        ("Quit", terminate)
    ]

    paused = True
    while paused:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for index, (text, action) in enumerate(options):
            button_x = (WIDTH - BUTTON_WIDTH) // 2
            button_y = 200 + index * (BUTTON_HEIGHT + BUTTON_MARGIN)
            button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

            color = GRAY if button_rect.collidepoint(mouse_pos) else BLACK
            draw_button(button_rect, text, color)

            if button_rect.collidepoint(mouse_pos) and mouse_click[0]:
                if text == "Resume":
                    paused = False
                else:
                    action()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()


if __name__ == '__main__':
    start_menu()
