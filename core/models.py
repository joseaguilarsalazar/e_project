from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # ✅ prevents Django from creating a BaseModel table

class Notification(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    body = models.TextField(max_length=1000)

class Company(BaseModel):
    email = models.EmailField(null = True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=15)
    logo = models.ImageField(null=True, blank=True)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name 

class Rol(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 

class UserCompany(BaseModel):
    empresa = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)

class Ship(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    construction_year = models.IntegerField()

class SeatType(BaseModel):
    ship = models.ForeignKey(Ship, on_delete=models.CASCADE)
    aditionalPrice = models.FloatField(default=0.0)

class Seat(BaseModel):
    seatType = models.ForeignKey(SeatType, on_delete=models.CASCADE)
    number = models.IntegerField()

class Route(BaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    origin = models.CharField(max_length=100)
    destiny = models.CharField(max_length=100)
    

class Trip(BaseModel):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    basePrice = models.FloatField(default=0.0)
    dateDeparture = models.DateTimeField()

class TripSeat(BaseModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)

    STATE_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado'),
        ('reservado', 'Reservado'),
    ]

    state = models.CharField(choices=STATE_CHOICES, max_length=10)


class Booking(BaseModel):
    tripSeat = models.ForeignKey(TripSeat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    paid = models.BooleanField(default=False)

class PaymentMethod(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)

class Payment(BaseModel):
    method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

