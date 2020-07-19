"""functions for checking if a username is free"""

from bonsai import LDAPClient

from ..accounts import check_username_free
from ..fs import read_file_to_string
from .prompt import get_username


async def free(args):
    """check if a username is free in ldap cli interface"""
    client = LDAPClient(f"ldap://{args.host}")
    client.set_credentials(
        "SIMPLE", user=args.user, password=read_file_to_string(args.password)
    )
    username = get_username(args.username)
    async with client.connect(is_async=True) as conn:
        if await check_username_free(conn, username):
            print(f"{username} is free")
        else:
            print(f"{username} is taken")
