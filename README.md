   # CARELINK Health System

A modern healthcare management platform built with Streamlit and Python.

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

## Development Status

### Completed
- Login page with mock authentication
- Role-based dashboards (Patient, Doctor, Admin)
- Modern UI with custom CSS
- Session management
- Mock data layer
- Component library
- Data visualization charts

### In Progress
- Backend API integration
- Real database implementation

### Planned
- Real authentication system with password hashing
- Appointment booking functionality
- Medical records management
- Prescription management system
- Messaging system
- Billing and payments
- Lab results integration
- Report generation
- Email notifications

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

## Contributing

This is an educational project. For improvements or bug fixes:

1. Document your changes
2. Test thoroughly
3. Follow existing code structure
4. Update README if needed


## Contact

For questions or support regarding this project, please contact the development team.

---

**Note:** This is a prototype application for educational purposes. It uses mock data and should not be used in a production healthcare environment without proper security implementations and compliance certifications.
