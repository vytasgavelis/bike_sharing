from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Site
from .models import ParkingSpot
from .models.charge_rule import ChargeRule

admin.site.register(ParkingSpot)
admin.site.register(ChargeRule)


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'street', 'city', 'get_qr_code_url_html',)
