from django.db import models
from django.db.models import QuerySet


class Site(models.Model):
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    external_id = models.CharField(max_length=50)
    gate_open_url = models.CharField(max_length=100, null=True, blank=True)
    lock_open_url = models.CharField(max_length=100, null=True, blank=True)

    def get_available_spots(self, spot_type: str) -> QuerySet:
        return self.parkingspot_set.filter(spot_type=spot_type, taken=False)

    def get_bike_spots(self) -> QuerySet:
        return self.parkingspot_set.filter(spot_type='bike')

    def get_scooter_spots(self) -> QuerySet:
        return self.parkingspot_set.filter(spot_type='scooter')

    def get_available_bike_spots(self) -> QuerySet:
        # TODO: use type from constant
        return self.get_available_spots('bike')

    def get_available_scooter_spots(self) -> QuerySet:
        # TODO: use type from constant
        return self.get_available_spots('scooter')

    def __str__(self) -> str:
        return f"{self.name} - {self.street}, {self.city}"
