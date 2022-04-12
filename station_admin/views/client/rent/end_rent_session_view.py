from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from station_admin.handler.rent import rent_handler
from station_admin.models import RentSpot


class EndRentSessionView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        rent_spot = get_object_or_404(RentSpot, pk=kwargs['id'])

        rent_handler.end_session(rent_spot, self.request.user)

        return redirect('renting_site_list')
