def validate_amount(value: str) -> float:
    '''
    This validates and converts a string to a positive float amount.
    '''
    try:
        amount = float(value)
    except ValueError:
        raise ValueError(f"Invalid number: '{value}'")
    
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    
    return amount


def validate_name(value: str) -> str:
    '''
    This validates that a name is non-empty and within 50 characters.
    '''
    name = value.strip()
    if not name:
        raise ValueError("Name cannot be empty.")
    
    if len(name) > 50:
        raise ValueError("Name too long (max 50 chars).")
    
    return name


def validate_pin(value: str) -> str:
    '''
    This ensures the PIN is exactly 4 digits.
    '''
    pin = value.strip()
    if not pin.isdigit() or len(pin) != 4:
        raise ValueError("PIN must be exactly 4 digits.")
    
    return pin
