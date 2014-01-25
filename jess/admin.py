from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

import models
# Register your models here.

class RSVPInline(admin.StackedInline):
    verbose_name_plural = 'RSVP'
    model = models.RSVP
    can_delete = False

class RSVPUserAdmin(UserAdmin):
    inlines = (RSVPInline,)

admin.site.unregister(User)
admin.site.register(User, RSVPUserAdmin)
