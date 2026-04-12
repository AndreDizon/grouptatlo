# UA Parking System - How to Run Backend & Frontend

## Quick Start

### Prerequisites
- Complete the installation steps in **INSTALLATION_AND_DEPENDENCIES.md**
- Backend setup completed (see **BACKEND_SETUP_GUIDE.md**)
- Frontend ready (see **FRONTEND_SETUP_GUIDE.md**)

---

## Running the Backend (Django)

### Step 1: Activate Virtual Environment

**Windows (PowerShell)**:
```powershell
.\.venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**:
```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux**:
```bash
source .venv/bin/activate
```

### Step 2: Navigate to Backend Directory
```bash
cd backend
```

### Step 3: Start Development Server
```bash
python manage.py runserver
```

**Expected Output**:
```
Watching for file changes with StatReloader
Quit the server with CTRL-BREAK.
Starting development server at http://127.0.0.1:8000/
Django version 4.2.11, using settings 'parking_system.settings'
```

### Step 4: Verify Backend is Running
Open your browser and navigate to:
- **API Root**: `http://127.0.0.1:8000/api/`
- **Admin Dashboard**: `http://127.0.0.1:8000/admin/`

### Optional: Run on Different Port
```bash
python manage.py runserver 8001
```

### Optional: Run on All Network Interfaces
```bash
python manage.py runserver 0.0.0.0:8000
```
This allows access from other machines on your network at `http://your-ip-address:8000`

---

## Running the Frontend

### Method 1: Using Live Server Extension (Recommended)

**In Visual Studio Code**:
1. Install "Live Server" extension (by Ritwick Dey)
2. Right-click on `index.html` in the `frontend/` folder
3. Select "Open with Live Server"
4. The frontend will open at `http://127.0.0.1:5500/`

### Method 2: Using Python HTTP Server

**Open a new terminal** (keep backend running in another terminal):

```bash
cd frontend

# Start HTTP server on port 8080
python -m http.server 8080
```

Open your browser to: `http://127.0.0.1:8080/`

### Method 3: Using Node.js HTTP Server

If you have Node.js installed:
```bash
cd frontend

# Install http-server globally (one-time)
npm install -g http-server

# Start server
http-server
```

### Method 4: Using Docker

```bash
docker run -d --name frontend -p 8080:80 -v "$(pwd)/frontend:/usr/share/nginx/html" nginx:latest
```

Access at: `http://127.0.0.1:8080/`

---

## Complete Local Development Setup

### Terminal 1: Backend Server
```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Start Django development server
cd backend
python manage.py runserver
```

### Terminal 2: Frontend Server
```bash
# Option A: Live Server (VSCode extension)
# Right-click index.html → Open with Live Server

# Option B: Python HTTP Server
cd frontend
python -m http.server 8080
```

### Step 3: Access the Application

1. **Frontend Login Page**: `http://127.0.0.1:5500/` (or 8080 if using Python server)
2. **Backend API**: `http://127.0.0.1:8000/api/`
3. **Admin Dashboard**: `http://127.0.0.1:8000/admin/`

---

## Testing Different User Roles

### Admin Login
1. Navigate to login page
2. Create superuser account or use:
   ```bash
   python manage.py createsuperuser
   ```
3. Username: `admin`
4. Password: (as configured)

### Driver Account
1. Register new account
2. Select "Driver" role
3. Login and access driver dashboard

### Guard Account
1. Register new account
2. Select "Guard" role
3. Login and access QR code scanner

---

## API Testing

### Using cURL (Windows PowerShell)
```powershell
# Get all vehicles
curl -s http://127.0.0.1:8000/api/vehicles/ | ConvertFrom-Json

# Get parking sessions
curl -s http://127.0.0.1:8000/api/parking-sessions/ | ConvertFrom-Json

# Get users list
curl -s http://127.0.0.1:8000/api/users/ | ConvertFrom-Json
```

