"""functions for checking if a username is free"""

from ..accounts import check_username_free
from ..accounts.clients import LDAPConnection


async def free(rb_client: LDAPConnection, username: str) -> int:
    """
    check if a username is free

    Args:
        rb_client: ldap client configured for redbrick ldap
        username: Redbrick username to check if free
    """
    async with rb_client.connect() as conn:
        if await check_username_free(conn, username):
            print(f"{username} is free")
            return 0
        print(f"{username} is taken")
        return 1
