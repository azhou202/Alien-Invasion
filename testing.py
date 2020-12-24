import pygame as pg
from boss import Boss
from settings import Settings



def run_game():
    # Initialize game, settings and create screen obj
    pg.init()
    fmt_settings = Settings()
    # print("bullet wdith", fmt_settings.bullet_width)
    screen = pg.display.set_mode((fmt_settings.screen_width, fmt_settings.screen_height))
    pg.display.set_caption("Alien Invasion")

    runs = 0
    while runs < 20:
        test = Boss(fmt_settings, screen)
        test.blitme()
        runs += 1

run_game()