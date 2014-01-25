from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RSVP(models.Model):
    user = models.OneToOneField(User)
    passphrase = models.CharField(max_length=30, unique=True)
    is_attending = models.BooleanField(default=False)
    number_of_guests = models.SmallIntegerField(default=0)
    song = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return u'RSVP for %s' % self.user
