"""functions for checking if a username is free"""

from bonsai.ldapconnection import LDAPConnection


async def check_username_free(conn: LDAPConnection, username: str) -> bool:
    """check if a username is free in ldap"""
    res = await conn.search("ou=accounts,o=redbrick", 2, f"(uid={username})")
    return bool(res)
