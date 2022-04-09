from django.db import models

from station_admin.enum.vehicle_type import VehicleType
from station_admin.models.rent_spot import RentSpot


class Vehicle(models.Model):
    current_spot = models.OneToOneField(RentSpot, on_delete=models.CASCADE, null=True, blank=True)
    spot_type = models.CharField(
        max_length=50,
        choices=VehicleType.choices,
        default=VehicleType.BIKE
    )
