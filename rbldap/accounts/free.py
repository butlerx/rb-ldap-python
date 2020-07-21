"""functions for checking if a username is free"""

from bonsai.ldapconnection import LDAPConnection


async def check_username_free(conn: LDAPConnection, username: str) -> bool:
    """
    check if a username is free in ldap

    Args:
        conn: LDAP connection to use
        username: username to check

    Return:
        boolean indicating if the username already exists in ldap
    """
    res = await conn.search("ou=accounts,o=redbrick", 2, f"(uid={username})")
    return bool(res)
