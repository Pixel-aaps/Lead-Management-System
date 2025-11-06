import re

ALLOWED_STATUS = ["New", "In Progress", "Converted"]

def validate_lead(data, partial=False):
    errors = []

    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    status = data.get('status')

    if not partial or 'name' in data:
        if not name or len(name.strip()) < 2:
            errors.append("Name must be at least 2 chars")

    if not partial or 'email' in data:
        if not email or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            errors.append("Invalid email")

    if phone:
        digits = re.sub(r"\D", "", phone)
        if len(digits) != 10:
            errors.append("Phone must be 10 digits")

    if not partial or 'status' in data:
        if status not in ALLOWED_STATUS:
            errors.append(f"Status must be one of {ALLOWED_STATUS}")

    return errors
