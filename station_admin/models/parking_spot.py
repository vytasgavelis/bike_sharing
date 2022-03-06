from django.db import models

class ParkingSpot(models.Model):


    #SpotType = models.TextChoices(SCOOTER_TYPE, BIKE_TYPE)

    taken = models.BooleanField()
    #spot_type = models.CharField(choices=SpotType.choices, max_length=50)

    class SpotType(models.TextChoices):
        SCOOTER = 'scooter'
        BIKE = 'bike'

    spot_type = models.CharField(
        max_length=30,
        choices=SpotType.choices,
        default=SpotType.BIKE,
    )