from django.http import HttpResponse
from django.views import View
from station_admin.models import Site
from django.shortcuts import render
from station_admin.repository import site_repository
from station_admin.repository import renting_session_repository

class RentingSiteListView(View):
    def get(self, request) -> HttpResponse:
        sites = site_repository.find_with_rent_configured()
        if request.user.is_authenticated:
            active_sessions = renting_session_repository.find_active_sessions(self.request.user)
        else:
            active_sessions = None

        return render(request, 'client/renting_site/list.html', {'sites': sites, 'active_sessions': active_sessions})
