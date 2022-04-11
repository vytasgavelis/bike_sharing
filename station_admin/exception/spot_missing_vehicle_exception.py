class SpotMissingVehicleException(Exception):
    def __init__(self, message='Spot does not have a vehicle.'):
        self.message = message
        super().__init__(self.message)