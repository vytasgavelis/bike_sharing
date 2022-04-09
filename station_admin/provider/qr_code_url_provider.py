from django.urls import path, reverse


class QrCodeUrlProvider:
    def get_site_qrcode_url(self, site_id: int) -> str:
        return reverse('qr_code_download', args=[site_id])

    def get_rent_spot_qrcode_url(self, rent_spot_id: int) -> str:
        return reverse('rent_spot_qr_code_download', args=[rent_spot_id])