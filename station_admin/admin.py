from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Site
from .models import ParkingSpot

admin.site.register(Site)
admin.site.register(ParkingSpot)
#admin.site.unregister(Group)