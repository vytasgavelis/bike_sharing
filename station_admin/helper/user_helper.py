from django.contrib.auth.models import User
from station_admin.models.site import Site
from station_admin.models.parking_session import ParkingSession
from station_admin.repository.parking_session_repository import ParkingSessionRepository

class UserHelper():
    def has_parking_session_in_site(self, site: Site, user: User) -> bool:
        return 0 < len(ParkingSessionRepository.find_active_sessions(user, site))

