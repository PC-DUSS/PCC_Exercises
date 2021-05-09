"""
Pierre-Charles Dussault
April 21, 2021

Small program to get a grasp of unittest.
Sister program to 'calculator.py'.
"""
import unittest
import calculator as calc


class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.my_calc = calc.Calculator()

    def test_add(self):
        self.assertEqual(self.my_calc.add(1, 2), 3)

    def test_subtract(self):
        self.assertEqual(self.my_calc.subtract(1, 2), -1)

    def test_multiply(self):
        self.assertEqual(self.my_calc.multiply(1, 2), 2)

    def test_divide(self):
        self.assertEqual(self.my_calc.divide(1, 2), 0.5)


if __name__ == '__main__':
    unittest.main()
