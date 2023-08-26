""""Sample tests."""


from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):
    """Test calc func for test."""

    def test_add_numbers(self):
        """Test first func project."""
        res = calc.add(5, 10)

        self.assertEqual(res, 15)

    def test_subtract_numbers(self):
        """Test of subtract numbers."""
        res = calc.subtract(20, 10)

        self.assertEqual(res, 10)
