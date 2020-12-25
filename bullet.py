import pygame as pg
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class that manages bullets fired from ship"""

    def __init__(self, fmt_settings, screen, ship, perk=False):
        """Create a bullet at the ship's current position"""

        super().__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and set correct position
        if perk:
            width = fmt_settings.bullet_width + 120
            height = fmt_settings.bullet_height - 8
        else:
            width = fmt_settings.bullet_width
            height = fmt_settings.bullet_height

        self.rect = pg.Rect(0, 0, width, height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store bullet's position as a decimal value
        self.y = float(self.rect.y)

        self.color = fmt_settings.bullet_color
        self.speed_factor = fmt_settings.bullet_speed_factor

        # Bullet firing sound
        self.firing_sound = pg.mixer.Sound('sounds/laser.wav')  # Sounds gathered from sound.bible.com

    def update(self):
        """Move bullet up the screen"""

        # Update decimal position of the bullet
        self.y -= self.speed_factor
        # Update rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet on the screen"""

        pg.draw.rect(self.screen, self.color, self.rect)