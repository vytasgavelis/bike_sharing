from django.http import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from station_admin.forms import SignupForm
from station_admin.models import UserProfile


class RegistrationView(View):

    def get(self, request) -> HttpResponse:
        form = SignupForm()

        context = {'form': form}

        return render(request, 'registration/register.html', context)

    def post(self, request) -> HttpResponse:
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            profile = UserProfile()
            profile.credits = 0
            profile.user = user
            profile.phone_number = form.cleaned_data['phone_number']
            profile.save()
            login(request, user)

            return redirect('index')

        context = {'form': form}

        return render(request, 'registration/register.html', context)
