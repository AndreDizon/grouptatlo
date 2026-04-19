# UA Parking System - How to Run Backend & Frontend

## Quick Start

### Prerequisites
- Complete the installation steps in **[INSTALLATION_AND_DEPENDENCIES.md](INSTALLATION_AND_DEPENDENCIES.md)**
- Python 3.11+ with virtual environment activated
- All dependencies installed from `requirements.txt`
- Node.js optional (for frontend server)

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

### Method 1: Using Python HTTP Server (Recommended)

**Open a new terminal** (keep backend running in another terminal):

```bash
cd frontend

# Start HTTP server on port 3000
python -m http.server 3000
```

Open your browser to: `http://localhost:3000/`

### Method 2: Using Live Server Extension

**In Visual Studio Code**:
1. Install "Live Server" extension (by Ritwick Dey)
2. Right-click on `index.html` in the `frontend/` folder
3. Select "Open with Live Server"
4. The frontend will open at `http://localhost:5500/`

### Method 3: Using Node.js HTTP Server

If you have Node.js installed:
```bash
cd frontend

# Install http-server globally (one-time)
npm install -g http-server

# Start server on port 3000
http-server -p 3000
```

### Method 4: Direct File Access (Offline)

Simply open the `frontend/index.html` file in your browser:
```
File → Open → C:\Users\...\dre\frontend\index.html
```

---

## Complete Local Development Setup

### Terminal 1: Backend Server
```bash
# Activate virtual environment (from project root)
.\.venv\Scripts\Activate.ps1

# Navigate to backend and start Django development server
cd backend
python manage.py runserver
```

### Terminal 2: Frontend Server
```bash
# Navigate to frontend directory (from project root)
cd frontend

# Start Python HTTP server on port 3000
python -m http.server 3000
```

### Step 3: Access the Application

1. **Frontend Login Page**: `http://localhost:3000/`
2. **Backend API**: `http://localhost:8000/api/`
3. **Admin Dashboard**: `http://localhost:8000/admin/`

### Verify Everything Works
- Frontend loads and displays the login page with loading animation
- Backend API responds with vehicle/session/user data
- Login/Register flows work properly
- Each role (Driver/Guard/Admin) accesses their respective dashboards

---

## Testing Different User Roles

## Test Credentials

The system comes pre-configured with test data. Use these credentials to test different roles:

### Admin Panel
```
Username: admin
Password: admin123
URL: http://localhost:8000/admin/
```

### Test User Accounts
| Role | Username | Password | Dashboard |
|------|----------|----------|-----------|
| Driver | driver1 | password123 | Driver Home |
| Driver | driver2 | password123 | Driver Home |
| Guard | guard1 | password123 | Guard Home |
| Guard | guard2 | password123 | Guard Home |

### Test Vehicles
- **TEST2024** - Car, Owner: driver1, registered and paid
- **abc122** - Truck, Owner: driver1, registered and paid
- **ddd123** - Van, Owner: driver2, registered and paid

---

## API Testing

### Using cURL (Windows PowerShell)
```powershell
# Get all vehicles
curl -s http://localhost:8000/api/vehicles/ | ConvertFrom-Json

# Get parking sessions
curl -s http://localhost:8000/api/parking-sessions/ | ConvertFrom-Json

# Get users list
curl -s http://localhost:8000/api/users/ | ConvertFrom-Json
```

### Using Postman
1. Download [Postman](https://www.postman.com/downloads/)
2. Import API collection or create requests manually
3. Set base URL: `http://localhost:8000/api`

### Using Python
```python
import requests

# Get vehicles
response = requests.get('http://localhost:8000/api/vehicles/')
print(response.json())

# Create vehicle
data = {
    'vehicle_type': 'car',
    'brand': 'Toyota',
    'model': 'Corolla',
    'plate_number': 'ABC-1234'
}
response = requests.post('http://localhost:8000/api/vehicles/', json=data)
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
- **Python HTTP Server**: Press `CTRL + C`
- **Live Server**: Click "Go Live" again to stop

### Deactivate Virtual Environment
```bash
deactivate
```

---

## Troubleshooting

### Backend Won't Start

**Error**: `Address already in use`
```bash
# Kill process on port 8000 (Windows PowerShell)
$proc = Get-NetTCPConnection -LocalPort 8000 | Get-Process
Stop-Process -Id $proc.Id -Force

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
cd backend
python manage.py migrate
```

### Frontend Won't Load

**Error**: `CORS Error in browser console`
- Ensure backend API URL is correct in HTML files
- Check `CORS_ALLOWED_ORIGINS` in backend `parking_system/settings.py`
- Backend should be running and accessible at `http://localhost:8000/api/`

**Error**: `API calls failing / 404 responses`
- Verify backend is running: `http://localhost:8000/api/`
- Check browser console for errors (F12 → Console tab)
- Verify API endpoint URLs match in frontend JavaScript
- Ensure you're logged in before accessing protected endpoints

**Error**: `Favicon not loading`
- Verify `logo.png` exists in `frontend/` directory
- Refresh browser cache (CTRL + Shift + Delete)

### Port Already in Use

**Find and kill process** (Windows PowerShell):
```powershell
# Find process using port 8000
Get-NetTCPConnection -LocalPort 8000 | Select-Object -ExpandProperty OwningProcess | Get-Process

# Kill the process (replace PID with actual number)
Stop-Process -Id <PID> -Force
```

**Use different ports**:
```bash
# Backend on different port
python manage.py runserver 8001

# Frontend on different port
python -m http.server 3001
```

### Virtual Environment Issues

**Error**: `'Activate.ps1' cannot be loaded because running scripts is disabled`
```powershell
# Set execution policy for current session only
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Then activate
.\.venv\Scripts\Activate.ps1
```

### Database/Migration Issues

**Reset database to initial state**:
```bash
cd backend

# Delete current database
del db.sqlite3

# Run migrations from scratch
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load test data (if script exists)
python setup_initial_data.py
```

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
