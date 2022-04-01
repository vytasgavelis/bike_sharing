from django.db import models

from station_admin.models import ParkingSpot
from station_admin.models.charge_rule import ChargeRule
from django.contrib.auth.models import User
from datetime import datetime, timezone, timedelta


class ParkingSession(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    parking_spot = models.ForeignKey(ParkingSpot, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    charge_rule = models.ForeignKey(ChargeRule, on_delete=models.CASCADE)
    #TODO: add relation to session here so this can be filtered out in the admin.

    class Meta:
        db_table = "parking_session"

    def get_elapsed_minutes(self) -> str:
        return self.format_timedelta(datetime.now(timezone.utc) - self.start_time)

    def format_timedelta(self, delta: timedelta) -> str:
        """Formats a timedelta duration to [N days] %H:%M:%S format"""
        seconds = int(delta.total_seconds())

        secs_in_a_day = 86400
        secs_in_a_hour = 3600
        secs_in_a_min = 60

        days, seconds = divmod(seconds, secs_in_a_day)
        hours, seconds = divmod(seconds, secs_in_a_hour)
        minutes, seconds = divmod(seconds, secs_in_a_min)

        time_fmt = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        if days > 0:
            suffix = "s" if days > 1 else ""
            return f"{days} day{suffix} {time_fmt}"

        return time_fmt
