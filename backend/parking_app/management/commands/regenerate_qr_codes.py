from django.core.management.base import BaseCommand
from parking_app.models import Vehicle


class Command(BaseCommand):
    help = 'Regenerate QR codes for all vehicles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--vehicle-id',
            type=int,
            help='Regenerate QR code for a specific vehicle ID',
        )

    def handle(self, *args, **options):
        vehicle_id = options.get('vehicle_id')
        
        if vehicle_id:
            try:
                vehicle = Vehicle.objects.get(id=vehicle_id)
                vehicle.generate_qr_code()
                vehicle.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully regenerated QR code for vehicle: {vehicle.plate_number}'
                    )
                )
            except Vehicle.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Vehicle with ID {vehicle_id} not found')
                )
        else:
            # Regenerate for all vehicles
            vehicles = Vehicle.objects.all()
            count = 0
            for vehicle in vehicles:
                vehicle.generate_qr_code()
                vehicle.save()
                count += 1
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully regenerated QR codes for {count} vehicles'
                )
            )
