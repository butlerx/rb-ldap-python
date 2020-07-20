"""dcu ldap search"""

from typing import List

from bonsai.ldapconnection import LDAPConnection

from ..types import DCU_ATTR, DCUUser


async def search_dcu(
    ldap_conn: LDAPConnection, dcu_id: str = None, uid: str = None, fullname: str = None
) -> List[DCUUser]:
    """Seach DCU ldap for user"""
    """
    Seach DCU AD for user

    Args:
        ldap_conn: LDAP connection to use for searching
        uid: Usersname to search for
        dcu_id: dcu student id number
        fullname: Users full name

    Returns:
        A list of user found in ad matching search criteria
    """
    query = list(
        filter(
            None,
            [
                f"(displayName={fullname})" if fullname else None,
                f"(cn={uid})" if uid else None,
                f"(id={dcu_id})" if dcu_id else None,
            ],
        )
    )
    if not query:
        return []
    res = await ldap_conn.search(
        "o=ad,o=dcu,o=ie", 2, f"({'&'.join(query)})", attrlist=DCU_ATTR
    )
    return [DCUUser.from_ldap(user) for user in res]
