"""
Pierre-Charles Dussault
March 14, 2021

Die module.
"""

from random import randint


class Die():
    """Representation of a six-sided die."""

    def __init__(self, num_sides=6):
        """Initialize a die instance. Assume 6-sided by default."""
        self.num_sides = num_sides

    def roll(self):
        """Roll the die. Return a random value between 1 and the num_sides."""
        return randint(1, self.num_sides)
