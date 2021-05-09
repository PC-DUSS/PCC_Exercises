"""
Pierre-Charles Dussault
October 29, 2020

Doctor avatar to be displayed on the center of the screen in BlueSky game.

This is the interactive avatar.
"""
import pygame


class BlueSkyDoctor():
    """Class to manage assets for the BlueSky doctor avatar."""

    def __init__(self, bs_game):
        """Initialize the assets of the BlueSky doctor avatar and his
        starting position."""
        # Match the screen for the doctor with the screen for the general game.
        self.screen = bs_game.screen
        # Set the local screen rect to the screen rect of the general game.
        self.screen_rect = bs_game.screen.get_rect()
        # Load the doctor image and get his rect.
        self.image = pygame.image.load("../Covid_exterminator"
                                       "/images/doctor.png"
                                       )
        self.rect = self.image.get_rect()
        # Start each new doctor avatar at the center of the screen.
        self.rect.center = self.screen_rect.center
        # Store a decimal value for the doctor avatar's horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # Set movement flags.
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        # Set avatar movement speed
        self.movement_speed = 2.5

    def update(self):
        """Update and reposition the avatar for each pass in the
        loop, according to movement flags."""
        if self.moving_right:
            if self.x >= (self.screen_rect.width - self.rect.width):
                self.x = (self.screen_rect.width - self.rect.width)
            else:
                self.x += self.movement_speed
        elif self.moving_left:
            if self.x <= 0:
                self.x = 0
            else:
                self.x -= self.movement_speed
        elif self.moving_up:
            if self.y <= 0:
                self.y = 0
            else:
                self.y -= self.movement_speed
        elif self.moving_down:
            if self.y >= (self.screen_rect.height - self.rect.height):
                self.y = (self.screen_rect.height - self.rect.height)
            else:
                self.y += self.movement_speed

        # Update the real object's rect to match the local rect's position.
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """Draw (reposition) the doctor at his current saved position."""
        self.screen.blit(self.image, self.rect)
