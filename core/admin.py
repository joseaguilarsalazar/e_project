# admin.py
from django.contrib import admin
from .models import (
    Notification, Company, Rol, UserCompany, Ship, SeatType, 
    Seat, Route, Trip, TripSeat, Booking, PaymentMethod, Payment
)

admin.site.register(Notification)
admin.site.register(Company)
admin.site.register(Rol)
admin.site.register(UserCompany)
admin.site.register(Ship)
admin.site.register(SeatType)
admin.site.register(Seat)
admin.site.register(Route)
admin.site.register(Trip)
admin.site.register(TripSeat)
admin.site.register(Booking)
admin.site.register(PaymentMethod)
admin.site.register(Payment)