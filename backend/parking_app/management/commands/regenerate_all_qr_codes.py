from django.core.management.base import BaseCommand
from parking_app.models import Vehicle


class Command(BaseCommand):
    help = 'Regenerate QR codes for all vehicles and upload to Cloudinary'

    def handle(self, *args, **options):
        vehicles = Vehicle.objects.all()
        
        if not vehicles.exists():
            self.stdout.write(self.style.WARNING('No vehicles found'))
            return
        
        count = 0
        for vehicle in vehicles:
            try:
                vehicle.generate_qr_code()
                vehicle.save()
                count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Generated QR code for vehicle {vehicle.id}: {vehicle.plate_number}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Failed to generate QR code for vehicle {vehicle.id}: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Successfully regenerated {count} QR codes'))
