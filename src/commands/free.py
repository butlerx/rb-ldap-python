"""functions for checking if a username is free"""

from bonsai import LDAPClient

from ..accounts import check_username_free


async def free(rb_client: LDAPClient, username: str):
    """
    check if a username is free
    ---
    username: Redbrick username to check if free
    """
    async with rb_client.connect(is_async=True) as conn:
        if await check_username_free(conn, username):
            print(f"{username} is free")
        else:
            print(f"{username} is taken")
