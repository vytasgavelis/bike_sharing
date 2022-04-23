from django.http import HttpResponse
from django.views import View

from station_admin.handler.rent import rent_handler
from station_admin.helper.response_helper import ResponseHelper


class EndReservationView(View):
    def post(self, request) -> HttpResponse:
        try:
            rent_handler.end_reservation(request.user)
        except Exception as e:
            return ResponseHelper.get_failed_response(str(e))

        return ResponseHelper.get_sucess_response()
