from datetime import datetime


class ValidatorDate:
    def __init__(self, message=None):
        self.datetime = datetime.strptime(message, '%d.%m.%Y')

    def __str__(self):
        return str(self.datetime)
