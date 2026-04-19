"""
Django management command to populate initial data
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking_system.settings')
django.setup()

from django.contrib.auth.models import User
from parking_app.models import ParkingLot, ParkingRate, Vehicle
from datetime import datetime, timedelta

# Create test users
users_data = [
    {'username': 'driver1', 'email': 'driver1@uaparking.com', 'first_name': 'Juan', 'last_name': 'Dela Cruz', 'role': 'driver'},
    {'username': 'driver2', 'email': 'driver2@uaparking.com', 'first_name': 'Maria', 'last_name': 'Santos', 'role': 'driver'},
    {'username': 'guard1', 'email': 'guard1@uaparking.com', 'first_name': 'Marlon', 'last_name': 'Garcia', 'role': 'guard'},
    {'username': 'guard2', 'email': 'guard2@uaparking.com', 'first_name': 'Carlos', 'last_name': 'Reyes', 'role': 'guard'},
]

print("Creating test users...")
for user_data in users_data:
    if not User.objects.filter(username=user_data['username']).exists():
        role = user_data['role']
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password='password123'
        )
        
        # Set staff/superuser status based on role
        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        elif role == 'guard':
            user.is_staff = True
            user.is_superuser = False
        else:
            # driver
            user.is_staff = False
            user.is_superuser = False
        
        user.save()
        print(f"✓ Created {user_data['role']} user: {user_data['username']}")
    else:
        print(f"✓ {user_data['username']} already exists")

# Create parking lots
parking_lots_data = [
    {'name': 'Main Campus Lot A', 'location': 'Building 1', 'total_slots': 100},
    {'name': 'Main Campus Lot B', 'location': 'Building 2', 'total_slots': 80},
    {'name': 'Science Building Lot', 'location': 'Science Complex', 'total_slots': 60},
    {'name': 'Sports Complex Lot', 'location': 'Sports Area', 'total_slots': 120},
]

print("\nCreating parking lots...")
for lot_data in parking_lots_data:
    if not ParkingLot.objects.filter(name=lot_data['name']).exists():
        ParkingLot.objects.create(
            name=lot_data['name'],
            location=lot_data['location'],
            total_slots=lot_data['total_slots'],
            available_slots=lot_data['total_slots']
        )
        print(f"✓ Created parking lot: {lot_data['name']}")
    else:
        print(f"✓ {lot_data['name']} already exists")

# Create parking rates
rates_data = [
    {'vehicle_type': 'car', 'pass_type': 'daily', 'price': 250},
    {'vehicle_type': 'car', 'pass_type': 'monthly', 'price': 5000},
    {'vehicle_type': 'motorcycle', 'pass_type': 'daily', 'price': 100},
    {'vehicle_type': 'motorcycle', 'pass_type': 'monthly', 'price': 2000},
    {'vehicle_type': 'truck', 'pass_type': 'daily', 'price': 500},
    {'vehicle_type': 'truck', 'pass_type': 'monthly', 'price': 10000},
    {'vehicle_type': 'van', 'pass_type': 'daily', 'price': 350},
    {'vehicle_type': 'van', 'pass_type': 'monthly', 'price': 7000},
]

print("\nCreating parking rates...")
for rate_data in rates_data:
    combined_key = f"{rate_data['vehicle_type']}_{rate_data['pass_type']}"
    if not ParkingRate.objects.filter(**{k: v for k, v in rate_data.items() if k != 'description'}).exists():
        ParkingRate.objects.create(**rate_data)
        print(f"✓ Created rate: {rate_data['vehicle_type']} - {rate_data['pass_type']} - PHP {rate_data['price']}")
    else:
        print(f"✓ Rate for {rate_data['vehicle_type']} ({rate_data['pass_type']}) already exists")

# Create sample vehicles
driver1 = User.objects.get(username='driver1')
vehicles_data = [
    {'vehicle_type': 'car', 'brand': 'Toyota', 'model': 'Vios', 'plate_number': 'ABC1234', 'color': 'Silver', 'pass_type': 'park'},
    {'vehicle_type': 'car', 'brand': 'Honda', 'model': 'Civic', 'plate_number': 'BCD5678', 'color': 'Black', 'pass_type': 'drop_off'},
]

print("\nCreating sample vehicles...")
for vehicle_data in vehicles_data:
    if not Vehicle.objects.filter(plate_number=vehicle_data['plate_number']).exists():
        Vehicle.objects.create(owner=driver1, **vehicle_data)
        print(f"✓ Created vehicle: {vehicle_data['brand']} {vehicle_data['model']} - {vehicle_data['plate_number']}")
    else:
        print(f"✓ Vehicle {vehicle_data['plate_number']} already exists")

print("\n✅ Initial data setup completed!")
print("\nTest Credentials:")
print("=" * 50)
print("Admin Account:")
print("  Username: admin")
print("  Password: admin123")
print("\nTest Accounts:")
for user_data in users_data:
    print(f"  {user_data['role'].title()}: {user_data['username']} / password123")
print("=" * 50)
