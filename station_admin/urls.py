from django.urls import path

# from . import views
from .views import RegistrationView
#from views.station_admin import IndexView # sitaip nepavyksta
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register', RegistrationView.as_view(), name='register'),
]