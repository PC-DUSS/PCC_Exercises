import unittest
from city_country import format_city_country

class CityCountryTestCase(unittest.TestCase):
    """Tests for format_city_country()."""

    def test_city_country(self):
        """Test if formatting works."""
        formatted_output = format_city_country('santiago', 'chile')
        self.assertEqual(formatted_output, 'Santiago, Chile')

    def test_city_country_with_population(self):
        """Test if it works with population number."""
        formatted_output = format_city_country('montreal','canada', 1780000)

unittest.main()
