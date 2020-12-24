import pygame as pg
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import functions as f
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from boss import Boss


def run_game():
    # Initialize game, settings and create screen obj
    pg.init()
    fmt_settings = Settings()
    screen = pg.display.set_mode((fmt_settings.screen_width, fmt_settings.screen_height))
    pg.display.set_caption("Alien Invasion")

    # Make a ship
    ship = Ship(screen, fmt_settings)

    # Make the Play button
    play_button = Button(fmt_settings, screen, "PLAY")

    # Make a group to store stars
    stars = Group()
    # Create star background
    f.create_stars(fmt_settings, screen, ship, stars, 8)

    # Make a group to store aliens
    aliens = Group()

    # Make group to store perks
    perks = Group()

    # Create alien fleet
    f.create_fleet(fmt_settings, screen, ship, aliens, perks)

    # Make a group to store bullets in
    bullets = Group()

    # Create instance to store game stats and make scoreboard
    stats = GameStats(fmt_settings)
    sb = Scoreboard(fmt_settings, screen, stats)

    #  Start main loop
    while True:
        f.check_events(fmt_settings, screen, stats, sb, play_button, ship, aliens, bullets, perks)

        if stats.game_active:
            # Update various aspects of game
            ship.update()
            f.update_bullets(fmt_settings, screen, stats, sb, ship, aliens, bullets)
            f.update_aliens(fmt_settings, screen, stats, sb, ship, aliens, bullets, perks)

        f.update_screen(fmt_settings, screen, stats, sb, ship, aliens, stars, bullets, play_button)


run_game()
