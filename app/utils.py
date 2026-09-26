import secrets
import string

def create_shortcode():
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(6))