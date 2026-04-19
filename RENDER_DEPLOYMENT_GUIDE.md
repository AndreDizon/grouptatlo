# UA Parking System - Render Backend Deployment Guide

## Overview
This guide prepares the Django backend for deployment on Render.com, a modern cloud platform for running apps and databases.

---

## Prerequisites
- Active Render.com account (free or paid tier)
- GitHub repository pushed with all code
- PostgreSQL database (Render provides this)
- Environment variables configured

---

## Step 1: Prepare Backend for Production

### 1.1 Create `.env.production` File
Create `backend/.env.production` file with production settings:

```env
# Django Settings
DEBUG=False
SECRET_KEY=your-very-secure-secret-key-change-this-in-render-dashboard
ALLOWED_HOSTS=your-app-name.onrender.com,localhost

# Database (Render will provide connection string)
DATABASE_URL=postgresql://user:password@host:port/dbname

# CORS Settings
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.vercel.app,https://your-app-name.onrender.com

# Static Files
STATIC_URL=/static/
STATIC_ROOT=/var/data/static
MEDIA_URL=/media/
MEDIA_ROOT=/var/data/media

# Email (Optional - for notifications)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 1.2 Update `settings.py` for Production

**Location**: `backend/parking_system/settings.py`

Add the following at the end of the file:

```python
# ============ PRODUCTION SETTINGS ============
import os
from pathlib import Path

# Read from .env.production if it exists
if os.path.exists(os.path.join(BASE_DIR, '.env.production')):
    from dotenv import load_dotenv
    load_dotenv(os.path.join(BASE_DIR, '.env.production'))

# Security
DEBUG = os.getenv('DEBUG', 'False') == 'True'
SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database - Priority: DATABASE_URL (Render) → SQLite (local)
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# CORS
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security Headers (Production)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

### 1.3 Create `render.yaml` (Build Configuration)

Create `render.yaml` in project root:

```yaml
services:
  - type: web
    name: ua-parking-backend
    env: python
    plan: free
    region: oregon
    
    buildCommand: |
      pip install -r backend/requirements.txt
      cd backend
      python manage.py migrate
      python manage.py collectstatic --noinput
    
    startCommand: |
      gunicorn parking_system.wsgi:application --bind 0.0.0.0:$PORT
    
    envVars:
      - key: DEBUG
        value: "False"
      - key: PYTHON_VERSION
        value: "3.11"
      - key: DATABASE_URL
        fromService:
          type: pgsql
          name: ua-parking-db
          envVarName: DATABASE_URL

  - type: pgsql
    name: ua-parking-db
    plan: free
    region: oregon
```

### 1.4 Install Production Dependencies

Add to `backend/requirements.txt`:

```
dj-database-url==1.3.0
psycopg2-binary==2.9.9
gunicorn==21.2.0
whitenoise==6.6.0
python-dotenv==1.0.0
```

### 1.5 Create `Procfile`

Create `Procfile` in backend directory:

```
web: gunicorn parking_system.wsgi:application --bind 0.0.0.0:$PORT --workers 3
release: python manage.py migrate
```

---

## Step 2: Deploy to Render

