# UA Parking System - Installation & Dependencies Guide

## Overview
This guide provides complete instructions for installing all dependencies and setting up the development environment for both the backend (Django REST API) and frontend (HTML/CSS/JS) of the UA Parking System.

## Prerequisites
Before you begin, ensure you have the following installed on your system:

### Required Software
- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/download/win) (for Windows)
- **A Modern Web Browser** - Chrome, Firefox, Safari, or Edge
- **Code Editor** - Visual Studio Code recommended

### Verify Installation
```bash
# Check Python version
python --version

# Check Git version
git git --version

# Check pip (Python package manager)
pip --version
```

## Project Structure
```
dre/
├── backend/                    # Django REST API
│   ├── parking_system/        # Project settings
│   ├── parking_app/           # Main application
│   ├── manage.py
│   ├── requirements.txt
│   └── db.sqlite3
├── frontend/                   # Web application
│   ├── *.html files
│   └── Supporting resources
└── Documentation files
```

---

## Backend Installation

### Step 1: Clone the Repository
```bash
cd /path/to/work/directory
git clone https://github.com/AndreDizon/grouptatlo.git
cd grouptatlo
```

### Step 2: Create Python Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows - PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate virtual environment (Windows - Command Prompt)
.venv\Scripts\activate.bat

# Activate virtual environment (macOS/Linux)
source .venv/bin/activate
```

### Step 3: Install Backend Dependencies
```bash
cd backend

# Install all required packages
pip install -r requirements.txt

# Verify installations
pip list
```

### Backend Dependencies
The project requires the following Python packages (see `requirements.txt`):

| Package | Version | Purpose |
|---------|---------|---------|
| Django | 4.2.11 | Web framework |
| djangorestframework | 3.14.0 | REST API toolkit |
| django-cors-headers | 4.3.1 | CORS support |
| django-filter | 23.5 | API filtering |
| qrcode | 7.4.2 | QR code generation |
| Pillow | 10.1.0 | Image processing |
| psycopg2-binary | 2.9.9 | PostgreSQL adapter (optional for production) |
| python-dotenv | 1.0.0 | Environment variables |
| celery | 5.3.4 | Async task queue |
| redis | 5.0.1 | Caching & message broker |
| gunicorn | 21.2.0 | Production WSGI server |
| whitenoise | 6.6.0 | Static files serving |
| pycryptodome | 3.19.0 | Encryption utilities |

### Step 4: Initialize Database
```bash
cd backend

# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Load initial data (optional)
python manage.py setup_initial_data
```

### Step 5: Verify Backend Setup
```bash
# Test API endpoint
python manage.py runserver

# Should display:
# Starting development server at http://127.0.0.1:8000/
# Quit the server with CTRL-BREAK
```

---

## Frontend Installation

### Frontend Requirements
The frontend is built with vanilla HTML, CSS, and JavaScript. It requires:

1. **Tailwind CSS** - CDN link (no installation needed)
2. **Lucide Icons** - CDN link (no installation needed)
3. **Fetch API** - Native browser support (no installation needed)
4. **LocalStorage** - Native browser support (no installation needed)

### Step 1: No Installation Needed!
The frontend doesn't require `npm` or any package manager. All dependencies are loaded via CDN links in the HTML files.

### Step 2: Verify Frontend Files
```bash
# From workspace root
cd frontend

# List all HTML pages
dir *.html

# You should see:
# - index.html (login page)
# - login.html
# - register.html
# - driver-*.html (driver pages)
# - guard-*.html (guard pages)
# - admin-*.html (admin pages)
# - setup-profile.html
# - loading-page.html
```

### Step 3: Configure API Endpoint (Optional)
If you need to change the backend API endpoint:

1. Open any HTML file in the `frontend/` folder
2. Look for the API URL configuration:
   ```javascript
   const API_BASE_URL = 'http://127.0.0.1:8000/api';
   ```
3. Update to your desired endpoint if needed

---

## Environment Configuration

### Backend Environment Variables (Optional)
Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=sqlite:///db.sqlite3

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Debugging
DEBUG=True

# Secret Key
SECRET_KEY=your-secret-key-here

# API Configuration
API_DOCUMENTATION=http://127.0.0.1:8000/api/
```

---

## Dependency Troubleshooting

### Issue: Permission Denied (Virtual Environment)
**Solution**: Check execution policy on Windows
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: `pip: command not found`
**Solution**: Ensure Python is properly installed and added to PATH
```bash
# Reinstall Python with "Add Python to PATH" option checked
python -m pip install --upgrade pip
```

### Issue: Incompatible Package Versions
**Solution**: Reinstall all dependencies
```bash
pip install --upgrade pip
pip install --force-reinstall -r requirements.txt
```

### Issue: Database Errors
**Solution**: Reset database
```bash
cd backend
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Issue: Port Already in Use
**Solution**: Change the port when running the server
```bash
python manage.py runserver 8001
```

---

## Installation Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Git installed and configured
- [ ] Repository cloned successfully
- [ ] Virtual environment created and activated
- [ ] Backend dependencies installed (`pip list` shows Django 4.2.11+)
- [ ] Database migrated (`db.sqlite3` exists)
- [ ] Superuser account created
- [ ] Frontend HTML files exist in `frontend/` folder
- [ ] No error messages when starting development server

---

## Next Steps

After successful installation, proceed to:
1. **BACKEND_SETUP_GUIDE.md** - Configure backend models and API endpoints
2. **FRONTEND_SETUP_GUIDE.md** - Configure frontend and API integration
3. **HOW_TO_RUN_GUIDE.md** - Start developing

---

## Support & Troubleshooting

For additional help:
- Check [Django Documentation](https://docs.djangoproject.com/)
- Review [Django REST Framework Docs](https://www.django-rest-framework.org/)
- Visit the project README files in each directory

**Last Updated**: April 2026
