from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View

from station_admin.helper import user_helper
from station_admin.repository import site_repository
from station_admin.repository.parking_session_repository import ParkingSessionRepository


class ParkingMapView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        sites = site_repository.find_with_parking_configured()
        sites_with_sessions = []
        if request.user.is_authenticated:
            active_sessions = ParkingSessionRepository.find_active_sessions(request.user)
            for site in sites:
                if user_helper.has_parking_session_in_site(site, request.user):
                    sites_with_sessions.append((site, True))
                else:
                    sites_with_sessions.append((site, False))
        else:
            active_sessions = None
            for site in sites:
                sites_with_sessions.append((site, False))



        return render(
            request,
            'client/parking_site/map.html',
            {'sites': sites, 'active_sessions': active_sessions, 'sites_with_sessions': sites_with_sessions}
        )
