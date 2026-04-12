# 🚀 UA Parking System - Complete Startup Guide

## ✅ System is Ready!

Your UA Parking System has been fully set up with:
- ✅ **Frontend** - 12 HTML dashboard pages + Loading & Login
- ✅ **Backend** - Django REST API running on port 8000
- ✅ **Database** - SQLite (development), ready for PostgreSQL
- ✅ **Authentication** - Login with test credentials
- ✅ **Complete Flow** - Loading → Login → Dashboard

---

## 🎯 Quick Start (30 seconds)

### Option 1: Using GUI (Easiest)
```
1. Navigate to: C:\Users\Christine Dizon\OneDrive\Desktop\dre\frontend\
2. Double-click: index.html
3. Wait for loading animation (watch the car!)
4. Login with: driver1 / password123
5. Explore dashboard!
```

### Option 2: Browser File Open
```
1. Open browser (Chrome, Firefox, Edge, Safari)
2. Press: Ctrl+O (or Cmd+O on Mac)
3. Navigate to: C:\Users\Christine Dizon\OneDrive\Desktop\dre\frontend\index.html
4. Click Open
5. Watch the loading animation!
```

### Option 3: Using HTTP Server (Recommended)
```bash
# Open Terminal/PowerShell
cd "C:\Users\Christine Dizon\OneDrive\Desktop\dre\frontend"

# Start Python HTTP server
python -m http.server 3000

# Open browser to:
http://localhost:3000/

# Ctrl+C to stop server
```

---

## 📱 System Flow

```
ENTRY POINT
    ↓
    index.html
    (Blank page that redirects)
    ↓
    loading-page.html
    (Car animation for 2-4 seconds)
    ↓
AUTOMATIC REDIRECT WHEN ANIMATION COMPLETES
    ↓
    login.html
    (Enter username & password)
    ↓
AFTER SUCCESSFUL LOGIN
    ↓
    Your Role's Dashboard
    ├─ admin → admin-home-page.html
    ├─ driver → driver-home-page.html
    └─ guard → guard-home-page.html
```

---

## 🔑 Test Credentials (Use These to Login)

Pick ONE and use the exact username/password:

### 👨‍💼 Admin Account
```
Username: admin
Password: admin123
```
Redirects to: **Admin Dashboard** with all admin features

### 👤 Driver Account 1
```
Username: driver1
Password: password123
```
Redirects to: **Driver Dashboard** (vehicle & parking)

### 👤 Driver Account 2
```
Username: driver2
Password: password123
```
Same dashboard as driver1

### 👮 Guard Account 1
```
Username: guard1
Password: password123
```
Redirects to: **Guard Dashboard** (QR scanning)

### 👮 Guard Account 2
```
Username: guard2
Password: password123
```
Same dashboard as guard1

---

## 📊 Dashboard Features by Role

### Admin Dashboard
- Statistics (campus wide)
- Vehicle management
- Account management
- General contact/info

### Driver Dashboard
- Welcome/home page
- My vehicles (register & manage)
- Parking statistics & history
- Profile settings
- Contact/info

### Guard Dashboard
- Statistics (guard specific)
- QR code scanning
- Vehicle logs
- Profile settings
- Contact/info

---

## 🔌 Backend API (Optional but Recommended)

### Backend is Already Running!
The Django backend is running on: **http://localhost:8000/**

### Admin Panel (Manage Database)
- URL: http://localhost:8000/admin/
- Username: admin
- Password: admin123

### API Endpoints
- **Parking Rates**: http://localhost:8000/api/parking-rates/
- **Parking Lots**: http://localhost:8000/api/parking-lots/
- **Other endpoints**: http://localhost:8000/api/

---

## 🗂️ File Structure

```
dre/
├── frontend/
│   ├── index.html ⭐ START HERE
│   ├── loading-page.html (auto loads)
│   ├── login.html (auto loads after animation)
│   ├── register.html
│   ├── setup-profile.html
│   │
│   ├── admin-home-page.html
│   ├── admin-statistics-page.html
│   ├── admin-vehicle-page.html
│   ├── admin-manageaccounts-page.html
│   ├── admin-profile-page.html
│   ├── admin-contact&information-page.html
│   │
│   ├── driver-home-page.html
│   ├── driver-vehicle-page.html
│   ├── driver-parking-page.html
│   ├── driver-profile-page.html
│   ├── driver-contact&information-page.html
│   │
│   ├── guard-home-page.html
│   ├── guard-statistics-page.html
│   ├── guard-scanqrcode-page.html
│   ├── guard-vehicle-page.html
│   ├── guard-profile-page.html
│   ├── guard-contact&information-page.html
│   │
│   ├── logo.png (system logo)
│   ├── banner-day.png
│   ├── banner-night.png
│   ├── University-of-the-Assumption.jpeg (background)
│   └── Other images...
│
└── backend/
    ├── manage.py
    ├── db.sqlite3 (database)
    ├── venv/ (virtual environment)
    ├── parking_system/ (Django project)
    └── parking_app/ (Django app)
```

