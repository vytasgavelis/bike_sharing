from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from station_admin.models import Site
from station_admin.repository import site_repository, renting_session_repository


class RentMapView(View):
    def get(self, request) -> HttpResponse:
        sites: list[Site] = site_repository.find_with_rent_configured()
        renting_session = renting_session_repository.find_active_session(self.request.user)

        return render(request, 'client/renting_site/map.html', {'sites': sites, 'renting_session': renting_session})