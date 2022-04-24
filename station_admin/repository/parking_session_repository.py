from django.db.models import QuerySet
from station_admin.models.parking_session import ParkingSession
from station_admin.models.site import Site
from django.contrib.auth.models import User


class ParkingSessionRepository:
    @staticmethod
    def find_active_sessions(user: User, site: Site = None) -> list[ParkingSession]:
        user_sessions = ParkingSession.objects.filter(user=user, end_time=None)

        if not site:
            return user_sessions

        return [session for session in user_sessions if session.parking_spot.site == site]

    @staticmethod
    def find_sessions(user: User) -> QuerySet:
        return ParkingSession.objects.filter(user=user)