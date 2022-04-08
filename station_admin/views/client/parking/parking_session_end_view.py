from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from station_admin.models.site import Site
from station_admin.helper import user_helper
from django.contrib import messages
from station_admin.handler import parking_handler
from station_admin.repository.parking_session_repository import ParkingSessionRepository

class ParkingSessionEndView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        site_id = kwargs['site_id']

        user = User.objects.get(pk=self.request.user.id)
        site = Site.objects.get(pk=site_id)

        sessions = ParkingSessionRepository.find_active_sessions(user, site)

        if len(sessions) > 0:
            try:
                parking_handler.end_session(sessions[0], site, user)
            except Exception as e:
                raise e
                messages.error(self.request, str(e))
                return redirect('parking_site_service_list', id=site_id)
        else:
            messages.error(self.request, 'You do not have parking session in this site.')
            return redirect('parking_site_service_list', id=site_id)

        return redirect('parking_site_list')

