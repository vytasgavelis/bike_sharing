class NotEnoughCreditsException(Exception):
    def __init__(self, message='User does not have enough credits'):
        self.message = message
        super().__init__(self.message)
