"""
Pierre-Charles Dussault
October 28, 2020

Covid Exterminator, a 2D shooting game made while completing
"Python Crash Course".

Projectile/bullets module.
"""
import pygame


class Bullet(pygame.sprite.Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, game_instance):
        """Create bullet object at the ship's current position."""
        super().__init__()
        self.screen = game_instance.screen
        self.settings = game_instance.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect((0, 0), (self.settings.bullet_width,
                                         self.settings.bullet_height))
        self.rect.midtop = game_instance.doctor.rect.midtop

        # Store the bullet's y-axis position as a decimal value to enable
        # fine-tuning of the bullet's speed.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        # Update the decimal position of the bullet. Subtract because going up
        # the screen decreases y value.
        self.y -= self.settings.bullet_speed

        # Update the position of the rect.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet on the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
