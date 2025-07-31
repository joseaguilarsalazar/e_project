# filters.py
import django_filters
from django.contrib.auth.models import User
from django_filters import rest_framework as filters
from .models import (
    Notification, Company, Rol, UserCompany, Ship, SeatType, 
    Seat, Route, Trip, TripSeat, Booking, PaymentMethod, Payment
)


class NotificationFilter(filters.FilterSet):
    user = filters.ModelChoiceFilter(queryset=User.objects.all())
    user_id = filters.NumberFilter(field_name='user__id')
    user_username = filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    topic = filters.CharFilter(lookup_expr='icontains')
    body = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter()
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Notification
        fields = ['user', 'topic']

    @property
    def qs(self):
        parent = super().qs
        return parent.select_related('user')


class CompanyFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    email = filters.CharFilter(lookup_expr='icontains')
    address = filters.CharFilter(lookup_expr='icontains')
    phoneNumber = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    has_logo = filters.BooleanFilter(field_name='logo', lookup_expr='isnull', exclude=True)
    created_at = filters.DateFromToRangeFilter()
    
    class Meta:
        model = Company
        fields = ['name', 'email']

    def filter_has_logo(self, queryset, name, value):
        if value is True:
            return queryset.exclude(logo__isnull=True).exclude(logo__exact='')
        elif value is False:
            return queryset.filter(logo__isnull=True) | queryset.filter(logo__exact='')
        return queryset


class RolFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Rol
        fields = ['name']


class UserCompanyFilter(filters.FilterSet):
    empresa = filters.ModelChoiceFilter(queryset=Company.objects.all())
    empresa_id = filters.NumberFilter(field_name='empresa__id')
    empresa_name = filters.CharFilter(field_name='empresa__name', lookup_expr='icontains')
    user = filters.ModelChoiceFilter(queryset=User.objects.all())
    user_id = filters.NumberFilter(field_name='user__id')
    user_username = filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    user_email = filters.CharFilter(field_name='user__email', lookup_expr='icontains')
    rol = filters.ModelChoiceFilter(queryset=Rol.objects.all())
    rol_id = filters.NumberFilter(field_name='rol__id')
    rol_name = filters.CharFilter(field_name='rol__name', lookup_expr='icontains')
    has_rol = filters.BooleanFilter(field_name='rol', lookup_expr='isnull', exclude=True)

    class Meta:
        model = UserCompany
        fields = ['empresa', 'user', 'rol']

    @property
    def qs(self):
        parent = super().qs
        return parent.select_related('empresa', 'user', 'rol')


