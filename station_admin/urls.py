from django.contrib.auth.decorators import login_required
from django.urls import path

from .helper.response_helper import ResponseHelper
from .views import RegistrationView
from .views import IndexView
from .views.client.parking import ParkingSiteListView
from .views.admin.qr_code_download_view import QrCodeDownloadView
from .views.admin.rent_spot_qr_code_download_view import RentSpotQrCodeDownloadView
from django.contrib.admin.views.decorators import staff_member_required

from .views.client.parking.current_session_view import CurrentSessionView
from .views.client.parking.parking_session_start_view import ParkingSessionStartView
from .views.client.parking.parking_map_view import ParkingMapView
from .views.client.parking.parking_site_open_gate_view import ParkingSiteOpenGateView
from .views.client.rent.end_rent_session_view import EndRentSessionView
from .views.client.rent.start_reservation_view import StartReservationView
from .views.client.rent.end_reservation_view import EndReservationView
from .views.client.rent.rent_map_view import RentMapView
from .views.client.rent.site_list_view import SiteListView
from .views.client.user.user_profile_view import UserProfileView
from .views.demo.site_demo_view_success import SiteDemoViewSuccess
from .views.demo.site_demo_view_fail import SiteDemoViewFail
from .views.client.parking.parking_site_service_view import ParkingSiteServiceView
from .views.client.parking.parking_session_end_view import ParkingSessionEndView
from django.views.decorators.csrf import csrf_exempt
from .views.client.rent.start_rent_session_view import StartRentSessionView
from .views.client.rent.renting_site_list_view import RentingSiteListView
from .views.client.rent.vehicle_view import VehicleView
from .views.client.user.add_credits_view import AddCreditsView
from .views.client.parking.site_list_view import SiteListView as ParkingSiteListView

def login_required_json(function):
    def wrapper(request, *args, **kw):
        user = request.user
        if not user.id:
            return ResponseHelper.get_failed_response('You must be logged in')
        else:
            return function(request, *args, **kw)
    return wrapper

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register', RegistrationView.as_view(), name='register'),
    path('parking-site', ParkingSiteListView.as_view(), name='parking_site_list'),
    path('renting', RentingSiteListView.as_view(), name='renting_site_list'),
    path('rent-map', RentMapView.as_view(), name='renting_map'),
    path('parking-map', ParkingMapView.as_view(), name='parking_map'),
    path('parking-site/<int:id>/services', ParkingSiteServiceView.as_view(),
         name='parking_site_service_list'),
    # todo: add following to admin urls.
    path('site/<int:id>/qr-code', staff_member_required(QrCodeDownloadView.as_view()), name='qr_code_download'),
    path('rent-spot/<int:id>/qr-code', staff_member_required(RentSpotQrCodeDownloadView.as_view()),
         name='rent_spot_qr_code_download'),
    path('api/site/<int:id>/session/start/<str:parking_spot_type>', login_required_json(ParkingSessionStartView.as_view()),
         name='parking_gate_open'),
    path('api/site/<int:id>/gate/open', login_required_json(ParkingSiteOpenGateView.as_view()),
         name='parking_site_gate_open'),
    path('api/site/<int:site_id>/session/end', login_required_json(ParkingSessionEndView.as_view()),
         name='end_parking_session'),
    path('api/spot/<int:id>/reservation/start', login_required_json(StartReservationView.as_view()),
         name='start_reservation'),
    path('api/reservation/end', login_required_json(EndReservationView.as_view()),
         name='end_reservation'),
    path('user/profile', login_required(UserProfileView.as_view()), name='user_profile'),
    path('user/credits', login_required(AddCreditsView.as_view()), name='add_credits'),
    path('demo/success', csrf_exempt(SiteDemoViewSuccess.as_view()), name='demo_open_gate_success'),
    path('demo/fail', csrf_exempt(SiteDemoViewFail.as_view()), name='demo_open_gate_fail'),
    path('rent-spot/<int:id>/session/start', login_required(StartRentSessionView.as_view()), name='start_rent_session'),
    path('rent-spot/<int:id>/session/end', login_required(EndRentSessionView.as_view()), name='end_rent_session'),
    path('rent-spot/<int:id>/vehicle', VehicleView.as_view(), name='rent_spot_vehicle'),

    path('api/rent-sites', csrf_exempt(SiteListView.as_view()), name='get_rent_sites'),
    path('api/parking-sites', csrf_exempt(ParkingSiteListView.as_view()), name='get_parking_sites'),
    path('api/current-parking-session', login_required_json(CurrentSessionView.as_view()), name='get_current_parking_session'),
]
