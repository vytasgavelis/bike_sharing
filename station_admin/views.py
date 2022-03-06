from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def client_index(request):
    return render(request, 'station_client/index.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = authenticate(username=form.cleaned_data['username'])
            password = authenticate(username=form.cleaned_data['password1'])

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('index')
    else:
        form = UserCreationForm()

    context = {'form': form}

    return render(request, 'registration/register.html', context)