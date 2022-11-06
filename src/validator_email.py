class ValidatorEmail:
    def __init__(self, message=None):
        if message is not None:
            self.message = message
            if "@" not in message:
                raise ValueError(self.message)
