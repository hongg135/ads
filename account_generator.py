import random
import string

def generate_account():
    """Generate random account details for Gmail registration.
    
    Returns:
        dict: Account details including name, username, password, birth date and gender
    """
    # Common English first and last names
    first_names = [
        'James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph',
        'Thomas', 'Charles', 'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth',
        'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen'
    ]
    
    last_names = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
        'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
        'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin'
    ]

    # Generate name
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    
    # Generate username (lowercase name + 4 random digits)
    username = f"{first_name.lower()}{last_name.lower()}{random.randint(1000,9999)}"
    
    # Generate strong password (12 chars with mix of upper, lower, digits)
    password_chars = (
        random.choices(string.ascii_uppercase, k=4) +
        random.choices(string.ascii_lowercase, k=4) +
        random.choices(string.digits, k=4)
    )
    random.shuffle(password_chars)
    password = ''.join(password_chars)
    
    # Generate birth date (age between 18-35 years)
    birth_year = random.randint(1988, 2005)
    birth_month = random.randint(1, 12)
    # Adjust max days based on month
    max_days = 31 if birth_month in [1,3,5,7,8,10,12] else 30
    max_days = 28 if birth_month == 2 else max_days
    birth_day = random.randint(1, max_days)
    
    # Generate gender
    gender = random.choice(['Male', 'Female'])
    
    return {
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "password": password,
        "birth_day": str(birth_day),
        "birth_month": str(birth_month), 
        "birth_year": str(birth_year),
        "gender": gender
    }
