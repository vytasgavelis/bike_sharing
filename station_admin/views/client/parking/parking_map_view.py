from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from station_admin.repository import site_repository
from station_admin.repository.parking_session_repository import ParkingSessionRepository


class ParkingMapView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        sites = site_repository.find_with_parking_configured()
        if request.user.is_authenticated:
            active_sessions = ParkingSessionRepository.find_active_sessions(request.user)
        else:
            active_sessions = None

        return render(request, 'client/parking_site/map.html', {'sites': sites, 'active_sessions': active_sessions})
