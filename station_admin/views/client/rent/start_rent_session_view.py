from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views import View
from station_admin.handler.rent import rent_handler
from django.contrib import messages
from station_admin.exception.not_enough_credits_exception import NotEnoughCreditsException
from django.shortcuts import redirect, render, get_object_or_404

from station_admin.models import RentSpot


class StartRentSessionView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        rent_spot_id = kwargs['id']

        rent_spot = get_object_or_404(RentSpot, pk=rent_spot_id)

        # if user_helper.has_active_rent_session
        try:
            rent_handler.open_rent_spot_lock(rent_spot, self.request.user)
            rent_handler.start_session(rent_spot, self.request.user)
        except NotEnoughCreditsException:
            messages.error(self.request, 'You don\'t have enough credits to use parking.')
            return redirect('user_credits')
        except Exception as e:
            messages.error(self.request, str(e))
            return redirect('renting_site_list')

        messages.success(self.request, 'Rent session has been started!')
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
            rent_handler.open_rent_spot_lock(rent_spot, self.request.user)
            rent_handler.start_session(rent_spot, self.request.user)
        except NotEnoughCreditsException:
            return JsonResponse({'success': False, 'message': 'You don\'t have enough credits to use parking.'}, safe=False)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)},safe=False)

        return JsonResponse({'success': True}, safe=False)

        #return JsonResponse({'success': False, 'message': 'Could not start session'}, safe=False)