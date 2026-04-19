# UA Parking System - Frontend Documentation

## Overview
The UA Parking System frontend is a responsive web application built with HTML5, CSS (Tailwind), and vanilla JavaScript. It provides role-based interfaces for drivers, guards, and administrators to manage parking operations.

## Technology Stack
- **Markup**: HTML5
- **Styling**: Tailwind CSS (CDN)
- **Icons**: Lucide Icons (CDN)
- **JavaScript**: Vanilla ES6+
- **Storage**: LocalStorage for user session data
- **API Communication**: Fetch API

## Project Structure
```
frontend/
├── index.html                          # Landing/login page
├── login.html                          # Login form
├── register.html                       # User registration
├── setup-profile.html                  # Profile setup after registration
├── loading-page.html                   # Loading animation page
│
├── driver-home-page.html               # Driver dashboard
├── driver-parking-page.html            # Driver parking info
├── driver-profile-page.html            # Driver profile management
├── driver-vehicle-page.html            # Driver vehicle registration
├── driver-contact&information-page.html # Driver contact/info
│
├── guard-home-page.html                # Guard dashboard
├── guard-scan-qr-page.html             # QR code scanner
├── guard-scanqrcode-page.html          # Alternative scanner
├── guard-profile-page.html             # Guard profile
├── guard-vehicle-page.html             # Guard vehicle info
├── guard-statistics-page.html          # Guard scanning stats
├── guard-contact&information-page.html # Guard contact info
│
├── admin-home-page.html                # Admin dashboard
├── admin-manageaccounts-page.html      # Account management
├── admin-vehicle-page.html             # Vehicle pricing & registration
├── admin-profile-page.html             # Admin profile
├── admin-statistics-page.html          # Admin statistics
├── admin-contact&information-page.html # Admin contact info
│
├── Assets/
│   ├── logo.png                        # University of the Assumption logo (favicon)
│   ├── banner-day.png                  # Day mode banner
│   ├── banner-night.png                # Night mode banner
│   ├── bg1.jpg, bg2.jpg                # Background images
│   └── *.jpeg, *.jpg                   # Additional images
│
└── Documentation/
    ├── LOGIN_FLOW_GUIDE.md
    ├── REGISTRATION_FLOW.md
    ├── COMPLETE_USER_FLOW.md
    └── UA PARKING SYSTEM INSTRUCTIONS.txt
```

## Styling & Assets
- **Favicon**: logo.png (University of the Assumption logo)
- **Page Title**: "UA Parking System" (all pages)
- **Color Scheme**: Blue, white, and gray with Tailwind utilities
- **Responsive Design**: Mobile-first approach with Tailwind breakpoints

## Core Pages

### Authentication Pages
- **index.html** - Landing page with system overview
- **login.html** - User login form with role selection
- **register.html** - New user registration
- **setup-profile.html** - Profile completion after registration
- **loading-page.html** - Loading animation with car animation

### Driver Section
- **driver-home-page.html** - Main dashboard showing statistics, mission, vision
- **driver-parking-page.html** - Current parking status, today's sessions, vehicle list
- **driver-vehicle-page.html** - Vehicle registration and management
- **driver-profile-page.html** - Profile information and settings
- **driver-contact&information-page.html** - Contact, FAQ, university info

### Guard Section
- **guard-home-page.html** - Main dashboard
- **guard-scan-qr-page.html** - QR code scanner interface
- **guard-scanqrcode-page.html** - Alternative scanning page
- **guard-statistics-page.html** - Personal scanning statistics with filtering
- **guard-profile-page.html** - Guard profile management
- **guard-vehicle-page.html** - Vehicle information reference
- **guard-contact&information-page.html** - System information

### Admin Section
- **admin-home-page.html** - Dashboard and system overview
- **admin-vehicle-page.html** - Vehicle pricing tier management
- **admin-manageaccounts-page.html** - User account management
- **admin-statistics-page.html** - System-wide statistics
- **admin-profile-page.html** - Admin profile
- **admin-contact&information-page.html** - System information

## Key Features

### User Authentication
- Role-based login (driver, guard, admin)
- LocalStorage-based session management
- User data caching after login

### Responsive Design
- Mobile-first approach with Tailwind CSS
- Dark mode support across all pages
- Animated transitions and reveals
- Smooth counter animations

### Dashboard Statistics
- Real-time counter animations with proper number formatting
- University statistics display
- Mission and Vision statements
- Core Values and University Goals display

### Driver Features
- View today's parking sessions (time in/out)
- Register/manage multiple vehicles
- Vehicle type flexibility
- QR code display for parking sessions

### Guard Features
- QR code scanning with camera integration
- Manual vehicle entry option
- Personal scanning statistics dashboard
- Time-based filtering (day, week, month, year)
- Display of guard ID and scanning metrics

### Admin Features
- Create pricing tiers for any vehicle type + pass type combo
- Flexible pricing management (add, edit, delete)
- Duplicate prevention with error messages
- User account management interface
- System-wide statistics dashboard

