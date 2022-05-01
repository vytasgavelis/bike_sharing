from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.views import View


class SiteDemoViewFail(View):
    def post(self, *args, **kwargs) -> HttpResponse:
        return HttpResponseServerError('server error')
