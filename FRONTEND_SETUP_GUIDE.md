# UA Parking System - Frontend Setup & Configuration Guide

## Overview
This guide provides comprehensive setup and configuration instructions for the HTML5, CSS (Tailwind), and vanilla JavaScript frontend of the UA Parking System.

## Prerequisites
Before proceeding, ensure:
- ✅ Backend is installed and running on `http://127.0.0.1:8000`
- ✅ All backend API endpoints are accessible
- ✅ You have a modern web browser (Chrome, Firefox, Safari, or Edge)
- ✅ Basic understanding of HTML, CSS, and JavaScript

For backend installation, see **INSTALLATION_AND_DEPENDENCIES.md** and **BACKEND_SETUP_GUIDE.md**

---

## Frontend Architecture

### Technology Stack
- **Markup**: HTML5
- **Styling**: Tailwind CSS (CDN)
- **Icons**: Lucide Icons (CDN)
- **JavaScript**: Vanilla ES6+
- **Storage**: LocalStorage (browser)
- **Communication**: Fetch API
- **No Build Tool Required** - Runs directly in browser

### Project Structure
```
frontend/
├── index.html                              # Landing/login page
├── login.html                              # User login form
├── register.html                           # User registration
├── setup-profile.html                      # Post-registration profile setup
├── loading-page.html                       # Loading animation
│
├── DRIVER PAGES
├── driver-home-page.html                   # Driver dashboard
├── driver-parking-page.html                # Parking information
├── driver-profile-page.html                # Profile management
├── driver-vehicle-page.html                # Vehicle management
├── driver-contact&information-page.html    # Contact/info
│
├── GUARD PAGES
├── guard-home-page.html                    # Guard dashboard
├── guard-scan-qr-page.html                 # QR code scanner
├── guard-scanqrcode-page.html              # Alternative scanner
├── guard-profile-page.html                 # Guard profile
├── guard-vehicle-page.html                 # Vehicle information
├── guard-statistics-page.html              # Scanning statistics
├── guard-contact&information-page.html     # Contact/info
│
├── ADMIN PAGES
├── admin-home-page.html                    # Admin dashboard
├── admin-manageaccounts-page.html          # User account management
├── admin-vehicle-page.html                 # Vehicle pricing & rates
├── admin-profile-page.html                 # Admin profile
├── admin-statistics-page.html              # System statistics
├── admin-contact&information-page.html     # Contact/info
│
└── DOCUMENTATION
    ├── COMPLETE_USER_FLOW.md
    ├── LOGIN_FLOW_GUIDE.md
    ├── REGISTRATION_FLOW.md
    ├── UA PARKING SYSTEM INSTRUCTIONS.txt
    └── (This guide)
```

---

## Frontend Configuration

### API Endpoint Configuration

All HTML files use a centralized API configuration. Update the API base URL if needed:

**In each HTML file, find**:
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api';
```

**Change to** (for production):
```javascript
const API_BASE_URL = 'https://your-api-domain.com/api';
// or
const API_BASE_URL = 'https://api.yourdomain.com';
```

### Development vs Production URLs

**Development**:
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api';
```

**Production**:
```javascript
const API_BASE_URL = 'https://api.yourdomain.com/api';
```

---

## Page Structure & Components

### 1. Authentication Pages

#### index.html (Landing/Login)
- Entry point of the application
- Redirects logged-in users to appropriate dashboard
- Contains login form with email/password

**Features**:
- Email input validation
- Password input field
- "Remember me" checkbox (optional)
- Link to registration page
- Loading state management

#### register.html (Registration)
- User account creation
- Role selection (Driver, Guard, Admin)
- Email, password validation
- Terms of service acceptance

**Form Fields**:
```
- Full Name (required)
- Email (required, unique)
- Password (required, min 8 chars)
- Confirm Password (required)
- Phone Number (optional)
- Role Selection (Driver/Guard/Admin)
- Terms Acceptance (required)
```

#### setup-profile.html (Post-Registration)
- Create user profile after registration
- Upload profile picture (optional)
- Set additional information
- Verify user details

**Features**:
- Profile picture upload
- Address information
- Contact number validation
- Role-specific additional fields

### 2. Driver Pages

#### driver-home-page.html (Dashboard)
- Welcome message with user's name
- Quick parking statistics
- Recent parking sessions
- Pending payments
- Navigation to other sections

**Key Sections**:
```
- Current Status (Parked/Not Parked)
- Total Hours Parked (This Month)
- Total Amount Paid
- Vehicle Count
- Recent Sessions Table
- Quick Actions (Park, View Vehicles, etc.)
```

