# Generated migration to delete UserProfile model

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parking_app', '0005_migrate_userprofile_to_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
