from django.http import HttpResponse
from django.views import View
from station_admin.handler.rent import rent_handler
from django.contrib import messages
from station_admin.exception.not_enough_credits_exception import NotEnoughCreditsException
from django.shortcuts import redirect, render

class StartRentSessionView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        rent_spot_id = kwargs['id']

        try:
            rent_handler.open_rent_spot_lock(rent_spot_id, self.request.user)
        except NotEnoughCreditsException as e:
            raise e
            messages.error(self.request, 'You don\'t have enough credits to use parking.')
            return redirect('user_credits')
        except Exception as e:
            raise e
            messages.error(self.request, str(e))
            return redirect('renting_site_list')

        return HttpResponse('all ok :)')
