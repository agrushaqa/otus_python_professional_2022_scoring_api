class ValidatorEmail:
    def __init__(self, message=None):
        if message is not None:
            self.message = message
            if "@" not in message:
                raise ValueError(self.message)


    # def __call__(self, value):
    #     print(f"value: {value}")
    #     if not value and "@" not in value:
    #         raise ValueError(self.message)

a = ValidatorEmail("test@test.ru")
