import pygame as pg
from pygame.sprite import Sprite


class Star(Sprite):
    """A class that represents a star that decorates the background"""

    def __init__(self, fmt_settings, screen):
        """Initiliaze the star and set its starting position"""

        super().__init__()
        self.screen = screen
        self.fmt_settings = fmt_settings

        # Load star image, transform it, set rect
        self.prev_image = pg.image.load('images/star.bmp')
        self.image = pg.transform.scale(self.prev_image, (10, 10))
        self.rect = self.image.get_rect()

        # Start each new star at top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store star's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the star at its current location"""

        self.screen.blit(self.image, self.rect)