import secrets
import string

def create_shortcode(length: int = 6) -> str:
        chars = string.ascii_letters + string.digits

        shortcode = ""
        for _ in range(length):
            random_char = secrets.choice(chars)
            shortcode += random_char

        return shortcode

