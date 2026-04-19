# UA Parking System - Backend Documentation

## Overview
The UA Parking System is a Django REST Framework-based backend application that manages vehicle parking operations, QR code scanning, vehicle registration, and parking rate configurations for the University of the Assumption.

## Technology Stack
- **Framework**: Django 4.2.11
- **API**: Django REST Framework 3.14.0
- **Database**: SQLite (development) | PostgreSQL (production-ready)
- **Authentication**: Django User Model with role-based access
- **QR Code Generation**: qrcode 7.4.2 with Pillow 10.1.0
- **Async Tasks**: Celery 5.3.4 with Redis 5.0.1
- **Encryption**: pycryptodome 3.19.0

## Project Structure
```
backend/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── parking_system/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── parking_app/             # Main application
│   ├── models.py           # Database models
│   ├── views.py            # API endpoints
│   ├── serializers.py      # Data serialization
│   ├── urls.py             # URL routing
│   ├── admin.py            # Django admin config
│   └── migrations/         # Database migrations
└── media/
    └── qr_codes/           # Generated QR codes storage
```

## Core Models

### User (Django Built-in)
Extended user model with role assignment (admin, driver, guard)

### Vehicle
- **Fields**: owner, vehicle_type, brand, model, plate_number, color, registration_date, is_registered, is_paid, qr_code, sticker_number
- **Purpose**: Vehicle registration and tracking
- **Constraints**: plate_number is unique, vehicle_type is restricted to predefined choices

### ParkingSession
- **Fields**: vehicle, time_in, time_out, entry_point, exit_point, notes, session_date
- **Purpose**: Track vehicle parking duration and location
- **Features**: 
  - Records entry and exit times
  - Calculates parking duration
  - Links to vehicle

### ScanLog
- **Fields**: vehicle, scan_type, timestamp, entry_point, guard_id
- **Purpose**: Log QR code scanning events by security guards
- **Features**:
  - Records scan entries and exits
  - Associates guard performing the scan
  - Tracks scan location

### ParkingRate
- **Fields**: vehicle_type, pass_type, price, description, is_active
- **Purpose**: Configure parking pricing tiers
- **Features**:
  - Flexible vehicle type (any string value)
  - Pass types: Drop-Off, Park
  - Supports multiple pricing combinations
  - Unique constraint on vehicle_type + pass_type combination

### Announcement
- **Fields**: title, content, created_by, created_at
- **Purpose**: System announcements and notifications

## API Endpoints

### ParkingSession Endpoints
- `GET /api/parking-sessions/` - List all parking sessions
- `POST /api/parking-sessions/` - Create new parking session
- `GET /api/parking-sessions/{id}/` - Get session details
- `PUT/PATCH /api/parking-sessions/{id}/` - Update session
- `DELETE /api/parking-sessions/{id}/` - Delete session
- `GET /api/parking-sessions/today_sessions/?user_id={userId}` - Get today's sessions for a user

### ScanLog Endpoints
- `GET /api/scan-logs/` - List all scan logs
- `POST /api/scan-logs/` - Create scan log
- `GET /api/scan-logs/{id}/` - Get scan details
- `POST /api/scan-logs/scan_qr/` - QR code scanning endpoint
- `POST /api/scan-logs/manual_entry/` - Manual vehicle entry
- `GET /api/scan-logs/guard_statistics/?guard_id={guardId}&filter={day|week|month|year}` - Guard scan statistics
- `GET /api/scan-logs/debug_all_scans/` - Debug endpoint showing all scans

### ParkingRate Endpoints
- `GET /api/parking-rates/` - List all pricing tiers
- `POST /api/parking-rates/` - Create new pricing tier
- `GET /api/parking-rates/{id}/` - Get rate details
- `PUT/PATCH /api/parking-rates/{id}/` - Update rate
- `DELETE /api/parking-rates/{id}/` - Delete rate

