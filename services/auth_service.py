"""Authentication service for user login."""
from Database.mock_Data import MOCK_USERS
import hashlib

class AuthService:
    """Handle authentication operations."""
    
    @staticmethod
    def authenticate(username: str, password: str):
        """
        Authenticate user with username and password.
        Returns user data if successful, None otherwise.
        
        Note: This is a mock implementation. Real implementation
        would hash passwords and check against database.
        """
        # TODO: Implement real authentication with password hashing
        # For now, this is just a placeholder
        return None
    
    @staticmethod
    def mock_login(role: str):
        """
        Mock login for testing purposes.
        Returns user data for the specified role.
        """
        if role in MOCK_USERS:
            return MOCK_USERS[role]
        return None
    
    @staticmethod
    def hash_password(password: str):
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password: str, hashed: str):
        """Verify password against hash."""
        return AuthService.hash_password(password) == hashed
    
    @staticmethod
    def validate_email(email: str):
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str):
        """Validate phone number format."""
        import re
        pattern = r'^\(\d{3}\)\s\d{3}-\d{4}$'
        return re.match(pattern, phone) is not None
