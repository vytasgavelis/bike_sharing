import math

from django.http import HttpResponse, JsonResponse
from django.views import View
from station_admin.models.site import Site

from station_admin.handler import parking_handler


class ParkingSiteOpenGateView(View):
    def post(self, *args, **kwargs) -> HttpResponse:
        site_id = kwargs['id']

        site = Site.objects.get(pk=site_id)

        try:
            parking_handler.open_site_door_for_renting(self.request.user, site)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, safe=False)

        return JsonResponse({'success': True}, safe=False)