"""
Pierre-Charles Dussault
February 22, 2021

Covid Exterminator, a 2D shooting game made while completing
"Python Crash Course".

On-screen Button module.
"""
import pygame


class Button():

    def __init__(self, game_instance, text):
        """Initialize button attributes."""
        self.screen = game_instance.screen

        # Set dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)  # green
        self.text_color = (255, 255, 255)  # white
        self.font = pygame.font.SysFont("DejaVu Mono", 48)

        # Build the button's Rect object and position it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen.get_rect().center

        # The displayed message only needs to be prepped once.
        self._prep_text(text)

    def _prep_text(self, text):
        """Convert text into a rendered image and center it inside the
        button."""
        self.text_img = self.font.render(text, True, self.text_color,
                                         self.button_color)
        self.text_img_rect = self.text_img.get_rect()
        self.text_img_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button, then draw text image inside of it."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.text_img, self.text_img_rect)
