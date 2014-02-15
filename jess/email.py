from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string

def generate_rsvp_notification(rsvp):
    subject, body = render_to_string('jess/rsvp_notification_email.txt', {
        'rsvp': rsvp
    }).split('\n\n', 1)
    subject = subject.split(':', 1)[1]
    return subject.strip(), body.strip()

def notify_user_of_rsvp(user, rsvp):
    subject, body = generate_rsvp_notification(rsvp)
    user.email_user(subject, body, settings.DEFAULT_FROM_EMAIL)

def get_all_staff_with_email():
    staff = User.objects.filter(is_active=True, is_staff=True)
    return staff.exclude(email=u'')

def notify_all_staff_of_rsvp(rsvp):
    for user in get_all_staff_with_email():
        notify_user_of_rsvp(user, rsvp)