### Vehicle Endpoints
- `GET /api/vehicles/` - List all vehicles
- `POST /api/vehicles/` - Register new vehicle
- `GET /api/vehicles/{id}/` - Get vehicle details
- `PUT/PATCH /api/vehicles/{id}/` - Update vehicle
- `DELETE /api/vehicles/{id}/` - Delete vehicle

### User Endpoints
- `GET /api/users/` - List all users
- `POST /api/users/` - Create new user
- `GET /api/users/{id}/` - Get user details

## Key Features

### QR Code Management
- Automatic QR code generation during vehicle registration
- QR codes stored in `media/qr_codes/` directory
- Each QR code encodes the vehicle ID for scanning

### Parking Session Tracking
- Records vehicle entry and exit times
- Tracks parking duration
- Supports multiple sessions per vehicle per day
- Filters for today's sessions by user ID

### Guard Statistics
- Tracks total vehicles scanned by each guard
- Counts time_in and time_out entries separately
- Counts manual entries
- Supports time-based filtering (day, week, month, year)
- Records which guard performed each scan

### Flexible Pricing
- Create pricing tiers for any vehicle type + pass type combination
- Prevent duplicate pricing tier creation with error message
- Support for flexible vehicle type input (not limited to predefined list)

### Permission System
- Uses `AllowAny` permissions for open access
- Requires explicit ID passing from frontend (no user authentication required)

## Database Setup

### Initial Setup
```bash
# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Load initial data (if exists)
python manage.py setup_initial_data
```

### Migrations Applied
- `0001_initial.py` - Initial model creation
- `0002_parkingsession_parking_lot.py` - Parking lot field addition
- `0003_alter_parkingpass_pass_type_and_more.py` - Pass type modifications
- `0004_vehicle_is_paid.py` - Payment status field
- `0005_migrate_userprofile_to_user.py` - User profile migration
- `0006_delete_userprofile.py` - Cleanup
- `0007_remove_parking_rate_vehicle_type_choices.py` - Remove vehicle type constraints

## Running the Server

### Development Server
```bash
python manage.py runserver 8000
```

### Production Server
```bash
# Use gunicorn
gunicorn parking_system.wsgi:application --bind 0.0.0.0:8000
```

## Environment Configuration
- **DEBUG**: True (development) / False (production)
- **SECRET_KEY**: Configure in settings.py
- **ALLOWED_HOSTS**: Configure for production deployment
- **DATABASE**: SQLite for development, PostgreSQL recommended for production

## Common Tasks

### Create Pricing Tier
```
POST /api/parking-rates/
{
  "vehicle_type": "car",
  "pass_type": "park",
  "price": "100.00",
  "description": "Standard car parking",
  "is_active": true
}
```

### Record Vehicle Scan
```
POST /api/scan-logs/scan_qr/
{
  "vehicle_id": 1,
  "guard_id": 5,
  "scan_type": "in",
  "entry_point": "Main Gate"
}
```

### Get Today's Sessions for User
```
GET /api/parking-sessions/today_sessions/?user_id=1
```

### Get Guard Statistics
```
GET /api/scan-logs/guard_statistics/?guard_id=5&filter=day
```

## Troubleshooting

### QR Code Issues
- Ensure `media/` directory exists and is writable
- Check PIL/Pillow is installed correctly
- Verify vehicle registration creates QR code

### Scanning Not Recording Guard ID
- Ensure frontend sends `guard_id` in request body
- Check guard_id exists in database
- Verify ScanLog model accepts guard_id field

### Duplicate Pricing Tier Error
- Clear message returned if vehicle_type + pass_type already exists
- Use PATCH to edit existing tier instead
- Database constraint prevents duplicates

## Dependencies
See `requirements.txt` for complete package list. Key dependencies:
- Django
- djangorestframework
- qrcode
- pillow
- django-cors-headers (for CORS support)

## Notes
- All endpoints return JSON responses
- Timestamps are timezone-aware (UTC)
- Error responses include descriptive messages
- Database uses CASCADE deletion for related objects
