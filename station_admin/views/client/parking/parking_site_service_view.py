from django.http import HttpResponse
from django.shortcuts import render
from station_admin.models import Site
from django.views import View

class ParkingSiteServiceView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        site_id = kwargs['id']
        site = Site.objects.get(pk=site_id)

        return render(self.request, 'client/parking_site/service_list.html', {'site': site})
