"""search command"""

from typing import List

from bonsai import LDAPClient

from ..accounts import search_dcu, search_rb


async def search(
    rb_client: LDAPClient,
    dcu_client: LDAPClient,
    *,
    dcu: bool = False,
    id: str = None,
    uid: str = None,
    altmail: str = None,
    fullname: List[str] = [],
    noob: bool = False,
):
    """
    Search ldap for user
    ---
    dcu: Query DCU Active Directory
    altmail: Users email address
    uid: Users username
    id: DCU id Number
    fullname: User's fullname
    noob: filter for new users
    """
    if dcu:
        async with dcu_client.connect(is_async=True) as conn:
            results = await search_dcu(
                conn, dcu_id=id, uid=uid, fullname=" ".join(fullname)
            )
            print("No User found" if not results else results)
    else:
        async with rb_client.connect(is_async=True) as conn:
            results = await search_rb(
                conn,
                uid=uid,
                dcu_id=id,
                altmail=altmail,
                fullname=" ".join(fullname),
                noob=noob,
            )
            print("No User found" if not results else results)
