import pygame as pg
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, screen, fmt_settings, scale_factor=50):
        """Initialize the ship and set starting position"""
        super().__init__()

        self.screen = screen
        self.fmt_settings = fmt_settings

        # Load ship image
        self.prev_image = pg.image.load('images/ship.bmp')

        # Scale down the image
        self.image = pg.transform.scale(self.prev_image, (scale_factor, scale_factor))

        # Get the rect of the transformed image
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at bottom center of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for ship's center
        self.center = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

        # Sounds
        self.death_sound = pg.mixer.Sound('sounds/explosion.wav')  # Sounds gathered from sound.bible.com

    def update(self):
        """Update ship's position based on movement flags"""

        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.fmt_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.fmt_settings.ship_speed_factor

        # Update rect obj from self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Draw ship at current location"""

        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship"""

        self.center = self.screen_rect.centerx
