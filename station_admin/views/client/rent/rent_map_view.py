from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from station_admin.models import Site, RentSpot
from station_admin.repository import site_repository, renting_session_repository


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

        renting_session = renting_session_repository.find_active_session(self.request.user) if self.request.user.is_authenticated else None

        return render(
            request,
            'client/renting_site/map.html',
            {'sites': sites, 'renting_session': renting_session, 'spot': spot, 'preselected_site': preselected_site}
        )