### Using Postman
1. Download [Postman](https://www.postman.com/downloads/)
2. Import API collection or create requests manually
3. Set base URL: `http://127.0.0.1:8000/api`

### Using Python
```python
import requests

# Get vehicles
response = requests.get('http://127.0.0.1:8000/api/vehicles/')
print(response.json())

# Create vehicle
data = {
    'vehicle_type': 'car',
    'brand': 'Toyota',
    'model': 'Corolla',
    'plate_number': 'ABC-1234'
}
response = requests.post('http://127.0.0.1:8000/api/vehicles/', json=data)
print(response.json())
```

---

## Stopping the Servers

### Backend
In the terminal running the backend, press:
```
CTRL + C
```

### Frontend
- **Live Server**: Click "Go Live" again to stop
- **Python HTTP Server**: Press `CTRL + C`

### Deactivate Virtual Environment
```bash
deactivate
```

---

## Troubleshooting

### Backend Won't Start

**Error**: `Address already in use`
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
python manage.py runserver 8001
```

**Error**: `Module not found`
```bash
# Ensure virtual environment is activated
.\.venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

**Error**: `No such table`
```bash
# Run migrations
python manage.py migrate
```

### Frontend Won't Load

**Error**: `CORS Error`
- Ensure backend API URL is correct in HTML files
- Check `CORS_ALLOWED_ORIGINS` in backend `settings.py`

**Error**: `API calls failing`
- Verify backend is running: `http://127.0.0.1:8000/api/`
- Check browser console for errors (F12)
- Verify API endpoint URLs in frontend JavaScript

### Port Already in Use

**Find and kill process**:
```powershell
# Find process using port
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID 5678 /F
```

**Use different port**:
```bash
python manage.py runserver 8001
```

---

## Performance Tips

### Backend Optimization
```bash
# Use faster development server
pip install django-extensions Werkzeug
python manage.py runserver --use-reloader

# Or use threading
python manage.py runserver --nothreading
```

### Frontend Optimization
- Open DevTools (F12)
- Check Network tab for slow assets
- Clear cache: `CTRL + Shift + Delete`

---

## Environment Variables (Production)

Create `.env` file in backend directory:

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:pass@localhost:5432/parking_db
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

Load in `settings.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY')
```

---

## Running Tests

### Backend Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test parking_app

# Run specific test class
python manage.py test parking_app.tests.VehicleTestCase

# Verbose output
python manage.py test --verbosity=2

# With coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Creates htmlcov/index.html
```

### Frontend Tests
Frontend uses vanilla JavaScript - test manually or use:
```bash
# Install testing tools
npm install --save-dev jest @testing-library/dom

# Run tests
npm test
```

---

## Monitoring & Debugging

### Django Debug Toolbar (Optional)
```bash
pip install django-debug-toolbar

# Add to INSTALLED_APPS in settings.py
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

# Add middleware
MIDDLEWARE = [
    # ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Add URL
urlpatterns = [
    # ...
    path('__debug__/', include('debug_toolbar.urls')),
]
```

### View Server Logs
```bash
# Backend logs are displayed in terminal running Django

# Capture logs to file
python manage.py runserver > backend.log 2>&1

# View logs
tail -f backend.log  # macOS/Linux
Get-Content backend.log -Wait  # PowerShell
```

---

## Production Deployment

For production deployment with Gunicorn and Nginx:

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
cd backend
gunicorn parking_system.wsgi:application --bind 0.0.0.0:8000

# With multiple workers
gunicorn parking_system.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

---

## Quick Reference Commands

| Task | Command |
|------|---------|
| Activate virtual env | `.\.venv\Scripts\Activate.ps1` |
| Start backend | `cd backend && python manage.py runserver` |
| Start frontend | `cd frontend && python -m http.server 8080` |
| Create migrations | `python manage.py makemigrations` |
| Run migrations | `python manage.py migrate` |
| Create superuser | `python manage.py createsuperuser` |
| Access admin | `http://127.0.0.1:8000/admin/` |
| Access frontend | `http://127.0.0.1:5500/` or `http://127.0.0.1:8080/` |
| View database | `python manage.py dbshell` |
| Load test data | `python manage.py setup_initial_data` |

---

## Next Steps

- Deploy to production servers
- Configure domain names and SSL certificates
- Set up automated testing and CI/CD pipelines
- Monitor performance and uptime
- Implement backup and recovery procedures

---

**Last Updated**: April 2026