### 2.1 Connect GitHub Repository
1. Go to [render.com](https://render.com)
2. Login/Sign up
3. Click "New +" → "Web Service"
4. Select "Deploy an existing project from a Git repository"
5. Connect your GitHub account
6. Select `grouptatlo` repository

### 2.2 Configure Deployment Settings

| Setting | Value |
|---------|-------|
| **Name** | `ua-parking-backend` |
| **Environment** | Python 3 |
| **Region** | Oregon or closest to you |
| **Branch** | main |
| **Build Command** | `pip install -r backend/requirements.txt && cd backend && python manage.py migrate && python manage.py collectstatic --noinput` |
| **Start Command** | `cd backend && gunicorn parking_system.wsgi:application --bind 0.0.0.0:$PORT` |
| **Plan** | Free or Starter (0.5 CPU, 512MB RAM) |

### 2.3 Add Environment Variables

In Render dashboard → Environment:

```
DEBUG=False
SECRET_KEY=your-random-secret-key-here-min-50-chars
ALLOWED_HOSTS=ua-parking-backend.onrender.com,localhost
DATABASE_URL=postgresql://user:password@host:5432/dbname
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://ua-parking-backend.onrender.com
```

### 2.4 Add PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. Name: `ua-parking-db`
3. Region: Same as backend
4. Plan: Free tier
5. Copy connection string to `DATABASE_URL` in environment variables

### 2.5 Deploy

1. Click "Create Web Service"
2. Render will build and deploy automatically
3. Monitor build logs for errors
4. Once deployed, get the URL: `https://ua-parking-backend.onrender.com`

---

## Step 3: Post-Deployment Setup

### 3.1 Run Initial Migrations

Connect to Render and run:
```bash
python manage.py migrate
python manage.py createsuperuser
```

Or use Render Shell in dashboard:
- Go to your Web Service
- Click "Shell" tab
- Run migration commands

### 3.2 Verify API Endpoints

```bash
# Test API
curl https://ua-parking-backend.onrender.com/api/

# Test Admin
https://ua-parking-backend.onrender.com/admin/
```

### 3.3 Upload Static Files (If Not Auto-Collected)

```bash
python manage.py collectstatic --noinput
```

---

## Step 4: Frontend Configuration

### Update Frontend API Base URL

In `frontend/*.html` files, update:

```javascript
const API_BASE_URL = 'https://ua-parking-backend.onrender.com/api';
```

Or create a config file and import it in all pages.

---

## Common Issues & Solutions

### Issue: `ModuleNotFoundError: No module named 'parking_system'`
**Solution**: Ensure `cd backend` before running gunicorn in start command

### Issue: Database connection failed
**Solution**: 
- Verify `DATABASE_URL` is correct
- Check PostgreSQL is up and running
- Test connection string locally first

### Issue: Static files not loading (404 errors)
**Solution**:
- Run `python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` and `STATIC_URL` in settings.py
- Enable WhiteNoise middleware

### Issue: CORS errors on frontend
**Solution**:
- Add frontend URL to `CORS_ALLOWED_ORIGINS`
- Include protocol: `https://`
- Restart service after updating env vars

### Issue: Secret key error
**Solution**: Generate secure key:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## Performance Optimization for Render

### Free Tier Limitations
- 0.5 CPU, 512MB RAM
- Spins down after 15 min inactivity
- Best for: Development, staging

### Upgrade to Starter+ for Production
- 0.5-4 CPU cores
- 1-8GB RAM
- Always-on service
- Performance: $12/month

### Database Optimization
- Use indexes on frequently queried fields (plate_number, vehicle_id)
- Archive old scan logs monthly
- Regular backups enabled by default

### API Caching
- Add Redis instance for caching
- Cache guard statistics (updates every hour)
- Cache parking rates (static data)

---

## Monitoring & Maintenance

### Check Backend Health
```bash
curl https://ua-parking-backend.onrender.com/api/
```

### View Logs
- Render Dashboard → Logs tab
- Real-time monitoring of all requests
- Error tracking and debugging

### Update & Redeployment
1. Push changes to GitHub `main` branch
2. Render auto-deploys (can be disabled)
3. Monitor deployment status in dashboard
4. Check logs for errors

### Database Backups
- Automatic daily backups in Render
- Download backups from dashboard
- Restore to new instance if needed

---

## Next Steps

1. ✅ Prepare backend code (done)
2. ⏳ Deploy to Render (in progress)
3. ⏳ Deploy frontend to Vercel (separate guide)
4. ⏳ Connect frontend to backend API
5. ⏳ Test all features in production
6. ⏳ Monitor and optimize performance

---

## Useful Links

- Render Docs: https://render.com/docs
- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
- PostgreSQL: https://www.postgresql.org/docs/
- Gunicorn: https://gunicorn.org/
