"""Redbrick ldap search"""

from typing import List

from bonsai.ldapconnection import LDAPConnection

from ..types import RB_ATTR, RBUser


async def search_rb(
    ldap_conn: LDAPConnection,
    uid: str = None,
    dcu_id: str = None,
    altmail: str = None,
    fullname: str = None,
    noob: bool = False,
) -> List[RBUser]:
    """Seach RB ldap for user"""
    query = list(
        filter(
            None,
            [
                f"(cn={fullname})" if fullname else None,
                "(newbie=TRUE)" if noob else None,
                f"(altmail={altmail})" if altmail else None,
                f"(id={dcu_id})" if dcu_id else None,
                f"((uid={uid})|(gecos={uid}))" if uid else None,
            ],
        )
    )
    if not query:
        return []
    res = await ldap_conn.search(
        "ou=accounts,o=redbrick", 2, f"({'&'.join(query)})", attrlist=RB_ATTR
    )
    return [RBUser.from_ldap(user) for user in res]