#### driver-parking-page.html
- Active parking sessions
- Session duration and cost
- Entry/exit information
- Current rate information

**Features**:
- Real-time parking timer
- Current parking charges
- Session history
- Check-out functionality

#### driver-vehicle-page.html
- Register new vehicles
- View registered vehicles
- Update vehicle information
- View vehicle QR codes

**Vehicle Registration Form**:
```
- Vehicle Type (Car, Motorcycle, Truck, etc.)
- Brand (Toyota, Honda, etc.)
- Model (Corolla, Civic, etc.)
- Plate Number (required, unique)
- Color
- Registration Type (Annual, Semester, etc.)
```

#### driver-profile-page.html
- User profile information
- Edit personal details
- Change password
- Upload/update profile picture
- Contact preferences

#### driver-contact&information-page.html
- Contact form
- Frequently Asked Questions
- System information
- Support contact details

### 3. Guard Pages

#### guard-home-page.html (Dashboard)
- QR code scanner status
- Today's statistics
- Total vehicles scanned
- Active sessions
- Quick scanner link

**Features**:
- Daily statistics
- Scanner status indicator
- Recent scan logs
- Shift information

#### guard-scan-qr-page.html (QR Scanner)
- Real-time QR code scanning
- Vehicle/driver validation
- Session check-in/check-out
- Scan history
- Error handling

**Functionality**:
```javascript
// Example scan result handling
const scanResult = {
    vehicle_id: 123,
    plate_number: "ABC-1234",
    owner_name: "John Doe",
    vehicle_type: "car",
    status: "valid",
    last_session: "2024-04-13 09:30"
}
```

#### guard-statistics-page.html
- Daily/weekly/monthly statistics
- Vehicle type breakdown
- Peak hours analysis
- Revenue tracking
- Export reports option

#### guard-profile-page.html
- Guard profile information
- Shift schedule
- Performance metrics
- Contact information

#### guard-vehicle-page.html
- General vehicle information
- Registered vehicle list
- Search functionality
- Filter by vehicle type

#### guard-contact&information-page.html
- Contact form
- System FAQs
- Support information
- Reporting problematic situations

### 4. Admin Pages

#### admin-home-page.html (Dashboard)
- System overview
- Key performance indicators (KPIs)
- Revenue summary
- User statistics
- Quick admin actions

**Dashboard Widgets**:
```
- Total Users
- Total Vehicles
- Today's Revenue
- Active Sessions
- System Status
- Recent Transactions
```

#### admin-manageaccounts-page.html
- User account management
- Create/edit/delete users
- Set user roles
- Suspend/activate accounts
- View user activity logs
- Bulk actions

**Features**:
```
- User list with search/filter
- Role assignment
- Account status management
- Activity tracking
- Bulk operations
- Export user data
```

#### admin-vehicle-page.html
- Vehicle pricing management
- Parking rate configuration
- Pricing tier setup
- Duration-based rates (hourly, daily, monthly)

**Rate Management**:
```
- Vehicle Type Selection
- Hourly Rate
- Daily Rate
- Monthly Rate
- Flat Rate Option
- Special Rates/Discounts
- Activation/Deactivation
```

#### admin-statistics-page.html
- Comprehensive analytics
- Revenue reports
- Usage trends
- Performance metrics
- Data visualization
- Custom date range filtering
- Export reports (CSV/PDF)

**Report Types**:
```
- Daily Revenue Report
- Vehicle Type Analysis
- Peak Hours Analysis
- User Activity Report
- Parking Duration Analysis
- Payment Status Report
```

#### admin-profile-page.html
- Admin profile management
- Change password
- Update contact information
- System preferences
- API key management
- Audit log viewing

#### admin-contact&information-page.html
- System announcements area
- Support information
- FAQ management
- System status
- Maintenance schedule

---

## Frontend JavaScript Implementation

### Core JavaScript Structure

All pages follow this general structure:

```javascript
// 1. API Configuration
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// 2. Authentication State
const authState = {
    token: localStorage.getItem('token'),
    userId: localStorage.getItem('userId'),
    userRole: localStorage.getItem('userRole'),
    userName: localStorage.getItem('userName')
};

// 3. API Communication Functions
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'Authorization': authState.token ? `Token ${authState.token}` : ''
        }
    };

    if (data) {
        options.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API Call failed:', error);
        throw error;
    }
}

// 4. Page Initialization
document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
    loadPageData();
});

// 5. Authentication Check
function checkAuthentication() {
    if (!authState.token) {
        window.location.href = 'login.html';
    }
}

// 6. Page-Specific Functions
function loadPageData() {
    // Load role-specific data
    switch(authState.userRole) {
        case 'driver':
            loadDriverData();
            break;
        case 'guard':
            loadGuardData();
            break;
        case 'admin':
            loadAdminData();
            break;
    }
}
```

