from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import RegistrationView
from .views import IndexView
from .views.client.parking import ParkingSiteListView
from .views.admin.qr_code_download_view import QrCodeDownloadView
from .views.admin.rent_spot_qr_code_download_view import RentSpotQrCodeDownloadView
from django.contrib.admin.views.decorators import staff_member_required
from .views.client.parking.parking_gate_opening_view import ParkingGateOpeningView
from .views.client.parking.parking_map_view import ParkingMapView
from .views.client.rent.end_rent_session_view import EndRentSessionView
from .views.client.rent.rent_map_view import RentMapView
from .views.client.rent.site_list_view import SiteListView
from .views.client.user.user_profile_view import UserProfileView
from .views.demo.site_demo_view import SiteDemoView
from .views.client.parking.parking_site_service_view import ParkingSiteServiceView
from .views.client.parking.parking_session_end_view import ParkingSessionEndView
from django.views.decorators.csrf import csrf_exempt
from .views.client.rent.start_rent_session_view import StartRentSessionView
from .views.client.rent.renting_site_list_view import RentingSiteListView
from .views.client.rent.vehicle_view import VehicleView
from .views.client.user.add_credits_view import AddCreditsView
from .views.client.parking.site_list_view import SiteListView as ParkingSiteListView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register', RegistrationView.as_view(), name='register'),
    path('parking-site', ParkingSiteListView.as_view(), name='parking_site_list'),
    path('renting', RentingSiteListView.as_view(), name='renting_site_list'),
    path('rent-map', RentMapView.as_view(), name='renting_map'),
    path('parking-map', ParkingMapView.as_view(), name='parking_map'),
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
    path('user/profile', login_required(UserProfileView.as_view()), name='user_profile'),
    path('user/credits', login_required(AddCreditsView.as_view()), name='add_credits'),
    path('demo/open-gate', csrf_exempt(SiteDemoView.as_view()), name='demo_open_gate'),
    path('rent-spot/<int:id>/session/start', login_required(StartRentSessionView.as_view()), name='start_rent_session'),
    path('rent-spot/<int:id>/session/end', login_required(EndRentSessionView.as_view()), name='end_rent_session'),
    path('rent-spot/<int:id>/vehicle', VehicleView.as_view(), name='rent_spot_vehicle'),

    path('api/rent-sites', csrf_exempt(SiteListView.as_view()), name='get_rent_sites'),
    path('api/parking-sites', csrf_exempt(ParkingSiteListView.as_view()), name='get_parking_sites'),
]
