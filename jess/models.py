from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

# Create your models here.
class RSVP(models.Model):
    user = models.OneToOneField(User)
    passphrase = models.CharField(
        help_text="The phrase sent to the person/family in the hard-copy "
                  "invitation, allowing them to sign into the site "
                  "without needing to additionally remember a username.",
        max_length=30,
        unique=True
    )
    is_attending = models.BooleanField(
        default=False
    )
    number_of_guests = models.SmallIntegerField(
        help_text="How many people are attending? Please include yourself.",
        default=0
    )
    song = models.CharField(
        help_text="There will be dancing! We'll try our best to include "
                  "your favorite song.",
        max_length=200,
        blank=True
    )

    def __unicode__(self):
        return u'RSVP for %s' % self.user

    def clean(self):
        if self.is_attending:
            if self.number_of_guests < 1:
              raise ValidationError("Accepted invitations can't have "
                                    "0 guests.")
        elif self.number_of_guests > 0:
            raise ValidationError("Declined invitations can't have guests.")
