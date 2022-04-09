from django.db import models
from django.db.models import QuerySet
from django.contrib.auth.models import User

# TODO: use inline forms to edit parking spot in site form.
from django.contrib import admin

from station_admin.models.charge_rule import ChargeRule
from station_admin.provider import qr_code_url_provider
from django.utils.html import format_html
from station_admin.enum.vehicle_type import VehicleType


class Site(models.Model):
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    external_id = models.CharField(max_length=50)
    gate_open_url = models.CharField(max_length=100, null=True, blank=True)
    lock_open_url = models.CharField(max_length=100, null=True, blank=True)
    lock_close_url = models.CharField(max_length=100, null=True, blank=True)

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

    def is_bike_rent_available(self) -> bool:
        return True

    def is_scooter_rent_available(self) -> bool:
        return True

    def __str__(self) -> str:
        return f"{self.name} - {self.street}, {self.city}"

    def get_formatted_address(self) -> str:
        return f"{self.street}, {self.city}"

    @admin.display
    def get_qr_code_url_html(self) -> str:
        # TODO: move this outside model
        return format_html('<a href="{}">Download QR code</a>', qr_code_url_provider.get_site_qrcode_url(self.id))

    def enough_credits_for_parking(self, user: User) -> bool:
        if not self.parking_charge_rule:
            return False

        return user.userprofile.credits >= self.parking_charge_rule.get_min_parking_price()

    def enough_credits_for_renting(self, user: User) -> bool:
        if not self.rent_charge_rule:
            return False

        return user.userprofile.credits >= self.rent_charge_rule.get_min_renting_price()

    def get_available_rent_bikes_spots(self) -> QuerySet:
        return self.get_bike_rent_spots().exclude(vehicle=None)

    def get_available_rent_scooter_spots(self) -> QuerySet:
        return self.get_scooter_rent_spots().exclude(vehicle=None)

    def get_bike_rent_spots(self) -> QuerySet:
        return self.rentspot_set.filter(spot_type=VehicleType.BIKE)

    def get_scooter_rent_spots(self) -> QuerySet:
        return self.rentspot_set.filter(spot_type=VehicleType.SCOOTER)