### Common Utility Functions

```javascript
// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'PHP'
    }).format(amount);
}

// Format date/time
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Format duration
function formatDuration(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 3000);
}

// Handle errors
function handleError(error) {
    console.error('Error:', error);
    showNotification(error.message || 'An error occurred', 'error');
}
```

---

## LocalStorage Management

### Stored Data Structure

The frontend uses browser's LocalStorage to maintain session state:

```javascript
// User Authentication
localStorage.setItem('token', response.token);        // API authentication token
localStorage.setItem('userId', response.userId);      // User ID
localStorage.setItem('userRole', response.role);      // User role (admin/driver/guard)
localStorage.setItem('userName', response.name);      // User name
localStorage.setItem('userEmail', response.email);    // User email

// Session Data
localStorage.setItem('currentVehicle', vehicleId);    // Currently selected vehicle
localStorage.setItem('currentSession', sessionId);    // Active parking session
```

### Clear Session (Logout)
```javascript
function logout() {
    // Clear all stored data
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    localStorage.removeItem('userRole');
    localStorage.removeItem('userName');
    localStorage.removeItem('userEmail');
    localStorage.removeItem('currentVehicle');
    localStorage.removeItem('currentSession');
    
    // Redirect to login
    window.location.href = 'login.html';
}
```

---

## API Integration Patterns

### Fetch User Data
```javascript
async function fetchUser() {
    try {
        const response = await apiCall('/users/profile/');
        if (response.success) {
            const user = response.data;
            updateUIWithUser(user);
        }
    } catch (error) {
        handleError(error);
    }
}
```

### Create New Vehicle
```javascript
async function registerVehicle(vehicleData) {
    try {
        const response = await apiCall('/vehicles/', 'POST', vehicleData);
        if (response.success) {
            showNotification('Vehicle registered successfully', 'success');
            fetchVehicles();  // Refresh vehicle list
        }
    } catch (error) {
        handleError(error);
    }
}
```

### Get Parking Sessions
```javascript
async function fetchParkingSessions() {
    try {
        const response = await apiCall('/parking-sessions/');
        if (response.success) {
            displaySessions(response.data);
        }
    } catch (error) {
        handleError(error);
    }
}
```

### Update User Profile
```javascript
async function updateProfile(profileData) {
    try {
        const response = await apiCall('/users/profile/', 'PUT', profileData);
        if (response.success) {
            showNotification('Profile updated successfully', 'success');
            localStorage.setItem('userName', response.data.name);
        }
    } catch (error) {
        handleError(error);
    }
}
```

---

## Responsive Design

### Tailwind CSS Breakpoints
The frontend uses Tailwind CSS for responsive design:

```HTML
<!-- Mobile first (default) -->
<div class="text-sm p-2"></div>

<!-- Tablet (md) -->
<div class="md:text-base md:p-4"></div>

<!-- Desktop (lg) -->
<div class="lg:text-lg lg:p-6"></div>

<!-- Large Desktop (xl) -->
<div class="xl:text-xl xl:p-8"></div>
```

### Common Responsive Patterns
```HTML
<!-- Responsive Grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    <!-- Cards go here -->
</div>

<!-- Responsive Navigation -->
<nav class="flex flex-col md:flex-row">
    <!-- Nav items go here -->
</nav>

<!-- Responsive Typography -->
<h1 class="text-2xl md:text-3xl lg:text-4xl font-bold">
    Responsive Heading
</h1>
```

---

## Forms & Validation

### Form Validation Pattern
```javascript
function validateForm(formData) {
    const errors = {};
    
    // Email validation
    if (!isValidEmail(formData.email)) {
        errors.email = 'Invalid email format';
    }
    
    // Password validation
    if (formData.password.length < 8) {
        errors.password = 'Password must be at least 8 characters';
    }
    
    // Required fields
    if (!formData.name || formData.name.trim() === '') {
        errors.name = 'Name is required';
    }
    
    return errors;
}

function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}
```

### Display Form Errors
```javascript
function displayFormErrors(errors) {
    clearPreviousErrors();
    
    Object.keys(errors).forEach(field => {
        const fieldElement = document.querySelector(`[name="${field}"]`);
        if (fieldElement) {
            const errorElement = document.createElement('span');
            errorElement.className = 'error-message text-red-500 text-sm';
            errorElement.textContent = errors[field];
            fieldElement.parentElement.appendChild(errorElement);
            fieldElement.classList.add('error');
        }
    });
}

function clearPreviousErrors() {
    document.querySelectorAll('.error-message').forEach(el => el.remove());
    document.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
}
```

