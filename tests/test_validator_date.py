import unittest
from ..src.validator_date import ValidatorDate


class TestValidatorDate(unittest.TestCase):
    def test_simple_date(self):
        ValidatorDate("01.12.2001")

    def test_invalid_date_without_point(self):
        with self.assertRaises(Exception):
            ValidatorDate("01122021")

    def test_date_without_zero(self):
        ValidatorDate("1.12.2001")
