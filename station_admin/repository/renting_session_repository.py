from django.contrib.auth.models import User
from django.db.models import QuerySet

from station_admin.models.rent_session import RentSession

class RentingSessionRepository:
    def find_active_sessions(self, user: User) -> QuerySet:
        return \
            RentSession.objects.filter(user=user, returned_to_spot=None) \
            | RentSession.objects.filter(user=user, end_time=None)