---

## 🎬 Step-by-Step Walkthrough

### Step 1: Open the System
Open this file in your browser:
```
C:\Users\Christine Dizon\OneDrive\Desktop\dre\frontend\index.html
```

### Step 2: Watch Loading Animation
- You'll see the UA Parking System logo
- A car 🚗 will move across a progress bar
- Percentage will count from 0% to 100%
- Takes about 2-4 seconds

### Step 3: Login Form Appears Automatically
After animation finishes, login form appears with:
- Username field
- Password field
- Login button
- Link to register

### Step 4: Enter Credentials
Pick one from the test accounts above, for example:
```
Username: driver1
Password: password123
```

### Step 5: Click Login
- Button will show loading spinner
- If backend is available: Real authentication happens
- If backend unavailable: Test account validation
- If credentials match: Redirects to dashboard
- If invalid: Shows error message

### Step 6: Explore Your Dashboard
You're now in your role's dashboard! Features available:
- **Admin**: Full system management
- **Driver**: Vehicle & parking management
- **Guard**: QR scanning & vehicle logs

### Step 7: Navigate & Explore
- Click menu items to navigate
- Use theme toggle (sun/moon icon)
- Check animations and responsive design
- Test on mobile/tablet/desktop

---

## 🐛 Troubleshooting

### Q: Loading page doesn't show
**A:** Clear browser cache (Ctrl+Shift+Del) and refresh

### Q: Animation doesn't work
**A:** Check browser console (F12) for JavaScript errors

### Q: Can't login
**A:** Make sure you're using the EXACT credentials from above (case-sensitive)

### Q: "Invalid username or password" message
**A:** Try: `driver1` with `password123`

### Q: Page doesn't load dashboard
**A:** Check that `driver-home-page.html` exists in frontend folder

### Q: Backend connection error
**A:** This is OK! Frontend works without backend using test accounts

### Q: Can't access backend admin
**A:** Make sure backend is running: Check Terminal for "Running on http://0.0.0.0:8000/"

---

## 🚀 Advanced Usage

### Connect with Backend API
Open browser console (F12) and try:
```javascript
// Get parking rates
fetch('http://localhost:8000/api/parking-rates/')
    .then(r => r.json())
    .then(d => console.log(d))

// Get user profile (requires login)
fetch('http://localhost:8000/api/profiles/my_profile/', {
    headers: { 'Authorization': 'Bearer YOUR_TOKEN' }
})
    .then(r => r.json())
    .then(d => console.log(d))
```

### Start Backend Server
```bash
cd "C:\Users\Christine Dizon\OneDrive\Desktop\dre\backend"
venv\Scripts\activate
python manage.py runserver 0.0.0.0:8000
```

### Access Backend Admin
```
URL: http://localhost:8000/admin/
Username: admin
Password: admin123
```

---

## 📱 Responsive Testing

The system works on all screen sizes:

- **Desktop**: Full layout with all features
- **Tablet**: Responsive grid layout
- **Mobile**: Single column, touch-friendly

Test by resizing browser or using F12 responsive design mode.

---

## 🎯 What You Have

| Component | Status | Location |
|-----------|--------|----------|
| Frontend - 12 Pages | ✅ Complete | `/frontend/` |
| Loading Animation | ✅ Complete | `loading-page.html` |
| Login Form | ✅ Complete | `login.html` |
| Administrator Dashboard | ✅ Complete | `admin-home-page.html` |
| Driver Dashboard | ✅ Complete | `driver-home-page.html` |
| Guard Dashboard | ✅ Complete | `guard-home-page.html` |
| Backend API | ✅ Running | Port 8000 |
| Database | ✅ SQLite | `db.sqlite3` |
| Admin Panel | ✅ Available | Port 8000/admin |

---

## 💡 Tips

1. **First Time?** Use `driver1 / password123`
2. **Theme Toggle**: Look for sun/moon icon in top bar
3. **Fast Loading**: Use HTTP server (faster than file://)
4. **Multiple Roles**: Logout and login as different users
5. **Mobile Test**: Open on phone to test responsive design

---

## 📞 Credentials Summary

```
ADMIN LOGIN:
   username: admin
   password: admin123

DRIVER LOGIN (use this first):
   username: driver1
   password: password123

GUARD LOGIN:
   username: guard1
   password: password123

BACKEND ADMIN:
   username: admin
   password: admin123
```

---

## 🎉 Ready to Go!

Everything is set up and working. Just:

1. **Open** `index.html` from the frontend folder
2. **Wait** for the loading animation (watch the car!)
3. **Login** with any test credential above
4. **Enjoy** exploring the UA Parking System!

---

**Happy Parking! 🚗**

**Need help?** Check LEFT/RIGHT files exist and close any other processes on port 8000 or 3000.