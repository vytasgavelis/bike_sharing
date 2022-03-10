from django.http import HttpResponse
from django.shortcuts import render
from station_admin.models import Site
from django.views import View

class ParkingSiteListView(View):
    def get(self, request) -> HttpResponse:
        sites = Site.objects.all()

        return render(request, 'client/parking_site/list.html', {'sites': sites})
