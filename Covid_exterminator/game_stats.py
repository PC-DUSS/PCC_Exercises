"""
Pierre-Charles Dussault
February 22, 2021

Covid Exterminator, a 2D shooting game made while completing
"Python Crash Course".

Game statistics module.
"""
import pygame
import json


class GameStats():
    """Track statistics for Covid Exterminator."""

    def __init__(self, game_instance):
        """Initialize statistics."""
        self.game_active = False  # Start the game in an inactive state.
        self.settings = game_instance.settings
        self.reset_stats()

        # High score should never be reset.
        self.high_score = 0

    def activate_game(self):
        self.game_active = True

    def deactivate_game(self):
        self.game_active = False

    def reset_stats(self):
        """Initialize base statistics that are subject to change during
        gameplay."""
        self.doctors_remaining = self.settings.doctors_limit
        self.score = 0
        self.level = 1

    def increase_score(self):
        """Increase score by 1."""
        self.score += self.settings.virus_points

    def update_high_score(self, new_high_score):
        """Change the value of the high score to a new value."""
        self.high_score = new_high_score

    def increase_level(self):
        """Increase the level statistic."""
        self.level += 1

    def remove_a_doctor(self):
        """Remove a doctor life from the player."""
        self.doctors_remaining -= 1

    def save_high_score(self):
        """Save the high score in a save file."""
        f_obj = self.settings.high_score_savefile

        with open(f_obj, 'w+') as f:
            json.dump(self.high_score, f)

    def load_high_score(self):
        """Load the high score from a save file."""
        f_obj = self.settings.high_score_savefile

        try:
            with open(f_obj, 'r') as f:
                self.high_score = json.load(f)

        # If the file does not exist, ignore this command.
        except FileNotFoundError:
            pass

        # If the file is empty, or not decodable, ignore this command.
        except json.decoder.JSONDecodeError:
            pass
