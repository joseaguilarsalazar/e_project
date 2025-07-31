# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Notification, Company, Rol, UserCompany, Ship, SeatType, 
    Seat, Route, Trip, TripSeat, Booking, PaymentMethod, Payment
)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})  # confirm password

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')  # remove password2 before creating user
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'user_id', 'topic', 'body', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'id', 'email', 'name', 'address', 'phoneNumber', 
            'logo', 'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_phoneNumber(self, value):
        if len(value) > 15:
            raise serializers.ValidationError("Phone number cannot exceed 15 characters.")
        return value


class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['id', 'name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCompanySerializer(serializers.ModelSerializer):
    empresa = CompanySerializer(read_only=True)
    empresa_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    rol = RolSerializer(read_only=True)
    rol_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = UserCompany
        fields = [
            'id', 'empresa', 'empresa_id', 'user', 'user_id', 
            'rol', 'rol_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ShipSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Ship
        fields = [
            'id', 'company', 'company_id', 'name', 
            'construction_year', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_construction_year(self, value):
        import datetime
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Construction year cannot be in the future.")
        if value < 1800:
            raise serializers.ValidationError("Construction year seems too old.")
        return value


class SeatTypeSerializer(serializers.ModelSerializer):
    ship = ShipSerializer(read_only=True)
    ship_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = SeatType
        fields = [
            'id', 'ship', 'ship_id', 'aditionalPrice', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_aditionalPrice(self, value):
        if value < 0:
            raise serializers.ValidationError("Additional price cannot be negative.")
        return value


class SeatSerializer(serializers.ModelSerializer):
    seatType = SeatTypeSerializer(read_only=True)
    seatType_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Seat
        fields = [
            'id', 'seatType', 'seatType_id', 'number', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_number(self, value):
        if value <= 0:
            raise serializers.ValidationError("Seat number must be positive.")
        return value


class RouteSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Route
        fields = [
            'id', 'company', 'company_id', 'origin', 
            'destiny', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        if data.get('origin') == data.get('destiny'):
            raise serializers.ValidationError("Origin and destiny cannot be the same.")
        return data


class TripSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    route_id = serializers.IntegerField(write_only=True)
    seat = SeatSerializer(read_only=True)
    seat_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Trip
        fields = [
            'id', 'route', 'route_id', 'seat', 'seat_id', 
            'basePrice', 'dateDeparture', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_basePrice(self, value):
        if value < 0:
            raise serializers.ValidationError("Base price cannot be negative.")
        return value


class TripSeatSerializer(serializers.ModelSerializer):
    trip = TripSerializer(read_only=True)
    trip_id = serializers.IntegerField(write_only=True)
    seat = SeatSerializer(read_only=True)
    seat_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = TripSeat
        fields = [
            'id', 'trip', 'trip_id', 'seat', 'seat_id', 
            'state', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    tripSeat = TripSeatSerializer(read_only=True)
    tripSeat_id = serializers.IntegerField(write_only=True)
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'tripSeat', 'tripSeat_id', 'user', 'user_id', 
            'paid', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    method = PaymentMethodSerializer(read_only=True)
    method_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    booking = BookingSerializer(read_only=True)
    booking_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'method', 'method_id', 'booking', 'booking_id', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# Lightweight serializers for listing views
class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'email', 'address']


class ShipListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Ship
        fields = ['id', 'name', 'construction_year', 'company_name']


class RouteListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Route
        fields = ['id', 'origin', 'destiny', 'company_name']


class TripListSerializer(serializers.ModelSerializer):
    route_info = serializers.SerializerMethodField()
    seat_number = serializers.CharField(source='seat.number', read_only=True)

    class Meta:
        model = Trip
        fields = ['id', 'route_info', 'seat_number', 'basePrice', 'dateDeparture']

    def get_route_info(self, obj):
        return f"{obj.route.origin} → {obj.route.destiny}"