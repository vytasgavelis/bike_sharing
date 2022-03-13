from django.http import HttpResponse
from django.views import View


class ParkingGateOpeningView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        site_id = kwargs['id']

        return HttpResponse(f"opening parking gate for site: {site_id}!")