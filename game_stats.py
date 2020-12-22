class GameStats():
    """Tracks statistics for the game, Alien Invasion"""

    def __init__(self, fmt_settings):
        """Initiliaze statistics"""

        # Start the game in an active state
        self.game_active = False

        self.fmt_settings = fmt_settings
        self.reset_stats()

        # High score
        with open('_highscore.txt', 'r') as reader:
            # initialize high score as high score from text doc
            self.high_score = int(reader.read())

    def reset_stats(self):
        """Initializes stats that can change during the game"""

        self.ships_left = self.fmt_settings.ship_limit
        self.score = 0
        self.level = 1
