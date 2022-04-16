from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View

from station_admin.handler.rent import rent_handler
from station_admin.models import RentSpot


class EndRentSessionView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        rent_spot = get_object_or_404(RentSpot, pk=kwargs['id'])

        rent_handler.end_session(rent_spot, self.request.user)

        return redirect('renting_site_list')

    def post(self, *args, **kwargs) -> HttpResponse:
        rent_spot_id = kwargs['id']

        rent_spot = None
        if rent_spot_id:
            try:
                rent_spot = RentSpot.objects.get(pk=rent_spot_id)
            except ObjectDoesNotExist:
                return JsonResponse({'success': False, 'message': 'Rent spot does not exist'}, safe=False)

        try:
            rent_handler.end_session(rent_spot, self.request.user)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, safe=False)

        return JsonResponse({'success': True}, safe=False)