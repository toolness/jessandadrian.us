from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from .models import RSVP

# Create your views here.

class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ['is_attending', 'number_of_guests']
        labels = {
            'is_attending': 'Are you attending the wedding?',
            'number_of_guests': 'Number of guests (including yourself)'
        }

def home(request):
    context = {}
    if request.user.is_authenticated():
        rsvp = request.user.rsvp
        if request.method == 'POST':
            rsvp_form = RSVPForm(request.POST, instance=rsvp)
            if rsvp_form.is_valid():
                messages.success(request, 'RSVP updated! Thanks, buddy.')
                rsvp_form.save()
                return redirect('home')
            messages.error(request, 'Your RSVP has some problems.')
        else:
            rsvp_form = RSVPForm(instance=rsvp)
        context['rsvp_form'] = rsvp_form
    return render(request, 'jess/home.html', context)

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
