from django.db import models
from django.db.models import QuerySet

# TODO: use inline forms to edit parking spot in site form.
from django.contrib import admin

from station_admin.models.charge_rule import ChargeRule
#from station_admin.provider import qr_code_url_provider
from django.utils.html import format_html


class Site(models.Model):
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    external_id = models.CharField(max_length=50)
    gate_open_url = models.CharField(max_length=100, null=True, blank=True)
    lock_open_url = models.CharField(max_length=100, null=True, blank=True)

    # TODO: maybe this should not allow for nulls.
    parking_charge_rule = models.ForeignKey(
        ChargeRule,
        on_delete=models.CASCADE,
        related_name='parking_charge_rule',
        null=True,
        blank=True,
    )

    rent_charge_rule = models.ForeignKey(
        ChargeRule,
        on_delete=models.CASCADE,
        related_name='rent_charge_rule',
        null=True,
        blank=True,
    )

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

    @admin.display
    def get_qr_code_url_html(self) -> str:
        #TODO: move this outside model
        #return format_html('<a href="{}">Download</a>', qr_code_url_provider.get_url(self.id))
        return 'random+url'
