# CareLink Health Dashboard

> **Jan 9, 2025 Demo Build** - A modern role-based healthcare management platform

A comprehensive healthcare dashboard system built with Streamlit, featuring role-based authentication, appointment management, lab result workflows, and prescription tracking.

---

## 🎯 Jan 9 Demo - Quick Start

### Demo Accounts

| Role | Username | Password | Purpose |
|------|----------|----------|---------|
| **Patient** | `john_doe` | `patient123` | General patient testing |
| **Patient** | `sarah_johnson` | `patient123` | Has shared lab results |
| **Doctor** | `dr_smith` | `doctor123` | Primary care physician |
| **Admin** | `admin` | `admin123` | System administrator |

### Demo Workflows (Working!)

**1. Lab Results Review & Sharing** ✅
- Doctor reviews pending lab results → adds interpretation → shares with patient
- Patient views only shared results with doctor's notes

**2. Appointment Booking & Confirmation** ✅
- Patient books appointment → doctor receives request → confirms or declines
- Bidirectional workflow with status tracking

**3. Prescription Refill Requests** ✅
- Patient requests refill → appears in doctor's queue → doctor approves/denies
- Status badges and visual feedback throughout

### Running the Demo

```powershell
# 1. Activate virtual environment
.venv\Scripts\Activate.ps1

# 2. Run Streamlit
streamlit run Home.py

# 3. Open browser at http://localhost:8501
```

**Demo Tips:**
- Don't refresh pages during demo (session state persists within session)
- Use balloons animation to show success states
- Reference `DEMO.md` for detailed walkthrough script

---

## Features

- **Role-based authentication** - Patient, Doctor, and Admin user types
- **Patient Dashboard** - View appointments, medical records, prescriptions, and messages
- **Doctor Dashboard** - Manage patients, appointments, and medical information
- **Admin Dashboard** - System management, analytics, and user administration
- **Modern UI** - Custom CSS styling with professional healthcare color scheme
- **Responsive Design** - Works on desktop and mobile devices
- **Data Visualization** - Interactive charts and graphs with Plotly

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download this repository**

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   
   **Windows (PowerShell):**
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
   
   **Windows (Command Prompt):**
   ```cmd
   .venv\Scripts\activate.bat
   ```
   
   **Mac/Linux:**
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
streamlit run Home.py
```

The application will open in your default browser at `http://localhost:8501`

## 🧪 Mock Login

For testing purposes, use the mock login buttons on the home page:

| Role | User | Specialty |
|------|------|-----------|
| **Patient** | John Smith | N/A |
| **Doctor** | Dr. Sarah Johnson | Cardiology |
| **Admin** | Admin User | System Administration |

## Project Structure

```
├── .streamlit/          # Streamlit configuration
│   ├── config.toml      # Theme and server settings
│   └── secrets.toml     # Secrets (gitignored)
├── assets/              # Images and static files
│   ├── images/
│   └── icons/
├── components/          # Reusable UI components
│   ├── auth.py          # Authentication components
│   └── cards.py         # Card components
├── config/              # Application configuration
│   ├── settings.py      # App constants and settings
│   └── database.py      # Database configuration
├── database/            # Database layer
│   ├── mock_data.py     # Mock data for testing
│   ├── models.py        # Data models
│   └── connection.py    # Database connection handler
├── pages/               # Multi-page dashboards
│   ├── Patient_Dashboard.py
│   ├── Doctor_Dashboard.py
│   └── Admin_Dashboard.py
├── services/            # Business logic
│   ├── auth_service.py      # Authentication logic
│   └── session_manager.py   # Session state management
├── styles/              # CSS stylesheets
│   ├── main.css         # Global styles
│   ├── login.css        # Login page styles
│   └── dashboard.css    # Dashboard styles
├── utils/               # Utility functions
│   └── helpers.py       # Helper functions
├── Home.py              # Main entry point (login page)
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Design System

### Color Palette

- **Primary Blue:** `#0066CC` - Trust, reliability
- **Secondary Teal:** `#00A896` - Calm, healing
- **Success Green:** `#06D6A0` - Positive results
- **Warning Amber:** `#FFB703` - Alerts
- **Error Red:** `#EF476F` - Critical alerts
- **Dark Gray:** `#2B2D42` - Text, headers
- **Light Gray:** `#EDF2F4` - Backgrounds

