import unittest
from ..src.validator_client_ids import ValidatorClientIds


class TestValidatorClientIds(unittest.TestCase):
    def test_dict(self):
        with self.assertRaises(Exception):
            ValidatorClientIds({1: 2})

    def test_list_str_as_number(self):
        with self.assertRaises(Exception):
            ValidatorClientIds(["1", "2"])

    def test_list(self):
         ValidatorClientIds([1, 2])

    def test_tuple(self):
        with self.assertRaises(Exception):
            ValidatorClientIds((1, 2))

    def test_tuple(self):
         ValidatorClientIds([])

    def test_invalid_client_ids_number(self):
        with self.assertRaises(Exception):
            ValidatorClientIds(56)

    def test_invalid_client_ids_str(self):
        with self.assertRaises(Exception):
            ValidatorClientIds("M")
