# Generated migration to remove unused ParkingPass and Announcement models

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking_app', '0007_remove_parking_rate_vehicle_type_choices'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Announcement',
        ),
        migrations.DeleteModel(
            name='ParkingPass',
        ),
    ]
