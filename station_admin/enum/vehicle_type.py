from django.db import models


class VehicleType(models.TextChoices):
    SCOOTER = 'scooter'
    BIKE = 'bike'
