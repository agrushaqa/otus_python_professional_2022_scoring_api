import re


class ValidatorPhone:
    def __init__(self, phone=None):
        self.phone = str(phone)
        if re.match(r"^7\d{10}$", self.phone) is None:
            raise ValueError(f"'{self.phone}' invalid first symbol")
