import os
import random
import sys
import pygame

# Константы
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
SIZE = WIDTH, HEIGHT = 1000, 700
FPS = 24
DATA_PATH = "data"
background_music = 'pop_liluzivert.mp3'

BUTTON_WIDTH, BUTTON_HEIGHT = 300, 60
BUTTON_MARGIN = 20
FONT_SIZE = 60

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(background_music)
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 60)
records_file = "records.txt"
pygame.mixer.music.load(background_music)
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(-1)


def load_recods():
    if os.path.exists(records_file):
        with open(records_file, 'r') as file:
            records = file.readline().split()
            file.close()
            return records
    return []


def save_record(record):
    with open(records_file, 'a') as file:
        file.write(f' {record}')
        file.close()


def load_image(name, colorkey=None):
    fullname = os.path.join(DATA_PATH, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        return pygame.Surface((50, 50))
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
    SHIP_SIZE = 65, 100
    IMAGES = [
        pygame.transform.rotate(load_image(f"ship{i}.png", -1), -90)
        for i in range(3)
    ]

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Ship.IMAGES[0]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 10
        self.rect.y = HEIGHT // 2 - Ship.SHIP_SIZE[0] // 2
        self.speed = 10
        self.cur_frame = 0
        self.count = 0

    def update(self, *args):
        self.count += 1
        if self.count > 4:
            self.cur_frame = (self.cur_frame + 1) % len(Ship.IMAGES)
            self.image = Ship.IMAGES[self.cur_frame]
            self.count = 0

    def move(self, direction):
        y_offset = self.speed * direction
        if 0 <= self.rect.y + y_offset <= HEIGHT - Ship.SHIP_SIZE[0]:
            self.rect.y += y_offset


class Asteroid(pygame.sprite.Sprite):
    IMAGE = pygame.transform.scale(load_image("asteroid.png", -1), (150, 150))
    all_asteroids = []

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Asteroid.IMAGE
        self.rect = self.image.get_rect()
        self.speed = random.randrange(5, 10)
        self.mask = pygame.mask.from_surface(self.image)

        while True:
            self.rect.x = random.randrange(WIDTH, 2 * WIDTH)
            self.rect.y = random.randrange(0, HEIGHT - self.rect.height)
            if not any(self.rect.colliderect(asteroid.rect) for asteroid in Asteroid.all_asteroids):
                break

        Asteroid.all_asteroids.append(self)

    def update(self, *args):
        self.rect.x -= self.speed
        if self.rect.x <= -self.rect.width:
            self.respawn()

    def respawn(self):
        while True:
            self.rect.x = random.randrange(WIDTH, 2 * WIDTH)
            self.rect.y = random.randrange(0, HEIGHT - self.rect.height)
            if not any(self.rect.colliderect(asteroid.rect) for asteroid in Asteroid.all_asteroids if asteroid != self):
                break


class Star(pygame.sprite.Sprite):
    IMAGE = pygame.transform.scale(load_image("star.png", -1), (50, 47))

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Star.IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH, 2 * WIDTH)
        self.rect.y = random.randrange(self.rect.height, HEIGHT - self.rect.height)
        self.speed = 10
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args):
        self.rect.x -= self.speed
        if self.rect.x <= -self.rect.width:
            self.respawn()

    def on_collect(self):
        self.respawn()

    def respawn(self):
        self.rect.x = random.randrange(WIDTH, 2 * WIDTH)
        self.rect.y = random.randrange(self.rect.height, HEIGHT - self.rect.height)


def terminate():
    pygame.quit()
    sys.exit()


def draw_button(rect, text, color, text_color):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


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

        text_surface = font.render('Main menu', True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
        records = load_recods()
        records = set(map(int, records))
        records = sorted(list(records), reverse=True)[:10]
        for i, score in enumerate(records):
            text = font.render(f"{i + 1}. {score}", True, BLACK)
            screen.blit(text, (50, 50 + i * 40))

        if button_rect.collidepoint(mouse_pos) and mouse_click[0]:
            start_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()


def start_menu():
    menu_options = [
        ("Start game", game),
        ("Leaderboard", leaderboard),
        ("Quit", terminate)
    ]
    button_width, button_height = 300, 60
    running = True
    while running:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for index, (text, action) in enumerate(menu_options):
            button_x = (WIDTH - button_width) // 2
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
                terminate()

        pygame.display.flip()


def lose(score):
    options = [
        ("Play Again", lambda: None),
        ("Main menu", start_menu),
        ("Quit", terminate)
    ]

    paused = True
    while paused:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        text = font.render(f"Your score: {score}", True, BLACK)
        screen.blit(text, ((WIDTH - text.get_width()) // 2, 100))
        for index, (text, action) in enumerate(options):
            button_x = (WIDTH - BUTTON_WIDTH) // 2
            button_y = 200 + index * (BUTTON_HEIGHT + BUTTON_MARGIN)
            button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)

            color = GRAY if button_rect.collidepoint(mouse_pos) else BLACK
            draw_button(button_rect, text, color, WHITE)

            if button_rect.collidepoint(mouse_pos) and mouse_click[0]:
                if text == "Resume":
                    paused = False
                else:
                    action()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

        pygame.display.flip()


def game():
    all_sprites = pygame.sprite.Group()
    asteroids_group = pygame.sprite.Group()
    ship = Ship(all_sprites)
    for _ in range(7):
        Asteroid(all_sprites, asteroids_group)
    star = Star(all_sprites)

    TIMER_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(TIMER_EVENT, 1000)

    background = pygame.transform.scale(load_image('background.jpg'), (WIDTH, HEIGHT))
    score = 0
    running = True
    pause_rect = pygame.Rect(WIDTH - 160, 10, 150, 40)

    while running:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and pause_rect.collidepoint(event.pos):
                pause_menu()
            if event.type == TIMER_EVENT:
                score += 10

        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            ship.move(1)
        if keys[pygame.K_UP]:
            ship.move(-1)

        for asteroid in asteroids_group:
            if pygame.sprite.collide_mask(asteroid, ship):
                if score > 0:
                    save_record(score)
                lose(score)

        if pygame.sprite.collide_mask(star, ship):
            score += 100
            star.on_collect()

        all_sprites.update()
        all_sprites.draw(screen)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        draw_button(pause_rect, "Pause", WHITE, BLACK)

        pygame.display.flip()
        clock.tick(FPS)

    terminate()


def pause_menu():
    options = [
        ("Resume", lambda: None),
        ("Main menu", start_menu),
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
            draw_button(button_rect, text, color, WHITE)

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
