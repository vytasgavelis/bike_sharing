from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    phone_number = models.CharField(max_length=50)

    def full_name(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

    def date_joined(self) -> str:
        return self.user.date_joined.strftime("%m/%d/%Y")