from django.db import models

from station_admin.enum.vehicle_type import VehicleType
from station_admin.models.rent_spot import RentSpot
from django.core.exceptions import ValidationError

class Vehicle(models.Model):
    current_spot = models.OneToOneField(RentSpot, on_delete=models.CASCADE, null=True, blank=True)
    spot_type = models.CharField(
        max_length=50,
        choices=VehicleType.choices,
        default=VehicleType.BIKE
    )
    name = models.CharField(max_length=50)
    #TODO: rename this to vehicle_type

    def clean(self) -> None:
        if self.current_spot and self.current_spot.spot_type != self.spot_type:
            raise ValidationError('Vehicle and spot types must match')

    def __str__(self) -> str:
        return f"{self.spot_type} - #{self.id} - {self.name}"
