import os

import pygame
import sys


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


def start_menu(screen, options):
    pygame.init()
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)

    font = pygame.font.Font(None, 74)

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


if __name__ == "__main__":
    def start_game():
        print("Начало игры!")


    def open_settings():
        print("Настройки")


    def quit_game():
        pygame.quit()
        sys.exit()


    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Стартовое меню")

    menu_options = [
        ("Start Game", start_game),
        ("Settings", open_settings),
        ("Quit", quit_game)
    ]

    start_menu(screen, menu_options)
