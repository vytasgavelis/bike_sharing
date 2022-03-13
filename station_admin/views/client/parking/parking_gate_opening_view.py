from django.http import HttpResponse
from django.views import View
from station_admin.handler import parking_handler
from station_admin.models.site import Site
from station_admin.exception.not_enough_credits_exception import NotEnoughCreditsException

class ParkingGateOpeningView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        site_id = kwargs['id']

        try:
            parking_handler.start_parking_session(
                self.request.user, Site.objects.get(pk=site_id)
            )
        except NotEnoughCreditsException:
            #TODO: redirect to credits adding page
            return HttpResponse('user does not have enough credits')

        return HttpResponse(f"opening parking gate for site: {1}!")