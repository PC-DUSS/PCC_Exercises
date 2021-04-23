"""
Pierre-Charles Dussault
October 28, 2020

Covid Exterminator, a 2D shooting game made while completing
"Python Crash Course".

Game settings module.
"""
import pygame


class Settings():
    """A class to store all settings for Covid Exterminator game."""

    def __init__(self):
        """Initialize the game's STATIC settings."""
        # Screen settings
        self.fullscreen = False
        self.screen_width = 1600
        self.screen_height = 900
        self.bg_color = (230, 230, 230)  # This is an 8-bit [0-255] RGB

        # Framerate cap / movement speed multiplier cap
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(self.fps)
        self.ms_multiplier = 60/self.fps

        # Testing settings (cheat codes)
        self.INVINCIBLE_BULLET = True
        self.SUPER_BULLET = True
        self.INVINCIBLE_VIRUS = False
        self.INVINCIBLE_DOCTOR = False
        if self.SUPER_BULLET:
            self.bullet_width = 300
        else:
            self.bullet_width = 3

        self.doctors_limit = 3
        self.bullet_height = 15
        self.bullets_allowed = 3
        self.bullet_color = (100, 0, 0)
        self.virus_drop_speed = 150  # Default is 10.
        self.virus_direction = 1
        self.speedup_scale = 1.1  # Game speed-up upon reaching next level.
        self.score_scaling = 1.3  # How quickly alien point values increase.
        self.initialize_dynamic_settings()

        # Name of save file to load and save the high score.
        self.high_score_savefile = "high_score_save.json"

    def initialize_dynamic_settings(self):
        '''Initialize settings susceptible to change during gameplay.'''
        self.doctor_speed = 4.5 * self.ms_multiplier
        self.virus_speed = 0.8 * self.ms_multiplier
        self.bullet_speed = 7.5 * self.ms_multiplier
        self.virus_direction = 1  # (+)1 represents right; (-)1 represents left

        # Scoring.
        self.virus_points = 50

    def change_virus_direction(self):
        self.virus_direction *= -1

    def increase_speed(self):
        '''Change game settings upon reaching the next level.'''
        self.virus_speed *= self.speedup_scale
        self.doctor_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.virus_points = int(self.score_scaling * self.virus_points)
