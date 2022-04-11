from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from station_admin.exception.not_enough_credits_exception import NotEnoughCreditsException
from station_admin.exception.site_not_configured_correctly_exception import SiteNotConfiguredCorrectlyException
from station_admin.exception.spot_missing_vehicle_exception import SpotMissingVehicleException
from station_admin.exception.user_already_has_rent_session_exception import UserAlreadyHasRentSessionException
from station_admin.models.vehicle import Vehicle
from station_admin.models.rent_spot import RentSpot
from station_admin.helper import user_helper

class VehicleView(View):
    def get(self, *args, **kwargs) -> HttpResponse:

        #spot_missing_vehicle = user_already_has_rent_session = not_enough_credits = site_not_configured = False

        # try:
        #     user_helper.validate_is_eligible_for_rent(rent_spot, self.request.user)
        # except SpotMissingVehicleException:
        #     spot_missing_vehicle = True
        # except UserAlreadyHasRentSessionException:
        #     user_already_has_rent_session = True
        # except NotEnoughCreditsException:
        #     not_enough_credits = True
        # except SiteNotConfiguredCorrectlyException:
        #     site_not_configured = True

        rent_spot = get_object_or_404(RentSpot, pk=kwargs['id'])

        has_active_session = user_helper.has_active_rent_session(self.request.user)

        return render(self.request, 'client/renting_site/vehicle.html', {
            'rent_spot': rent_spot,
            'has_active_session': has_active_session
            # 'spot_missing_vehicle': spot_missing_vehicle,
            # 'user_already_has_rent_session': user_already_has_rent_session,
            # 'not_enough_credits': not_enough_credits,
            # 'site_not_configured': site_not_configured,
        })
