from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class RentMapView(View):
    def get(self, request) -> HttpResponse:
        return render(request, 'client/renting_site/map.html')