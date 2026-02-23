import re

def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return "Must contain an uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Must contain a lowercase letter."
    if not re.search(r"[0-9]", password):
        return "Must contain a number."
    if not re.search(r"[!@#$%^&*()]", password):
        return "Must contain a special character."
    return "Valid"