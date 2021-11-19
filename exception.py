class BeansException(Exception):
    def __init__(self, message: str):
        self.message = message

    def get_message(self):
        return self.message


class InvalidArgumentException(BeansException):
    def __init__(self, argument: str):
        super().__init__(f"Invalid argument: {argument}")


class MissingArgumentException(BeansException):
    def __init__(self, argument: str):
        super().__init__(f"Missing argument: {argument}")


class NotEnoughArgumentsException(BeansException):
    def __init__(self, required: int, provided: int = 0):
        super().__init__(f"This command requires {required} arguments, {provided} provided")


class InvalidCredentialsException(BeansException):
    def __init__(self, host: str = '127.0.0.1', port: int = 11300):
        super().__init__(f"Can't connect to {host}:{port}")


class ClientNotInitializedException(BeansException):
    def __init__(self):
        super().__init__(f"Client is not initialized. You have to call connect() method first")
