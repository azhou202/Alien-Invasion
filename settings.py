class Settings:
    """A class that stores settings for Alien Invasion."""

    def __init__(self):
        """Initialize static game settings"""

        # Screen settings
        self.screen_width = 1000   # 1600
        self.screen_height = 700     # 900
        self.bg_color = (53, 56, 57)

        # Ship settings
        self.ship_limit = 2

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 3

        # Alien settings
        self.fleet_drop_speed = 10

        # How quickly game speeds up
        self.speedup_scale = 1.1
        # How quickly alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize dynamic settings"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 0.75
        self.perks_allowed = 1

        # fleet_direction of 1 represents right, -1 is left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self, stats):
        """Increase speed settings and point values"""

        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.perks_allowed *= (self.speedup_scale * (stats.level / 2))

        self.alien_points = int(self.alien_points * self.score_scale)