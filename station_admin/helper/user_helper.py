from django.contrib.auth.models import User

from station_admin.exception.not_enough_credits_exception import NotEnoughCreditsException
from station_admin.exception.site_not_configured_correctly_exception import SiteNotConfiguredCorrectlyException
from station_admin.exception.spot_missing_vehicle_exception import SpotMissingVehicleException
from station_admin.exception.user_already_has_rent_session_exception import UserAlreadyHasRentSessionException
from station_admin.models.site import Site
from station_admin.models.parking_session import ParkingSession
from station_admin.repository.parking_session_repository import ParkingSessionRepository
from station_admin.repository import renting_session_repository
from station_admin.models.rent_spot import RentSpot
from django.core.exceptions import ObjectDoesNotExist

class UserHelper:
    def has_parking_session_in_site(self, site: Site, user: User) -> bool:
        return 0 < len(ParkingSessionRepository.find_active_sessions(user, site))

    def has_active_rent_session(self, user: User) -> bool:
        return 0 < len(renting_session_repository.find_active_sessions(user))

    def validate_is_eligible_for_rent(self, spot: RentSpot, user: User) -> None:
        #TODO: bug exists here because it allows for reserved vehicle to be rented.
        try:
            if not spot.vehicle:
                raise SpotMissingVehicleException
        except ObjectDoesNotExist:
            raise SpotMissingVehicleException

        if self.has_active_rent_session(user):
            raise UserAlreadyHasRentSessionException

        site = spot.site

        if not site.enough_credits_for_renting(user):
            raise NotEnoughCreditsException

        if not site.lock_open_url or not site.lock_close_url:
            raise SiteNotConfiguredCorrectlyException