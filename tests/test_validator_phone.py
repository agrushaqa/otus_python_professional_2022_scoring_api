import unittest

from ..src.validator_phone import ValidatorPhone


class TestValidatorEmail(unittest.TestCase):
    def test_simple_email_str(self):
        ValidatorPhone("71234567890")

    def test_simple_email_int(self):
        ValidatorPhone(71234567890)

    def test_invalid_email_long(self):
        with self.assertRaises(ValueError):
            ValidatorPhone(712345678902)

    def test_invalid_email_short(self):
        with self.assertRaises(ValueError):
            ValidatorPhone(7123456789)

    def test_invalid_first_number(self):
        with self.assertRaises(ValueError):
            ValidatorPhone(81234567890)