### University Information
- Mission statement: Integral development through Academic Excellence, Christian Formation, Community Services
- Vision: Leading Formator of academically competent, morally upright, socially responsible leaders
- Founded: 1963 in San Fernando, Pampanga
- Students: 23,000+, Faculty & Staff: 500+, Years of Excellence: 63

## API Integration Points

### Frontend Base URL
Configure in each page's JavaScript: `http://localhost:8000/api/`

### Key API Calls

#### Driver Dashboard
```javascript
GET /api/parking-sessions/today_sessions/?user_id={userId}
```

#### Guard Statistics
```javascript
GET /api/scan-logs/guard_statistics/?guard_id={guardId}&filter={day|week|month|year}
```

#### QR Code Scanning
```javascript
POST /api/scan-logs/scan_qr/
{
  "vehicle_id": id,
  "guard_id": guardId,
  "entry_point": "Main Gate"
}
```

#### Vehicle Registration
```javascript
POST /api/vehicles/
{
  "vehicle_type": "car",
  "brand": "Toyota",
  "model": "Corolla",
  "plate_number": "ABC-1234",
  "color": "White"
}
```

#### Pricing Management
```javascript
POST /api/parking-rates/
{
  "vehicle_type": "car",
  "pass_type": "park",
  "price": "100.00"
}
```

## LocalStorage Data Structure

```javascript
// User Session
localStorage.userId = "1"
localStorage.userRole = "driver"  // driver, guard, admin
localStorage.userName = "John Doe"

// Guard Information
localStorage.guardId = "5"        // For guard role
localStorage.guardName = "Officer Smith"
```

## Custom Functions

### Counter Animation
```javascript
function animateCounter(cardElement)
// Animates numerical counters with proper comma formatting
// Supports numbers with suffixes like "+" (e.g., 23,000+)
```

### Vehicle Display
```javascript
function loadUserVehicles()
// Fetches and displays user's registered vehicles
```

### Statistics Loading
```javascript
function loadGuardScanningStat(filterType)
// Loads guard's scan statistics with time-based filtering
```

### QR Scanning
```javascript
function logVehicle(plateNumber)
// Records vehicle entry/exit via camera or manual input
```

## Styling & Themes

### Color Scheme
- **Primary Blue**: #002366
- **Secondary Red**: #CE2029
- **Accent Gold**: #FFD700
- **Light Background**: #f8fafc
- **Dark Mode Background**: #0d1117

### Custom CSS Classes
- `.stat-card` - Statistics card styling
- `.reveal` - Scroll reveal animations
- `.animated-footer` - Footer with sky/cloud animations
- `night-mode` - Dark theme class
- `.nav-link` - Navigation link styling with hover effects

### Animations
- Scroll reveal effects (up, down, left, right)
- Counter counter animations (1500ms duration)
- Card hover transitions
- Banner slide transitions
- Cloud/star animations in footer

## Navigation Structure

### Global
- Navbar with role-based links
- User profile dropdown
- Role indicator (Driver/Guard/Admin)
- Dark mode toggle
- Logout button

### Driver Navigation
- Home → Parking → Vehicle → Profile → Contact

### Guard Navigation
- Home → Scan QR → Statistics → Profile → Vehicle → Contact

### Admin Navigation
- Home → Vehicle (Pricing) → Manage Accounts → Statistics → Profile → Contact

## Forms & Input Validation

### Vehicle Registration
- Vehicle type: Free text input (any type accepted)
- Brand: Text input
- Model: Text input
- Plate number: Required, checked for duplicates
- Color: Optional text input

### Pricing Management
- Vehicle type: Free text input (any type)
- Pass type: Select dropdown (Drop-Off, Park)
- Price: Number input with decimal support
- Duplicate prevention: Error message if combination exists

### User Profile
- Name, Email, Contact fields
- Role display (read-only)
- Profile picture upload (optional)

## Troubleshooting

### API Connection Issues
- Check backend server is running on http://localhost:8000
- Verify CORS headers are configured
- Check browser console for network errors
- Ensure user_id/guard_id are being sent correctly

### QR Code Scanner Not Working
- Allow camera permissions in browser
- Check mobile device has camera access
- Verify QR code format matches system specs
- Try alternative scanner page

### Numbers Displaying Incorrectly
- Check animateCounter function uses toLocaleString()
- Verify data-value attribute has correct number
- Ensure suffix (like "+") is properly extracted
- Clear browser cache if issue persists

### Dark Mode Not Working
- Check night-mode class is applied to body
- Verify CSS has night-mode overrides
- Check localStorage for theme preference
- Manually toggle from navbar if needed

## Performance Tips
- Use lazy loading for images
- Cache API responses in localStorage when possible
- Minimize DOM manipulations in loops
- Use event delegation for dynamic elements
- Debounce frequent API calls

## Browser Support
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Development Notes
- All pages use external CDNs (Tailwind, Lucide, etc.)
- No build process required
- Direct file-based development
- LocalStorage persists user sessions
- Clear cache if CSS/JS changes don't appear

## Future Enhancements
- Progressive Web App (PWA) support
- Offline mode with sync
- Real-time notifications
- Advanced analytics dashboard
- Multi-language support
- Accessibility improvements (WCAG 2.1)
