from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import datetime
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image

ROLE_CHOICES = [
    ('admin', 'Administrator'),
    ('driver', 'Driver'),
    ('guard', 'Security Guard'),
]

VEHICLE_TYPES = [
    ('car', 'Car'),
    ('motorcycle', 'Motorcycle'),
    ('truck', 'Truck'),
    ('van', 'Van'),
]

PASS_TYPES = [
    ('drop-off', 'Drop-Off'),
    ('park', 'Park'),
]


class Vehicle(models.Model):
    """Vehicle registration model"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vehicles')
    vehicle_type = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=20, unique=True)
    color = models.CharField(max_length=50, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    is_registered = models.BooleanField(default=True)  # Auto-register vehicles on creation
    is_paid = models.BooleanField(default=False)  # Payment status for vehicle registration
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    sticker_number = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model} - {self.plate_number}"

    def generate_qr_code(self):
        """Generate QR code for vehicle"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"UA_PARKING_{self.id}_{self.plate_number}")
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        filename = f"qr_code_{self.plate_number}.png"
        self.qr_code.save(filename, File(buffer), save=False)

    class Meta:
        ordering = ['-registration_date']


class ParkingLot(models.Model):
    """Parking lot information"""
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    total_slots = models.IntegerField(validators=[MinValueValidator(1)])
    available_slots = models.IntegerField(validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def occupied_slots(self):
        return self.total_slots - self.available_slots

    @property
    def occupancy_rate(self):
        return (self.occupied_slots / self.total_slots) * 100 if self.total_slots > 0 else 0

    class Meta:
        verbose_name_plural = "Parking Lots"


class ParkingSession(models.Model):
    """Parking session tracking"""
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='sessions')
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(null=True, blank=True)
    scanned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.vehicle.plate_number} - {self.time_in}"

    @property
    def duration_hours(self):
        """Calculate parking duration in hours"""
        if self.time_out:
            delta = self.time_out - self.time_in
            return delta.total_seconds() / 3600
        return None

    class Meta:
        ordering = ['-time_in']


class ParkingRate(models.Model):
    """Parking rates configuration"""
    vehicle_type = models.CharField(max_length=20)  # Allow any vehicle type
    pass_type = models.CharField(max_length=20, choices=PASS_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.vehicle_type} - {self.get_pass_type_display()}: PHP {self.price}"

    class Meta:
        unique_together = ['vehicle_type', 'pass_type']
        verbose_name_plural = "Parking Rates"





class ScanLog(models.Model):
    """QR code scan logs for guards"""
    guard = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='scan_logs')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='scan_logs')
    scan_time = models.DateTimeField(auto_now_add=True)
    scan_type = models.CharField(max_length=10, choices=[('in', 'Time In'), ('out', 'Time Out')])
    manual_entry = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.vehicle.plate_number} - {self.scan_type} at {self.scan_time}"

    class Meta:
        ordering = ['-scan_time']
