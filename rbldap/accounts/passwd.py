"""Generate password"""
from secrets import choice
from string import ascii_letters, digits

ALPHABET = ascii_letters + digits


def generate_passwd(length: int) -> str:
    """
    Generate a password
    Args:
        length: length of password to generate
    Returns:
        String containing a randomly generated password
    """
    return "".join(choice(ALPHABET) for i in range(length))
