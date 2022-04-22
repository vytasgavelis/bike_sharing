from django.http import HttpResponse
from django.views import View

from station_admin.helper.response_helper import ResponseHelper


class EndReservationView(View):
    def post(self, request) -> HttpResponse:
        return ResponseHelper.get_sucess_response()
