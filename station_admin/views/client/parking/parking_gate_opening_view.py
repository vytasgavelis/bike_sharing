from django.http import HttpResponse
from django.shortcuts import redirect
from django.views import View
from station_admin.handler import parking_handler
from station_admin.models.site import Site
from station_admin.exception.not_enough_credits_exception import NotEnoughCreditsException
from django.contrib import messages


class ParkingGateOpeningView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        site_id = kwargs['id']

        try:
            parking_handler.open_site_door(
                self.request.user, Site.objects.get(pk=site_id)
            )
        except NotEnoughCreditsException:
            messages.error(self.request, 'You don\'t have enough credits to use parking.')
            return redirect('user_credits')

        return HttpResponse(f"opening parking gate for site: {1}!")
