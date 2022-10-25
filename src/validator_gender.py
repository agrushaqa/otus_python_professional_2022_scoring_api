class ValidatorGender:
    def __init__(self, message=None):
        self.value = message
        if self.value < 0:
            raise ValueError(f"{self.value} less then 0")
        if self.value > 2:
            raise ValueError(f"{self.value} more then 2")
        if not isinstance(self.value, int):
            raise ValueError(f"{self.value} type is {type(self.value)}")
