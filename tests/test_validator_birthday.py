import unittest
from ..src.validator_birthday import ValidatorBirthday


class TestValidatorDate(unittest.TestCase):
    def test_simple_date(self):
         ValidatorBirthday("01.12.2001")

    def test_invalid_date_without_point(self):
        with self.assertRaises(Exception):
            ValidatorBirthday("01122021")

    def test_date_without_zero(self):
        ValidatorBirthday("1.12.1995")

    def test_invalid_date_in_future(self):
        with self.assertRaises(Exception):
            ValidatorBirthday("01.12.2030")

    def test_invalid_date_too_old(self):
        with self.assertRaises(Exception):
            ValidatorBirthday("01.12.1950")