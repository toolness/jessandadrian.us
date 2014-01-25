from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class RSVP(models.Model):
    user = models.OneToOneField(User)
    passphrase = models.CharField(max_length=30, unique=True)
    is_attending = models.BooleanField()
    number_of_guests = models.SmallIntegerField()

    def __unicode__(self):
    	return u'RSVP for %s' % self.user
