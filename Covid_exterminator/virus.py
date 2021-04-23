"""
Pierre-Charles Dussault
October 28, 2020

Covid Exterminator, a 2D shooting game made while completing
"Python Crash Course".

Virus enemy NPCs module.
"""
import pygame


class Virus(pygame.sprite.Sprite):
    """Class to handle virus assets and behaviour."""

    def __init__(self, game_instance):
        # Initialize an instance while inheriting from the super class Sprite.
        super().__init__()
        self.screen = game_instance.screen
        self.settings = game_instance.settings
        self.screen_rect = game_instance.screen.get_rect()

        # Load the image for the virus and store its rect.
        self.image = pygame.image.load("images/virus.png")
        self.rect = self.image.get_rect()

        # Start each new virus near, but not exactly at, the top-left corner of
        # the screen, leaving one rect's worth of space away from the corner.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Create a float attribute for the virus' x-axis coordinates in order
        # to enable fine tuning of horizontal its movement speed.
        self.x = float(self.rect.x)

        # Movement flags to handle continuous movement.
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False

    def check_edges(self):
        """Return True if virus is at edge of screen."""
        if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
            return True

    def drop_down(self):
        """Drop a virus down by its appropriate drop speed."""
        self.rect.y += self.settings.virus_drop_speed

    def update(self):
        """Move the virus to the right or left."""
        self.x += self.settings.virus_speed * self.settings.virus_direction
        self.rect.x = self.x
