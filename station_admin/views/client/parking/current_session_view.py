from django.http import HttpResponse, JsonResponse
from django.views import View

from station_admin.helper.response_helper import ResponseHelper
from station_admin.repository.parking_session_repository import ParkingSessionRepository


class CurrentSessionView(View):
    def get(self, request) -> HttpResponse:
        sessions = ParkingSessionRepository.find_active_sessions(self.request.user)
        if len(sessions) == 0:
            return ResponseHelper.get_failed_response("You don't have active parking session")

        site = sessions[0].parking_spot.site
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

