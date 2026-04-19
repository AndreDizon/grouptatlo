# UA Parking System - QR Code Feature Documentation

## Overview
The QR Code feature is a core component of the UA Parking System that enables:
- Automatic QR code generation for vehicle registration
- QR code scanning by security guards for vehicle entry/exit tracking
- Vehicle identification through encoded QR data
- Parking session logging through quick scanning

---

## QR Code Generation & Storage

### Automatic Generation
QR codes are automatically generated when a vehicle is registered:

1. **Trigger Point**: Vehicle creation via API endpoint `POST /api/vehicles/`
2. **Automatic Call**: `vehicle.generate_qr_code()` method executes automatically
3. **Storage Location**: `backend/media/qr_codes/` directory
4. **Filename Format**: `qr_code_{plate_number}_{randomsuffix}.png`

### QR Code Data Format
Each QR code encodes the following format:
```
UA_PARKING_{vehicle_id}_{plate_number}
```

**Examples:**
- `UA_PARKING_1_TEST2024`
- `UA_PARKING_2_abc122`
- `UA_PARKING_3_ddd123`

This dual-encoded approach ensures:
- Vehicle lookup by plate_number (primary - case-insensitive)
- Fallback to vehicle_id if plate_number fails
- Protection against stale QR codes with outdated vehicle IDs

---

## Backend Dependencies

### Required Python Packages

#### QR Code Generation
| Package | Version | Purpose | Location |
|---------|---------|---------|----------|
| **qrcode** | 7.4.2 | QR code generation library | requirements.txt |
| **Pillow** | 10.1.0 | Image processing (PIL/Image) | requirements.txt |

#### Installation
These are included in `requirements.txt`. Install with:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install qrcode==7.4.2
pip install Pillow==10.1.0
```

### Direct Imports in Code
In `backend/parking_app/models.py`:
```python
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
```

---

## QR Code Generation Process

### The `generate_qr_code()` Method

**Location**: `backend/parking_app/models.py` in the `Vehicle` model

```python
def generate_qr_code(self):
    """Generate QR code for vehicle"""
    # Initialize QR code generator
    qr = qrcode.QRCode(
        version=1,                                      # QR version (size)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,                                    # Size of each box in pixels
        border=4,                                       # Border size in boxes
    )
    
    # Add vehicle data to QR code
    qr.add_data(f"UA_PARKING_{self.id}_{self.plate_number}")
    qr.make(fit=True)

    # Generate image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to bytes buffer
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Save to Django media files
    filename = f"qr_code_{self.plate_number}.png"
    self.qr_code.save(filename, File(buffer), save=False)
```

### Process Breakdown
1. **QR Code Configuration**
   - Version 1: ~21×21 pixels (auto-expanded if needed)
   - Error Correction Level L: ~7% error recovery
   - Box Size: 10 pixels per module
   - Border: 4 boxes (whitespace around QR)

2. **Data Encoding**
   - Format: `UA_PARKING_{vehicle_id}_{plate_number}`
   - Example: `UA_PARKING_1_TEST2024`

3. **Image Generation**
   - Creates PNG image (black QR code on white background)
   - Uses PIL/Pillow for image processing

4. **File Storage**
   - Saves to `backend/media/qr_codes/`
   - Filename: `qr_code_{plate_number}.png`
   - Uses Django's file storage system

---

## QR Code Regeneration

### Manual Regeneration (via Frontend)
Drivers can regenerate their vehicle's QR code from `driver-vehicle-page.html`:
```javascript
POST /api/vehicles/{vehicle_id}/generate_qr/
```

**Response:**
```json
{
  "message": "QR code generated successfully"
}
```

### Batch Regeneration (Management Command)
Regenerate QR codes for all or specific vehicles via Django management command:

```bash
cd backend

# Regenerate ALL vehicle QR codes
python manage.py regenerate_qr_codes

