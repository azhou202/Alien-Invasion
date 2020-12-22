import pygame.font

class Button():
    """A class that creates interactable buttons on the screen"""

    def __init__(self, fmt_settings, screen, msg):
        """Initialize button attributes"""

        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set dimensions and button properties
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Create button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Button message needs to only be prepped once
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered iamge and center text on button"""

        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Creates a blank button and then draws the message"""

        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
