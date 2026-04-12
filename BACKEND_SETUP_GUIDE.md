# UA Parking System - Backend Setup & Configuration Guide

## Overview
This guide provides comprehensive setup and configuration instructions for the Django REST Framework backend of the UA Parking System.

## Prerequisites
Before proceeding, ensure you have completed:
- ✅ Python 3.8+ installed
- ✅ Virtual environment activated
- ✅ Dependencies installed from `requirements.txt`
- ✅ Database migrations run

For installation steps, see **INSTALLATION_AND_DEPENDENCIES.md**

---

## Backend Architecture

### Project Structure
```
backend/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── db.sqlite3                  # SQLite database
├── README.md                   # Backend README
│
├── parking_system/             # Main project settings
│   ├── __init__.py
│   ├── settings.py            # Django configuration
│   ├── urls.py                # Global URL routing
│   ├── wsgi.py                # WSGI configuration (production)
│   └── asgi.py                # ASGI configuration (async)
│
├── parking_app/               # Main Django application
│   ├── __init__.py
│   ├── models.py              # Database models (User, Vehicle, ParkingSession, etc.)
│   ├── views.py               # API views and endpoints
│   ├── serializers.py         # Data serialization
│   ├── urls.py                # App URL routing
│   ├── admin.py               # Django admin configuration
│   ├── apps.py                # App configuration
│   │
│   └── migrations/            # Database schema migrations
│       ├── __init__.py
│       ├── 0001_initial.py
│       ├── 0002_parkingsession_parking_lot.py
│       ├── 0003_alter_parkingpass_pass_type_and_more.py
│       ├── 0004_vehicle_is_paid.py
│       ├── 0005_migrate_userprofile_to_user.py
│       ├── 0006_delete_userprofile.py
│       └── 0007_remove_parking_rate_vehicle_type_choices.py
│
└── media/                     # Generated files
    └── qr_codes/              # QR code storage
```

---

## Core Data Models

### 1. User Model (Django Built-in Extended)
**Purpose**: Authentication and authorization

**Role Types**:
- `admin` - Administrator privileges
- `driver` - Driver privileges
- `guard` - Guard/attendant privileges

**Key Methods**:
```python
user.is_admin          # Check if admin
user.is_driver         # Check if driver
user.is_guard          # Check if guard
user.get_vehicles()    # Get user vehicles
user.get_parking_sessions()  # Get parking history
```

### 2. Vehicle Model
**Purpose**: Manage vehicle registration and tracking

**Fields**:
```
- owner (ForeignKey to User)
- vehicle_type (choices: car, motorcycle, truck, etc.)
- brand (e.g., "Toyota")
- model (e.g., "Corolla")
- plate_number (unique)
- color
- registration_date
- is_registered (boolean)
- is_paid (boolean)
- qr_code (unique, auto-generated)
- sticker_number
```

**Key Features**:
- Automatic QR code generation on creation
- Unique plate number constraint
- Valid status tracking

**API Endpoints**:
```
GET    /api/vehicles/              # List all vehicles
GET    /api/vehicles/<id>/         # Get vehicle details
POST   /api/vehicles/              # Create vehicle
PUT    /api/vehicles/<id>/         # Update vehicle
DELETE /api/vehicles/<id>/         # Delete vehicle
```

### 3. ParkingSession Model
**Purpose**: Track parking events and duration

**Fields**:
```
- vehicle (ForeignKey to Vehicle)
- time_in (datetime)
- time_out (datetime, nullable)
- entry_point (string)
- exit_point (string, nullable)
- notes (text, optional)
- session_date (date)
```

**Key Features**:
- Automatic duration calculation
- Entry/exit point tracking
- Session status management

**API Endpoints**:
```
GET    /api/parking-sessions/              # List all sessions
GET    /api/parking-sessions/<id>/         # Get session details
POST   /api/parking-sessions/              # Create session
PUT    /api/parking-sessions/<id>/         # Update session
DELETE /api/parking-sessions/<id>/         # Delete session
```

### 4. ParkingRate Model
**Purpose**: Define parking rates and pricing

**Fields**:
```
- vehicle_type (choices: car, motorcycle, truck, etc.)
- hourly_rate (decimal)
- daily_rate (decimal)
- monthly_rate (decimal)
- is_active (boolean)
```

**API Endpoints**:
```
GET    /api/parking-rates/              # List all rates
GET    /api/parking-rates/<id>/         # Get rate details
POST   /api/parking-rates/              # Create rate
PUT    /api/parking-rates/<id>/         # Update rate
```

### 5. ParkingLot Model
**Purpose**: Define parking lot locations and capacity

**Fields**:
```
- name (string)
- location (string)
- capacity (integer)
- available_spots (integer)
- is_active (boolean)
```

---

## API Endpoints Overview

### Authentication Endpoints
```
POST   /api/users/login/              # User login
POST   /api/users/register/           # User registration
POST   /api/users/logout/             # User logout
GET    /api/users/profile/            # Get current user profile
PUT    /api/users/profile/            # Update user profile
```

