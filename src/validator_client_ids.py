import re


class ValidatorClientIds:
    def __init__(self, value=None):
        self.client_ids = value
        # if type(value) is dict:
        #     self.client_ids = value.values()
        if type(value) is not list:  # and type(value) is not tuple:
            raise TypeError(f"type is {type(value)}")
        for i_value in value:
            if type(i_value) is not int:
                raise TypeError(f"value '{i_value} has type {type(i_value)}")

        for i_value in self.client_ids:
            if re.match("^[-+]?\d+$", str(i_value)) is None:
                raise ValueError(f"'{i_value}' invalid client id")
