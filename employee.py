"""
Pierre-Charles Dussault
28 October, 2020

Exercise to practice unit testing of a custom class.
"""

class Employee():
    """Representation of an employee."""

    def __init__(self, first, last, salary):
        """Constructor for instances of an employee."""
        self.first = first
        self.last = last
        self.salary = salary

    def give_raise(self, salary_raise=5000):
        """Give a raise to an employee. Default value of the raise is 5000$."""
        self.salary += salary_raise
