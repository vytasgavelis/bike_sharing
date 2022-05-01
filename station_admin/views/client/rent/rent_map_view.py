from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from station_admin.models import Site, RentSpot
from station_admin.repository import site_repository, renting_session_repository, rent_spot_repository


class RentMapView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        spot_id = request.GET.get('spot_id')
        spot = None
        if spot_id:
            try:
                spot = RentSpot.objects.get(pk=spot_id)
            except ObjectDoesNotExist:
                pass

        site_id = request.GET.get('site_id')
        preselected_site = None
        if site_id:
            try:
                preselected_site = Site.objects.get(pk=site_id)
            except ObjectDoesNotExist:
                pass

        sites: list[Site] = site_repository.find_with_rent_configured()

        renting_session = renting_session_repository.find_active_rent_session(self.request.user) if self.request.user.is_authenticated else None

        renting_reservation = None
        has_renting_reservation = False
        if self.request.user:
            reservations = renting_session_repository.find_active_reservations_by_user(self.request.user)
            if len(reservations) > 0:
                has_renting_reservation = True
                renting_reservation = reservations[0]

        available_rent_spots = rent_spot_repository.get_available_rent_spots()

        return render(
            request,
            'client/renting_site/map.html',
            {
                'sites': sites,
                'renting_session': renting_session,
                'spot': spot,
                'preselected_site': preselected_site,
                'has_renting_reservation': has_renting_reservation,
                'available_rent_spots': available_rent_spots,
                'renting_reservation': renting_reservation,
            }
        )