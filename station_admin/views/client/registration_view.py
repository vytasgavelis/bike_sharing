from django.http import HttpResponse
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


class RegistrationView(View):

    def get(self, request) -> HttpResponse:
        form = UserCreationForm()

        context = {'form': form}

        return render(request, 'registration/register.html', context)

    def post(self, request) -> HttpResponse:
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('index')

        context = {'form': form}

        return render(request, 'registration/register.html', context)
