from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from station_admin.repository import parking_session_repository, renting_session_repository
from station_admin.repository.parking_session_repository import ParkingSessionRepository


class UserProfileView(View):
    def get(self, request) -> HttpResponse:
        parking_sessions = ParkingSessionRepository.find_sessions(request.user)
        renting_sessions = renting_session_repository.find_sessions(request.user)

        return render(
            request,
            'client/user/profile/index.html',
            {'parking_sessions': parking_sessions, 'renting_sessions': renting_sessions})