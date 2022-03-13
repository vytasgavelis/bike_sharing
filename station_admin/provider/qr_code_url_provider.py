from django.urls import path, reverse


class QrCodeUrlProvider:
    def get_url(self, site_id: int) -> str:
        return reverse('qr_code_download', args=[site_id])