# Migration for UserProfile consolidation - empty for now, will use Python migration if needed
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking_app', '0004_vehicle_is_paid'),
    ]

    operations = [
        # Keep UserProfile table as-is - no schema migration needed
        # The app now treats User as primary with optional UserProfile for backward compatibility
    ]
