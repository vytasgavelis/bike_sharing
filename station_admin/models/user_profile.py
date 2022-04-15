from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.FloatField(default=0)

    def full_name(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"
