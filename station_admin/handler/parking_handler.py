import datetime
from django.contrib.auth.models import User
from station_admin.models import Site
from station_admin.exception.not_enough_credits_exception import NotEnoughCreditsException
from station_admin.exception.site_not_configured_correctly_exception import SiteNotConfiguredCorrectlyException
from station_admin.exception.error_opening_site_gate_exception import ErrorOpeningSiteGateException
import requests
from station_admin.models.parking_session import ParkingSession
from station_admin.models.parking_spot import ParkingSpot
from copy import deepcopy
from station_admin.models.charge_rule import ChargeRule

class ParkingHandler:
    def open_site_door(self, user: User, site: Site) -> None:
        if not site.enough_credits_for_parking(user):
            raise NotEnoughCreditsException

        if not site.gate_open_url or not site.external_id:
            raise SiteNotConfiguredCorrectlyException

        #TODO: send external_id via request body.
        response = requests.post(f"{site.gate_open_url}")

        if response.status_code != 200:
            raise ErrorOpeningSiteGateException()

    def start_session(self, user: User, site: Site, spot_type: str) -> None:
        spot: ParkingSpot = site.get_available_spots(spot_type).first()

        if not spot:
            raise Exception("No free spot is available")

        copied_charge_rule: ChargeRule = deepcopy(site.parking_charge_rule)
        copied_charge_rule.id = None

        session = ParkingSession()
        session.start_time = datetime.datetime.now()
        session.parking_spot = spot
        session.user = user
        session.charge_rule = copied_charge_rule

        spot.taken = True

        copied_charge_rule.save()
        session.save()
        spot.save()
