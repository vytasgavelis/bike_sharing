from django.contrib.auth.models import User
from django.db.models import QuerySet

from station_admin.models.rent_session import RentSession

class RentingSessionRepository:
    # TODO: this should throw exception if more than one session is found.
    def find_active_sessions(self, user: User) -> QuerySet:
        return \
            RentSession.objects.filter(user=user, returned_to_spot=None) \
            | RentSession.objects.filter(user=user, end_time=None)

    def find_active_session(self, user: User) -> RentSession | None:
        sessions = self.find_active_sessions(user)
        if len(sessions) > 1:
            raise Exception('More than one rent session found.')

        if len(sessions) == 1:
            return sessions[0]

        return None


