"""
Pierre-Charles Dussault
28 October, 2020

Tests for Employee class from 'employee.py'.
"""

import unittest
from employee import Employee

class EmployeeTestCase(unittest.TestCase):
    """Test case for Employee class."""

    def setUp(self):
        """Define global variables and class instances for the test case."""
        self.my_employee = Employee('John', 'Doe', 25000)

    def test_default_raise(self):
        """
        Test if the default raise of employee salary gives a raise of the
        appropriate default amount.
        """
        self.my_employee.give_raise()
        self.assertEqual(self.my_employee.salary, 30000)

    def test_custom_raise(self):
        """Test if the custom raising of employee salary gives a raise of the
        appropriate custom amount.
        """
        self.my_employee.give_raise(10000)
        self.assertEqual(self.my_employee.salary, 35000)

unittest.main()
