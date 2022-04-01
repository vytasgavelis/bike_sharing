from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from station_admin.handler import parking_handler
from station_admin.models.site import Site
from station_admin.exception.not_enough_credits_exception import NotEnoughCreditsException
from django.contrib import messages


class ParkingGateOpeningView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        site_id = kwargs['id']
        parking_spot_type = kwargs['parking_spot_type']

        site = Site.objects.get(pk=site_id)

        try:
            parking_handler.open_site_door(
                self.request.user, site
            )
        except NotEnoughCreditsException:
            messages.error(self.request, 'You don\'t have enough credits to use parking.')
            return redirect('user_credits')

        parking_handler.start_session(self.request.user, site, parking_spot_type)

        return render(self.request, 'client/parking_site/parking_session_start_success.html')
