from django.http import HttpResponse
from django.shortcuts import render, redirect
from station_admin.models import Site
from django.views import View
from django.contrib.auth.models import User
from station_admin.helper import user_helper
from urllib.parse import urlencode

class ParkingSiteServiceView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        response = redirect('parking_map')

        query_string = urlencode({'site_id': kwargs['id']})
        response['Location'] += '?' + query_string

        return response

        # site_id = kwargs['id']
        # site = Site.objects.get(pk=site_id)
        # user = User.objects.get(pk=self.request.user.id)
        #
        # return render(
        #     self.request,
        #     'client/parking_site/service_list.html',
        #     {
        #         'site': site,
        #         'user_has_parking_session_in_site': user_helper.has_parking_session_in_site(site, user),
        #         'user': self.request.user,
        #     }
        # )
