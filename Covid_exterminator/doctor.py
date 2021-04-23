"""
Pierre-Charles Dussault
October 28, 2020

Covid Exterminator, a 2D shooting game made while completing
"Python Crash Course".

Doctor player avatar module.
"""
import pygame


class Doctor(pygame.sprite.Sprite):
    """A class to manage the doctor."""

    def __init__(self, game_instance):
        """Initialize the doctor and his starting position."""
        super().__init__()
        # Make a class attribute to easily access the screen from the
        # inherited game.
        self.screen = game_instance.screen
        self.settings = game_instance.settings

        # Set a class attribute to the game screen's rectangle to know where
        # the game screen is located in order to correctly position the doctor.
        self.screen_rect = game_instance.screen.get_rect()

        # Load the doctor image and store its rectangle inside an attribute.
        self.image = pygame.image.load("images/doctor.png")
        self.rect = self.image.get_rect()

        # Start each new doctor at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the doctor's horizontal position.
        self.x = float(self.rect.x)

        # Movement flags for continous movement.
        self.moving_right = False
        self.moving_left = False

    def move_right(self):
        self.moving_right = True

    def move_left(self):
        self.moving_left = True

    def stop_moving_right(self):
        self.moving_right = False

    def stop_moving_left(self):
        self.moving_left = False

    def update(self):
        """Update the doctor's position based on the movement flag."""
        # Only allow movement if the doctor has not passed the screens limits.
        if self.moving_right:
            if self.x < (self.screen_rect.width - self.rect.width):
                self.x += self.settings.doctor_speed
            else:
                self.x = (self.screen_rect.width - self.rect.width)

        elif self.moving_left:
            if self.x > 0:
                self.x -= self.settings.doctor_speed
            else:
                self.x = 0

        # Update the rect object (the real object position) from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the doctor at his current position."""
        self.screen.blit(self.image, self.rect)

    def center_doctor(self):
        """Center the doctor on the game screen."""
        self.rect.midbottom = self.screen.get_rect().midbottom

        # Update the floating point holding the doctor's x-coordinate, as it
        # was only previously set in the __init__() method. Failing to do this
        # will keep using the doctor's previous x-coordinate when the game
        # resumes. This acts like a reset to the doctor's starting point.
        self.x = float(self.rect.x)
