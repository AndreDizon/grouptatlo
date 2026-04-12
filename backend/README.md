# UA Parking System - Backend (Django + PostgreSQL)

## Project Structure
```
backend/
├── parking_system/          # Main Django project
│   ├── __init__.py
│   ├── settings.py          # Django settings with PostgreSQL config
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI application
│   └── asgi.py              # ASGI application
├── parking_app/             # Main application
│   ├── migrations/
│   ├── __init__.py
│   ├── models.py            # Database models
│   ├── views.py             # API ViewSets
│   ├── serializers.py       # DRF Serializers
│   ├── urls.py              # API routing
│   ├── admin.py             # Django admin configuration
│   └── apps.py
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Installation & Setup

### 1. Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Redis (for Celery, optional)
- Git

### 2. Clone & Navigate
```bash
cd backend
```

### 3. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your configuration
```

### 6. PostgreSQL Setup
```bash
# Create database and user
createdb ua_parking_db
createuser postgres  # if not exists

# Or using psql
psql
CREATE DATABASE ua_parking_db;
CREATE USER ua_admin WITH PASSWORD 'secure_password';
ALTER ROLE ua_admin SET client_encoding TO 'utf8';
ALTER ROLE ua_admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE ua_admin SET default_transaction_deferrable TO on;
ALTER ROLE ua_admin SET timezone TO 'Asia/Manila';
GRANT ALL PRIVILEGES ON DATABASE ua_parking_db TO ua_admin;
\q
```

### 7. Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 8. Create Superuser
```bash
python manage.py createsuperuser
```

### 9. Run Development Server
```bash
python manage.py runserver
```

Access the API at: `http://localhost:8000/api/`
Admin panel at: `http://localhost:8000/admin/`

## API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/refresh/` - Refresh token

### User Management
- `GET /api/profiles/` - List all profiles (Admin only)
- `GET /api/profiles/my_profile/` - Get current user profile
- `PUT /api/profiles/{id}/` - Update profile

### Vehicles
- `GET /api/vehicles/` - List user's vehicles
- `POST /api/vehicles/` - Register new vehicle
- `GET /api/vehicles/{id}/` - Get vehicle details
- `PUT /api/vehicles/{id}/` - Update vehicle
- `POST /api/vehicles/{id}/generate_qr/` - Generate QR code

### Parking Sessions
- `GET /api/parking-sessions/` - List parking sessions
- `POST /api/parking-sessions/check_in/` - Check vehicle in
- `POST /api/parking-sessions/{id}/check_out/` - Check vehicle out
- `GET /api/parking-sessions/active_sessions/` - Active sessions

### Parking Rates
- `GET /api/parking-rates/` - List all pricing

### Scan Logs (Guard)
- `GET /api/scan-logs/` - List scan logs
- `POST /api/scan-logs/scan_qr/` - Log QR scan
- `POST /api/scan-logs/manual_entry/` - Manual plate entry

### Announcements
- `GET /api/announcements/` - List announcements

### Parking Lots
- `GET /api/parking-lots/` - List parking lots

## Database Models

### UserProfile
- UserProfile associated with each User
- Fields: role, phone, address, profile_image, is_verified

### Vehicle
- Vehicle registration with QR code generation
- Fields: vehicle_type, brand, model, plate_number, is_registered, qr_code

### ParkingPass
- Sticker/pass management
- Fields: pass_type, expiry_date, amount_paid, is_active

### ParkingSession
- Track vehicle parking duration
- Fields: time_in, time_out, duration_hours (calculated)

### ScanLog
- Guard scanning records
- Fields: scan_type (in/out), manual_entry, scan_time

### ParkingLot
- Parking lot information
- Fields: total_slots, available_slots, occupancy_rate (calculated)

### ParkingRate
- Pricing configuration
- Fields: vehicle_type, pass_type, price

## Security Considerations

- Use strong `SECRET_KEY` in production
- Set `DEBUG=False` in production
- Use environment variables for sensitive data
- Implement proper authentication (JWT recommended)
- Add rate limiting on API endpoints
- Enable CORS properly
- Use HTTPS in production
- Implement input validation and sanitization

## CORS Configuration

Update `CORS_ALLOWED_ORIGINS` in `.env` to allow frontend domains:
```
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

## Celery Tasks (Optional)

For background tasks:
```bash
# Windows
celery -A parking_system worker -l info

# macOS/Linux
celery -A parking_system worker -l info
```

## Production Deployment

### Using Gunicorn
```bash
gunicorn parking_system.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker
Create a `Dockerfile` and `docker-compose.yml` for containerized deployment.

## Troubleshooting

### PostgreSQL Connection Error
- Verify PostgreSQL is running
- Check database name, user, and password in `.env`
- Ensure `psycopg2-binary` is installed

### QR Code Generation Error
- Install Pillow: `pip install Pillow`
- Ensure `media/` directory exists

### CORS Issues
- Add frontend URL to `CORS_ALLOWED_ORIGINS`
- Check browser console for specific CORS errors

## Contributing

1. Create a new branch for features
2. Follow Django best practices
3. Write tests for new functionality
4. Submit pull requests with descriptions

## License

This project is part of the UA Parking System. All rights reserved.

## Support

For issues or questions, contact the development team.
