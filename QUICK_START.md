# Quick Start Guide - UA Parking System Backend

## 🚀 Backend is NOW RUNNING!

### Access Points
| Service | URL |
|---------|-----|
| **API** | http://localhost:8000/api/ |
| **Admin Panel** | http://localhost:8000/admin/ |
| **Development** | http://localhost:8000/ |

---

## 📝 Test Credentials

### Admin Panel
```
Username: admin
Password: admin123
```

### Test Users (API)
| Role | Username | Password |
|------|----------|----------|
| Driver | driver1 | password123 |
| Driver | driver2 | password123 |
| Guard | guard1 | password123 |
| Guard | guard2 | password123 |

---

## 🔌 Connect Your Frontend

### Update CORS Settings
In `backend/parking_system/settings.py`, CORS is already configured for:
- http://localhost:3000 (React default)
- http://localhost:8000
- http://127.0.0.1:3000
- http://127.0.0.1:8000

### Connect to API from Frontend

```javascript
// Example: Login API call
fetch('http://localhost:8000/api-token-auth/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'driver1',
    password: 'password123'
  })
})
.then(response => response.json())
.then(data => console.log('Token:', data.token))
```

---

## 📊 Sample API Responses

### Get Parking Rates
```
GET http://localhost:8000/api/parking-rates/

Response:
{
  "count": 8,
  "results": [
    {
      "id": 1,
      "vehicle_type": "car",
      "pass_type": "daily",
      "price": "250.00",
      "is_active": true
    },
    ...
  ]
}
```

### Get Parking Lots
```
GET http://localhost:8000/api/parking-lots/

Response:
{
  "count": 4,
  "results": [
    {
      "id": 1,
      "name": "Main Campus Lot A",
      "location": "Building 1",
      "total_slots": 100,
      "available_slots": 100,
      "occupancy_rate": 0.0
    },
    ...
  ]
}
```

---

## 🗄️ Database Models

### UserProfile
- User account extended with roles
- Fields: role, phone, address, profile_image, is_verified

### Vehicle  
- Vehicle registration
- Fields: vehicle_type, brand, model, plate_number, is_registered, qr_code

### ParkingPass
- Sticker/pass management
- Fields: pass_type, expiry_date, amount_paid, is_active

### ParkingSession
- Track parking duration
- Fields: time_in, time_out, duration_hours (calculated)

### ScanLog
- Guard scanning records
- Fields: scan_type, manual_entry, scan_time

---

## 🛠️ Manage Running Server

### Stop Server
In the terminal running the server: `CTRL + BREAK` or `CTRL + C`

### Restart Server
```bash
cd backend
venv\Scripts\activate
python manage.py runserver 0.0.0.0:8000
```

### Check Logs
Server logs are displayed in the terminal window

---

## 🔐 Admin Panel Features

Login at: http://localhost:8000/admin/

**Available Models to Manage:**
- User Profiles
- Vehicles
- Parking Passes
- Parking Sessions
- Parking Lots
- Parking Rates
- Announcements
- Scan Logs

---

## 📱 Frontend Integration Tips

### CORS Headers
Backend automatically includes in responses:
- `Access-Control-Allow-Origin: *` (configured origins)
- `Access-Control-Allow-Credentials: true`
- `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`

### Authentication
Token-based authentication is configured. Use:
```
Authorization: Bearer YOUR_TOKEN
```

### Common API Errors
| Status | Issue | Solution |
|--------|-------|----------|
| 401 | Not authenticated | Login and include token in headers |
| 403 | Permission denied | User role doesn't have access |
| 404 | Not found | Check resource ID or URL |
| 400 | Bad request | Validate request data |

---

## 🚨 Troubleshooting

### Port 8000 Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID PID_HERE /F

# Or use different port
python manage.py runserver 0.0.0.0:8001
```

### Database Errors
```bash
# Reset database
python manage.py migrate --run-syncdb

# Recreate admin user
python manage.py createsuperuser
```

### Module Not Found Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt

# Or install specific package
pip install django-rest-framework
```

---

## 📚 Next Steps

1. ✅ Backend server is running
2. ⏭️ Start your frontend development server
3. ⏭️ Update frontend API base URL to `http://localhost:8000/api/`
4. ⏭️ Test API endpoints with sample credentials
5. ⏭️ Implement authentication flow in frontend
6. ⏭️ Build pages for each role (Driver, Guard, Admin)
7. ⏭️ Deploy to production when ready

---

## 🎯 Key Endpoints for Frontend

### Public Endpoints (No Auth Required)
- `GET /api/parking-rates/` - Get all parking prices
- `GET /api/parking-lots/` - Get parking lot information
- `GET /api/announcements/` - Get system announcements

### Driver Endpoints
- `GET /api/vehicles/` - List my vehicles
- `POST /api/vehicles/` - Register new vehicle
- `POST /api/parking-sessions/check_in/` - Check in
- `POST /api/parking-sessions/{id}/check_out/` - Check out

### Guard Endpoints
- `POST /api/scan-logs/scan_qr/` - Scan QR code
- `POST /api/scan-logs/manual_entry/` - Manual plate entry
- `GET /api/parking-sessions/active_sessions/` - View active sessions

### Admin Endpoints
- `GET /api/profiles/` - List all user profiles
- `GET /api/parking-sessions/` - View all sessions
- `GET /api/scan-logs/` - View all scan logs

---

**Happy coding! 🎉**