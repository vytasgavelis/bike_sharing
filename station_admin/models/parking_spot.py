from django.db import models
from .site import Site
from station_admin.enum.vehicle_type import VehicleType


class ParkingSpot(models.Model):
    taken = models.BooleanField()
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    spot_type = models.CharField(
        max_length=30,
        choices=VehicleType.choices,
        default=VehicleType.BIKE,
    )

    def __str__(self):
        return f"{self.id} - {self.spot_type}"
