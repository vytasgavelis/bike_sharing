from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.views import View


class SiteDemoView(View):
    return_failed = False

    def post(self, *args, **kwargs) -> HttpResponse:
        if self.return_failed:
            return HttpResponseServerError('server error')

        return HttpResponse('ok')
