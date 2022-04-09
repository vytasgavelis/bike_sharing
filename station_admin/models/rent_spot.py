from django.db import models
from station_admin.models.site import Site
from station_admin.enum.vehicle_type import VehicleType
from django.contrib import admin
from station_admin.provider import qr_code_url_provider
from django.utils.html import format_html

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

    @admin.display
    def get_qr_code_url_html(self) -> str:
        return format_html('<a href="{}">Download QR code</a>', qr_code_url_provider.get_rent_spot_qrcode_url(self.id))