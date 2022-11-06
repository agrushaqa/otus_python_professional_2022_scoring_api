import unittest
from ..src.validator_gender import ValidatorGender


class TestValidatorGender(unittest.TestCase):
    def test_simple_gender_0(self):
        ValidatorGender(0)

    def test_simple_gender_1(self):
        ValidatorGender(1)

    def test_simple_gender_2(self):
        ValidatorGender(2)

    def test_invalid_gender_not_number(self):
        with self.assertRaises(Exception):
            ValidatorGender("M")

    def test_invalid_gender_more_then_3(self):
        with self.assertRaises(Exception):
            ValidatorGender("4")
