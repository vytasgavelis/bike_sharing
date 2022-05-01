from django.db.models import QuerySet

from station_admin.models import RentSpot, RentSession
from station_admin.repository import renting_session_repository


class RentSpotRepository:
    def get_available_rent_spots(self) -> list[RentSpot]:
        rent_sessions: list[RentSession] = RentSession.objects.filter(end_time=None)
        taken_vehicle_ids = [rent_session.vehicle_id for rent_session in rent_sessions]

        return RentSpot.objects.exclude(vehicle__in=taken_vehicle_ids).exclude(vehicle=None)