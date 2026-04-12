# Generated migration to remove vehicle_type choices from ParkingRate

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parking_app', '0006_delete_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkingrate',
            name='vehicle_type',
            field=models.CharField(max_length=20),
        ),
    ]