# Regenerate specific vehicle (by ID)
python manage.py regenerate_qr_codes --vehicle-id=1
```

**Command Details:**
- **Location**: `backend/parking_app/management/commands/regenerate_qr_codes.py`
- **Purpose**: Batch regenerate QR codes (useful after plate changes or system updates)
- **Idempotent**: Safe to run multiple times

**Example Output:**
```
Successfully regenerated QR codes for 3 vehicles
```

---

## QR Code Scanning

### Guard Scanning (Frontend)
Security guards use the QR scanner interface to capture vehicle entry/exit:

**Pages:**
- `guard-scan-qr-page.html` - Primary scanner with camera integration
- `guard-scanqrcode-page.html` - Alternative scanner interface

**Workflow:**
1. Guard opens QR scanner page
2. Selects scan type (Time In / Time Out)
3. Scans vehicle QR code via camera
4. System identifies vehicle and logs scan
5. Confirms with vehicle details

### QR Scan API Endpoint
**Endpoint**: `POST /api/scan-logs/scan_qr/`

**Request Body**:
```json
{
  "qr_data": "UA_PARKING_1_TEST2024",
  "scan_type": "in",
  "notes": "Optional notes"
}
```

**Process:**
1. Parses QR data: `UA_PARKING_{id}_{plate_number}`
2. Extracts `plate_number` and `vehicle_id`
3. Looks up vehicle by plate_number (case-insensitive) - PRIMARY METHOD
4. Fallback to vehicle_id if plate lookup fails
5. Creates `ScanLog` entry
6. Creates or updates `ParkingSession`
7. Returns vehicle and session details

**Response:**
```json
{
  "id": 1,
  "vehicle": {
    "id": 1,
    "plate_number": "TEST2024",
    "brand": "Toyota",
    "model": "Corolla",
    "vehicle_type": "car",
    "owner": "driver1"
  },
  "scan_type": "in",
  "timestamp": "2026-04-19T10:30:00Z",
  "message": "Vehicle scanned successfully"
}
```

### Manual Entry Fallback
If QR scanning fails, guards can manually enter vehicle plate number:

**Endpoint**: `POST /api/scan-logs/manual_entry/`

**Request Body**:
```json
{
  "plate_number": "TEST2024",
  "scan_type": "in",
  "notes": "Manual scan - power outage"
}
```

---

## Frontend QR Code Display

### Driver Vehicle Page
Drivers view their vehicle QR codes on `driver-vehicle-page.html`:

```html
<!-- QR Code Display -->
<img src="${vehicle.qr_code}" alt="QR Code" class="w-40 h-40 border-2 border-gray-300 rounded-lg">

<!-- Regenerate Button -->
<button onclick="regenerateQR(${vehicle.id}, '${vehicle.plate_number}')">
    Regenerate QR
</button>
```

### QR Code Blurring (Payment Status)
- **Unpaid Vehicles**: QR codes are blurred (CSS filter: blur(6px))
- **Paid Vehicles**: QR codes display clearly
- **Purpose**: Visual indicator of payment status

```javascript
${!vehicle.is_paid ? 'blur-sm' : ''}  // Apply blur if not paid
```

### Auto-Regeneration on Load Error
If QR code image fails to load, the frontend automatically triggers regeneration:

```javascript
async function autoRegenerateQR(vehicleId, plateNumber) {
    const response = await fetch(`${API_BASE_URL}/vehicles/${vehicleId}/generate_qr/`);
    // Reload vehicle to get new QR
}
```

---

## Database Schema

### Vehicle Model (QR-Related Fields)
```python
class Vehicle(models.Model):
    # ... other fields ...
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)
    sticker_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
```

### ScanLog Model (Captures QR Scans)
```python
class ScanLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    scan_type = models.CharField(max_length=10)  # 'in' or 'out'
    timestamp = models.DateTimeField(auto_now_add=True)
    entry_point = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
