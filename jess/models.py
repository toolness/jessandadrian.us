from django.db import models
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
        help_text="Whether the person/family is attending the event.",
        default=False
    )
    number_of_guests = models.SmallIntegerField(
        help_text="The number of guests the person/family is bringing to "
                  "the event, including themselves.",
        default=0
    )
    song = models.CharField(
        help_text="A song the person/family would like to dance to at "
                  "the event.",
        max_length=200,
        blank=True
    )

    def __unicode__(self):
        return u'RSVP for %s' % self.user