### Typography

- **Font Family:** Inter, Roboto, System UI
- **Headers:** 600-700 weight
- **Body:** 400 weight

## Technologies Used

- **Streamlit** - Web framework for Python
- **Python** - Backend programming language
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive data visualization
- **Custom CSS** - Professional styling
- **SQLite** - Database (planned)

### Completed ✅

- ✅ **Role-based authentication** - Patient, Doctor, Admin roles with session management
- ✅ **Patient Dashboard** - View appointments, prescriptions, messages, lab results
- ✅ **Doctor Dashboard** - Manage appointments, review lab results, approve prescriptions
- ✅ **Admin Dashboard** - System statistics and user management (stub)
- ✅ **Lab Results Workflow** - Doctor review → interpretation → share with patient
- ✅ **Appointment Booking** - Patient request → doctor confirmation workflow
- ✅ **Prescription Refills** - Patient request → doctor approval workflow
- ✅ **Modern UI** - Custom CSS with healthcare-specific color palette
- ✅ **Session State Management** - Cross-page workflow persistence
- ✅ **Mock Data Layer** - Comprehensive test data with status fields

### In Progress 🔄

- 🔄 **Database Integration** - PostgreSQL connection (planned post-demo)
- 🔄 **Password Hashing** - bcrypt implementation (planned)
- 🔄 **Automated Testing** - pytest suite (started, see `TESTING.md`)

### Planned 📋

- 📋 **Messaging System** - Full send/reply functionality
- 📋 **Document Upload** - Lab reports, insurance cards
- 📋 **Email Notifications** - Appointment reminders, refill approvals
- 📋 **Admin User Management** - Full CRUD for users
- 📋 **Billing Integration** - Payment processing
- 📋 **Calendar Integration** - Google Calendar sync
- 📋 **HIPAA Compliance** - Full security audit and certification

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | This file - project overview and setup |
| [DEMO.md](DEMO.md) | Jan 9 demo script with workflows and talking points |
| [RISKS.md](RISKS.md) | Known technical debt and mitigation strategies |
| [TESTING.md](TESTING.md) | Testing procedures and quality assurance |

---

## Development Status

## Security Notes

**⚠️ Current Status:** This is a **Jan 9 interim demo build** with mock authentication and data.

**For Production Use, Implement:**
- ✅ Secure password hashing with bcrypt
- ✅ JWT token-based authentication
- ✅ SSL/TLS encryption (HTTPS)
- ✅ HIPAA compliance measures (encryption at rest, audit logs)
- ✅ Input validation and sanitization
- ✅ SQL injection prevention with parameterized queries
- ✅ XSS protection with proper escaping
- ✅ CSRF tokens for form submissions
- ✅ Session timeout policies
- ✅ Two-factor authentication (2FA)

**See [RISKS.md](RISKS.md) for detailed technical debt inventory.**

---

## 🧪 Testing

### Manual Testing (Completed for Demo)

All three core workflows manually tested and verified:
- ✅ Lab results (doctor → patient flow)
- ✅ Appointment booking (patient → doctor flow)
- ✅ Prescription refills (patient → doctor flow)

See [TESTING.md](TESTING.md) for:
- Pre-demo checklist
- Manual testing procedures
- Automated testing roadmap
- Test coverage goals

### Automated Testing (Planned)

```powershell
# Run unit tests (when implemented)
pytest tests/ --cov=. --cov-report=html
```

**Current Coverage:** 0% (planned for week of Jan 16)  
**Target Coverage:** 80%+ for production

---

## 🏗️ Architecture

### Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Streamlit 1.29.0+ | Web UI framework |
| **Backend** | Python 3.9+ | Business logic |
| **Database** | PostgreSQL (planned) | Data persistence |
| **ORM** | SQLAlchemy (planned) | Database abstraction |
| **Testing** | pytest 7.4.0 | Automated testing |
| **Auth** | bcrypt (planned) | Password hashing |