class ShipFilter(filters.FilterSet):
    company = filters.ModelChoiceFilter(queryset=Company.objects.all())
    company_id = filters.NumberFilter(field_name='company__id')
    company_name = filters.CharFilter(field_name='company__name', lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')
    construction_year = filters.NumberFilter()
    construction_year_min = filters.NumberFilter(field_name='construction_year', lookup_expr='gte')
    construction_year_max = filters.NumberFilter(field_name='construction_year', lookup_expr='lte')
    construction_year_range = filters.RangeFilter(field_name='construction_year')

    class Meta:
        model = Ship
        fields = ['company', 'name', 'construction_year']

    @property
    def qs(self):
        parent = super().qs
        return parent.select_related('company')


class SeatTypeFilter(filters.FilterSet):
    ship = filters.ModelChoiceFilter(queryset=Ship.objects.all())
    ship_id = filters.NumberFilter(field_name='ship__id')
    ship_name = filters.CharFilter(field_name='ship__name', lookup_expr='icontains')
    ship_company = filters.NumberFilter(field_name='ship__company__id')
    aditionalPrice = filters.NumberFilter()
    aditionalPrice_min = filters.NumberFilter(field_name='aditionalPrice', lookup_expr='gte')
    aditionalPrice_max = filters.NumberFilter(field_name='aditionalPrice', lookup_expr='lte')
    aditionalPrice_range = filters.RangeFilter(field_name='aditionalPrice')
    is_free = filters.BooleanFilter(method='filter_is_free')

    class Meta:
        model = SeatType
        fields = ['ship', 'aditionalPrice']

    def filter_is_free(self, queryset, name, value):
        if value is True:
            return queryset.filter(aditionalPrice=0.0)
        elif value is False:
            return queryset.exclude(aditionalPrice=0.0)
        return queryset

    @property
    def qs(self):
        parent = super().qs
        return parent.select_related('ship', 'ship__company')


class SeatFilter(filters.FilterSet):
    seatType = filters.ModelChoiceFilter(queryset=SeatType.objects.all())
    seatType_id = filters.NumberFilter(field_name='seatType__id')
    ship = filters.NumberFilter(field_name='seatType__ship__id')
    ship_name = filters.CharFilter(field_name='seatType__ship__name', lookup_expr='icontains')
    company = filters.NumberFilter(field_name='seatType__ship__company__id')
    number = filters.NumberFilter()
    number_min = filters.NumberFilter(field_name='number', lookup_expr='gte')
    number_max = filters.NumberFilter(field_name='number', lookup_expr='lte')
    number_range = filters.RangeFilter(field_name='number')

    class Meta:
        model = Seat
        fields = ['seatType', 'number']

    @property
    def qs(self):
        parent = super().qs
        return parent.select_related('seatType', 'seatType__ship', 'seatType__ship__company')


class RouteFilter(filters.FilterSet):
    company = filters.ModelChoiceFilter(queryset=Company.objects.all())
    company_id = filters.NumberFilter(field_name='company__id')
    company_name = filters.CharFilter(field_name='company__name', lookup_expr='icontains')
    origin = filters.CharFilter(lookup_expr='icontains')
    destiny = filters.CharFilter(lookup_expr='icontains')
    origin_exact = filters.CharFilter(field_name='origin', lookup_expr='exact')
    destiny_exact = filters.CharFilter(field_name='destiny', lookup_expr='exact')
    route_search = filters.CharFilter(method='filter_route_search')

    class Meta:
        model = Route
        fields = ['company', 'origin', 'destiny']

    def filter_route_search(self, queryset, name, value):
        """Search in both origin and destiny fields"""
        return queryset.filter(
            django_filters.Q(origin__icontains=value) | 
            django_filters.Q(destiny__icontains=value)
        )

    @property
    def qs(self):
        parent = super().qs
        return parent.select_related('company')


class TripFilter(filters.FilterSet):
    route = filters.ModelChoiceFilter(queryset=Route.objects.all())
    route_id = filters.NumberFilter(field_name='route__id')
    origin = filters.CharFilter(field_name='route__origin', lookup_expr='icontains')
    destiny = filters.CharFilter(field_name='route__destiny', lookup_expr='icontains')
    company = filters.NumberFilter(field_name='route__company__id')
    company_name = filters.CharFilter(field_name='route__company__name', lookup_expr='icontains')
    seat = filters.ModelChoiceFilter(queryset=Seat.objects.all())
    seat_id = filters.NumberFilter(field_name='seat__id')
    seat_number = filters.NumberFilter(field_name='seat__number')
    ship = filters.NumberFilter(field_name='seat__seatType__ship__id')
    basePrice = filters.NumberFilter()
    basePrice_min = filters.NumberFilter(field_name='basePrice', lookup_expr='gte')
    basePrice_max = filters.NumberFilter(field_name='basePrice', lookup_expr='lte')
    basePrice_range = filters.RangeFilter(field_name='basePrice')
    dateDeparture = filters.NumberFilter()
    dateDeparture_min = filters.NumberFilter(field_name='dateDeparture', lookup_expr='gte')
    dateDeparture_max = filters.NumberFilter(field_name='dateDeparture', lookup_expr='lte')

    class Meta:
        model = Trip
        fields = ['route', 'seat', 'basePrice', 'dateDeparture']

    @property
    def qs(self):
        parent = super().qs
        return parent.select_related(
            'route', 'route__company', 'seat', 
            'seat__seatType', 'seat__seatType__ship'
        )


class TripSeatFilter(filters.FilterSet):
    trip = filters.ModelChoiceFilter(queryset=Trip.objects.all())
    trip_id = filters.NumberFilter(field_name='trip__id')
    seat = filters.ModelChoiceFilter(queryset=Seat.objects.all())
    seat_id = filters.NumberFilter(field_name='seat__id')
    seat_number = filters.NumberFilter(field_name='seat__number')
    ship = filters.NumberFilter(field_name='seat__seatType__ship__id')
    company = filters.NumberFilter(field_name='trip__route__company__id')
    origin = filters.CharFilter(field_name='trip__route__origin', lookup_expr='icontains')
    destiny = filters.CharFilter(field_name='trip__route__destiny', lookup_expr='icontains')
    state = filters.ChoiceFilter(choices=TripSeat.STATE_CHOICES)
    available_seats = filters.BooleanFilter(method='filter_available_seats')

    class Meta:
        model = TripSeat
        fields = ['trip', 'seat', 'state']

    def filter_available_seats(self, queryset, name, value):
        if value is True:
            return queryset.filter(state='disponible')
        elif value is False:
            return queryset.exclude(state='disponible')
        return queryset

    @property
    def qs(self):
        parent = super().qs
        return parent.select_related(
            'trip', 'trip__route', 'trip__route__company',
            'seat', 'seat__seatType', 'seat__seatType__ship'
        )


class BookingFilter(filters.FilterSet):
    tripSeat = filters.ModelChoiceFilter(queryset=TripSeat.objects.all())
    tripSeat_id = filters.NumberFilter(field_name='tripSeat__id')
    user = filters.ModelChoiceFilter(queryset=User.objects.all())
    user_id = filters.NumberFilter(field_name='user__id')
    user_username = filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    user_email = filters.CharFilter(field_name='user__email', lookup_expr='icontains')
    paid = filters.BooleanFilter()
    trip_id = filters.NumberFilter(field_name='tripSeat__trip__id')
    seat_number = filters.NumberFilter(field_name='tripSeat__seat__number')
    company = filters.NumberFilter(field_name='tripSeat__trip__route__company__id')
    origin = filters.CharFilter(field_name='tripSeat__trip__route__origin', lookup_expr='icontains')
    destiny = filters.CharFilter(field_name='tripSeat__trip__route__destiny', lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Booking
        fields = ['tripSeat', 'user', 'paid']

    @property
    def qs(self):
        parent = super().qs
        return parent.select_related(
            'tripSeat', 'tripSeat__trip', 'tripSeat__trip__route',
            'tripSeat__trip__route__company', 'tripSeat__seat',
            'tripSeat__seat__seatType', 'user'
        )


class PaymentMethodFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = PaymentMethod
        fields = ['name']


class PaymentFilter(filters.FilterSet):
    method = filters.ModelChoiceFilter(queryset=PaymentMethod.objects.all())
    method_id = filters.NumberFilter(field_name='method__id')
    method_name = filters.CharFilter(field_name='method__name', lookup_expr='icontains')
    booking = filters.ModelChoiceFilter(queryset=Booking.objects.all())
    booking_id = filters.NumberFilter(field_name='booking__id')
    user = filters.NumberFilter(field_name='booking__user__id')
    user_username = filters.CharFilter(field_name='booking__user__username', lookup_expr='icontains')
    trip_id = filters.NumberFilter(field_name='booking__tripSeat__trip__id')
    company = filters.NumberFilter(field_name='booking__tripSeat__trip__route__company__id')
    has_method = filters.BooleanFilter(field_name='method', lookup_expr='isnull', exclude=True)
    created_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Payment
        fields = ['method', 'booking']

    @property
    def qs(self):
        parent = super().qs
        return parent.select_related(
            'method', 'booking', 'booking__user',
            'booking__tripSeat', 'booking__tripSeat__trip',
            'booking__tripSeat__trip__route', 'booking__tripSeat__trip__route__company'
        )