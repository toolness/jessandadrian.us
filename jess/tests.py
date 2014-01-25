from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import RSVP

# Create your tests here.
class RSVPTests(TestCase):
    def setUp(self):
        user = User(username='john')
        user.save()
        rsvp = RSVP(user=user)
        rsvp.passphrase = 'a unique passphrase'
        rsvp.save()
        self.user = user

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
