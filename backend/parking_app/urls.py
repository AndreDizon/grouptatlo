from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, VehicleViewSet,
    ParkingSessionViewSet, ParkingLotViewSet, ParkingRateViewSet,
    ScanLogViewSet, login_view, register_view
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'parking-sessions', ParkingSessionViewSet, basename='parking-session')
router.register(r'parking-lots', ParkingLotViewSet, basename='parking-lot')
router.register(r'parking-rates', ParkingRateViewSet, basename='parking-rate')
router.register(r'scan-logs', ScanLogViewSet, basename='scan-log')

urlpatterns = [
    path('auth/login/', login_view, name='auth-login'),
    path('auth/register/', register_view, name='auth-register'),
    path('', include(router.urls)),
]
