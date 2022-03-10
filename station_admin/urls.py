from django.urls import path

# from . import views
from .views import RegistrationView
#from views.station_admin import IndexView # sitaip nepavyksta
from .views import IndexView
#from .views.client import ParkingSiteListView
from .views.client.parking import ParkingSiteListView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register', RegistrationView.as_view(), name='register'),
    path('parking-site', ParkingSiteListView.as_view(), name='parking_site_list')
]