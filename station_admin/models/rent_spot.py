from django.db import models
from station_admin.models.site import Site
from station_admin.enum.vehicle_type import VehicleType

class RentSpot(models.Model):
    external_id = models.CharField(max_length=50)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    spot_type = models.CharField(
        max_length=50,
        choices=VehicleType.choices,
        default=VehicleType.BIKE
    )

    def __str__(self):
        return f"{self.site}.  {self.id} - {self.spot_type}"