### Project Structure

```
carelink/
├── components/              # Reusable UI components
│   ├── cards.py             # Card components (stat, appointment, prescription, etc.)
│   ├── sidebar.py           # Role-based navigation sidebars
│   └── login_Portal.py      # Login form component
├── config/                  # Application configuration
│   ├── settings.py          # Constants and app settings
│   └── database.py          # Database connection config
├── database/                # Data layer
│   ├── mock_data.py         # Mock data with workflow status fields
│   ├── models.py            # SQLAlchemy models (planned)
│   └── connection.py        # Database connection handler
├── pages/                   # Streamlit multi-page app
│   ├── Patient_*.py         # Patient-facing pages (Dashboard, Appointments, etc.)
│   ├── Doctor_*.py          # Doctor-facing pages (Dashboard, Lab Results, etc.)
│   └── Admin_*.py           # Admin pages (Dashboard, User Management)
├── services/                # Business logic layer
│   ├── auth_service.py      # Authentication logic
│   └── session_manager.py   # Session state management
├── styles/                  # Custom CSS
│   ├── main.css             # Global styles
│   ├── dashboard.css        # Dashboard-specific styles
│   ├── login.css            # Login page styles
│   └── sidebar.css          # Navigation sidebar styles
├── tests/                   # Automated tests (planned)
│   ├── test_mock_data.py    # Data structure tests
│   └── test_session_manager.py  # Session logic tests
├── Home.py                  # Main entry point (login page)
├── requirements.txt         # Python dependencies
├── DEMO.md                  # Demo walkthrough script
├── RISKS.md                 # Technical debt documentation
├── TESTING.md               # Testing strategy
└── README.md                # This file
```

---

## Security Notes

**Current Status:** This is a prototype with mock authentication. For production use, implement:

- Secure password hashing (bcrypt)
- SSL/TLS encryption
- HIPAA compliance measures
- Proper session management
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CSRF tokens

## Documentation

### Adding New Pages

1. Create a new file in the `pages/` directory
2. Use naming convention: `#_emoji_PageName.py`
3. Include authentication check: `SessionManager.require_auth()`
4. Load CSS styling at the top of the page

### Creating New Components

1. Add component functions to `components/` directory
2. Import and use in dashboard pages
3. Follow existing component patterns (cards.py)

---

## 🚀 Roadmap

### Jan 9, 2025 - Interim Demo ✅
- ✅ 3 working workflows (lab results, appointments, prescriptions)
- ✅ Role-based UI complete
- ✅ Documentation (DEMO, RISKS, TESTING)

### Week of Jan 16 - Post-Demo
- [ ] Database integration (PostgreSQL + SQLAlchemy)
- [ ] Password hashing with bcrypt
- [ ] Unit test suite (80%+ coverage)
- [ ] Messaging system implementation

### February 2025 - Beta Release
- [ ] Admin user management CRUD
- [ ] Document upload functionality
- [ ] Email/SMS notifications
- [ ] CI/CD pipeline with GitHub Actions

### March 2025 - Production Prep
- [ ] HIPAA compliance audit
- [ ] Security penetration testing
- [ ] Performance optimization
- [ ] Accessibility (WCAG 2.1)

---

## 🤝 Contributing

This is an educational project for the Full Year Project course.

**To Contribute:**
1. Create a feature branch: `git checkout -b feature/your-feature`
2. Follow existing code structure and patterns
3. Update documentation (README, RISKS, TESTING as needed)
4. Test thoroughly before committing
5. Submit pull request with clear description

---

## 📧 Contact

**Project Lead:** [Your Name]  
**Course:** Full Year Project  
**Demo Date:** January 9, 2025

---

## 📄 License

This is an educational project. Not intended for production healthcare use without proper certifications and compliance measures.

---

**Last Updated:** January 9, 2025  
**Version:** Jan9_MVP Demo Build  
**Branch:** `Jan9_MVP`