```

### Media Directory Structure
```
backend/media/
└── qr_codes/
    ├── qr_code_TEST2024.png
    ├── qr_code_abc122.png
    └── qr_code_ddd123.png
```

---

## Configuration Requirements

### 1. Media Files Configuration (settings.py)
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 2. URL Routing (urls.py)
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your URLs ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 3. Directory Permissions
Ensure `backend/media/qr_codes/` directory exists and is writable:
```bash
# Create directory if missing
mkdir -p backend/media/qr_codes

# Set permissions (Linux/Mac)
chmod 755 backend/media/qr_codes
```

---

## Troubleshooting

### QR Code Not Generating
**Problem**: "QR code generating..." message persists
**Solutions**:
1. Verify `media/` directory exists: `mkdir -p backend/media/qr_codes`
2. Check Pillow is installed: `pip install Pillow==10.1.0`
3. Check qrcode is installed: `pip install qrcode==7.4.2`
4. Verify Django `MEDIA_URL` and `MEDIA_ROOT` are configured
5. Check file permissions on media directory

### QR Code Image Not Displaying
**Problem**: QR code displays as broken image
**Solutions**:
1. Check URL is correct: `http://localhost:8000/media/qr_codes/qr_code_*.png`
2. Verify backend is serving media files (check DEBUG=True for development)
3. Check browser console for 404 errors
4. Clear browser cache (CTRL+SHIFT+Delete)
5. Regenerate QR code from frontend button

### Scanning Returns Wrong Vehicle
**Problem**: QR scan returns incorrect vehicle
**Solutions**:
1. Regenerate all QR codes: `python manage.py regenerate_qr_codes`
2. Check database for duplicate plate_numbers
3. Verify vehicle lookup is using plate_number (not stale vehicle_id)
4. Check guard is scanning correct vehicle's QR code

### PIL/Pillow Import Error
**Problem**: `ModuleNotFoundError: No module named 'PIL'`
**Solution**:
```bash
# Pillow is the modern PIL package
pip install Pillow==10.1.0
```

### QRCode Version Not Found
**Problem**: `QRCodeException: Some data could not fit into the QR Code`
**Solution**: 
- Increase `version` parameter in `generate_qr_code()` method
- Current: `version=1` (fits most plate numbers)
- For extra-long plate numbers: `version=2` or higher

---

## API Summary

| Endpoint | Method | Purpose | Authentication |
|----------|--------|---------|-----------------|
| `/api/vehicles/{id}/generate_qr/` | POST | Generate/regenerate QR code | Public |
| `/api/scan-logs/scan_qr/` | POST | Scan QR code | Public |
| `/api/scan-logs/manual_entry/` | POST | Manual plate entry | Public |
| `/api/vehicles/` | GET/POST | List/create vehicles | Public |
| `/api/scan-logs/` | GET/POST | List/create scan logs | Public |

---

## Best Practices

### For Drivers
1. Keep QR codes visible and undamaged
2. Register vehicle with clear, accurate plate number
3. Use Regenerate button if QR appears damaged
4. Maintain payment status for visible QR codes

### For Guards
1. Position camera steady when scanning
2. Ensure good lighting on QR code
3. Keep scanner app active while on patrol
4. Use manual entry as fallback only

### For Administrators
1. Periodically regenerate QR codes (quarterly or after migrations)
2. Monitor for scanning failures
3. Keep media directory backed up
4. Archive old QR code images when vehicles are deleted

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-04-19 | Initial QR feature documentation |

---

## Related Documentation
- [BACKEND_DOCUMENTATION.md](BACKEND_DOCUMENTATION.md) - Backend architecture
- [FRONTEND_DOCUMENTATION.md](FRONTEND_DOCUMENTATION.md) - Frontend structure
- [HOW_TO_RUN_GUIDE.md](HOW_TO_RUN_GUIDE.md) - Running the system
- [INSTALLATION_AND_DEPENDENCIES.md](INSTALLATION_AND_DEPENDENCIES.md) - Installation steps