---

## Performance Optimization

### Image Optimization
```HTML
<!-- Lazy loading images -->
<img src="image.jpg" loading="lazy" alt="Description" />

<!-- Responsive images -->
<picture>
    <source media="(min-width: 1024px)" srcset="large.jpg" />
    <source media="(min-width: 640px)" srcset="medium.jpg" />
    <img src="small.jpg" alt="Responsive" />
</picture>
```

### Caching API Responses
```javascript
const cache = new Map();

async function apiCallWithCache(endpoint, method = 'GET', ttl = 300000) {
    const cacheKey = `${method}:${endpoint}`;
    
    if (cache.has(cacheKey)) {
        const { data, timestamp } = cache.get(cacheKey);
        if (Date.now() - timestamp < ttl) {
            return data;  // Return cached data
        }
    }
    
    const data = await apiCall(endpoint, method);
    cache.set(cacheKey, { data, timestamp: Date.now() });
    return data;
}
```

### Debouncing Search
```javascript
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

// Usage
const searchUsers = debounce(async (query) => {
    const results = await apiCall(`/users/search/?q=${query}`);
    displayResults(results);
}, 300);  // Wait 300ms after user stops typing
```

---

## Security Considerations

### Prevent XSS (Cross-Site Scripting)
```javascript
// Instead of innerHTML, use textContent for user data
element.textContent = userData.name;  // Safe
element.innerHTML = userData.name;    // Unsafe with user input

// Use a function to safely escape HTML
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
```

### CSRF Protection
```javascript
// Always include Auth token in headers for state-changing operations
const options = {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${authState.token}`
    },
    body: JSON.stringify(data)
};
```

### Sensitive Data Handling
```javascript
// NEVER store sensitive data like passwords in localStorage
// NEVER log sensitive information
console.log(sensitiveData);  // Bad practice

// Use secure HTTP-only cookies for tokens (if available)
// Never include sensitive data in URLs
// Always use HTTPS in production
```

---

## Browser Compatibility

### Supported Browsers
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Polyfills (if needed for older browsers)
```html
<!-- Array.includes polyfill -->
<script src="https://polyfill.io/v3/polyfill.min.js?features=Array.prototype.includes"></script>

<!-- Fetch API polyfill -->
<script src="https://cdn.jsdelivr.net/npm/whatwg-fetch@3"></script>
```

---

## Debugging Frontend

### Browser DevTools
- **Open DevTools**: `F12` or `Ctrl+Shift+I`
- **Console Tab**: View errors and logs
- **Network Tab**: Monitor API calls
- **Storage Tab**: Check LocalStorage
- **Elements Tab**: Inspect HTML structure

### Common Console Errors

**Enable debug logging**:
```javascript
// Add to application
const DEBUG = true;

function log(message, data = null) {
    if (DEBUG) {
        console.log(`[APP] ${message}`, data || '');
    }
}
```

**Monitor API calls**:
```javascript
// Add to console
monitorFetch();

function monitorFetch() {
    const originalFetch = window.fetch;
    window.fetch = function(...args) {
        console.log('API Call:', args[0]);
        return originalFetch.apply(this, args)
            .then(response => {
                console.log('API Response:', response.status);
                return response;
            });
    };
}
```

---

## Troubleshooting

### Pages Not Loading
1. Check browser console for errors (F12)
2. Verify backend is running: `http://127.0.0.1:8000/api/`
3. Check API endpoint URLs in JavaScript
4. Clear browser cache: `Ctrl+Shift+Delete`

### API Calls Failing
1. Verify CORS settings in backend
2. Check authentication token validity
3. Verify API endpoint exists
4. Monitor Network tab in DevTools

### LocalStorage Not Working
```javascript
// Verify localStorage is available
if (typeof(Storage) !== "undefined") {
    console.log("LocalStorage is available");
} else {
    console.log("LocalStorage is not available");
}
```

### Form Submission Issues
1. Check form validation logic
2. Inspect network request payload
3. Verify API authentication
4. Check for JavaScript errors in console

---

## Next Steps

1. Review **HOW_TO_RUN_GUIDE.md** for running the complete stack
2. Test all user roles (Driver, Guard, Admin)
3. Verify API integration with backend
4. Run performance and security checks
5. Deploy to production environment

---

**Last Updated**: April 2026
