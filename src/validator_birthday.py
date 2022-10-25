import datetime
import os
import sys

from config import Config

script_dir = os.path.dirname(__file__)
sys.path.append(script_dir)


class ValidatorBirthday:
    def __init__(self, message=None):
        self.datetime = datetime.datetime.strptime(message, '%d.%m.%Y')
        expected_delta = datetime.timedelta(
            days=Config().birthday_delta)
        actual_delta = datetime.datetime.now() - self.datetime
        if actual_delta.days < 0:
            raise ValueError("data in future")
        if actual_delta > expected_delta:
            raise ValueError("data is too old")

    def __str__(self):
        return str(self.datetime)
