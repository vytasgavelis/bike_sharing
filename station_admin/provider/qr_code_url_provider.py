from django.urls import path, reverse


class QrCodeUrlProvider:
    def get_url(self, qr_code_id: int) -> str:
        return reverse('qr_code_download', args=[qr_code_id])