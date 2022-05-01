from django.db import models


class ChargeRule(models.Model):
    price = models.FloatField()
    max_time_mins = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.price}€ - {self.max_time_mins} min."

    def get_min_parking_price(self) -> float:
        # Hardcoded 5 minutes as min parking time
        return self.price * 5

    def get_min_renting_price(self) -> float:
        # Hardcoded 5 minutes as min renting time
        return self.price * 5

    def get_max_time_formatted(self) -> str:
        hours = int(self.max_time_mins / 60)
        minutes = self.max_time_mins - hours * 60

        hours_formatted = str(hours).rjust(2, '0')
        minutes_formatted = str(minutes).rjust(2, '0')

        return f"{hours_formatted}:{minutes_formatted}:00"
