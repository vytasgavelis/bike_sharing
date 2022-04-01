from django.http import HttpResponse
from django.shortcuts import render
from station_admin.models import Site
from station_admin.models.parking_session import ParkingSession
from django.views import View

class ParkingSiteListView(View):
    def get(self, request) -> HttpResponse:
        sites = Site.objects.all()
        active_sessions = ParkingSession.objects.filter(user=request.user)

        return render(request, 'client/parking_site/list.html', {'sites': sites, 'active_sessions': active_sessions})
