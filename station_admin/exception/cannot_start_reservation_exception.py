class CannotStartReservationException(Exception):
    def __init__(self, message='Cannot start reservation.'):
        self.message = message
        super().__init__(self.message)