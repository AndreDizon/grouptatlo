from django.core.management.base import BaseCommand
from django.conf import settings
from parking_app.models import Vehicle
import os
import re


class Command(BaseCommand):
    help = 'Delete QR code files that do not have corresponding vehicles in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        # Path to QR codes directory
        qr_codes_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
        
        if not os.path.exists(qr_codes_dir):
            self.stdout.write(self.style.WARNING(f'QR codes directory not found: {qr_codes_dir}'))
            return
        
        # Get all QR code files
        qr_files = [f for f in os.listdir(qr_codes_dir) if f.endswith('.png')]
        
        if not qr_files:
            self.stdout.write(self.style.SUCCESS('No QR code files found'))
            return
        
        self.stdout.write(f'Found {len(qr_files)} QR code files')
        self.stdout.write('-' * 80)
        
        # Get all plate numbers from vehicles in database
        vehicle_plate_numbers = set(Vehicle.objects.values_list('plate_number', flat=True))
        
        orphaned_files = []
        
        # Check each QR file
        for qr_file in qr_files:
            # Extract plate number from filename: qr_code_{plate_number}.png
            # Pattern: qr_code_(.+)\.png
            match = re.match(r'qr_code_(.+?)(?:_[a-zA-Z0-9]+)?\.png$', qr_file)
            
            if match:
                plate_number = match.group(1)
                
                # Check if vehicle with this plate number exists
                if plate_number not in vehicle_plate_numbers:
                    orphaned_files.append((qr_file, plate_number))
                    self.stdout.write(f'  [ORPHANED] {qr_file} (plate: {plate_number})')
            else:
                # Could not parse filename
                orphaned_files.append((qr_file, 'unknown'))
                self.stdout.write(f'  [INVALID NAME] {qr_file}')
        
        if not orphaned_files:
            self.stdout.write(self.style.SUCCESS('\n✓ No orphaned QR code files found'))
            return
        
        self.stdout.write('-' * 80)
        self.stdout.write(f'\nFound {len(orphaned_files)} orphaned QR code files')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\n[DRY RUN] No files were deleted. Use without --dry-run to delete.'))
            return
        
        # Delete orphaned files
        deleted_count = 0
        for qr_file, plate_number in orphaned_files:
            file_path = os.path.join(qr_codes_dir, qr_file)
            try:
                os.remove(file_path)
                deleted_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ Deleted: {qr_file}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ✗ Failed to delete {qr_file}: {str(e)}'))
        
        self.stdout.write('-' * 80)
        self.stdout.write(self.style.SUCCESS(f'\n✓ Cleanup complete! Deleted {deleted_count} orphaned QR code files'))
