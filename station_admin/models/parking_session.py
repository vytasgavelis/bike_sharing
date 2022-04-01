from django.db import models

from station_admin.models import ParkingSpot
from station_admin.models.charge_rule import ChargeRule
from django.contrib.auth.models import User

class ParkingSession(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    charge_rule = models.ForeignKey(ChargeRule, on_delete=models.CASCADE)
    #TODO: add relation to session here so this can be filtered out in the admin.

    class Meta:
        db_table = "parking_session"