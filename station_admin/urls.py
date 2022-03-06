from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('client', views.client_index, name='client_index'),
    path('register', views.register, name='register'),
]