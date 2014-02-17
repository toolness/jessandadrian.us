import json
from django import forms
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
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

def render_home(request, show_rsvp_form):
    context = {
        'title': settings.ALLOWED_HOSTS[0],
        'show_rsvp_form': show_rsvp_form
    }
    if request.user.is_authenticated():
        rsvp = request.user.rsvp
        if request.method == 'POST':
            rsvp_form = RSVPForm(request.POST, instance=rsvp)
            if rsvp_form.is_valid():
                rsvp_form.save()
                notify_all_staff_of_rsvp(rsvp)
                if rsvp.is_attending:
                    msg = 'Awesome! The wedding staff has been notified ' \
                          'and eagerly awaits your arrival.'
                else:
                    msg = 'Bummer! The wedding staff has been notified ' \
                          'of your inability to attend.'
                messages.success(request, msg)
                return redirect('rsvp')
            messages.error(request, 'Your RSVP has some problems.')
        else:
            rsvp_form = RSVPForm(instance=rsvp)
        context['rsvp_form'] = rsvp_form
    return render(request, 'jess/home.html', context)

def routes(request):
    routes = {}
    for route in ['home', 'rsvp', 'login', 'logout']:
        routes[reverse(route)[1:]] = route
    return HttpResponse('var ROUTES = %s;' % json.dumps(routes),
                        content_type='application/javascript')

def rsvp(request):
    return render_home(request, show_rsvp_form=True)

def home(request):
    return render_home(request, show_rsvp_form=False)

def login(request):
    if request.method == 'POST':
        passphrase = request.POST.get('passphrase')
        if not passphrase:
            messages.error(request, 'Passphrase required.')
            return redirect('rsvp')
        try:
            rsvp = RSVP.objects.get(passphrase=passphrase)

            if not rsvp.user.is_active:
                raise ObjectDoesNotExist()

            if rsvp.user.is_staff or rsvp.user.is_superuser:
                return redirect('/admin/')

            # http://stackoverflow.com/a/2787747
            rsvp.user.backend = 'django.contrib.auth.backends.ModelBackend'

            auth.login(request, rsvp.user)
        except ObjectDoesNotExist, e:
            messages.error(request, 'Unknown passphrase.')
    return redirect('rsvp')

def logout(request):
    if request.method == 'POST': auth.logout(request)
    return redirect('home')
