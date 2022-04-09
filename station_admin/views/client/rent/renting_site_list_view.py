from django.http import HttpResponse
from django.views import View
from station_admin.models import Site
from django.shortcuts import render
from station_admin.repository import site_repository


class RentingSiteListView(View):
    def get(self, request) -> HttpResponse:
        sites = site_repository.find_with_rent_configured()

        return render(request, 'client/renting_site/list.html', {'sites': sites})
