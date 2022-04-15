from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class UserProfileView(View):
    def get(self, request) -> HttpResponse:
        return render(request, 'client/user/profile/index.html')