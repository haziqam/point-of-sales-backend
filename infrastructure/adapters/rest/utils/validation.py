import re

PIN_LENGTH = 6
MIN_PASSWORD_LENGTH = 8


def validate_email(email: str) -> bool:
    match = re.match(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", email)
    if match is None:
        raise ValueError("Invalid email format")
    return True


def validate_PIN(PIN: str) -> bool:
    if len(PIN) != PIN_LENGTH:
        raise ValueError(f"PIN must be exactly {PIN_LENGTH} characters")
    if not PIN.isnumeric():
        raise ValueError(f"PIN must be numbers")
    return True


def validate_password(password: str) -> bool:
    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValueError(f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
    return True
