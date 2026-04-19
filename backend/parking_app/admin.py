from django.contrib import admin
from .models import (
    Vehicle, ParkingSession,
    ParkingLot, ParkingRate, ScanLog
)


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['plate_number', 'brand', 'model', 'vehicle_type', 'owner', 'is_paid', 'pass_type']
    list_filter = ['vehicle_type', 'is_paid', 'pass_type', 'registration_date']
    search_fields = ['plate_number', 'brand', 'model', 'owner__first_name']
    readonly_fields = ['registration_date']


@admin.register(ParkingSession)
class ParkingSessionAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'time_in', 'time_out', 'is_valid', 'duration_hours']
    list_filter = ['is_valid', 'time_in']
    search_fields = ['vehicle__plate_number']
    readonly_fields = ['time_in']


@admin.register(ParkingLot)
class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'total_slots', 'occupied_slots', 'occupancy_rate', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'location']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ParkingRate)
class ParkingRateAdmin(admin.ModelAdmin):
    list_display = ['vehicle_type', 'pass_type', 'price', 'is_active']
    list_filter = ['vehicle_type', 'pass_type', 'is_active']
    search_fields = ['vehicle_type', 'pass_type']


@admin.register(ScanLog)
class ScanLogAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'guard', 'scan_type', 'scan_time', 'manual_entry']
    list_filter = ['scan_type', 'manual_entry', 'scan_time']
    search_fields = ['vehicle__plate_number', 'guard__first_name']
    readonly_fields = ['scan_time']
