from django.contrib.auth.models import User
from django.db.models import QuerySet

from station_admin.models import RentSpot, Vehicle
from station_admin.models.rent_session import RentSession


class RentingSessionRepository:
    # TODO: this should throw exception if more than one session is found.
    #TODO: this causes bug in reservation beause it reservation do not have returned to spot and it counts that as actuve
    def find_active_sessions(self, user: User) -> QuerySet:
        return RentSession.objects.filter(user=user, end_time=None)

    def find_active_session(self, user: User) -> RentSession | None:
        sessions = self.find_active_sessions(user)
        if len(sessions) > 1:
            raise Exception('More than one rent session found.')

        if len(sessions) == 1:
            return sessions[0]

        return None

    def find_active_reservations_by_vehicle(self, vehicle: Vehicle) -> QuerySet:
        # Reservation - session with no taken from spot and returned to spot and no end time
        return RentSession.objects.filter(
            vehicle=vehicle, taken_from_spot=None, returned_to_spot=None, end_time=None
        )

    def find_active_reservations_by_user(self, user: User) -> QuerySet:
        return RentSession.objects.filter(
            user=user, taken_from_spot=None, returned_to_spot=None, end_time=None
        )

    def find_sessions(self, user: User) -> QuerySet:
        return RentSession.objects.filter(user=user)

    def find_all_active_sessions(self) -> QuerySet:
        return RentSession.objects.filter(end_time=None)