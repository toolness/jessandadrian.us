from django.test import TestCase
from django.test.client import Client
from django.core import mail
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import RSVP
from . import email

def create_user_with_rsvp(**kwargs):
    user = User()
    rsvp = RSVP()
    for key in kwargs:
        if hasattr(user, key):
            setattr(user, key, kwargs[key])
        else:
            setattr(rsvp, key, kwargs[key])
    user.save()
    rsvp.user = user
    rsvp.save()
    return user

class ViewTests(TestCase):
    def test_views_return_OK(self):
        for path in ['/', '/rsvp', '/rsvp/yay', '/rsvp/boo', '/routes.js']:
            c = Client()
            response = c.get(path)
            if response.status_code != 200:
                raise Exception('GET %s returned %d' % (
                    path,
                    response.status_code)
                )

    def test_login_does_not_accept_empty_passphrases(self):
        c = Client()
        response = c.post('/login', {'passphrase': ''}, follow=True)
        self.assertRegexpMatches(response.content, 'Passphrase required')

    def test_login_rejects_incorrect_passphrases(self):
        c = Client()
        response = c.post('/login', {'passphrase': 'lol'}, follow=True)
        self.assertRegexpMatches(response.content, 'Unknown passphrase')

    def test_login_accepts_valid_passphrases(self):
        user = create_user_with_rsvp(username='john', passphrase='lol')
        c = Client()
        response = c.post('/login', {'passphrase': 'lol'}, follow=True)
        self.assertEqual(response.context['user'], user)

    def test_login_rejects_inactive_users(self):
        user = create_user_with_rsvp(username='john', passphrase='lol',
                                     is_active=False)
        c = Client()
        response = c.post('/login', {'passphrase': 'lol'}, follow=True)
        self.assertNotEqual(response.context['user'], user)
        self.assertRegexpMatches(response.content, 'Unknown passphrase')

    def test_login_rejects_staff_passphrases(self):
        user = create_user_with_rsvp(username='john', passphrase='lol',
                                     is_staff=True)
        c = Client()
        response = c.post('/login', {'passphrase': 'lol'}, follow=True)
        self.assertNotEqual(response.context['user'], user)
        self.assertRegexpMatches(response.content, 'Unknown passphrase')

class RSVPTests(TestCase):
    def setUp(self):
        self.user = create_user_with_rsvp(username='john', passphrase='huh')

    def test_attending_with_no_guests_is_impossible(self):
        rsvp = self.user.rsvp
        rsvp.is_attending = True
        rsvp.number_of_guests = 0
        self.assertRaisesRegexp(
            ValidationError,
            "Accepted .* can't have 0 guests",
            rsvp.full_clean
        )

    def test_not_attending_with_guests_is_impossible(self):
        rsvp = self.user.rsvp
        rsvp.is_attending = False
        rsvp.number_of_guests = 1
        self.assertRaisesRegexp(
            ValidationError,
            "Declined .* can't have guests",
            rsvp.full_clean
        )

    def test_accepted_invites_work(self):
        rsvp = self.user.rsvp
        rsvp.is_attending = True
        rsvp.number_of_guests = 1
        rsvp.full_clean()

    def test_declined_invites_work(self):
        rsvp = self.user.rsvp
        rsvp.is_attending = False
        rsvp.number_of_guests = 0
        rsvp.full_clean()

class EmailTests(TestCase):
    def test_get_all_staff_with_email_works(self):
        User(username='foo', is_active=True, is_staff=True).save()
        User(username='bar', is_active=True, is_staff=True,
             email='bar@example.org').save()
        User(username='baz', is_active=True).save()
        users = email.get_all_staff_with_email()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].email, 'bar@example.org')

    def test_generate_rsvp_notification_works(self):
        user = User(username='john', first_name='John',
                    last_name=u'\u2026')
        rsvp = RSVP(user=user, is_attending=True, number_of_guests=2, 
                    song=u'Songy Song\u2026')
        subject, body = email.generate_rsvp_notification(rsvp)
        self.assertRegexpMatches(subject, u'John \u2026')
        self.assertRegexpMatches(body, r'2 guest')
        self.assertRegexpMatches(body, u'Songy Song\u2026')

    def test_notify_all_staff_of_rsvp_works(self):
        admin = User(username='admin', is_active=True, is_staff=True,
                     email='admin@example.org')
        user = User(username='john', first_name=u'John\u2026')
        rsvp = RSVP(user=user)
        admin.save()
        email.notify_all_staff_of_rsvp(rsvp)
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        self.assertRegexpMatches(msg.subject, u'John\u2026')
        self.assertRegexpMatches(msg.body, u'John\u2026')
        self.assertEqual(msg.to, [u'admin@example.org'])
        self.assertEqual(msg.from_email, settings.DEFAULT_FROM_EMAIL)
