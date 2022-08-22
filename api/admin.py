from django.contrib import admin
from . models import CustomUser, Ticket, Parking, Area

admin.site.register(CustomUser)
admin.site.register(Ticket)
admin.site.register(Parking)
admin.site.register(Area)