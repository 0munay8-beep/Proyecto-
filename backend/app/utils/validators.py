"""
Data validation utilities
"""

import re


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_coordinates(lat: float, lon: float) -> bool:
    """Validate GPS coordinates"""
    return -90 <= lat <= 90 and -180 <= lon <= 180