from django.urls import path

# from . import views
from .views import RegistrationView
# from views.station_admin import IndexView # sitaip nepavyksta
from .views import IndexView
# from .views.client import ParkingSiteListView
from .views.client.parking import ParkingSiteListView
from .views.admin.qr_code_download_view import QrCodeDownloadView
from django.contrib.admin.views.decorators import staff_member_required
from .views.client.parking.parking_gate_opening_view import ParkingGateOpeningView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register', RegistrationView.as_view(), name='register'),
    path('parking-site', ParkingSiteListView.as_view(), name='parking_site_list'),
    # todo: add following to admin urls.
    path('site/<int:id>/qr-code', staff_member_required(QrCodeDownloadView.as_view()), name='qr_code_download'),
    path('site/<int:id>/gate/open', ParkingGateOpeningView.as_view(), name='parking_gate_open'),
]
