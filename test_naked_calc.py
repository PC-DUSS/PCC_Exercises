"""
Pierre-Charles Dussault
April 21, 2021

Get a grasp of unittest, but without object-orientation.
Sister file to 'naked_calc.py'.
"""
import unittest
import naked_calc as calc


class TestNakedCalc(unittest.TestCase):

    def test_add(self):
        self.assertEqual(calc.add(1, 2), 3)

    def test_subtract(self):
        self.assertEqual(calc.subtract(1, 2), -1)

    def test_multiply(self):
        self.assertEqual(calc.multiply(1, 2), 2)

    def test_divide(self):
        self.assertEqual(calc.divide(1, 2), 0.5)


if __name__ == '__main__':
    unittest.main()
