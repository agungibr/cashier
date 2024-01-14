from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout


from .models import Gun

def main(request):
     return render(request, 'main.html')

def login(request):
    page = 'login'

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user) 
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    else:
        form = AuthenticationForm()

    context = {'page': page, 'form': form}
    return render(request, 'auth/login.html', context)


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request) 
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'auth/register.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect(reverse('main'))

def home(request):
    return render(request, 'home.html')

def list(request):
    guns = Gun.objects.all()
    context = {'guns': guns}

    return render(request, 'list.html', context)