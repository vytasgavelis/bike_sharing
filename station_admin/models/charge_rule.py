from django.db import models


class ChargeRule(models.Model):
    price = models.IntegerField()
    max_time_mins = models.IntegerField(null=True, blank=True)
    # site = models.ForeignKey(
    #     # apps.get_model('station_admin', 'Site'),
    #     'station_admin.Site',
    #     related_name='site',
    #     on_delete=models.CASCADE,
    #     null=True,
    #     blank=True,
    # )
    # TODO: add relation for parking/rent session
