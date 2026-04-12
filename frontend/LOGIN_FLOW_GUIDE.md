# UA Parking System - Complete Login Flow Guide

## 🚀 System Entry Flow

### Entry Point Sequence:
```
1. User opens system → index.html
          ↓
2. index.html redirects → loading-page.html
          ↓
3. Loading animation plays (2-4 seconds)
          ↓
4. Animation completes → Redirects to login.html
          ↓
5. User enters credentials → Backend authentication
          ↓
6. Authentication successful → Role-based Dashboard
```

---

## 📄 Page Files

| File | Purpose | Entry Point |
|------|---------|------------|
| `index.html` | **System entry point** | Open this first time |
| `loading-page.html` | Animated loader | Auto-redirect from index.html |
| `login.html` | User authentication | Auto-redirect after loading |
| `register.html` | User registration | Linked from login |
| `setup-profile.html` | Profile configuration | Can link from register |

---

## 🔑 Test Credentials

### Development Test Accounts

All test accounts work with these credentials:

| Username | Password | Role | Redirects To |
|----------|----------|------|--------------|
| `admin` | `admin123` | Admin | admin-home-page.html |
| `driver1` | `password123` | Driver | driver-home-page.html |
| `driver2` | `password123` | Driver | driver-home-page.html |
| `guard1` | `password123` | Guard | guard-home-page.html |
| `guard2` | `password123` | Guard | guard-home-page.html |

---

## 🔐 Authentication Process

### How It Works:

1. **Loading Page** (2-4 seconds)
   - Shows animated car moving across progress bar
   - Displays percentage complete
   - Automatically redirects to login when finished

2. **Login Page**
   - User enters username and password
   - Attempts connection to Django backend at `http://localhost:8000/api/`
   - If backend is available: Uses real authentication
   - If backend is unreachable: Falls back to test account credentials
   - Shows error messages for invalid credentials
   - Stores user info in localStorage

3. **Dashboard Redirect**
   - Redirects based on user role:
     - **admin** → admin-home-page.html
     - **driver** → driver-home-page.html
     - **guard** → guard-home-page.html

---

## 🖥️ Backend Authentication (Optional)

### Django REST API Endpoint
```
POST http://localhost:8000/api/auth/login/
Content-Type: application/json

{
  "username": "driver1",
  "password": "password123"
}
```

### Expected Response
```json
{
  "token": "abc123xyz...",
  "user_id": 5,
  "username": "driver1",
  "role": "driver",
  "first_name": "Juan",
  "last_name": "Dela Cruz"
}
```

### Note:
- Backend is **optional** for frontend development
- Test accounts work without backend
- For production, ensure backend credentials are configured

---

## 💾 Local Storage Data

After successful login, the following is stored:

```javascript
localStorage.setItem('username', 'driver1');
localStorage.setItem('userRole', 'driver');
localStorage.setItem('authToken', 'token123...');  // If backend available
localStorage.setItem('isTestMode', 'true');       // If using test accounts
```

---

## 🔄 Navigation Flow

### Admin User Path
```
index.html 
  → loading-page.html (3 sec animate)
  → login.html (enter: admin / admin123)
  → admin-home-page.html
  → admin-statistics-page.html
  → admin-vehicle-page.html
  → admin-manageaccounts-page.html
  → admin-profile-page.html
  → admin-contact&information-page.html
  → back to login (logout)
```

### Driver User Path
```
index.html
  → loading-page.html (3 sec animate)
  → login.html (enter: driver1 / password123)
  → driver-home-page.html
  → driver-vehicle-page.html
  → driver-parking-page.html
  → driver-profile-page.html
  → driver-contact&information-page.html
  → back to login (logout)
```

### Guard User Path
```
index.html
  → loading-page.html (3 sec animate)
  → login.html (enter: guard1 / password123)
  → guard-home-page.html
  → guard-statistics-page.html
  → guard-scanqrcode-page.html
  → guard-vehicle-page.html
  → guard-profile-page.html
  → guard-contact&information-page.html
  → back to login (logout)
```

---

## 🚀 Quick Start

### From Browser:
1. Open: `file:///c:/Users/Christine Dizon/OneDrive/Desktop/dre/frontend/index.html`
2. Wait for loading animation (watch the car move!)
3. Enter test credentials from table above
4. Access your role's dashboard

### Or with HTTP Server:
```bash
cd frontend
# Using Python
python -m http.server 3000

# Then open: http://localhost:3000/
```

---

## 🐛 Troubleshooting

### Loading Page Doesn't Animate
- ✓ Check browser console for JavaScript errors
- ✓ Ensure `loading-page.html` is in the same folder as index.html

### Login Shows Error
- ✓ Check if username and password match table above exactly
- ✓ Try test account: `driver1` / `password123`
- ✓ Check browser console (F12) for error details

### Can't Access Dashboard After Login
- ✓ Check if dashboard HTML file exists (e.g., `driver-home-page.html`)
- ✓ Verify file path in redirect is correct
- ✓ Check browser console for CORS or loading errors

### Backend Not Connecting
- ✓ Start Django backend: `python manage.py runserver 0.0.0.0:8000`
- ✓ Verify Django is running on port 8000
- ✓ Check CORS settings in Django if errors appear
- ✓ Frontend will auto-fallback to test accounts if backend unavailable

---

## 🔒 Security Notes

### Development Mode:
- Test credentials are hardcoded for convenience
- No real password hashing
- localStorage used for simple session management
- ⚠️ NOT suitable for production

### Production Mode:
- Remove hardcoded test accounts
- Implement JWT token authentication
- Use HTTPS for all requests
- Implement proper session management
- Add CSRF protection
- Use secure password hashing

---

## 📱 Session Management

### Check If User Is Logged In:
```javascript
const username = localStorage.getItem('username');
const userRole = localStorage.getItem('userRole');

if (!username) {
    // User not logged in, redirect to login
    window.location.href = 'login.html';
}
```

### Logout User:
```javascript
function logout() {
    localStorage.removeItem('username');
    localStorage.removeItem('userRole');
    localStorage.removeItem('authToken');
    window.location.href = 'login.html';
}
```

---

## ✅ Feature Summary

| Feature | Status | Details |
|---------|--------|---------|
| Loading Animation | ✅ Complete | 3-second animated car loader |
| Login Form | ✅ Complete | Username/password with validation |
| Error Messages | ✅ Complete | Shows invalid login errors |
| Role-Based Routing | ✅ Complete | Redirects to correct dashboard |
| Test Accounts | ✅ Complete | 5 test accounts available |
| Backend Integration | ✅ Complete | Falls back to test if unavailable |
| Responsive Design | ✅ Complete | Works on mobile/tablet/desktop |
| LocalStorage | ✅ Complete | Persists user session |

---

## 🎯 Next Steps

1. ✅ **System Entry**: Open `index.html` to see loading animation
2. ✅ **Login**: Use test credentials from above
3. ✅ **Dashboard**: Explore your role's pages
4. ✅ **Backend**: Optional - connect to Django API
5. 📝 **Logout Link**: Add logout buttons to dashboard pages if needed

---

## 📞 Need Help?

- Check browser console (F12) for errors
- Verify all HTML files are in the `frontend/` folder
- Ensure backend is running on port 8000
- Test with `driver1 / password123` (simplest account)

---

**Happy Parking! 🚗**