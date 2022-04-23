from django.db import models
from station_admin.models.charge_rule import ChargeRule
from django.contrib.auth.models import User
from station_admin.models.rent_spot import RentSpot
from station_admin.models.vehicle import Vehicle
from datetime import datetime, timezone, timedelta

class RentSession(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    charge_rule = models.ForeignKey(ChargeRule, on_delete=models.CASCADE)
    taken_from_spot = models.ForeignKey(RentSpot, on_delete=models.CASCADE, related_name='taken_from_spot', null=True)
    returned_to_spot = models.ForeignKey(RentSpot, on_delete=models.CASCADE, related_name='returned_to_spot', null=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    def get_elapsed_seconds(self) -> int:
        return int((datetime.now(timezone.utc) - self.start_time).total_seconds())

    def get_elapsed_minutes(self) -> str:
        return self.format_timedelta(datetime.now(timezone.utc) - self.start_time)

    def get_price(self) -> float:
        elapsed_minutes = int((datetime.now(timezone.utc) - self.start_time).total_seconds() / 60)

        return elapsed_minutes * self.charge_rule.price

    def is_max_time_exceeded(self) -> bool:
        elapsed_minutes = int((datetime.now(timezone.utc) - self.start_time).total_seconds() / 60)

        return elapsed_minutes >= self.charge_rule.max_time_mins

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