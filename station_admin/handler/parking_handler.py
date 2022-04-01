from django.contrib.auth.models import User
from station_admin.models import Site
from station_admin.exception.not_enough_credits_exception import NotEnoughCreditsException
from station_admin.exception.site_not_configured_correctly_exception import SiteNotConfiguredCorrectlyException
from station_admin.exception.error_opening_site_gate_exception import ErrorOpeningSiteGateException
import requests

class ParkingHandler:
    def open_site_door(self, user: User, site: Site) -> None:
        if not site.enough_credits_for_parking(user):
            raise NotEnoughCreditsException

        if not site.gate_open_url or not site.external_id:
            raise SiteNotConfiguredCorrectlyException

        #TODO: send external_id via request body.
        response = requests.post(f"{site.gate_open_url}/{site.external_id}")

        if response.status_code != 200:
            raise ErrorOpeningSiteGateException

    def start_session(self, user: User, site: Site) -> None:
        pass