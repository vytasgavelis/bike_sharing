import qrcode
from django.urls import reverse
from bike_sharing.settings import BASE_URL
import uuid

class QrCodeProvider:
    def get_gate_open_png(self, site_id: int) -> str:
        return self._create_png(BASE_URL + reverse('parking_site_service_list', args=[site_id]))

    def get_rent_session_start_png(self, rent_spot_id: int) -> str:
        return self._create_png(BASE_URL + reverse('rent_spot_vehicle', args=[rent_spot_id]))

    def _create_png(self, content: str) -> str:
        img = qrcode.make(content)

        file_name = str(uuid.uuid4()) + ".png"
        file_path = f"station_admin/media/img/{file_name}"

        img.save(file_path)

        return file_path
