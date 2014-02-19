import json
from django import forms
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib import messages
from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from .models import RSVP
from .email import notify_all_staff_of_rsvp

class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ['is_attending', 'number_of_guests', 'song']
        labels = {
            'is_attending': 'Are you attending the wedding?',
            'number_of_guests': 'Number of guests (including yourself)',
            'song': 'What is a song you would like to dance to?'
        }

def home(request, show_rsvp_form=False, rsvp_result=None):
    context = {
        'title': settings.ALLOWED_HOSTS[0],
        'show_rsvp_form': show_rsvp_form,
        'rsvp_result': rsvp_result
    }
    if request.user.is_authenticated():
        rsvp = request.user.rsvp
        if request.method == 'POST':
            rsvp_form = RSVPForm(request.POST, instance=rsvp)
            if rsvp_form.is_valid():
                rsvp_form.save()
                notify_all_staff_of_rsvp(rsvp)
                if rsvp.is_attending:
                    return redirect('rsvp_yay')
                else:
                    return redirect('rsvp_boo')
            messages.error(request, 'Your RSVP has some problems.')
        else:
            rsvp_form = RSVPForm(instance=rsvp)
        context['rsvp_form'] = rsvp_form
    if request.META.get('HTTP_ACCEPT') == 'application/json':
        return HttpResponse(json.dumps({
            'path': request.path,
            'rsvp_form': render_to_string('jess/rsvp_form.html', context,
                                          RequestContext(request))
        }), content_type='application/json')
    return render(request, 'jess/home.html', context)

def routes(request):
    routes = {'backbone': {}, 'form': {}}
    for route in ['home', 'rsvp', 'rsvp_yay', 'rsvp_boo']:
        routes['backbone'][reverse(route)[1:]] = route
    for route in ['rsvp', 'login', 'logout']:
        routes['form'][reverse(route)[1:]] = route
    return HttpResponse('var ROUTES = %s;' % json.dumps(routes),
                        content_type='application/javascript')

def login(request):
    if request.method == 'POST':
        passphrase = request.POST.get('passphrase')
        if not passphrase:
            messages.error(request, 'Passphrase required.')
            return redirect('rsvp')
        try:
            rsvp = RSVP.objects.get(passphrase=passphrase,
                                    user__is_active=True,
                                    user__is_staff=False,
                                    user__is_superuser=False)

            # http://stackoverflow.com/a/2787747
            rsvp.user.backend = 'django.contrib.auth.backends.ModelBackend'

            auth.login(request, rsvp.user)
        except ObjectDoesNotExist, e:
            messages.error(request, 'Unknown passphrase.')
    return redirect('rsvp')

def logout(request):
    if request.method == 'POST': auth.logout(request)
    return redirect('home')
