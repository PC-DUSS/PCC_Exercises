"""
Pierre-Charles Dussault
October 29, 2020

Settings module for BlueSky game.
"""

class Settings():
    """Class to store all game settings for BlueSky game."""

    def __init__(self):
        """Initialize the game's settings."""
        #Screen settings.
        self.screen_width = 1600
        self.screen_height = 900
        self.bg_color = (0, 0, 230)
