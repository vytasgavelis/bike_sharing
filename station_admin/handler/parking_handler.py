import datetime
from decimal import Decimal

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
from station_admin.repository.parking_session_repository import ParkingSessionRepository

class ParkingHandler:
    def open_site_door(self, user: User, site: Site) -> None:
        sessions = ParkingSessionRepository.find_active_sessions(user)
        if len(sessions) > 0:
            raise Exception('You already have parking session in progress')

        if not site.enough_credits_for_parking(user):
            raise NotEnoughCreditsException

        if not site.gate_open_url or not site.external_id:
            raise SiteNotConfiguredCorrectlyException

        response = requests.post(f"{site.gate_open_url}", json={'id': site.external_id})

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

    def end_session(self, session: ParkingSession, site: Site, user: User) -> None:
        if not site.gate_open_url or not site.external_id:
            raise SiteNotConfiguredCorrectlyException('Site is not configured correctly.')

        response = requests.post(site.gate_open_url, json={'id': site.external_id})

        if response.status_code != 200:
            raise ErrorOpeningSiteGateException('Could not open site doors.')

        session.end_time = datetime.datetime.now()
        user.userprofile.credits -= Decimal(session.get_price())
        session.parking_spot.taken = False

        session.save()
        user.userprofile.save()
        session.parking_spot.save()

