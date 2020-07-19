"""functions for checking if a username is free"""

from bonsai import LDAPClient
from bonsai.ldapconnection import LDAPConnection

from .file import read_file
from .prompt import get_username


def check_free_cli(args):
    """check if a username is free in ldap cli interface"""
    client = LDAPClient(f"ldap://{args.host}")
    client.set_credentials("SIMPLE", user=args.user, password=read_file(args.password))
    username = get_username(args.username)
    with client.connect() as conn:
        if check_free(conn, username):
            print(f"{username} is free")
        else:
            print(f"{username} is taken")


def check_free(conn: LDAPConnection, username: str) -> bool:
    """check if a username is free in ldap"""
    res = conn.search("ou=accounts,o=redbrick", 2, f"(uid={username})")
    return bool(res)
