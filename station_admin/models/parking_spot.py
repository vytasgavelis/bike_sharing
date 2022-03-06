from django.db import models
from .site import Site


class ParkingSpot(models.Model):
    taken = models.BooleanField()
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

    class SpotType(models.TextChoices):
        SCOOTER = 'scooter'
        BIKE = 'bike'

    spot_type = models.CharField(
        max_length=30,
        choices=SpotType.choices,
        default=SpotType.BIKE,
    )

    def __str__(self):
        return f"{self.id} - {self.spot_type}"