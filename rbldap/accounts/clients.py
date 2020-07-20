from bonsai import LDAPClient

from ..fs import read_file_to_string


def ldap_client(host: str, port: int, user: str, password_file: str) -> LDAPClient:
    """generate ldap client"""
    client = LDAPClient(f"ldap://{host}:{port}")
    client.set_credentials(
        "SIMPLE", user=user, password=read_file_to_string(password_file),
    )
    return client
