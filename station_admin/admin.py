from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .models import Site
from .models import ParkingSpot
from .models.charge_rule import ChargeRule
from .models.rent_spot import RentSpot
from .models.vehicle import Vehicle

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(ParkingSpot)
admin.site.register(ChargeRule)
admin.site.register(Vehicle)

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'street', 'city', 'get_qr_code_url_html',)

@admin.register(RentSpot)
class RentSpotAdmin(admin.ModelAdmin):
    list_display = ('id', 'site', 'spot_type', 'external_id', 'get_qr_code_url_html')