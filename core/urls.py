# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create a router and register our viewsets with it
router = DefaultRouter()

# Register all viewsets
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'companies', views.CompanyViewSet, basename='company')
router.register(r'roles', views.RolViewSet, basename='rol')
router.register(r'user-companies', views.UserCompanyViewSet, basename='usercompany')
router.register(r'ships', views.ShipViewSet, basename='ship')
router.register(r'seat-types', views.SeatTypeViewSet, basename='seattype')
router.register(r'seats', views.SeatViewSet, basename='seat')
router.register(r'routes', views.RouteViewSet, basename='route')
router.register(r'trips', views.TripViewSet, basename='trip')
router.register(r'trip-seats', views.TripSeatViewSet, basename='tripseat')
router.register(r'bookings', views.BookingViewSet, basename='booking')
router.register(r'payment-methods', views.PaymentMethodViewSet, basename='paymentmethod')
router.register(r'payments', views.PaymentViewSet, basename='payment')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
    path('register/', views.RegisterView.as_view(), name='register'),  
]