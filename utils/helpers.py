"""Helper utility functions."""

def format_date(date_str: str, format: str = "%Y-%m-%d"):
    """Format date string."""
    from datetime import datetime
    try:
        date_obj = datetime.strptime(date_str, format)
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_str


def format_phone(phone: str):
    """Format phone number."""
    # Remove any non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    return phone


def calculate_age(dob: str):
    """Calculate age from date of birth."""
    from datetime import datetime
    try:
        birth_date = datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
    except:
        return None
