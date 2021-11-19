class InvalidArgumentException(BaseException):
    def __init__(self, argument):
        self.argument = argument

    def get_message(self):
        return f"Invalid argument: {self.argument}"
