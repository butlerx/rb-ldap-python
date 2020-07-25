"""search command"""

from typing import List, Union

from ..accounts import search_dcu, search_rb
from ..accounts.clients import LDAPConnection
from ..accounts.types import DCUUser, RBUser


async def search(
    rb_client: LDAPConnection,
    dcu_client: LDAPConnection,
    *,
    dcu: bool = False,
    id: str = None,
    uid: str = None,
    altmail: str = None,
    fullname: List[str] = [],
    noob: bool = False,
) -> int:
    """
    Search ldap for user

    Args:
        rb_client: ldap client configured for redbrick ldap
        dcu_client: ldap client configured for dcu ad
        dcu: Query DCU Active Directory
        altmail: Users email address
        uid: Users username
        id: DCU id Number
        fullname: User's fullname
        noob: filter for new users
    """
    results: List[Union[RBUser, DCUUser]] = []
    if dcu:
        async with dcu_client.connect() as conn:
            results = await search_dcu(
                conn, dcu_id=id, uid=uid, fullname=" ".join(fullname)
            )
    else:
        async with rb_client.connect() as conn:
            results = await search_rb(
                conn,
                uid=uid,
                dcu_id=id,
                altmail=altmail,
                fullname=" ".join(fullname),
                noob=noob,
            )
    print("No User found" if not results else results)
    return int(bool(results))
