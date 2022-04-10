from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import RegistrationView
from .views import IndexView
from .views.client.parking import ParkingSiteListView
from .views.admin.qr_code_download_view import QrCodeDownloadView
from .views.admin.rent_spot_qr_code_download_view import RentSpotQrCodeDownloadView
from django.contrib.admin.views.decorators import staff_member_required
from .views.client.parking.parking_gate_opening_view import ParkingGateOpeningView
from .views.client.user.user_credits_view import UserCreditsView
from .views.demo.site_demo_view import SiteDemoView
from .views.client.parking.parking_site_service_view import ParkingSiteServiceView
from .views.client.parking.parking_session_end_view import ParkingSessionEndView
from django.views.decorators.csrf import csrf_exempt
from .views.client.rent.rent_session_view import RentSessionView
from .views.client.rent.renting_site_list_view import RentingSiteListView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register', RegistrationView.as_view(), name='register'),
    path('parking-site', ParkingSiteListView.as_view(), name='parking_site_list'),
    path('renting', RentingSiteListView.as_view(), name='renting_site_list'),
    path('parking-site/<int:id>/services', login_required(ParkingSiteServiceView.as_view()),
         name='parking_site_service_list'),
    # todo: add following to admin urls.
    path('site/<int:id>/qr-code', staff_member_required(QrCodeDownloadView.as_view()), name='qr_code_download'),
    path('rent-spot/<int:id>/qr-code', staff_member_required(RentSpotQrCodeDownloadView.as_view()),
         name='rent_spot_qr_code_download'),
    path('site/<int:id>/gate/open/<str:parking_spot_type>', login_required(ParkingGateOpeningView.as_view()),
         name='parking_gate_open'),
    path('site/<int:site_id>/parking_sessions/users/<int:user_id>/end', login_required(ParkingSessionEndView.as_view()),
         name='end_parking_session'),
    path('user/credits', login_required(UserCreditsView.as_view()), name='user_credits'),
    path('demo/open-gate', csrf_exempt(SiteDemoView.as_view()), name='demo_open_gate'),
    path('rent-spot/<int:id>/session', login_required(RentSessionView.as_view()), name='rent_session'),
]
