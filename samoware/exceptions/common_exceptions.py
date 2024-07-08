class NotFoundConnection(Exception):
    def __init__(self, message="Connection with samoware not found"):
        self.message = message
        super().__init__(message)


class AuthenticationError(Exception):
    def __init__(self, message="Authentication error"):
        self.message = message
        super().__init__(message)


class ServiceError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)