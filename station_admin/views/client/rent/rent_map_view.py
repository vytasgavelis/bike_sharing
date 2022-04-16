from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from station_admin.models import Site
from station_admin.repository import site_repository


class RentMapView(View):
    def get(self, request) -> HttpResponse:
        sites: list[Site] = site_repository.find_with_rent_configured()
        return render(request, 'client/renting_site/map.html', {'sites': sites})