from django.db import models

class Site(models.Model):
    name = models.CharField(max_length=200)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    external_id = models.CharField(max_length=50)
    gate_open_url = models.CharField(max_length=100, null=True, blank=True)
    lock_open_url = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.street}, {self.city}"
