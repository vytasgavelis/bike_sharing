from django.views import View
from django.http import HttpResponse

class QrCodeDownloadView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        id = kwargs['qr_code_id']
        return HttpResponse('downloading qr code!')