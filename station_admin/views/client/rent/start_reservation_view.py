from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views import View

from station_admin.handler.rent import rent_handler
from station_admin.helper.response_helper import ResponseHelper
from station_admin.models import RentSpot


class StartReservationView(View):
    def post(self, *args, **kwargs) -> HttpResponse:
        rent_spot_id = kwargs['id']
        rent_spot = None
        if rent_spot_id:
            try:
                rent_spot = RentSpot.objects.get(pk=rent_spot_id)
            except ObjectDoesNotExist:
                return ResponseHelper.get_failed_response('Rent spot does not exist')

        try:
            rent_handler.start_reservation(rent_spot, self.request.user)
        except Exception as e:
            return ResponseHelper.get_failed_response(str(e))

        return ResponseHelper.get_sucess_response('Vehicle has been reserved')
