class UserAlreadyHasRentSessionException(Exception):
    def __init__(self, message='User already has rent session in progress.'):
        self.message = message
        super().__init__(self.message)