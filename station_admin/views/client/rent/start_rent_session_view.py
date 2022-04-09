from django.http import HttpResponse
from django.views import View


class StartRentSessionView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        return HttpResponse('starting rent!')
