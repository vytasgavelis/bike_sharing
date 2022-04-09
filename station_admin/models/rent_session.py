from django.db import models
from station_admin.models.charge_rule import ChargeRule
from django.contrib.auth.models import User
from station_admin.models.rent_spot import RentSpot

class RentSession(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    charge_rule = models.ForeignKey(ChargeRule, on_delete=models.CASCADE)
    taken_from_spot = models.ForeignKey(RentSpot, on_delete=models.CASCADE, related_name='taken_from_spot')
    returned_to_spot = models.ForeignKey(RentSpot, on_delete=models.CASCADE, related_name='returned_to_spot', null=True)