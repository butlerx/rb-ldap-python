"""ldap client"""
from bonsai import LDAPClient


def ldap_client(host: str, port: int, user: str, password_file: str) -> LDAPClient:
    """generate ldap client"""
    client = LDAPClient(f"ldap://{host}:{port}")
    with open(password_file, "r") as file:
        password = file.read().strip()
    client.set_credentials(
        "SIMPLE", user=user, password=password,
    )
    return client
