"""delete unpaid automation"""
from asyncio import gather

from bonsai import LDAPClient, LDAPEntry
from mailmanclient import Client

from ..accounts import del_user


async def delete_unpaid(
    rb_client: LDAPClient, mailman: Client, *, verify_delete: bool = False
) -> int:
    """
    Delete all unpaid users accounts that are outside their grace period (years paid = -1)

    Args:
        rb_client: ldap client configured for redbrick ldap
        mailman: mailman Rest Client
        verify_delete: Flag to indicate to skip prompt

    Returns:
        int indicating the exit code

    """

    if not verify_delete and not bool(
        input("Delete all unpaid users, THIS CANNOT BE UNDONE [y/N]: ")
        in ["y", "Y", "yes"]
    ):
        return 1

    async with rb_client.connect(is_async=True) as conn:
        res = await conn.search(
            "ou=accounts,o=redbrick",
            2,
            "(&((yearspaid=-1))(|(usertype=member)(usertype=associate)(usertype=staff))",
            attrlist=["uid", "yearsPaid", "homeDirectory", "usertype"],
        )
        users = [user for user in res if user["yearsPaid"][0] == -1]
        await gather(*[del_user(user, mailman=mailman) for user in users])

    print(f"{len(users)} accounts deleted")

    return 0
