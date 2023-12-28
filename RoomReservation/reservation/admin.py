from django.contrib import admin
from .models import Reservation, Attendee

# Register your models here.
admin.site.register(Reservation)
admin.site.register(Attendee)
