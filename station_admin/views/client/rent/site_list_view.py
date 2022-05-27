from django.http import JsonResponse
from django.views import View
import json

from station_admin.models import Site
from station_admin.repository import site_repository


class SiteListView(View):
    def get(self, request) -> JsonResponse:
        sites: list[Site] = site_repository.find_with_rent_configured()
        site_data = []
        for site in sites:
            site_data.append(
                {
                    'id': site.id,
                    'name': site.name,
                    'latitude': site.latitude,
                    'longitude': site.longitude,
                    'hasOpenSpots': len(site.get_bike_rent_spots()) + len(site.get_scooter_rent_spots()) > 0,
                    'rentSite': True
                 })

        return JsonResponse(site_data, safe=False)

