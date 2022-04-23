from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from station_admin.exception.cannot_start_reservation_exception import CannotStartReservationException
from station_admin.exception.not_enough_credits_exception import NotEnoughCreditsException
from station_admin.exception.site_not_configured_correctly_exception import SiteNotConfiguredCorrectlyException
from station_admin.exception.spot_missing_vehicle_exception import SpotMissingVehicleException
from station_admin.exception.user_already_has_rent_session_exception import UserAlreadyHasRentSessionException
from station_admin.models import Site
from station_admin.models.rent_spot import RentSpot
import requests
from station_admin.models.charge_rule import ChargeRule
from copy import deepcopy
from station_admin.models.rent_session import RentSession
import datetime
from station_admin.models.vehicle import Vehicle
from station_admin.helper import user_helper
from station_admin.repository import renting_session_repository


class RentHandler:
    def open_rent_spot_lock(self, spot: RentSpot, user: User) -> None:
        site = spot.site

        user_helper.validate_is_eligible_for_rent(spot, user)

        response = requests.post(f"{site.lock_open_url}", json={'id': spot.external_id})

        if response.status_code != 200:
            raise Exception('Could not open vehicle lock.')

    def start_session(self, spot: RentSpot, user: User) -> None:
        user_helper.validate_is_eligible_for_rent(spot, user)

        site = spot.site
        vehicle = spot.vehicle
        copied_charge_rule = self.clone_charge_rule(site.rent_charge_rule)

        session = self._create_session(copied_charge_rule, spot, user, vehicle)

        vehicle.current_spot = None

        copied_charge_rule.save()
        session.save()
        vehicle.save()

    def start_reservation(self, spot: RentSpot, user: User) -> None:
        user_helper.validate_is_eligible_for_rent(spot, user)
        self.validate_spot_is_not_reserved(spot)

        copied_charge_rule = self.clone_charge_rule(spot.site.rent_charge_rule)

        session = self._create_session(copied_charge_rule, None, user, spot.vehicle)
        copied_charge_rule.save()
        session.save()

    def end_reservation(self, user: User) -> None:
        sessions = renting_session_repository.find_active_reservations_by_user(user)
        if len(sessions) == 0:
            raise Exception('You do not have a reservation')

        session = sessions[0]

        session.end_time = datetime.datetime.now()
        user.userprofile.credits -= Decimal(session.get_price())

        session.save()
        user.userprofile.save()

    def validate_spot_is_not_reserved(self, spot: RentSpot) -> None:
        reservations = renting_session_repository.find_active_reservations_by_vehicle(spot.vehicle)
        if len(reservations) > 0:
            raise CannotStartReservationException('This vehicle is already reserved')



    def end_session(self, spot: RentSpot, user: User) -> None:
        session = self._validate_is_eligible_for_rent_completion(spot, user)

        self._close_rent_spot_lock(spot)

        vehicle = session.vehicle

        session.end_time = datetime.datetime.now()
        session.returned_to_spot = spot
        vehicle.current_spot = spot
        user.userprofile.credits -= Decimal(session.get_price())

        session.save()
        vehicle.save()
        user.userprofile.save()

    def _close_rent_spot_lock(self, spot: RentSpot) -> None:
        site = spot.site
        if not site.lock_open_url or not site.lock_close_url:
            raise SiteNotConfiguredCorrectlyException

        response = requests.post(f"{site.lock_close_url}", json={'id': spot.external_id})

        if response.status_code != 200:
            raise Exception('Could not close vehicle lock.')

    def _validate_is_eligible_for_rent_completion(self, spot: RentSpot, user: User) -> RentSession:
        try:
            if spot.vehicle:
                raise Exception('Spot already has vehicle in it.')
        except ObjectDoesNotExist:
            pass

        session = renting_session_repository.find_active_session(user)
        if not session:
            raise Exception('User does not have active rent session')

        rented_vehicle = session.vehicle
        if spot.spot_type != rented_vehicle.spot_type:
            raise Exception('Rent spot and vehicle types do not match.')

        return session

    def clone_charge_rule(self, charge_rule: ChargeRule) -> ChargeRule:
        copied_charge_rule: ChargeRule = deepcopy(charge_rule)
        copied_charge_rule.id = None

        return copied_charge_rule

    def _create_session(
            self,
            charge_rule: ChargeRule,
            spot: RentSpot | None,
            user: User,
            vehicle: Vehicle
    ) -> RentSession:
        session = RentSession()
        session.start_time = datetime.datetime.now()
        session.user = user
        session.charge_rule = charge_rule
        session.vehicle = vehicle

        if spot:
            session.taken_from_spot = spot

        return session

