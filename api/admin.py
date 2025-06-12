from django.contrib import admin
from . models import CustomUser, Ticket, Parking, ParkingPrice, ParkingSection, ParkingSlot, Vehicle, Passes

admin.site.register(CustomUser)
admin.site.register(Ticket)
admin.site.register(Parking)
admin.site.register(ParkingPrice)
admin.site.register(ParkingSection)
admin.site.register(ParkingSlot)
admin.site.register(Vehicle)