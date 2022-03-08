from django.urls import path

# from . import views
from .views import RegistrationView
#from views.client import IndexView # sitaip nepavyksta
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('register', RegistrationView.as_view(), name='register'),
]