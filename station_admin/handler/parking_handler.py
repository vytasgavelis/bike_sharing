from django.contrib.auth.models import User

from station_admin.models import Site
from station_admin.exception.not_enough_credits_exception import NotEnoughCreditsException


class ParkingHandler:
    def start_parking_session(self, user: User, site: Site) -> None:
        if not site.enough_credits_for_parking(user):
            raise NotEnoughCreditsException
