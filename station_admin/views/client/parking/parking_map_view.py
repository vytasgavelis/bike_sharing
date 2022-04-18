from station_admin.models.site import Site
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from station_admin.helper import user_helper
from station_admin.repository import site_repository
from station_admin.repository.parking_session_repository import ParkingSessionRepository


class ParkingMapView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        site_id = request.GET.get('site_id')
        preselected_site = None

        if site_id:
            try:
                preselected_site = Site.objects.get(pk=site_id)
            except ObjectDoesNotExist:
                pass

        sites = site_repository.find_with_parking_configured()
        sites_with_sessions = []
        parking_session = None
        if request.user.is_authenticated:
            active_sessions = ParkingSessionRepository.find_active_sessions(request.user)
            parking_session = active_sessions[0] if len(active_sessions) > 0 else None
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
            {
                'sites': sites,
                'active_sessions': active_sessions,
                'sites_with_sessions': sites_with_sessions,
                'parking_session': parking_session,
                'preselected_site': preselected_site
            }
        )
