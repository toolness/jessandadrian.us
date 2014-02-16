from django import forms
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from .models import RSVP
from .email import notify_all_staff_of_rsvp

# Create your views here.

class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ['is_attending', 'number_of_guests', 'song']
        labels = {
            'is_attending': 'Are you attending the wedding?',
            'number_of_guests': 'Number of guests (including yourself)',
            'song': 'What is a song you would like to dance to?'
        }

def home(request):
    context = {'title': settings.ALLOWED_HOSTS[0]}
    if request.user.is_authenticated():
        rsvp = request.user.rsvp
        if request.method == 'POST':
            rsvp_form = RSVPForm(request.POST, instance=rsvp)
            if rsvp_form.is_valid():
                messages.success(request, 'RSVP updated! Thanks, buddy.')
                rsvp_form.save()
                notify_all_staff_of_rsvp(rsvp)
                return redirect('home')
            messages.error(request, 'Your RSVP has some problems.')
        else:
            rsvp_form = RSVPForm(instance=rsvp)
        context['rsvp_form'] = rsvp_form
    return render(request, 'jess/home.html', context)

def login(request):
    if request.method == 'POST':
        passphrase = request.POST.get('passphrase')
        if not passphrase:
            messages.error(request, 'Passphrase required.')
            return redirect('home')
        try:
            rsvp = RSVP.objects.get(passphrase=passphrase)

            # http://stackoverflow.com/a/2787747
            rsvp.user.backend = 'django.contrib.auth.backends.ModelBackend'

            auth.login(request, rsvp.user)
        except ObjectDoesNotExist, e:
            messages.error(request, 'Unknown passphrase.')
    return redirect('home')

def logout(request):
    if request.method == 'POST': auth.logout(request)
    return redirect('home')
