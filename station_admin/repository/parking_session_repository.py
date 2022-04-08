from django.db.models import QuerySet
from station_admin.models.parking_session import ParkingSession
from station_admin.models.site import Site
from django.contrib.auth.models import User


class ParkingSessionRepository:
    @staticmethod
    def find_active_sessions(user: User, site: Site) -> list[ParkingSession]:
        user_sessions = ParkingSession.objects.filter(user=user, end_time=None)

        return [session for session in user_sessions if session.parking_spot.site == site]
