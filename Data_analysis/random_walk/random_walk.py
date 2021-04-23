"""
Pierre-Charles Dussault
March 11, 2021

Representation of a random walk: charting a course decided by randomness.
"""
from random import choice


class RandomWalk():
    """
    Class to generate random walks.

    To make random decisions, we'll store possible moves in a list, and then
    use the choice() function from the random module, to decide which move to
    make each time a step is taken.
    """

    def __init__(self, num_points=5000):

        # Default number of points is 5000.
        self.num_points = num_points

        # Progressing list of (x, y) coordinates, starting at 0, 0
        self.x_values = [0]
        self.y_values = [0]

    def fill_walk(self):
        """
        Calculate all the points in the walk.
        """

        # Keep walking until the walk reaches the desired length.
        while len(self.x_values) < self.num_points:
            # Decide which direction to go and how to far to go in
            # that direction.
            x_direction = choice([1, -1])
            x_distance = choice([0, 1, 2, 3, 4])
            x_step = x_direction * x_distance
            y_direction = choice([1, -1])
            y_distance = choice([0, 1, 2, 3, 4])
            y_step = y_direction * y_distance

            # Reject moves that go nowhere.
            if x_step == 0 and y_step == 0:
                continue

            # If the move is not rejected, calculate the new position.
            x = self.x_values[-1] + x_step
            y = self.y_values[-1] + y_step
            self.x_values.append(x)
            self.y_values.append(y)
