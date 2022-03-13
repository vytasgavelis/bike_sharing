class ErrorOpeningSiteGateException(Exception):
    def __init__(self, message='Error when opening site gate.'):
        self.message = message
        super().__init__(self.message)