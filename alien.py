import pygame as pg
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, fmt_settings, screen, classification='default'):
        """Initialize the alien and set its starting position"""

        super().__init__()
        self.screen = screen
        self.fmt_settings = fmt_settings

        # Load alien image, transform it, set rect attribute based on classification # TODO: using the img editor messed up the transparent pixels
        self.classification = classification

        prev_image = pg.image.load('images/alien_ship.bmp')  # default type which is regular alien
        if self.classification == 'shield':
            prev_image = pg.image.load('images/shield.bmp')
        elif self.classification == 'super_bullet':
            prev_image = pg.image.load('images/super_bullet.bmp')
        self.image = pg.transform.scale(prev_image, (45, 45))
        self.rect = self.image.get_rect()

        # Start each new alien at top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location"""

        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Determine if alien is at edge of screen
        :return True if alien is at edge of screen
        """

        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Move alien right or left"""

        self.x += self.fmt_settings.alien_speed_factor * self.fmt_settings.fleet_direction
        self.rect.x = self.x