### Vehicle Management
```
GET    /api/vehicles/                 # List vehicles
POST   /api/vehicles/                 # Create vehicle
GET    /api/vehicles/<id>/            # Get vehicle details
PUT    /api/vehicles/<id>/            # Update vehicle
DELETE /api/vehicles/<id>/            # Delete vehicle
GET    /api/vehicles/<id>/qr-code/    # Get QR code
```

### Parking Operations
```
GET    /api/parking-sessions/         # List sessions
POST   /api/parking-sessions/         # Create session
GET    /api/parking-sessions/<id>/    # Get session details
PUT    /api/parking-sessions/<id>/    # Update session
GET    /api/parking-statistics/       # Get parking stats
```

### Admin Operations
```
GET    /api/admin/users/              # List all users
GET    /api/admin/reports/            # Generate reports
GET    /api/admin/analytics/          # View analytics
PUT    /api/admin/settings/           # Update settings
```

---

## Configuration Files

### settings.py
Key configurations to review/modify:

```python
# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'parking_app',
]

# Database (SQLite for development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

# CORS Configuration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### urls.py
Main URL configuration:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('parking_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### App urls.py
Application-specific URL routing - defined in `parking_app/urls.py`

---

## Database Management

### Run Migrations
```bash
# Apply all pending migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Create new migration after model changes
python manage.py makemigrations

# Specific app migration
python manage.py migrate parking_app
```

### Create Superuser
```bash
python manage.py createsuperuser

# Interactive prompts will appear:
# Username: admin
# Email: admin@example.com
# Password: ••••••••
# Password (again): ••••••••
```

### Django Admin Access
1. Start server: `python manage.py runserver`
2. Navigate to: `http://127.0.0.1:8000/admin/`
3. Login with superuser credentials
4. Manage all models from the admin panel

### Backup Database
```bash
# Copy the database file
cp backend/db.sqlite3 backend/db.sqlite3.backup
```

### Reset Database
```bash
# WARNING: This deletes all data!
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## QR Code Generation

### Automatic QR Code Generation
QR codes are automatically generated when a vehicle is created.

**Configuration** (in `parking_app/models.py`):
```python
def generate_qr_code(self):
    """Auto-generates QR code for vehicles"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"Vehicle-{self.plate_number}")
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    # Save to media/qr_codes/
```

### Accessing QR Codes
- **Location**: `media/qr_codes/` directory
- **API Endpoint**: `GET /api/vehicles/<id>/qr-code/`
- **Format**: PNG image

---

## Debugging & Development

### Enable Debug Mode
In `settings.py`:
```python
DEBUG = True
ALLOWED_HOSTS = ['*']  # Development only!
```

### Display Database Queries
```python
# In Django shell
python manage.py shell

>>> from django.db import connection
>>> from django.test.utils import CaptureQueriesContext
>>> 
>>> with CaptureQueriesContext(connection) as queries:
...     # Your code here
...     pass
>>> 
>>> for query in queries:
...     print(query['sql'])
```

### Common Django Commands
```bash
# Start development server
python manage.py runserver

# Create new app
python manage.py startapp app_name

# Run shell with Django context
python manage.py shell

# Load test data
python manage.py setup_initial_data

# Create cache table
python manage.py createcachetable

# Check project for issues
python manage.py check
```

---

## Performance Optimization

### Enable Caching
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

### Database Query Optimization
```python
# Use select_related for ForeignKey
vehicles = Vehicle.objects.select_related('owner')

# Use prefetch_related for reverse relations
users = User.objects.prefetch_related('vehicles')

# Use only() to select specific fields
vehicles = Vehicle.objects.only('plate_number', 'vehicle_type')
```

### Static Files
```bash
# Collect static files (production)
python manage.py collectstatic --noinput
```

---

## Troubleshooting

### Issue: Database Migration Errors
```bash
# Check for unmigrated changes
python manage.py makemigrations --check

# Apply pending migrations
python manage.py migrate
```

### Issue: Port 8000 Already in Use
```bash
# Use different port
python manage.py runserver 8001
```

### Issue: CORS Errors
Update `CORS_ALLOWED_ORIGINS` in `settings.py` to include your frontend URL.

### Issue: Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic
```

---

## Security Considerations

### Production Deployment Checklist
- [ ] Set `DEBUG = False` in settings.py
- [ ] Update `SECRET_KEY` with strong random value
- [ ] Limit `ALLOWED_HOSTS` to your domain(s)
- [ ] Use HTTPS in production
- [ ] Configure proper CORS settings
- [ ] Use environment variables for sensitive data
- [ ] Set up proper database (PostgreSQL recommended)
- [ ] Enable CSRF protection
- [ ] Use secure cookies settings

---

## Next Steps

1. Review **FRONTEND_SETUP_GUIDE.md** for frontend configuration
2. See **HOW_TO_RUN_GUIDE.md** for running the complete stack
3. Check [Django Documentation](https://docs.djangoproject.com/)

---

**Last Updated**: April 2026
