from django.http import HttpResponse, JsonResponse
from django.views import View

from station_admin.helper.response_helper import ResponseHelper
from station_admin.models import RentSession
from station_admin.repository import renting_session_repository


class ActiveReservationView(View):
    def get(self, request) -> HttpResponse:
        reservations: list[RentSession] = renting_session_repository.find_active_reservations_by_user(request.user)

        if len(reservations) == 0:
            return ResponseHelper.get_failed_response('You do not have a reservation')
        print(reservations)
        reservation = reservations[0]
        site = reservation.vehicle.current_spot.site

        return JsonResponse(
            {
                'success': True,
                'message': 'Success',
                'siteId': site.id,
                'latitude': site.latitude,
                'longitude': site.longitude,
            },
            safe=False
        )