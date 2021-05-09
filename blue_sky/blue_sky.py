"""
Pierre-Charles Dussault
October 29, 2020

Make a blue background for a PyGame screen. Then center a player character in
the middle of the screen.

This is the base screen environment.
"""

import sys
import pygame
from blue_sky_doctor import BlueSkyDoctor
from blue_sky_settings import Settings


class BlueSkyGame():
    """Class to manage BlueSky game."""

    def __init__(self):
        """Initialize the attributes of BlueSky"""
        # Initialize PyGame
        pygame.init()
        # Import settings from settings module
        self.settings = Settings()
        # Calibrate game screen according to imported game resolution settings.
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height
                                               ))
        pygame.display.set_caption("Welcome to BlueSky. (press 'ESC' to quit)")
        self.doctor = BlueSkyDoctor(self)# Requires 'self' argument to store
                                         # the same 'screen' attribute as the
                                         # one stored in the general game.

    def _check_keydown_events(self, event):
        """Handle keypress events."""
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_d:
            self.doctor.moving_right = True
        elif event.key == pygame.K_a:
            self.doctor.moving_left = True
        elif event.key == pygame.K_w:
            self.doctor.moving_up = True
        elif event.key == pygame.K_s:
            self.doctor.moving_down = True

    def _check_keyup_events(self, event):
        """Handle key release events."""
        if event.key == pygame.K_d:
            self.doctor.moving_right = False
        elif event.key == pygame.K_a:
            self.doctor.moving_left = False
        elif event.key == pygame.K_w:
            self.doctor.moving_up = False
        elif event.key == pygame.K_s:
            self.doctor.moving_down = False

    def _check_events(self):
        """Private method to check for keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _update_screen(self):
        """Private method to update the game screen."""
        # 'Redraw' the background screen on every pass.
        self.screen.fill(self.settings.bg_color)
        # 'Redraw' the doctor avatar at his newly saved location on every pass.
        self.doctor.blitme()
        # Update the display to the most up to date surface.
        pygame.display.flip()

    def run_game(self):
        """Main loop for the game."""
        while True:
            self._check_events()
            self.doctor.update()
            self._update_screen()


def main():
    """Run the game when executed as main module."""
    bs_game = BlueSkyGame()
    bs_game.run_game()
    return 0


if __name__ == "__main__":
    main()
