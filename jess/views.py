from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from .models import RSVP

# Create your views here.

def home(request):
    return render(request, 'jess/home.html')

def login(request):
    if request.method == 'POST':
        try:
            rsvp = RSVP.objects.get(passphrase=request.POST['passphrase'])

            # http://stackoverflow.com/a/2787747
            rsvp.user.backend = 'django.contrib.auth.backends.ModelBackend'

            auth.login(request, rsvp.user)
        except ObjectDoesNotExist, e:
            messages.error(request, 'Unknown passphrase.')
    return redirect('home')

def logout(request):
    if request.method == 'POST': auth.logout(request)
    return redirect('home')
