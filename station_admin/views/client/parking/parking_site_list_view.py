from django.http import HttpResponse
from django.shortcuts import render
from station_admin.models import Site
from station_admin.models.parking_session import ParkingSession
from django.views import View
from station_admin.repository.parking_session_repository import ParkingSessionRepository
from station_admin.repository import site_repository

class ParkingSiteListView(View):
    def get(self, request) -> HttpResponse:
        sites = site_repository.find_with_parking_configured()
        if request.user.is_authenticated:
            active_sessions = ParkingSessionRepository.find_active_sessions(request.user)
        else:
            active_sessions = None

        return render(request, 'client/parking_site/list.html', {'sites': sites, 'active_sessions': active_sessions})
