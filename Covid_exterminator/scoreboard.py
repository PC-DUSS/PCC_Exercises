"""
Pierre-Charles Dussault
March 04, 2021

Covid Exterminator, a 2D shooting game made while completing
"Python Crash Course".

Scoreboard module.
"""
import pygame
from pygame.sprite import Group

from doctor import Doctor


class Scoreboard(object):
    """Class to report scoring information."""

    def __init__(self, game_instance):
        self.game_instance = game_instance
        self.screen = game_instance.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game_instance.settings
        self.stats = game_instance.stats

        # Font settings for scoring information.
        self.text_color = (30, 30, 30)  # 8-bit RGB
        self.font_name = "DejaVu Mono"
        self.font_size = 48
        self.font = pygame.font.SysFont(self.font_name, self.font_size)

        # Prepare the images for the more temporary items of the scoreboard.
        self.prep_images()

        # Prepare the image for the high score.
        self.prep_high_score()

    def prep_score(self):
        """Prepare the initial scoreboard."""
        rounded_score = round(self.stats.score, -1)
        self.score_str = "{:,}".format(rounded_score)
        self.score_img = self.font.render(self.score_str,
                                          True,
                                          self.text_color,
                                          self.settings.bg_color)

        # Display the scoreboard at the top-right of the screen.
        self.score_rect = self.score_img.get_rect()
        self.score_rect.top = 20
        self.score_rect.right = self.screen.get_rect().right - 20

    def show_score(self):
        """Draw scoreboard on the screen surface, with the current score, the
        high score, the current level and the amount of doctors remaining."""
        self.screen.blit(self.score_img, self.score_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.level_img, self.level_rect)
        self.doctors.draw(self.screen)

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        rounded_high_score = round(self.stats.high_score, -1)
        self.high_score_str = "{:,}".format(rounded_high_score)
        self.high_score_img = self.font.render(self.high_score_str,
                                               True,
                                               self.text_color,
                                               self.settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def check_high_score(self):
        """Check if the high score needs to be updated. If so, update its value
        and prep an image of the new value to be displayed."""
        tmp_rounded_score = round(self.stats.score, -1)
        if tmp_rounded_score > self.stats.high_score:
            self.stats.update_high_score(tmp_rounded_score)
            self.prep_high_score()

    def prep_level(self):
        """Prepare an image to be displayed for the current level."""
        self.level_str = str(self.stats.level)
        self.level_img = self.font.render(self.level_str,
                                          True,
                                          self.text_color,
                                          self.settings.bg_color)

        # Position the current level below the current score.
        self.level_rect = self.level_img.get_rect()

        # This here will also inject a dependancy upon 'self.score'. This means
        # that prep_level() must be called after prep_score() has been called,
        # otherwise it will raise an error.
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_doctors(self):
        """Prepare the images to display for the amount of lives the player has
        left."""
        self.doctors = Group()
        # For each doctor the player has left.
        for doctor_number in range(0, self.stats.doctors_remaining):
            # Create a new Doctor object.
            doctor = Doctor(self.game_instance)

            # Make doctor image smaller to fit without obstructing the game.
            doctor.image = pygame.transform.scale(doctor.image, (28, 50))

            # Position its rect to the top-left corner of the screen.
            doctor.rect.x = 5 + doctor_number * doctor.rect.width
            doctor.rect.y = 5

            # Then add this new doctor to the doctors group.
            self.doctors.add(doctor)

    def prep_images(self):
        """Prepare the images for the items of the scoreboard to display."""
        self.prep_score()
        self.prep_level()
        self.prep_doctors()
