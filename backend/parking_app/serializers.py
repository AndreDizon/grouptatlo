from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Vehicle, ParkingSession,
    ParkingLot, ParkingRate, ScanLog
)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    role = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'role', 'is_staff']
    
    def create(self, validated_data):
        """Create user with properly hashed password"""
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def get_role(self, obj):
        # Determine role based on is_superuser and is_staff flags
        if obj.is_superuser:
            return 'admin'
        elif obj.is_staff:
            return 'guard'
        else:
            return 'driver'


class VehicleSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            'id', 'owner', 'owner_name', 'vehicle_type', 'brand', 'model',
            'plate_number', 'color', 'registration_date', 'is_paid',
            'qr_code', 'sticker_number'
        ]


class ParkingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingRate
        fields = ['id', 'vehicle_type', 'pass_type', 'price', 'description', 'is_active']


class ParkingSessionSerializer(serializers.ModelSerializer):
    vehicle_info = VehicleSerializer(source='vehicle', read_only=True)
    guard_name = serializers.CharField(source='scanned_by.get_full_name', read_only=True, allow_null=True)
    duration_hours = serializers.ReadOnlyField()

    class Meta:
        model = ParkingSession
        fields = [
            'id', 'vehicle', 'parking_lot', 'vehicle_info', 'time_in', 'time_out',
            'scanned_by', 'guard_name', 'is_valid', 'notes', 'duration_hours'
        ]


class ParkingLotSerializer(serializers.ModelSerializer):
    occupied_slots = serializers.ReadOnlyField()
    occupancy_rate = serializers.ReadOnlyField()

    class Meta:
        model = ParkingLot
        fields = [
            'id', 'name', 'location', 'total_slots', 'available_slots',
            'occupied_slots', 'occupancy_rate', 'description', 'is_active'
        ]


class ScanLogSerializer(serializers.ModelSerializer):
    guard_name = serializers.CharField(source='guard.get_full_name', read_only=True)
    vehicle_info = VehicleSerializer(source='vehicle', read_only=True)

    class Meta:
        model = ScanLog
        fields = ['id', 'guard', 'guard_name', 'vehicle', 'vehicle_info', 'scan_time', 'scan_type', 'manual_entry', 'notes']
