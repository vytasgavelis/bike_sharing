from django.contrib.auth.models import User

from station_admin.exception.not_enough_credits_exception import NotEnoughCreditsException
from station_admin.exception.site_not_configured_correctly_exception import SiteNotConfiguredCorrectlyException
from station_admin.models.rent_spot import RentSpot
import requests

class RentHandler:
    def open_rent_spot_lock(self, spot_id: int, user: User) -> None:
        spot = RentSpot.objects.get(pk=spot_id)

        if not spot:
            raise Exception('Rent spot was not found.')

        site = spot.site

        if not site.enough_credits_for_renting(user):
            raise NotEnoughCreditsException('User does not have enough credits.')

        if not site.lock_open_url or not site.lock_close_url:
            raise SiteNotConfiguredCorrectlyException('Site and spot must be configured for renting.')

        response = requests.post(f"{site.lock_open_url}", json={'id': spot.external_id})

        if response.status_code != 200:
            raise Exception('Could not open vehicle lock.')