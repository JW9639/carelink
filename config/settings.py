"""Application configuration and constants."""

# Role definitions
ROLES = {
    "PATIENT": "patient",
    "DOCTOR": "doctor",
    "ADMIN": "admin"
}

# Color scheme
COLORS = {
    "primary": "#0066CC",
    "secondary": "#00A896",
    "success": "#06D6A0",
    "warning": "#FFB703",
    "error": "#EF476F",
    "dark": "#2B2D42",
    "light": "#EDF2F4",
    "white": "#FFFFFF"
}

# Application settings
APP_NAME = "MediCare Health System"
APP_VERSION = "1.0.0"
SESSION_TIMEOUT = 3600  # 1 hour in seconds
