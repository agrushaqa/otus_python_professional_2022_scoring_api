class ValidatorLastName:
    def __init__(self, message=None):
        self.value = message
        if not isinstance(self.value, str):
            raise ValueError(f"{self.value} type is {type(self.value)}")
