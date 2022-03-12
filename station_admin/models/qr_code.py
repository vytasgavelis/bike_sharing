from django.db import models


class QrCode(models.Model):
    file_path = models.CharField(max_length=255)
    url = models.CharField(max_length=255)