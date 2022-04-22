from django.http import HttpResponse, JsonResponse
from django.views import View

from station_admin.helper.response_helper import ResponseHelper


class StartReservationView(View):
    def post(self, *args, **kwargs) -> HttpResponse:
        return ResponseHelper.get_failed_response('Could not start reservation')
        # return ResponseHelper.get_sucess_response()
