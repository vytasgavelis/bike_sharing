from django.views import View
from django.http import HttpResponse
from station_admin.provider import qr_code_provider
import mimetypes


class RentSpotQrCodeDownloadView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        rent_spot_id = kwargs['id']
        filepath = qr_code_provider.get_rent_session_start_png(rent_spot_id)

        path = open(filepath, 'rb')

        mime_type, _ = mimetypes.guess_type(filepath)
        response = HttpResponse(path, content_type=mime_type)

        response['Content-Disposition'] = "attachment; filename=rent_spot_qr_code.png"

        return response
