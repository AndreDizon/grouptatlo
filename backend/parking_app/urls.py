from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, VehicleViewSet, ParkingPassViewSet,
    ParkingSessionViewSet, ParkingLotViewSet, ParkingRateViewSet,
    AnnouncementViewSet, ScanLogViewSet, login_view
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'parking-passes', ParkingPassViewSet, basename='parking-pass')
router.register(r'parking-sessions', ParkingSessionViewSet, basename='parking-session')
router.register(r'parking-lots', ParkingLotViewSet, basename='parking-lot')
router.register(r'parking-rates', ParkingRateViewSet, basename='parking-rate')
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register(r'scan-logs', ScanLogViewSet, basename='scan-log')

urlpatterns = [
    path('auth/login/', login_view, name='auth-login'),
    path('', include(router.urls)),
]
