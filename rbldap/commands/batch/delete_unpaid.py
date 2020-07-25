"""delete unpaid automation"""
from asyncio import gather

from mailmanclient import Client

from ...accounts import del_user
from ...accounts.clients import LDAPConnection


async def delete_unpaid(
    rb_client: LDAPConnection,
    mailman: Client,
    commit: bool,
    *,
    i_know_what_im_doing: bool = False,
) -> int:
    """
    Delete all unpaid users accounts that are outside their grace period (years paid = -1)

    Args:
        rb_client: ldap client configured for redbrick ldap
        mailman: mailman Rest Client
        commit: flag to commit any changes
        i_know_what_im_doing: Flag to indicate to skip prompt

    Returns:
        int indicating the exit code

    """

    if not i_know_what_im_doing and not bool(
        input("Delete all unpaid users, THIS CANNOT BE UNDONE [y/N]: ")
        in ["y", "Y", "yes"]
    ):
        return 1

    async with rb_client.connect() as conn:
        res = await conn.search(
            "ou=accounts,o=redbrick",
            "(&(yearspaid=-1)(|(usertype=member)(usertype=associate)(usertype=staff))",
            attributes=["uid", "yearsPaid", "homeDirectory", "usertype"],
        )
        users = [user for user in res if user["attributes"]["yearsPaid"][0] == -1]
        if commit:
            await gather(*[del_user(user, mailman=mailman) for user in users])

    print(f"{len(users)} accounts deleted")

    return 0
