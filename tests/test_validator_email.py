import unittest
from ..src.validator_email import ValidatorEmail


class TestValidatorEmail(unittest.TestCase):
    def test_simple_email(self):
        a = ValidatorEmail("test@test.ru")

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            a = ValidatorEmail("text.ru")
