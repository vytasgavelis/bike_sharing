from django.contrib.auth.models import User
from station_admin.exception.not_enough_credits_exception import NotEnoughCreditsException
from station_admin.exception.site_not_configured_correctly_exception import SiteNotConfiguredCorrectlyException
from station_admin.models.rent_spot import RentSpot
import requests
from station_admin.models.charge_rule import ChargeRule
from copy import deepcopy
from station_admin.models.rent_session import RentSession
import datetime
from station_admin.models.vehicle import Vehicle


class RentHandler:
    def open_rent_spot_lock(self, spot_id: int, user: User) -> None:
        spot = RentSpot.objects.get(pk=spot_id)

        if not spot:
            raise Exception('Rent spot was not found.')

        site = spot.site

        if not site.enough_credits_for_renting(user):
            raise NotEnoughCreditsException('User does not have enough credits.')

        if not site.lock_open_url or not site.lock_close_url:
            raise SiteNotConfiguredCorrectlyException('Site and spot must be configured for renting.')

        response = requests.post(f"{site.lock_open_url}", json={'id': spot.external_id})

        if response.status_code != 200:
            raise Exception('Could not open vehicle lock.')

    def start_session(self, spot_id: int, user: User) -> None:
        spot = RentSpot.objects.get(pk=spot_id)

        if not spot:
            raise Exception('Rent spot was not found.')

        if not spot.vehicle:
            raise Exception('Rent spot does not have vehicle.')

        site = spot.site
        vehicle = spot.vehicle
        copied_charge_rule = self.clone_charge_rule(site.rent_charge_rule)

        session = self._create_session(copied_charge_rule, spot, user, vehicle)

        vehicle.current_spot = None

        copied_charge_rule.save()
        session.save()
        vehicle.save()

    def clone_charge_rule(self, charge_rule: ChargeRule) -> ChargeRule:
        copied_charge_rule: ChargeRule = deepcopy(charge_rule)
        copied_charge_rule.id = None

        return copied_charge_rule

    def _create_session(
            self,
            charge_rule: ChargeRule,
            spot: RentSpot,
            user: User,
            vehicle: Vehicle
    ) -> RentSession:
        session = RentSession()
        session.start_time = datetime.datetime.now()
        session.taken_from_spot = spot
        session.user = user
        session.charge_rule = charge_rule
        session.vehicle = vehicle

        return session
