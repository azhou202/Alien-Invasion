import pygame as pg
from pygame.sprite import Sprite

class Boss(Sprite):
    """A class that represents the boss ships"""

    def __init__(self, fmt_settings, screen, level=5):
        """Create an instance of the boss"""

        super().__init__()
        self.fmt_settings = fmt_settings
        self.screen = screen
        self.level = level

        # Load alien image, transform it, set rect attribute
        self.prev_image = pg.image.load('images/alien_ship.bmp')
        self.image = pg.transform.scale(self.prev_image, (120, 120))
        self.rect = self.image.get_rect()

        # Start each new alien at top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location"""

        self.screen.blit(self.image, self.rect)