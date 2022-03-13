from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class UserCreditsView(View):
    def get(self, request) -> HttpResponse:
        return render(request, 'client/user/credits/index.html')